#!/usr/bin/env python3
"""Aplica acréscimos de fonte externa ao dados_final.json.

Corre depois de limpar.py e antes de ged_final.py.
Regras do CONTEXT.md: informação que não vem do blogue é marcada com a sua fonte,
nunca substitui em silêncio um valor existente, e a divergência fica registada.
"""
import json, csv, re, unicodedata, os

def sa(s):
    s = unicodedata.normalize('NFD', s or '')
    return ''.join(c for c in s if unicodedata.category(c) != 'Mn').lower()

FICH = 'arvore-geneologica-s8/dados/acrescentos_carlos.csv'
if not os.path.exists(FICH):
    FICH = 'dados/acrescentos_carlos.csv'

D = json.load(open('dados_final.json'))
P, F = D['p'], D['f']
NOME, SEXO, NASC, BAPT, OBITO, COD, FAMC, FAMS, FAMILIA, REFS, FONTES = range(11)

def conjuges(i):
    nomes = []
    for fi in P[i][FAMS]:
        o = F[fi][1] if F[fi][0] == i else F[fi][0]
        if o >= 0:
            nomes.append(sa(P[o][NOME]))
    return nomes

def acha(nome, data, conjuge=''):
    """Pessoa com este nome, confirmada pela data conhecida ou pelo cônjuge."""
    alvo = sa(nome)
    cands = [i for i, p in enumerate(P) if sa(p[NOME]) == alvo]
    if data:
        com = [i for i in cands if data in (P[i][NASC], P[i][BAPT], P[i][OBITO])]
        if com:
            return com[0]
    if conjuge:
        c = sa(conjuge)
        com = [i for i in cands if any(c in x or x in c for x in conjuges(i))]
        if com:
            return com[0]
    # sem data: a pessoa com mais informação preenchida
    if cands:
        return max(cands, key=lambda i: sum(1 for c in (NASC, BAPT, OBITO, COD) if P[i][c]))
    return -1

aplicados, divergencias, falhados = [], [], []
for r in csv.DictReader(open(FICH, encoding='utf-8')):
    i = acha(r['pessoa'], r['data_conhecida'], r.get('conjuge', ''))
    if i < 0:
        falhados.append(r['pessoa']); continue
    campo, valor = r['campo'], r['valor']
    fonte = r['fonte'] + (' — ' + r['nota'] if r['nota'] else '')

    if campo.endswith('_divergente'):
        base = {'nascimento_divergente': NASC, 'batismo_divergente': BAPT, 'obito_divergente': OBITO}[campo]
        divergencias.append([P[i][NOME], campo.replace('_divergente', ''), P[i][base], valor, r['fonte'], r['nota']])
        nota = 'Divergência: ' + campo.replace('_divergente', '') + ' ' + valor + ' segundo ' + r['fonte']
        if nota not in P[i][FONTES]:
            P[i][FONTES].append(nota)
        continue

    if campo == 'naturalidade_pais':
        nota = 'Pais naturais de ' + valor + ' — ' + r['fonte']
        if nota not in P[i][FONTES]:
            P[i][FONTES].append(nota)
        aplicados.append([P[i][NOME], campo, valor])
        continue

    if campo == 'pais':
        nomes = [x.strip() for x in valor.split('|')]
        npai, nmae = (nomes + [''])[:2]
        # 1) família já existente com este casal
        alvo = -1
        for fi, f in enumerate(F):
            hn = sa(P[f[0]][NOME]) if f[0] >= 0 else ''
            wn = sa(P[f[1]][NOME]) if f[1] >= 0 else ''
            if hn == sa(npai) and wn == sa(nmae):
                alvo = fi; break
        if alvo < 0:
            # 2) pessoas que já tenham o outro como cônjuge
            def pessoa_com_conjuge(nome, outro):
                cands = [k for k, q in enumerate(P) if sa(q[NOME]) == sa(nome)]
                for k in cands:
                    if any(sa(outro) == x for x in conjuges(k)):
                        return k
                return cands[0] if cands else -1
            jp = pessoa_com_conjuge(npai, nmae) if npai else -1
            jm = pessoa_com_conjuge(nmae, npai) if nmae else -1
            if jp < 0 and npai:
                P.append([npai, 'M', '', '', '', '', -1, [], P[i][FAMILIA], [], [r['fonte']]]); jp = len(P) - 1
            if jm < 0 and nmae:
                P.append([nmae, 'F', '', '', '', '', -1, [], P[i][FAMILIA], [], [r['fonte']]]); jm = len(P) - 1
            F.append([jp, jm, '', '', []]); alvo = len(F) - 1
            for x in (jp, jm):
                if x >= 0 and alvo not in P[x][FAMS]: P[x][FAMS].append(alvo)
        antigo = P[i][FAMC]
        if antigo >= 0 and antigo != alvo:
            if i in F[antigo][4]: F[antigo][4].remove(i)
            anteriores = [P[x][NOME] for x in (F[antigo][0], F[antigo][1]) if x >= 0]
            divergencias.append([P[i][NOME], 'filiação', ' e '.join(anteriores) or 'sem pais', valor.replace('|', ' e '), r['fonte'], r['nota']])
        if i not in F[alvo][4]: F[alvo][4].append(i)
        P[i][FAMC] = alvo
        marca = r['fonte'] + ' — filiação'
        if marca not in P[i][FONTES]: P[i][FONTES].append(marca)
        aplicados.append([P[i][NOME], 'pais', valor.replace('|', ' e ')])
        continue

    idx = {'nascimento': NASC, 'batismo': BAPT, 'obito': OBITO}.get(campo)
    if idx is None:
        falhados.append(r['pessoa'] + ' / campo ' + campo); continue
    if P[i][idx] and P[i][idx] != valor:
        divergencias.append([P[i][NOME], campo, P[i][idx], valor, r['fonte'], r['nota']])
        continue
    if not P[i][idx]:
        P[i][idx] = valor
        aplicados.append([P[i][NOME], campo, valor])
    marca = r['fonte'] + (' (' + r['nota'] + ')' if r['nota'] else '')
    if marca not in P[i][FONTES]:
        P[i][FONTES].append(marca)

json.dump({'p': P, 'f': F}, open('dados_final.json', 'w'), ensure_ascii=False, separators=(',', ':'))

with open('acrescentos_aplicados.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.writer(fh)
    w.writerow(['pessoa', 'campo', 'valor'])
    w.writerows(aplicados)
if divergencias:
    with open('conflitos_registos.csv', 'a', newline='', encoding='utf-8') as fh:
        w = csv.writer(fh)
        for d in divergencias:
            w.writerow([d[0], d[1], d[2], d[3], d[4] + (' — ' + d[5] if d[5] else '')])

print('acréscimos aplicados:', len(aplicados))
for a in aplicados:
    print('   ', a[0], '|', a[1], '->', a[2])
print('divergências registadas:', len(divergencias))
for d in divergencias:
    print('   ', d[0], '|', d[1], ':', d[2], 'vs', d[3])
if falhados:
    print('não encontrados:', falhados)
