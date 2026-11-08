import json,csv,re
D=json.load(open('dados_final.json')); P=[list(p) for p in D['p']]; F=[list(f) for f in D['f']]
def limpa_nome(nome):
    n=re.sub(r'\s+',' ',(nome or '')).strip(' .,;:()-')
    if n.lower() in ('pai incógnito','mãe incógnita','avô incógnito','avó incógnita'): return n
    n=re.sub(r'^.*?:\s*','',n)
    n=re.sub(r'^\(?\s*(?:segundo|terceiro|primeiro)\s+casamento\)?\s*','',n,flags=re.I)
    n=re.sub(r'^(?:tamb[ée]m|um filho|uma filha|filho|filha|o|a|os|as|e|de|do|da|dos|das|com|que|sua|seu)\s+','',n,flags=re.I)
    n=re.sub(r'^[\dA-Z]{1,3}[-:.]\s*','',n)
    n=re.sub(r'\s+(?:j[áa] defunt[oa]|falecid[oa]|vi[úu]v[oa])\b.*$','',n,flags=re.I)
    n=re.sub(r'\s+(?:que|em|no|na|nos|nas|ao|aos|pelo|pela|onde|quando|porque|depois|antes|morador[ae]?s?|natural|nascid[oa]|batizad[oa]|solteir[oa]|casad[oa]|filh[oa])\b.*$','',n,flags=re.I)
    n=re.sub(r'\s+e\s+(?:matern[oa]|patern[oa])\b.*$','',n,flags=re.I)
    n=re.sub(r',\s*(?:jornaleir|lavrador|pedreir|sapateir|alfaiat|cordoeir|tendeir|carpinteir|ferreir|negociant|proprietári)\w*.*$','',n,flags=re.I)
    n=re.sub(r'\s+\d{1,2}\s+de\s+\w+.*$','',n,flags=re.I)
    n=re.sub(r'\s+[A-Z]$','',n)
    n=re.sub(r'\s*\([^)]*$','',n)
    return n.strip(' .,;:()-')
def ano(s):
    m=re.search(r'(\d{4})',s or ''); return int(m.group(1)) if m else None
def nasc(i): return ano(P[i][2]) or ano(P[i][3])
alterados=0
for p in P:
    novo=limpa_nome(p[0])
    if novo and novo!=p[0]: p[0]=novo; alterados+=1
print('nomes limpos:',alterados)
removidas=[]
# casamentos impossíveis: cônjuge falecido antes, ou criança à data
for f in F:
    ym=ano(f[2])
    if not ym: continue
    for pos in (0,1):
        x=f[pos]
        if x<0: continue
        yo=ano(P[x][4]); yn=nasc(x)
        if (yo and yo<ym) or (yn and yn>ym-12):
            removidas.append([P[x][0],P[x][2] or P[x][3],'cônjuge',P[f[1-pos]][0] if f[1-pos]>=0 else '?',f[2],
                              'casamento depois do óbito' if (yo and yo<ym) else 'idade impossível à data do casamento','; '.join(P[x][10][:2])])
            f[pos]=-1
for fi,f in enumerate(F):
    manter=[]
    for c in f[4]:
        if c in (f[0],f[1]):
            removidas.append([P[c][0],P[c][2] or P[c][3],'próprio',P[c][0],'','pessoa ligada como filho de si mesma','; '.join(P[c][10][:2])])
            if P[c][6]==fi: P[c][6]=-1
            continue
        yc=nasc(c); mau=None
        if yc:
            for x,rot in ((f[0],'pai'),(f[1],'mãe')):
                if x<0: continue
                yp=nasc(x); yo=ano(P[x][4])
                if yp and (yp>yc-12 or yp<yc-70): mau=(rot,P[x][0],P[x][2] or P[x][3],'progenitor nascido '+('depois' if yp>yc else 'cedo demais')); break
                if yo and yo<yc-1: mau=(rot,P[x][0],P[x][4],'progenitor já falecido'); break
        if mau:
            removidas.append([P[c][0],P[c][2] or P[c][3],mau[0],mau[1],mau[2],mau[3],'; '.join(P[c][10][:2])])
            if P[c][6]==fi: P[c][6]=-1
        else: manter.append(c)
    f[4]=manter
# reparar quem ficou sem família de origem mas consta como filho noutra
reparados=0
for fi,f in enumerate(F):
    for c in f[4]:
        if P[c][6]<0: P[c][6]=fi; reparados+=1
print('ligações de filiação repostas:',reparados)
json.dump({'p':P,'f':F},open('dados_final.json','w'),ensure_ascii=False,separators=(',',':'))
with open('suspeitas.csv','w',newline='',encoding='utf-8') as fh:
    w=csv.writer(fh); w.writerow(['filho','data_filho','relacao','progenitor','data_progenitor','motivo','fontes_filho']); w.writerows(removidas)
print('ligações removidas e registadas:',len(removidas))
print('pessoas sem família de origem:',sum(1 for p in P if p[6]<0),'de',len(P))
