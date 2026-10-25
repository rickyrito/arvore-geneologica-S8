#!/usr/bin/env python3
"""Confere index.html contra docs/DESIGN.md.

Corre-se antes de publicar:  python3 scripts/validar_design.py
Sai com código 1 se houver violações.
"""
import re, sys, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(RAIZ, 'index.html')

TOKENS = ['--papel', '--papel-2', '--tinta', '--tinta-fraca', '--linha',
          '--azulejo', '--azulejo-claro', '--ocre', '--display', '--corpo']

def main():
    html = open(HTML, encoding='utf-8').read()
    blocos = re.findall(r'<style>(.*?)</style>', html, re.S)
    if not blocos:
        print('ERRO: não encontrei nenhum bloco <style>'); return 1
    css = '\n'.join(blocos)   # a versão pública tem um reset no <head> e o bloco principal
    erros, avisos = [], []

    # 1. os três blocos de tema
    if not re.search(r':root\s*\{', css):
        erros.append('falta o bloco :root com os tokens claros')
    if not re.search(r'@media\s*\(prefers-color-scheme:\s*dark\)\s*\{\s*:root:not\(\[data-theme="light"\]\)', css):
        erros.append('falta o bloco @media prefers-color-scheme:dark com :root:not([data-theme="light"])')
    if not re.search(r':root\[data-theme="dark"\]', css):
        erros.append('falta o bloco :root[data-theme="dark"]')

    # 2. todos os tokens definidos no bloco claro
    claro = css.split('@media')[0]
    for t in TOKENS:
        if t + ':' not in claro:
            erros.append(f'token {t} não está definido no bloco :root claro')

    # 3. cores literais fora das definições de token
    for linha in css.splitlines():
        s = linha.strip()
        if not s or s.startswith('/*'):
            continue
        if re.match(r'--[\w-]+\s*:', s):      # definição de token: pode ter literal
            continue
        for cor in re.findall(r'#[0-9a-fA-F]{3,8}\b', s):
            erros.append(f'cor literal {cor} fora de um token: {s[:70]}')
        if re.search(r'\b(rgb|rgba|hsl|hsla)\(', s) and 'var(' not in s:
            avisos.append(f'cor em função fora de token: {s[:70]}')

    # 4. bordas: raio máximo 2px, sem sombras
    for v in re.findall(r'border-radius:\s*([^;}]+)', css):
        for n in re.findall(r'(\d+(?:\.\d+)?)px', v):
            if float(n) > 2:
                erros.append(f'border-radius {n}px acima do máximo de 2px')
    if re.search(r'box-shadow\s*:', css):
        erros.append('box-shadow não é permitido')

    # 5. bordas com cor que não vem de token
    for b in re.findall(r'border(?:-\w+)?\s*:\s*([^;}]+)', css):
        if '#' in b or re.search(r'\b(rgb|hsl)', b):
            erros.append(f'borda com cor literal: {b.strip()[:60]}')

    # 6. foco visível
    if 'outline:2px solid var(--azulejo)' not in css.replace(' ', '').replace('outline:', 'outline:'):
        if not re.search(r'outline:\s*2px\s+solid\s+var\(--azulejo\)', css):
            avisos.append('não encontrei o foco de teclado com outline 2px azulejo')

    # 7. notação genealógica no JS
    js = html[html.rfind('<script>'):]
    for simbolo, nome in (("'* '", 'nascimento'), ("'† '", 'óbito'), ("'⚭ '", 'casamento')):
        if simbolo not in js:
            erros.append(f'falta o símbolo {simbolo.strip()} ({nome}) na apresentação das datas')
    if "replace(/\\//g, '-')" not in js and "replace(/\\//g,'-')" not in js:
        erros.append('as datas não estão a ser convertidas para DD-MM-AAAA')

    # 8. números em coluna com tabular-nums
    if css.count('tabular-nums') < 4:
        avisos.append('poucos elementos com font-variant-numeric:tabular-nums')

    # 9. segurança: nada de innerHTML com dados
    if re.search(r'\.innerHTML\s*=', js):
        erros.append('uso de innerHTML no script: os nomes vêm de transcrições, usar textContent')

    for e in erros:
        print('VIOLAÇÃO:', e)
    for a in avisos:
        print('aviso   :', a)
    print(f'\n{len(erros)} violações, {len(avisos)} avisos.')
    return 1 if erros else 0

if __name__ == '__main__':
    sys.exit(main())
