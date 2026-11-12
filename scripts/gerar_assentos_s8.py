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
            if assento['estado'] == 'confirmado':
                if assento.get('duvidas') or not assento.get('excerto'):
                    raise ValueError('Assento confirmado com dúvidas ou sem excerto: ' + ident)
                for valor in (assento['crianca']['nome'], assento['pai'], assento['mae']):
                    nome_legivel(valor)
                if assento['crianca']['sexo'] not in ('M', 'F'):
                    raise ValueError('Sexo inválido: ' + ident)
                dia = data(assento['data_batismo'])
                if not (datetime.fromisoformat(livro['data_inicial']).date() <= dia <=
                        datetime.fromisoformat(livro['data_final']).date()):
                    raise ValueError('Data fora do livro: ' + ident)
            elif not assento.get('duvidas'):
                raise ValueError('Leitura pendente sem dúvidas descritas: ' + ident)
            registos.append((assento, livro, caminho.parent / imagens[assento['imagem']]))
    por_id = {a['id']: a for a, _, _ in registos}
    for a, _, _ in registos:
        if a['estado'] == 'confirmado' and a.get('data_por_remissao'):
            anterior = por_id[a['data_por_remissao']]
            if anterior['estado'] != 'confirmado' or anterior['data_batismo'] != a['data_batismo']:
                raise ValueError('Remissão de data inconsistente: ' + a['id'])
    return registos


def construir(registos):
    pessoas, familias, aplicados, pendentes = [], [], [], []
    for a, livro, imagem in registos:
        if a['estado'] == 'pendente':
            pendentes.append(dict(a, livro=livro['referencia'], ficheiro_imagem=str(imagem)))
            continue
        i, fi = len(pessoas), len(familias)
        fonte = ('Fonte original S8 — Batismo ' + a['data_batismo'] + ' — ' +
                 livro['referencia'] + ', imagem ' + a['imagem'] + ', ' + a['lado'] +
                 ', assento ' + str(a['ordem']) + '. Leitura direta dos campos essenciais; '
                 'identidade com as genealogias do blogue por confirmar.')
        evidencia = dict(id=a['id'], origem='S8', url=livro['origem'], imagem=str(imagem),
                         lado=a['lado'], ordem=a['ordem'])
        for nome, sexo, papel in ((a['crianca']['nome'], a['crianca']['sexo'], 'criança'),
                                  (a['pai'], 'M', 'pai'), (a['mae'], 'F', 'mãe')):
            filho = papel == 'criança'
            pessoas.append([nome, sexo, '', a['data_batismo'] if filho else '', '', '',
                            fi if filho else -1, [] if filho else [fi],
                            'Assentos paroquiais', [], [fonte + ' Papel: ' + papel + '.'],
                            [dict(evidencia, papel=papel)]])
        familias.append([i + 1, i + 2, '',
                         'Casal identificado no batismo; data de casamento não indicada. '
                         'Ligação às famílias da base por confirmar.', [i]])
        aplicados.append(dict(a, livro=livro['referencia'], ficheiro_imagem=str(imagem),
                              pessoa=i, familia=fi))
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
    for i, p in enumerate(suplemento['p']):
        partes = p[0].rsplit(' ', 1)
        nome = p[0] if len(partes) == 1 else partes[0] + ' /' + partes[1] + '/'
        linhas.extend([f'0 @I{i+1}@ INDI', '1 NAME ' + nome, '1 SEX ' + p[1]])
        if p[3]:
            dia = data(p[3])
            linhas.extend(['1 BAPM', f'2 DATE {dia.day} {MESES[dia.month-1]} {dia.year}'])
        if p[6] >= 0:
            linhas.append(f'1 FAMC @F{p[6]+1}@')
        for fi in p[7]:
            linhas.append(f'1 FAMS @F{fi+1}@')
        linhas.extend([f'1 SOUR @S{i//3+1}@', '2 NOTE Papel: ' + p[11][0]['papel'],
                       '1 NOTE Identidade com as genealogias do blogue por confirmar.'])
    for i, f in enumerate(suplemento['f']):
        linhas.extend([f'0 @F{i+1}@ FAM', f'1 HUSB @I{f[0]+1}@', f'1 WIFE @I{f[1]+1}@'])
        linhas.extend(f'1 CHIL @I{c+1}@' for c in f[4])
        linhas.append('1 NOTE ' + f[3])
    for i, a in enumerate(aplicados):
        livro = next(p[11][0]['url'] for p in suplemento['p'] if p[11][0]['id'] == a['id'])
        linhas.extend([f'0 @S{i+1}@ SOUR', '1 TITL ' + a['livro'] + ' — ' + a['id'],
                       '1 PUBL ' + livro, '1 NOTE Imagem: ' + a['ficheiro_imagem'],
                       f"2 CONT {a['lado']}, assento {a['ordem']}; batismo {a['data_batismo']}.",
                       '2 CONT Leitura dos campos essenciais, sem data de nascimento inferida.'])
    return '\n'.join(linhas + ['0 TRLR', ''])


def gerar(raiz):
    suplemento, aplicados, pendentes = construir(ler(raiz))
    lotes = [json.loads(p.read_text(encoding='utf-8'))
             for p in sorted((raiz / 'fontes/S8/transcricoes').glob('*.json'))]
    base_js = (raiz / 'dados.js').read_text(encoding='utf-8')
    base = json.loads(base_js[base_js.index('{'):].strip().rstrip(';'))
    coincidencias = []
    for a in aplicados:
        for fi, f in enumerate(base['f']):
            if f[0] < 0 or f[1] < 0:
                continue
            if (normalizar(base['p'][f[0]][0]), normalizar(base['p'][f[1]][0])) == (normalizar(a['pai']), normalizar(a['mae'])):
                coincidencias.append(dict(assento=a['id'], familia_base=fi,
                    fundido=False, motivo='Só coincidência dos nomes do casal; identidade não demonstrada.'))
    relatorio = dict(confirmados=len(aplicados), pendentes=len(pendentes),
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
