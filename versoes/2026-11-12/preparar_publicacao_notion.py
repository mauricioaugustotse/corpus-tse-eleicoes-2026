"""Gera substituições pontuais para publicação, sem tocar na seção 7."""
import difflib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent
def conteudo(texto):
    if '<content>\n' in texto:texto=texto.split('<content>\n',1)[1].rsplit('</content>',1)[0]
    return texto.strip('\n')
def main():
    antigo=conteudo((ROOT/'pagina_referencia_notion.md').read_text(encoding='utf-8'))
    novo=(ROOT/'pagina_proposta.md').read_text(encoding='utf-8').split('\n\n',1)[1].rstrip('\n')
    arquivo=ROOT/'coleta_documental/publicacao/uploads_notion.json'
    uploads=json.loads(arquivo.read_text(encoding='utf-8'))
    fontes={r['filename']:r['markdown_source'] for r in uploads}
    def anexo(m):
        nome=m[1]
        if nome not in fontes:raise ValueError('Anexo sem upload: '+nome)
        return fontes[nome]
    novo=re.sub(r'graficos_interativos/([^"\n]+\.(?:html|png))',anexo,novo)
    if 'graficos_interativos/' in novo:raise ValueError('Referência gráfica local remanescente')
    limite_antigo=re.search(r'^## 7\.',antigo,re.M).start();limite_novo=re.search(r'^## 7\.',novo,re.M).start()
    assert antigo[limite_antigo:]==novo[limite_novo:],'Seção 7 difere'
    a=antigo[:limite_antigo].rstrip('\n').split('\n\n');b=novo[:limite_novo].rstrip('\n').split('\n\n')
    opcodes=difflib.SequenceMatcher(a=a,b=b,autojunk=False).get_opcodes()
    intervalos=[]
    original_prefixo=antigo[:limite_antigo]
    for pos,(tag,ini,fim,jini,jfim) in enumerate(opcodes):
        if tag=='equal':continue
        def unico():
            trecho='\n\n'.join(a[ini:fim])
            return bool(trecho) and original_prefixo.count(trecho)==1
        if not unico() and pos and opcodes[pos-1][0]=='equal':
            limite=opcodes[pos-1][1]
            while ini>limite and not unico():ini-=1;jini-=1
        if not unico() and pos+1<len(opcodes) and opcodes[pos+1][0]=='equal':
            limite=opcodes[pos+1][2]
            while fim<limite and not unico():fim+=1;jfim+=1
        if intervalos and ini<intervalos[-1][1]:
            anterior=intervalos[-1];intervalos[-1]=[anterior[0],max(fim,anterior[1]),anterior[2],max(jfim,anterior[3])]
        else:intervalos.append([ini,fim,jini,jfim])
    # Une grupos somente quando a âncora não é única (células de tabela se repetem).
    i=0
    while i<len(intervalos):
        ini,fim,jini,jfim=intervalos[i];s='\n\n'.join(a[ini:fim])
        if s and antigo.count(s)==1:i+=1;continue
        if i+1<len(intervalos):
            prox=intervalos.pop(i+1);intervalos[i]=[ini,prox[1],jini,prox[3]]
        elif i:
            atual=intervalos.pop(i);anterior=intervalos[i-1];intervalos[i-1]=[anterior[0],atual[1],anterior[2],atual[3]];i-=1
        else:raise ValueError('Não foi possível obter âncora única sem a seção 7')
    # Mantém as seções como limites de alteração mesmo quando todas as suas
    # frases mudaram; assim tabelas e relatos não viram uma única operação.
    for numero in range(2,7):
        marca=f'## {numero}.'
        ia=next(i for i,p in enumerate(a) if p.startswith(marca))
        ib=next(i for i,p in enumerate(b) if p.startswith(marca))
        novos=[]
        for i,f,j,k in intervalos:
            if i<ia<f and j<ib<k:novos.extend([[i,ia,j,ib],[ia,f,ib,k]])
            else:novos.append([i,f,j,k])
        intervalos=novos
    updates=[{'old_str':'\n\n'.join(a[i:f]),'new_str':'\n\n'.join(b[j:k])} for i,f,j,k in intervalos]
    simulado=antigo
    for u in updates:
        assert simulado.count(u['old_str'])==1,'Substituição ambígua'
        assert not re.search(r'^## 7\.',u['old_str']+'\n'+u['new_str'],re.M),'Seção 7 incluída na operação'
        simulado=simulado.replace(u['old_str'],u['new_str'],1)
    assert simulado==novo,'As substituições não reproduzem a proposta'
    saida=ROOT/'coleta_documental/publicacao';saida.mkdir(parents=True,exist_ok=True)
    (saida/'updates.json').write_text(json.dumps(updates,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (saida/'pagina_esperada.md').write_text(novo+'\n',encoding='utf-8')
    # A API limita o corpo das requisições. Se a substituição exata de mídias
    # não for aceita, estes passos recompõem os mesmos blocos por seções,
    # com trechos balanceados e a seção 7 copiada literalmente.
    marcas=list(re.finditer(r'^## ([1-7])\. ',novo,re.M));secoes={}
    for pos,m in enumerate(marcas):secoes[int(m[1])]=novo[m.start():marcas[pos+1].start() if pos+1<len(marcas) else len(novo)].strip('\n')
    ancoras={2:'Atualizando os quadros de volume e votação.',3:'Atualizando a metodologia do estudo.',4:'Atualizando o comparativo entre campanhas.',5:'Atualizando os relatos dos processos.',6:'Atualizando os demais eixos do estudo.'}
    inicial='\n\n'.join([secoes[1],*[ancoras[k] for k in range(2,7)],secoes[7]])
    passos=[{'command':'replace_content','new_str':inicial}]
    for k in [2,3,4,6]:passos.append({'command':'update_content','old_str':ancoras[k],'new_str':secoes[k]})
    relatos=list(re.finditer(r'^### \d+\. ',secoes[5],re.M));pre=secoes[5][:relatos[0].start()].strip('\n')
    partes=[secoes[5][m.start():relatos[i+1].start() if i+1<len(relatos) else len(secoes[5])].strip('\n') for i,m in enumerate(relatos)]
    ancora='Relatos em atualização.'
    passos.append({'command':'update_content','old_str':ancoras[5],'new_str':pre+'\n\n'+ancora})
    for i in range(0,len(partes),40):
        trecho='\n\n'.join(partes[i:i+40])
        if i+40<len(partes):trecho+='\n\n'+ancora
        passos.append({'command':'update_content','old_str':ancora,'new_str':trecho})
    simulado=inicial
    for passo in passos[1:]:
        assert simulado.count(passo['old_str'])==1
        simulado=simulado.replace(passo['old_str'],passo['new_str'],1)
    assert simulado==novo,'Publicação por seções difere da proposta'
    (saida/'passos_por_secoes.json').write_text(json.dumps(passos,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'substituicoes':len(updates),'maior_substituicao_bytes':max(len((u['old_str']+u['new_str']).encode('utf-8')) for u in updates),'secao7_fora_das_operacoes':True},ensure_ascii=False))
if __name__=='__main__':main()
