import json,csv,re,unicodedata,collections
def sa(s):
    s=unicodedata.normalize('NFD',s or ''); return ''.join(c for c in s if unicodedata.category(c)!='Mn').lower()
def ch(nome): return re.sub(r'\s*\(.*?\)\s*','',sa(nome)).strip()
def cauda(nome):
    p=ch(nome).split()
    return ' '.join(p[-3:]) if len(p)>=3 else ' '.join(p)
def limpa(nome):
    n=re.sub(r'\s+',' ',(nome or '')).strip(' .,;:()-')
    n=re.sub(r'^.*?:\s*','',n)
    n=re.sub(r'^\(?\s*(?:segundo|terceiro|primeiro)\s+casamento\)?\s*','',n,flags=re.I)
    n=re.sub(r'^(?:tamb[ée]m|um filho|uma filha|filho|filha|o|a|os|as|e|de|do|da|dos|das|com|que|sua|seu)\s+','',n,flags=re.I)
    n=re.sub(r'^[\dA-Z]{1,3}[-:.]\s*','',n)
    n=re.sub(r'^Dia\s+\d+.*?\s','',n,flags=re.I)
    n=re.sub(r'\s*\([^)]*$','',n)
    n=re.sub(r'\s+(?:j[áa] defunt[oa]|falecid[oa]|vi[úu]v[oa])\b.*$','',n,flags=re.I)
    n=re.sub(r'\s+(?:que|em|no|na|nos|nas|ao|aos|pelo|pela|onde|quando|porque|depois|antes|morador[ae]?s?|natural|nascid[oa]|batizad[oa]|solteir[oa]|casad[oa])\b.*$','',n,flags=re.I)
    n=re.sub(r'\s+\d{1,2}\s+de\s+\w+.*$','',n,flags=re.I)
    n=re.sub(r'\s+[A-Z]$','',n)
    return n.strip(' .,;:()-')
D=json.load(open('dados_fundido.json'))
P=[list(p) for p in D['p']]; F=[list(f) for f in D['f']]
NOME,SEXO,NASC,BAPT,OBITO,COD,FAMC,FAMS,FAMILIA,REFS=range(10)
for p in P: p.append([])            # 10 = fontes
FONTES=10
HUSB,WIFE,MARR,NOTA,CHIL=range(5)
por_nome=collections.defaultdict(list)
por_cauda=collections.defaultdict(list)
for i,p in enumerate(P):
    por_nome[ch(p[NOME])].append(i); por_cauda[cauda(p[NOME])].append(i)
casal={}
for fi,f in enumerate(F):
    casal[(f[HUSB],f[WIFE])]=fi
def pais_de(i):
    fc=P[i][FAMC]
    if fc<0: return ('','')
    h,w=F[fc][HUSB],F[fc][WIFE]
    return (ch(P[h][NOME]) if h>=0 else '', ch(P[w][NOME]) if w>=0 else '')
def novo(nome,familia='Assentos paroquiais'):
    P.append([limpa(nome),'','','','','',-1,[],familia,[],[]])
    i=len(P)-1; por_nome[ch(nome)].append(i); por_cauda[cauda(nome)].append(i); return i
def ano(s):
    m=re.search(r'(\d{4})',s or ''); return int(m.group(1)) if m else None
def encontra(nome,datas=(),pai='',mae='',criar=True,familia='Assentos paroquiais'):
    nome=limpa(nome)
    if len(nome)<4: return -1
    k=ch(nome); cands=list(por_nome.get(k,[]))
    primeiro=(k.split() or [''])[0]
    for x in por_cauda.get(cauda(nome),[]):
        px=(ch(P[x][NOME]).split() or [''])[0]
        if px==primeiro and x not in cands: cands.append(x)
    melhor=(-1,0)
    anos_reg=[int(re.search(r'(\d{4})',d).group(1)) for d in datas if d and re.search(r'(\d{4})',d)]
    for i in cands:
        if anos_reg:
            yo=ano(P[i][OBITO]); yn=ano(P[i][NASC]) or ano(P[i][BAPT])
            if yo and min(anos_reg)>yo: continue
            if yn and max(anos_reg)<yn: continue
        s=0
        dp={P[i][NASC],P[i][BAPT],P[i][OBITO]}-{''}
        if dp & set(d for d in datas if d): s+=3
        ppai,pmae=pais_de(i)
        if pai and ppai and ch(pai)==ppai: s+=2
        if mae and pmae and ch(mae)==pmae: s+=2
        if s>melhor[1]: melhor=(i,s)
    if melhor[1]>=2: return melhor[0]
    return novo(nome,familia) if criar else -1
casal_nome={}
def casal_por_nome(pn,mn,data=''):
    pn=limpa(pn); mn=limpa(mn)
    if not mn and ' e ' in pn: pn,mn=separa(pn)
    if len(pn)<4 and len(mn)<4: return -1
    k=(ch(pn),ch(mn)); k2=(cauda(pn),cauda(mn))
    if k not in casal_nome and k2 in casal_nome: k=k2
    if k in casal_nome:
        fi=casal_nome[k]
        if data and not F[fi][MARR]: F[fi][MARR]=data
        return fi
    i=encontra(pn,criar=True) if len(pn)>=4 else -1
    j=encontra(mn,criar=True) if len(mn)>=4 else -1
    fi=familia_de(i,j,data); casal_nome[k]=fi; casal_nome.setdefault(k2,fi)
    return fi
def familia_de(i,j,data=''):
    if i<0 and j<0: return -1
    k=(i,j)
    if k in casal:
        fi=casal[k]
        if data and not F[fi][MARR]: F[fi][MARR]=data
        return fi
    F.append([i,j,data,'',[]]); fi=len(F)-1; casal[k]=fi
    for x in (i,j):
        if x>=0 and fi not in P[x][FAMS]: P[x][FAMS].append(fi)
    return fi
def nasc_de(i):
    return ano(P[i][NASC]) or ano(P[i][BAPT])
def plausivel(fi,c):
    yc=nasc_de(c)
    if yc is None: return True
    for x in (F[fi][HUSB],F[fi][WIFE]):
        if x<0: continue
        yp=nasc_de(x)
        if yp is not None and (yp>yc-12 or yp<yc-70): return False
        yo=ano(P[x][OBITO])
        if yo is not None and yo<yc-1: return False
    return True
recusas=[0]
def liga_filho(fi,c):
    if fi<0 or c<0: return
    if not plausivel(fi,c): recusas[0]+=1; return
    if c not in F[fi][CHIL]: F[fi][CHIL].append(c)
    if P[c][FAMC]<0: P[c][FAMC]=fi
def separa(nome):
    p=re.split(r'\s+e\s+(?:de\s+)?',limpa(nome),maxsplit=1)
    return (limpa(p[0]), limpa(p[1]) if len(p)>1 else '')
def par(texto):
    t=limpa(texto)
    if not t: return ('','')
    p=re.split(r'\s+e\s+(?:de\s+)?',t,maxsplit=1)
    return (limpa(p[0]), limpa(p[1]) if len(p)>1 else '')
# ---- datas, parentesco e idade -------------------------------------------
import datetime
def dia(s):
    """DD/MM/AAAA -> número de dias; None se não for data completa."""
    m=re.match(r'\s*(\d{1,2})/(\d{1,2})/(\d{4})\s*$',s or '')
    if not m: return None
    d,mo,a=(int(x) for x in m.groups())
    try: return datetime.date(a,mo,d).toordinal()
    except ValueError: return None
def ordem(s):
    """Chave de ordenação cronológica; sem data vai para o fim."""
    return dia(s) or (ano(s) or 9999)*366
def primeiro_nome(n):
    p=ch(n).split(); return p[0] if p else ''
def casal_existente(pn,mn):
    """Índice da família deste casal, sem a criar."""
    pn=limpa(pn); mn=limpa(mn)
    for k in ((ch(pn),ch(mn)),(cauda(pn),cauda(mn))):
        if k in casal_nome: return casal_nome[k]
    return -1
IDADE=re.compile(r'(\d+)\s*(ano|anos|mes|mês|meses|mez|mezes|dia|dias|hora|horas)',re.I)
def idade_em_dias(t):
    m=IDADE.search(t or '')
    if not m: return None
    n=int(m.group(1)); u=sa(m.group(2))
    if u.startswith('ano'): return n*365
    if u.startswith('me'): return n*30
    if u.startswith('dia'): return n
    return 0
def filho_do_casal(fi,nome,nasc='',bapt='',data_obito='',idade=''):
    """Entre os filhos já ligados a este casal, o que é esta mesma pessoa.

    Serve para o assento não criar uma pessoa nova quando a criança já consta
    da genealogia: o nome próprio tem de coincidir e as datas têm de bater.
    """
    if fi<0: return -1
    pn=primeiro_nome(nome)
    if not pn: return -1
    alvo=None
    if data_obito and idade:
        d=idade_em_dias(idade); o=dia(data_obito)
        if d is not None and o is not None:
            alvo=o-d
            margem=10 if d<31 else (45 if d<366 else 400)
    for c in F[fi][CHIL]:
        if primeiro_nome(P[c][NOME])!=pn: continue
        datas_c=[dia(P[c][NASC]),dia(P[c][BAPT])]
        if alvo is not None:
            if P[c][OBITO] and P[c][OBITO]!=data_obito: continue
            dn=datas_c[0] or datas_c[1]
            if dn is not None and abs(dn-alvo)<=margem: return c
            continue
        for d in (nasc,bapt):
            if d and d in (P[c][NASC],P[c][BAPT]): return c
    return -1
NOVE_MESES=270
def irmao_perto(fi,nasc):
    """Data de nascimento de um irmão a menos de nove meses — gestação impossível."""
    n=dia(nasc)
    if fi<0 or n is None: return ''
    for c in F[fi][CHIL]:
        d=dia(P[c][NASC])
        if d is None or d==n: continue        # mesma data: gémeos
        if abs(d-n)<NOVE_MESES: return P[c][NASC]
    return ''
for fi,f in enumerate(F):
    pn=ch(P[f[HUSB]][NOME]) if f[HUSB]>=0 else ''
    mn=ch(P[f[WIFE]][NOME]) if f[WIFE]>=0 else ''
    if pn or mn:
        casal_nome.setdefault((pn,mn),fi)
        casal_nome.setdefault((cauda(P[f[HUSB]][NOME]) if f[HUSB]>=0 else '', cauda(P[f[WIFE]][NOME]) if f[WIFE]>=0 else ''),fi)
conflitos=[]
def poe(i,campo,valor,fonte,rotulo):
    if not valor: return
    if P[i][campo] and P[i][campo]!=valor:
        conflitos.append([P[i][NOME],rotulo,P[i][campo],valor,fonte]); return
    if not P[i][campo]: P[i][campo]=valor
stats=collections.Counter()
# ---- GENEALOGIAS EM PROSA
import os
if os.path.exists('familias_prosa.csv'):
    for u in csv.DictReader(open('familias_prosa.csv',encoding='utf-8')):
        fam=u['familia']
        i=encontra(u['pessoa'],(),u['pai'],u['mae'],familia=fam)
        j=encontra(u['conjuge'],(),u['pai_conjuge'],u['mae_conjuge'],familia=fam)
        if i<0 or j<0 or i==j: continue
        familia_de(i,j,u['casamento']); stats['prosa_unioes']+=1
        for pessoa,pn,mn in ((i,u['pai'],u['mae']),(j,u['pai_conjuge'],u['mae_conjuge'])):
            if P[pessoa][FAMC]<0 and (pn or mn):
                g=casal_por_nome(pn,mn)
                if g>=0: liga_filho(g,pessoa); stats['prosa_filiacao']+=1
        fonte='Genealogia — Família '+fam
        for pessoa in (i,j):
            if fonte not in P[pessoa][FONTES]: P[pessoa][FONTES].append(fonte)
# ---- BATISMOS  (ordem cronológica: cada assento lê-se depois dos anteriores)
for b in sorted(csv.DictReader(open('batismos.csv',encoding='utf-8')),key=lambda r:ordem(r['data'])):
    nome=b['nome']
    if len(limpa(nome))<5: continue
    fam=casal_existente(b['pai'],b['mae'])
    c=filho_do_casal(fam,nome,b['nascimento'],b['batismo'])
    if c>=0:
        stats['batismo_pela_filiacao']+=1
    else:
        irmao=irmao_perto(fam,b['nascimento'])
        if irmao:
            conflitos.append([limpa(nome),'nascimento',irmao,b['nascimento'],
                f"Batismos {b['ano']} ({b['artigo']}) — irmão nascido a menos de nove meses; assento não aplicado"])
            stats['batismo_recusado_nove_meses']+=1
            continue
        antes=len(P)
        c=encontra(nome,(b['batismo'],b['nascimento']),b['pai'],b['mae'])
        if c<0: continue
        stats['batismo_novo' if len(P)>antes else 'batismo_ligado']+=1
    fonte_b=f"Batismos {b['ano']} ({b['artigo']})"
    poe(c,NASC,b['nascimento'],fonte_b,'nascimento')
    poe(c,BAPT,b['batismo'],fonte_b,'batismo')
    poe(c,OBITO,b['obito_referido'],fonte_b,'óbito')
    P[c][FONTES].append(f"Batismo {b['ano']} — {b['artigo']}")
    fi=casal_por_nome(b['pai'],b['mae'])
    if fi>=0:
        liga_filho(fi,c); stats['pais_ligados']+=1
        pai,mae=F[fi][HUSB],F[fi][WIFE]
        avp=par(b['avos_paternos']); avm=par(b['avos_maternos'])
        if pai>=0 and (avp[0] or avp[1]) and P[pai][FAMC]<0:
            g=casal_por_nome(avp[0],avp[1])
            if g>=0: liga_filho(g,pai); stats['avos_paternos']+=1
        if mae>=0 and (avm[0] or avm[1]) and P[mae][FAMC]<0:
            g=casal_por_nome(avm[0],avm[1])
            if g>=0: liga_filho(g,mae); stats['avos_maternos']+=1
# ---- CASAMENTOS
for m in csv.DictReader(open('casamentos.csv',encoding='utf-8')):
    if len(limpa(m['noivo']))<5 or len(limpa(m['noiva']))<5: continue
    h=encontra(m['noivo'],(m['data'],),m['pai_noivo'],m['mae_noivo'])
    w=encontra(m['noiva'],(m['data'],),m['pai_noiva'],m['mae_noiva'])
    if h<0 or w<0: continue
    fi=familia_de(h,w,m['data']); stats['casamentos_ligados']+=1
    if not F[fi][NOTA] and m['testemunhas']: F[fi][NOTA]='Testemunhas: '+m['testemunhas'][:160]
    for pessoa,pn,mn in ((h,m['pai_noivo'],m['mae_noivo']),(w,m['pai_noiva'],m['mae_noiva'])):
        if P[pessoa][FAMC]<0 and (pn or mn):
            g=casal_por_nome(pn,mn)
            if g>=0: liga_filho(g,pessoa); stats['filiacao_casamento']+=1
    P[h][FONTES].append(f"Casamento {m['data']} — {m['artigo']}")
    P[w][FONTES].append(f"Casamento {m['data']} — {m['artigo']}")
# ---- ÓBITOS  (ordem cronológica; o óbito de criança liga pela idade declarada)
for o in sorted(csv.DictReader(open('obitos.csv',encoding='utf-8')),key=lambda r:ordem(r['data'])):
    if len(limpa(o['nome']))<5: continue
    fam=casal_existente(o['pai'],o['mae'])
    i=filho_do_casal(fam,o['nome'],data_obito=o['data'],idade=o['idade'])
    if i>=0:
        stats['obito_pela_idade']+=1
    else:
        antes=len(P)
        i=encontra(o['nome'],(o['data'],),o['pai'],o['mae'])
        if i<0: continue
        stats['obito_novo' if len(P)>antes else 'obito_ligado']+=1
    poe(i,OBITO,o['data'],f"Óbitos {o['ano']} ({o['artigo']})",'óbito')
    P[i][FONTES].append(f"Óbito {o['data']} — {o['artigo']}")
    if P[i][FAMC]<0 and (o['pai'] or o['mae']):
        g=casal_por_nome(o['pai'],o['mae'])
        if g>=0: liga_filho(g,i); stats['filiacao_obito']+=1
with open('conflitos_registos.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['pessoa','campo','valor_na_genealogia','valor_no_assento','assento']); w.writerows(conflitos)
print('conflitos entre genealogia e assentos:',len(conflitos))
json.dump({'p':P,'f':F},open('dados_registos.json','w'),ensure_ascii=False,separators=(',',':'))
print('pessoas:',len(P),'| famílias:',len(F))
for k,v in sorted(stats.items()): print(f"   {k}: {v}")
print('ligações recusadas por implausibilidade:',recusas[0])
print('pessoas com fontes:',sum(1 for p in P if p[FONTES]))
print('pessoas sem família de origem:',sum(1 for p in P if p[FAMC]<0))
