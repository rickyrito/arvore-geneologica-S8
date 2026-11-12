#!/usr/bin/env python3
"""Gera o suplemento S8 sem modificar a base produzida a partir do blogue."""
import argparse
import json
import re
import unicodedata
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MESES = 'JAN FEB MAR APR MAY JUN JUL AUG SEP OCT NOV DEC'.split()


def json_texto(valor):
    return json.dumps(valor, ensure_ascii=False, indent=2) + '\n'


def normalizar(nome):
    nome = nome.lower().replace('manoel', 'manuel').replace('joam', 'joao')
    return ''.join(c for c in unicodedata.normalize('NFD', nome)
                   if not unicodedata.combining(c)).strip()


def data(valor):
    if not re.fullmatch(r'\d{2}/\d{2}/\d{4}', valor):
        raise ValueError('Data deve ter formato DD/MM/AAAA: ' + valor)
    return datetime.strptime(valor, '%d/%m/%Y').date()


def nome_legivel(valor):
    if not isinstance(valor, str) or not valor.strip() or any(c in valor for c in '?[]\n\r'):
        raise ValueError('Nome confirmado em falta ou com marcas de dúvida: ' + repr(valor))


def tipo(assento):
    return assento.get('tipo', 'batismo')


def datas_evento(assento):
    campos = {'batismo': ('data_nascimento', 'data_batismo'), 'obito': ('data_obito', 'data_sepultura'),
              'casamento': ('data_casamento',)}[tipo(assento)]
    return {campo: assento[campo] for campo in campos if assento.get(campo)}


def validar_confirmado(a, livro):
    ident, evento = a['id'], tipo(a)
    if a.get('duvidas') or not isinstance(a.get('excerto'), str) or not a['excerto'].strip():
        raise ValueError('Assento confirmado com dúvidas ou sem excerto: ' + ident)
    if evento == 'batismo':
        for valor in (a['crianca']['nome'], a['pai'], a['mae']):
            nome_legivel(valor)
        if a['crianca']['sexo'] not in ('M', 'F') or not a.get('data_batismo'):
            raise ValueError('Batismo sem sexo/data válidos: ' + ident)
    elif evento == 'obito':
        nome_legivel(a['falecido']['nome'])
        if a['falecido']['sexo'] not in ('M', 'F', '') or not datas_evento(a):
            raise ValueError('Óbito sem sexo válido ou data explícita: ' + ident)
    else:
        nome_legivel(a['noivo'])
        nome_legivel(a['noiva'])
        if not a.get('data_casamento'):
            raise ValueError('Casamento sem data: ' + ident)
    if a.get('data_nascimento'):
        if not isinstance(a.get('evidencia_nascimento'), str) or not a['evidencia_nascimento'].strip():
            raise ValueError('Nascimento sem indicação explícita no original: ' + ident)
        if evento == 'batismo' and data(a['data_nascimento']) > data(a['data_batismo']):
            raise ValueError('Nascimento posterior ao batismo: ' + ident)
    permitidas = {'batismo': {'data_nascimento', 'data_batismo'}, 'obito': {'data_obito', 'data_sepultura'},
                  'casamento': {'data_casamento'}}[evento]
    for campo in ('data_nascimento', 'data_batismo', 'data_obito', 'data_sepultura', 'data_casamento'):
        if a.get(campo) and campo not in permitidas:
            raise ValueError('Data de outro tipo de evento: ' + ident)
    for campo, valor in datas_evento(a).items():
        dia = data(valor)
        if campo == 'data_nascimento':
            continue  # O nascimento explícito pode ser anterior ao intervalo do livro de batismos.
        if not (datetime.fromisoformat(livro['data_inicial']).date() <= dia <=
                datetime.fromisoformat(livro['data_final']).date()):
            raise ValueError('Data fora do livro: ' + ident)
    if a.get('data_obito') and a.get('data_sepultura'):
        if data(a['data_sepultura']) < data(a['data_obito']):
            raise ValueError('Sepultura anterior ao óbito: ' + ident)


def ler(raiz):
    registos, vistos, posicoes = [], set(), set()
    entradas = sorted((raiz / 'fontes/S8/transcricoes').glob('*.json'))
    if not entradas:
        raise ValueError('Não há transcrições S8.')
    for entrada in entradas:
        lote = json.loads(entrada.read_text(encoding='utf-8'))
        if lote.get('schema') != 1:
            raise ValueError('Versão de entrada desconhecida: ' + str(entrada))
        caminho = Path(lote['livro'])
        if caminho.is_absolute() or '..' in caminho.parts or caminho.name != 'registo.json':
            raise ValueError('Caminho de livro inválido.')
        livro = json.loads((raiz / caminho).read_text(encoding='utf-8'))
        imagens = {re.search(r'(m\d{4})\.jpg$', im['name'])[1]: im['name']
                   for im in livro['imagens']}
        if not livro['origem'].startswith('https://digitarq.arquivos.pt/'):
            raise ValueError('Origem do arquivo inválida.')
        duplicadas = lote.get('imagens_duplicadas', [])
        repetidas = {im['imagem'] for im in duplicadas}
        if len(repetidas) != len(duplicadas):
            raise ValueError('Imagem duplicada declarada mais de uma vez.')
        for im in duplicadas:
            if (im['imagem'] == im['repete'] or im['repete'] in repetidas or
                    im['imagem'] not in imagens or im['repete'] not in imagens or
                    im['imagem'] not in lote['imagens_examinadas'] or
                    im['repete'] not in lote['imagens_examinadas'] or not im.get('motivo')):
                raise ValueError('Declaração de repetição de imagem inválida.')
        for assento in lote['assentos']:
            ident = assento['id']
            if assento['imagem'] in repetidas:
                raise ValueError('Usar a imagem canónica em vez da imagem repetida: ' + ident)
            posicao = (livro['referencia'], assento['imagem'], assento['lado'], assento['ordem'])
            if ident in vistos or posicao in posicoes:
                raise ValueError('Assento repetido: ' + ident)
            vistos.add(ident)
            posicoes.add(posicao)
            if assento['imagem'] not in imagens or assento['imagem'] not in lote['imagens_examinadas']:
                raise ValueError('Imagem não identificada/examinada: ' + ident)
            if assento['lado'] not in ('esquerda', 'direita') or not isinstance(assento['ordem'], int) or assento['ordem'] < 1:
                raise ValueError('Posição inválida: ' + ident)
            if assento['estado'] not in ('confirmado', 'pendente'):
                raise ValueError('Estado desconhecido: ' + ident)
            if tipo(assento) not in ('batismo', 'obito', 'casamento'):
                raise ValueError('Tipo de assento desconhecido: ' + ident)
            if assento['estado'] == 'confirmado':
                validar_confirmado(assento, livro)
            elif not assento.get('duvidas'):
                raise ValueError('Leitura pendente sem dúvidas descritas: ' + ident)
            registos.append((assento, livro, caminho.parent / imagens[assento['imagem']]))
    por_id = {a['id']: a for a, _, _ in registos}
    for a, _, _ in registos:
        if a['estado'] == 'confirmado' and a.get('data_por_remissao'):
            anterior = por_id.get(a['data_por_remissao'])
            campo = {'batismo': 'data_batismo', 'obito': 'data_obito',
                     'casamento': 'data_casamento'}[tipo(a)]
            if (not anterior or anterior['estado'] != 'confirmado' or
                    tipo(anterior) != tipo(a) or not a.get(campo) or
                    anterior.get(campo) != a[campo]):
                raise ValueError('Remissão de data inconsistente: ' + a['id'])
    return registos


def construir(registos):
    pessoas, familias, aplicados, pendentes = [], [], [], []
    for a, livro, imagem in registos:
        if a['estado'] == 'pendente':
            pendentes.append(dict(a, livro=livro['referencia'], ficheiro_imagem=imagem.as_posix()))
            continue
        i, fi = len(pessoas), len(familias)
        evento = tipo(a)
        rotulo = {'batismo': 'Batismo', 'obito': 'Óbito', 'casamento': 'Casamento'}[evento]
        if evento == 'obito':
            data_fonte = a['data_obito'] if a.get('data_obito') else 'com data de óbito desconhecida'
            if a.get('data_sepultura'):
                data_fonte += '; sepultura ' + a['data_sepultura']
        else:
            data_fonte = a['data_batismo' if evento == 'batismo' else 'data_casamento']
        fonte = ('Fonte original S8 — ' + rotulo + ' ' + data_fonte + ' — ' +
                 livro['referencia'] + ', imagem ' + a['imagem'] + ', ' + a['lado'] +
                 ', assento ' + str(a['ordem']) + '. Leitura direta dos campos essenciais; '
                 'identidade com as genealogias do blogue por confirmar.')
        evidencia = dict(id=a['id'], origem='S8', url=livro['origem'], imagem=imagem.as_posix(),
                         lado=a['lado'], ordem=a['ordem'])
        if evento == 'batismo':
            if a.get('data_nascimento'):
                fonte += ' Nascimento explicitamente indicado: ' + a['data_nascimento'] + '.'
            for nome, sexo, papel in ((a['crianca']['nome'], a['crianca']['sexo'], 'criança'),
                                      (a['pai'], 'M', 'pai'), (a['mae'], 'F', 'mãe')):
                filho = papel == 'criança'
                pessoas.append([nome, sexo, a.get('data_nascimento', '') if filho else '',
                                a['data_batismo'] if filho else '', '', '',
                                fi if filho else -1, [] if filho else [fi],
                                'Assentos paroquiais', [], [fonte + ' Papel: ' + papel + '.'],
                                [dict(evidencia, papel=papel)]])
            familias.append([i + 1, i + 2, '',
                             'Casal identificado no batismo; data de casamento não indicada. '
                             'Ligação às famílias da base por confirmar.', [i]])
        else:
            evidencia.update(tipo=evento, excerto=a['excerto'])
            if a.get('data_sepultura'):
                evidencia['data_sepultura'] = a['data_sepultura']
            fonte += ' ' + a['excerto']
            if a.get('nota'):
                fonte += ' ' + a['nota']
            if evento == 'obito':
                pessoas.append([a['falecido']['nome'], a['falecido']['sexo'], '', '',
                                a.get('data_obito', ''), '', -1, [], 'Assentos paroquiais', [],
                                [fonte + ' Papel: falecido.'], [dict(evidencia, papel='falecido')]])
            else:
                for campo, sexo in (('noivo', 'M'), ('noiva', 'F')):
                    pessoas.append([a[campo], sexo, '', '', '', '', -1, [fi],
                                    'Assentos paroquiais', [], [fonte + ' Papel: ' + campo + '.'],
                                    [dict(evidencia, papel=campo)]])
                familias.append([i, i + 1, a['data_casamento'],
                                 'Casamento identificado no original S8; filiações e ligação '
                                 'às famílias da base por confirmar.', []])
        aplicados.append(dict(a, livro=livro['referencia'], ficheiro_imagem=imagem.as_posix(),
                              pessoa=i, familia=fi if evento != 'obito' else -1))
    return dict(p=pessoas, f=familias), aplicados, pendentes


def gerar_js(suplemento, ids):
    dados = json.dumps(suplemento, ensure_ascii=False, separators=(',', ':'))
    return '''// Gerado por scripts/gerar_assentos_s8.py; editar as transcrições, não este ficheiro.
(function(){
  var D = window.ARVORE;
  if (!D || !D.p || !D.f) throw new Error('Carregar dados.js antes de dados_s8.js.');
  if (D.assentosS8) return;
  var S = ''' + dados + ''';
  var np = D.p.length, nf = D.f.length;
  S.p.forEach(function(p){
    if (p[6] >= 0) p[6] += nf;
    p[7] = p[7].map(function(f){ return f + nf; });
    D.p.push(p);
  });
  S.f.forEach(function(f){
    if (f[0] >= 0) f[0] += np;
    if (f[1] >= 0) f[1] += np;
    f[4] = f[4].map(function(p){ return p + np; });
    D.f.push(f);
  });
  D.assentosS8 = ''' + json.dumps(ids, ensure_ascii=False) + ''';
})();
'''


def gerar_gedcom(suplemento, aplicados):
    linhas = ['0 HEAD', '1 SOUR Assentos originais S8', '1 GEDC', '2 VERS 5.5.1',
              '2 FORM LINEAGE-LINKED', '1 CHAR UTF-8', '1 FILE assentos_s8.ged']
    fontes = {a['id']: i + 1 for i, a in enumerate(aplicados)}
    por_id = {a['id']: a for a in aplicados}

    def evento(tag, valor):
        dia = data(valor)
        linhas.extend(['1 ' + tag, f'2 DATE {dia.day} {MESES[dia.month-1]} {dia.year}'])

    def nota(nivel, texto):
        for i, parte in enumerate(texto.splitlines()):
            prefixo = str(nivel) + ' NOTE ' if i == 0 else str(nivel + 1) + ' CONT '
            # Conserva o texto completo e os caracteres UTF-8 em linhas curtas.
            trecho = prefixo
            for caracter in parte:
                if len((trecho + caracter).encode('utf-8')) > 248:
                    sem_espacos = trecho.rstrip(' ')
                    linhas.append(sem_espacos)
                    trecho = str(nivel + 1) + ' CONC ' + trecho[len(sem_espacos):]
                trecho += caracter
            linhas.append(trecho)

    for i, p in enumerate(suplemento['p']):
        partes = p[0].rsplit(' ', 1)
        nome = p[0] if len(partes) == 1 else partes[0] + ' /' + partes[1] + '/'
        linhas.extend([f'0 @I{i+1}@ INDI', '1 NAME ' + nome])
        if p[1]:
            linhas.append('1 SEX ' + p[1])
        evidencia = p[11][0]
        a = por_id[evidencia['id']]
        if p[2]:
            evento('BIRT', p[2])
            linhas.append(f"2 SOUR @S{fontes[a['id']]}@")
        if p[3]:
            evento('BAPM', p[3])
        if p[4]:
            evento('DEAT', p[4])
        if tipo(a) == 'obito' and a.get('data_sepultura'):
            evento('BURI', a['data_sepultura'])
        if p[6] >= 0:
            linhas.append(f'1 FAMC @F{p[6]+1}@')
        for fi in p[7]:
            linhas.append(f'1 FAMS @F{fi+1}@')
        linhas.extend([f"1 SOUR @S{fontes[a['id']]}@", '2 NOTE Papel: ' + evidencia['papel'],
                       '1 NOTE Identidade com as genealogias do blogue por confirmar.'])
    for i, f in enumerate(suplemento['f']):
        linhas.extend([f'0 @F{i+1}@ FAM', f'1 HUSB @I{f[0]+1}@', f'1 WIFE @I{f[1]+1}@'])
        if f[2]:
            evento('MARR', f[2])
            ident = suplemento['p'][f[0]][11][0]['id']
            linhas.append(f'2 SOUR @S{fontes[ident]}@')
        linhas.extend(f'1 CHIL @I{c+1}@' for c in f[4])
        nota(1, f[3])
    urls = {p[11][0]['id']: p[11][0]['url'] for p in suplemento['p']}
    rotulos = {'data_nascimento': 'nascimento explícito', 'data_batismo': 'batismo', 'data_obito': 'óbito',
               'data_sepultura': 'sepultura', 'data_casamento': 'casamento'}
    for i, a in enumerate(aplicados):
        datas = '; '.join(rotulos[c] + ' ' + v for c, v in datas_evento(a).items())
        linhas.extend([f'0 @S{i+1}@ SOUR', '1 TITL ' + a['livro'] + ' — ' + a['id'],
                       '1 PUBL ' + urls[a['id']], '1 NOTE Imagem: ' + a['ficheiro_imagem'],
                       f"2 CONT {a['lado']}, assento {a['ordem']}; {datas}.",
                       '2 CONT Leitura dos campos essenciais, sem datas de outros eventos inferidas.'])
        nota(1, a['excerto'])
        if a.get('data_nascimento'):
            nota(1, a['evidencia_nascimento'])
        if a.get('nota'):
            nota(1, a['nota'])
    return '\n'.join(linhas + ['0 TRLR', ''])


def gerar(raiz):
    suplemento, aplicados, pendentes = construir(ler(raiz))
    lotes = [json.loads(p.read_text(encoding='utf-8'))
             for p in sorted((raiz / 'fontes/S8/transcricoes').glob('*.json'))]
    base_js = (raiz / 'dados.js').read_text(encoding='utf-8')
    base = json.loads(base_js[base_js.index('{'):].strip().rstrip(';'))
    coincidencias = []
    for a in aplicados:
        if tipo(a) != 'batismo':
            continue
        for fi, f in enumerate(base['f']):
            if f[0] < 0 or f[1] < 0:
                continue
            if (normalizar(base['p'][f[0]][0]), normalizar(base['p'][f[1]][0])) == (normalizar(a['pai']), normalizar(a['mae'])):
                coincidencias.append(dict(assento=a['id'], familia_base=fi,
                    fundido=False, motivo='Só coincidência dos nomes do casal; identidade não demonstrada.'))
    por_tipo = {t: dict(confirmados=sum(tipo(a) == t for a in aplicados),
                        pendentes=sum(tipo(a) == t for a in pendentes))
                for t in ('batismo', 'obito', 'casamento')}
    relatorio = dict(confirmados=len(aplicados), pendentes=len(pendentes), por_tipo=por_tipo,
                     novas_pessoas=len(suplemento['p']), novos_nucleos=len(suplemento['f']),
                     aplicados=aplicados, por_rever=pendentes, coincidencias_nao_fundidas=coincidencias,
                     imagens_duplicadas=[dict(im, livro=lote['livro']) for lote in lotes
                                         for im in lote.get('imagens_duplicadas', [])],
                     notas_pagina=[dict(nota, livro=lote['livro']) for lote in lotes
                                   for nota in lote.get('notas_pagina', [])])
    return {
        'dados_s8.js': gerar_js(suplemento, [a['id'] for a in aplicados]),
        'assentos_s8.ged': gerar_gedcom(suplemento, aplicados),
        'dados/assentos_s8_revisao.json': json_texto(relatorio),
    }, relatorio


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Validar resultados sem escrever.')
    args = parser.parse_args()
    resultados, relatorio = gerar(RAIZ)
    divergencias = []
    for nome, texto in resultados.items():
        caminho = RAIZ / nome
        if args.check:
            if not caminho.exists() or caminho.read_text(encoding='utf-8') != texto:
                divergencias.append(nome)
        else:
            caminho.write_text(texto, encoding='utf-8')
    print(f"S8: {relatorio['confirmados']} assentos integrados, {relatorio['pendentes']} pendentes; "
          f"{relatorio['novas_pessoas']} pessoas e {relatorio['novos_nucleos']} núcleos no suplemento.")
    if divergencias:
        raise SystemExit('Resultados desatualizados: ' + ', '.join(divergencias))


if __name__ == '__main__':
    main()
