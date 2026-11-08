import json,re,csv,unicodedata,collections
def sa(s):
    s=unicodedata.normalize('NFD',s or ''); return ''.join(c for c in s if unicodedata.category(c)!='Mn').lower()
def ch(n): return re.sub(r'\s*\(.*?\)\s*','',sa(n)).strip()
D=json.load(open('dados_registos.json')); P=[list(p) for p in D['p']]; F=[list(f) for f in D['f']]
NOME,SEXO,NASC,BAPT,OBITO,COD,FAMC,FAMS,FAMILIA,REFS,FONTES=range(11)
HUSB,WIFE,MARR,NOTA,CHIL=range(5)
def pais(i):
    fc=P[i][FAMC]
    if fc<0: return ('','')
    h,w=F[fc][HUSB],F[fc][WIFE]
    return (ch(P[h][NOME]) if h>=0 else '', ch(P[w][NOME]) if w>=0 else '')
pai=list(range(len(P)))
def find(x):
    while pai[x]!=x: pai[x]=pai[pai[x]]; x=pai[x]
    return x
def une(a,b):
    ra,rb=find(a),find(b)
    if ra!=rb: pai[max(ra,rb)]=min(ra,rb)
por_nome=collections.defaultdict(list)
for i,p in enumerate(P):
    k=ch(p[NOME])
    if len(k)>7: por_nome[k].append(i)
filhos_de={}
for fi,f in enumerate(F):
    for c in f[CHIL]:
        filhos_de.setdefault((f[HUSB],f[WIFE]),[]).append(c)
pai_de={}
for fi,f in enumerate(F):
    for c in f[CHIL]:
        for x in (f[HUSB],f[WIFE]):
            if x>=0: pai_de.setdefault(c,set()).add(x)
def parentes_diretos(i,j):
    return j in pai_de.get(i,()) or i in pai_de.get(j,())
conjuges={}
for f in F:
    for a,b2 in ((f[HUSB],f[WIFE]),(f[WIFE],f[HUSB])):
        if a>=0 and b2>=0: conjuges.setdefault(a,set()).add(ch(P[b2][NOME]))
pares=[]
for k,ids in por_nome.items():
    if len(ids)<2 or len(ids)>60: continue
    for a in range(len(ids)):
        for b in range(a+1,len(ids)):
            i,j=ids[a],ids[b]
            di={P[i][NASC],P[i][BAPT],P[i][OBITO]}-{''}
            dj={P[j][NASC],P[j][BAPT],P[j][OBITO]}-{''}
            dcom=di&dj
            pi,pj=pais(i),pais(j)
            pcom=(pi[0] and pi[0]==pj[0] and pi[1] and pi[1]==pj[1])
            motivo=''
            if parentes_diretos(i,j): continue
            if P[i][COD] and P[j][COD] and P[i][COD]!=P[j][COD] and P[i][FAMILIA]==P[j][FAMILIA]: continue
            if P[i][FAMC]>=0 and P[i][FAMC]==P[j][FAMC]: continue   # irmãos: nunca são a mesma pessoa
            def _a(x):
                m=re.search(r'(\d{4})',x or ''); return int(m.group(1)) if m else None
            oi,oj=_a(P[i][OBITO]),_a(P[j][OBITO])
            ni,nj=_a(P[i][NASC]) or _a(P[i][BAPT]),_a(P[j][NASC]) or _a(P[j][BAPT])
            if (oi and nj and oi<nj) or (oj and ni and oj<ni): continue   # um morreu antes de o outro nascer
            if dcom: motivo='data coincidente: '+', '.join(sorted(dcom))
            elif pcom: motivo='mesmo pai e mesma mãe'
            elif conjuges.get(i) and conjuges.get(j) and (conjuges[i]&conjuges[j]): motivo='mesmo cônjuge: '+', '.join(sorted(conjuges[i]&conjuges[j])[:1])
            if motivo:
                conf=''
                for campo,nm in ((NASC,'nascimento'),(BAPT,'batismo'),(OBITO,'óbito')):
                    if P[i][campo] and P[j][campo] and P[i][campo]!=P[j][campo]: conf+=f"{nm}: {P[i][campo]} vs {P[j][campo]}; "
                pares.append((i,j,motivo,conf.strip('; ')))
                if not conf: une(i,j)
grupos=collections.defaultdict(list)
for i in range(len(P)): grupos[find(i)].append(i)
novo={}; NP=[]
for raiz,ids in sorted(grupos.items()):
    ids.sort(key=lambda i:-sum(1 for c in (P[i][NASC],P[i][BAPT],P[i][OBITO],P[i][COD]) if c))
    base=list(P[ids[0]]); refs=list(base[REFS]); fontes=list(base[FONTES])
    for i in ids[1:]:
        for campo in (NASC,BAPT,OBITO,SEXO,COD,FAMILIA):
            if not base[campo] and P[i][campo]: base[campo]=P[i][campo]
        if len(P[i][NOME])>len(base[NOME]): base[NOME]=P[i][NOME]
        for r in P[i][REFS]:
            if r not in refs: refs.append(r)
        for f2 in P[i][FONTES]:
            if f2 not in fontes: fontes.append(f2)
    base[REFS]=refs; base[FONTES]=fontes[:12]; base[FAMS]=[]; base[FAMC]=-1
    for i in ids: novo[i]=len(NP)
    NP.append(base)
porcasal={}; FF=[]
for f in F:
    h=novo[f[HUSB]] if f[HUSB]>=0 else -1
    w=novo[f[WIFE]] if f[WIFE]>=0 else -1
    ch2=sorted(set(novo[c] for c in f[CHIL]))
    k=(h,w)
    if k!=(-1,-1) and k in porcasal:
        g=FF[porcasal[k]]
        if not g[2]: g[2]=f[MARR]
        if not g[3]: g[3]=f[NOTA]
        g[4]=sorted(set(g[4]+ch2)); continue
    porcasal[k]=len(FF); FF.append([h,w,f[MARR],f[NOTA],ch2])
for fi,f in enumerate(FF):
    for x in (f[0],f[1]):
        if x>=0 and fi not in NP[x][FAMS]: NP[x][FAMS].append(fi)
    for c in f[4]:
        if NP[c][FAMC]<0: NP[c][FAMC]=fi
json.dump({'p':NP,'f':FF},open('dados_final.json','w'),ensure_ascii=False,separators=(',',':'))
with open('duplicados.csv','a',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh)
    for i,j,motivo,conf in pares:
        da=' / '.join(x for x in (P[i][NASC],P[i][BAPT],P[i][OBITO]) if x)
        db=' / '.join(x for x in (P[j][NASC],P[j][BAPT],P[j][OBITO]) if x)
        w.writerow([P[i][NOME],P[i][FAMILIA],P[i][COD],da,P[j][NOME],P[j][FAMILIA],P[j][COD],db,motivo,conf,'sim'])
print('fusões por registo:',len(pares))
print('pessoas:',len(P),'->',len(NP),'| famílias:',len(F),'->',len(FF))
print('com fontes:',sum(1 for p in NP if p[FONTES]),'| sem família de origem:',sum(1 for p in NP if p[FAMC]<0))
print('com data:',sum(1 for p in NP if p[NASC] or p[BAPT] or p[OBITO]))
