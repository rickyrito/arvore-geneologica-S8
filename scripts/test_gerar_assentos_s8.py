"""Regressões da cadeia aditiva S8, com livros e nomes de teste temporários."""
import copy
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('s8', Path(__file__).with_name('gerar_assentos_s8.py'))
s8 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(s8)


class AssentosS8Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.raiz = Path(self.tmp.name)
        (self.raiz / 'fontes/S8/transcricoes').mkdir(parents=True)
        (self.raiz / 'fontes/S8/livro').mkdir()
        self.livro = dict(referencia='LIVRO-TESTE', data_inicial='1692-01-01',
                          data_final='1705-12-31', origem='https://digitarq.arquivos.pt/teste',
                          imagens=[dict(name=f'teste_m{n:04}.jpg') for n in range(1, 7)])
        (self.raiz / 'fontes/S8/livro/registo.json').write_text(json.dumps(self.livro))
        self.assentos = []
        for n in range(1, 6):
            self.assentos.append(dict(id=f'T-{n}', imagem=f'm{n:04}', lado='esquerda', ordem=1,
                                      estado='confirmado', duvidas=[], excerto='Excerto de teste.'))
        self.assentos[0].update(crianca=dict(nome='Bebé', sexo='F'), pai='Pai Teste',
                                mae='Mãe Teste', data_batismo='02/01/1692')
        self.assentos[1].update(tipo='obito', falecido=dict(nome='Sepultada', sexo='F'),
                                data_sepultura='03/01/1692')
        self.assentos[2].update(tipo='casamento', noivo='Noivo Teste', noiva='Noiva Teste',
                                data_casamento='04/01/1692')
        self.assentos[3].update(tipo='obito', falecido=dict(nome='Falecido', sexo=''),
                                data_obito='05/01/1692', data_sepultura='06/01/1692')
        self.assentos[4].update(tipo='casamento', estado='pendente', duvidas=['Nome ilegível.'])
        self.lote = dict(schema=1, livro='fontes/S8/livro/registo.json', assentos=self.assentos,
                         imagens_examinadas=[f'm{n:04}' for n in range(1, 7)])
        (self.raiz / 'dados.js').write_text('window.ARVORE = {"p":[],"f":[]};')

    def ler(self):
        (self.raiz / 'fontes/S8/transcricoes/teste.json').write_text(json.dumps(self.lote))
        return s8.ler(self.raiz)

    def test_eventos_e_campos_nao_inferidos(self):
        suplemento, aplicados, pendentes = s8.construir(self.ler())
        self.assertEqual((len(suplemento['p']), len(suplemento['f'])), (7, 2))
        self.assertEqual([a['id'] for a in pendentes], ['T-5'])
        self.assertEqual([a['familia'] for a in aplicados], [0, -1, 1, -1])
        self.assertTrue(all(p[2] == '' for p in suplemento['p']))
        self.assertEqual(suplemento['p'][3][3:8], ['', '', '', -1, []])
        self.assertEqual(suplemento['p'][3][11][0]['data_sepultura'], '03/01/1692')
        self.assertIn('sepultura 03/01/1692', suplemento['p'][3][10][0])
        self.assertEqual(suplemento['p'][6][4], '05/01/1692')
        self.assertEqual(suplemento['f'][1], [4, 5, '04/01/1692',
                         'Casamento identificado no original S8; filiações e ligação '
                         'às famílias da base por confirmar.', []])

    def test_gedcom_eventos_e_fontes_com_tamanhos_diferentes(self):
        suplemento, aplicados, _ = s8.construir(self.ler())
        ged = s8.gerar_gedcom(suplemento, aplicados)
        blocos = {b.split('\n', 1)[0]: b for b in ged.split('\n0 ')}
        sepultada = blocos['@I4@ INDI']
        self.assertIn('1 BURI\n2 DATE 3 JAN 1692', sepultada)
        self.assertNotIn('1 DEAT', sepultada)
        self.assertIn('1 SOUR @S2@', sepultada)
        self.assertIn('1 SOUR @S3@', blocos['@I5@ INDI'])
        falecido = blocos['@I7@ INDI']
        self.assertIn('1 DEAT\n2 DATE 5 JAN 1692', falecido)
        self.assertIn('1 BURI\n2 DATE 6 JAN 1692', falecido)
        self.assertIn('1 SOUR @S4@', falecido)
        self.assertNotIn('1 SEX', falecido)
        self.assertIn('1 MARR\n2 DATE 4 JAN 1692\n2 SOUR @S3@', blocos['@F2@ FAM'])
        self.assertNotIn('1 BIRT', ged)
        self.assertNotIn('T-5', ged)

    def test_gedcom_preserva_notas_longas_e_quebras(self):
        texto = 'çã ' * 180 + '\nSegunda linha.'
        self.assentos[2]['excerto'] = texto
        suplemento, aplicados, _ = s8.construir(self.ler())
        ged = s8.gerar_gedcom(suplemento, aplicados)
        fonte = ged.split('0 @S3@ SOUR\n')[1].split('0 @S4@ SOUR')[0]
        notas = fonte.split('1 NOTE ')
        excerto = notas[-1].splitlines()
        reconstruido = excerto[0]
        for linha in excerto[1:]:
            if linha.startswith('2 CONC '):
                reconstruido += linha[7:]
            elif linha.startswith('2 CONT '):
                reconstruido += '\n' + linha[7:]
        self.assertEqual(reconstruido, texto)
        self.assertTrue(all(len(l.encode('utf-8')) <= 248 for l in ged.splitlines()))

    def test_datas_invalidas_e_tipo_desconhecido(self):
        casos = [dict(data_sepultura='03/01/1800'), dict(data_sepultura='31/02/1692'),
                 dict(data_sepultura='03/01/1692', data_obito='04/01/1692'),
                 dict(data_sepultura=''), dict(tipo='outro'), dict(data_batismo='03/01/1692')]
        original = copy.deepcopy(self.assentos[1])
        for alteracao in casos:
            with self.subTest(alteracao=alteracao):
                self.assentos[1] = dict(original, **alteracao)
                with self.assertRaises(ValueError):
                    self.ler()
        self.assentos[1] = original
        self.assentos[4]['tipo'] = 'outro'
        with self.assertRaises(ValueError):
            self.ler()

    def test_remissao_so_para_data_confirmada_do_mesmo_evento(self):
        self.assentos[3].update(data_por_remissao='T-1', data_obito='02/01/1692')
        with self.assertRaises(ValueError):
            self.ler()
        self.assentos[3].update(data_por_remissao='T-2', data_obito='03/01/1692')
        with self.assertRaises(ValueError):  # Sepultura não prova a data do óbito.
            self.ler()
        self.assentos[3].pop('data_por_remissao')
        self.assentos[4].update(estado='confirmado', duvidas=[], noivo='Outro Noivo',
                                noiva='Outra Noiva', data_casamento='04/01/1692',
                                data_por_remissao='T-3')
        self.assertEqual(len(self.ler()), 5)
        self.assentos[4]['data_por_remissao'] = 'inexistente'
        with self.assertRaises(ValueError):
            self.ler()

    def test_fotografia_repetida_nao_gera_assentos(self):
        self.lote['imagens_duplicadas'] = [dict(imagem='m0006', repete='m0001', motivo='Teste')]
        self.assertEqual(len(self.ler()), 5)
        self.assentos[4]['imagem'] = 'm0006'
        with self.assertRaises(ValueError):
            self.ler()
        self.lote['imagens_duplicadas'].append(dict(imagem='m0001', repete='m0006', motivo='Ciclo'))
        with self.assertRaises(ValueError):
            self.ler()

    def test_relatorio_conta_tipos_sem_pedir_pais_aos_obitos(self):
        self.ler()
        resultados, relatorio = s8.gerar(self.raiz)
        self.assertEqual(relatorio['por_tipo'], dict(batismo=dict(confirmados=1, pendentes=0),
                          obito=dict(confirmados=2, pendentes=0), casamento=dict(confirmados=1, pendentes=1)))
        self.assertEqual(relatorio['coincidencias_nao_fundidas'], [])
        self.assertEqual(set(resultados), {'dados_s8.js', 'assentos_s8.ged', 'dados/assentos_s8_revisao.json'})

    @unittest.skipUnless(shutil.which('node'), 'Node necessário para executar o suplemento JS')
    def test_js_preserva_base_indices_e_aplicacao_unica(self):
        suplemento, aplicados, _ = s8.construir(self.ler())
        js = s8.gerar_js(suplemento, [a['id'] for a in aplicados])
        verificacao = r'''
const assert = require('node:assert/strict');
global.window = {ARVORE: {p: [['Base']], f: [[-1, -1, '', '', []]]}};
const base = JSON.stringify(window.ARVORE);
const js = INPUT;
eval(js);
const D = window.ARVORE;
assert.equal(D.p.length, 8); assert.equal(D.f.length, 3);
assert.equal(JSON.stringify({p: D.p.slice(0,1), f: D.f.slice(0,1)}), base);
D.p.slice(1).forEach((p,j) => {
  const i=j+1;
  if(p[6]>=0) assert.ok(D.f[p[6]][4].includes(i));
  p[7].forEach(fi => assert.ok(D.f[fi][0]===i || D.f[fi][1]===i));
});
D.f.slice(1).forEach((f,j) => {
  const fi=j+1;
  [f[0], f[1]].forEach(i => assert.ok(D.p[i][7].includes(fi)));
  f[4].forEach(i => assert.equal(D.p[i][6], fi));
});
const antes = JSON.stringify(D); eval(js); assert.equal(JSON.stringify(D), antes);
'''.replace('INPUT', json.dumps(js))
        subprocess.run(['node'], input=verificacao, text=True, check=True, capture_output=True)


if __name__ == '__main__':
    unittest.main()
