"""Controles locais de pausa, retomada e estado da coleta documental."""
import argparse
import contextlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
PASTA = ROOT / 'coleta_documental'

@contextlib.contextmanager
def trava_coleta(pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / 'coletor.lock'
    handle = os.fdopen(os.open(arquivo, os.O_CREAT | os.O_RDWR), 'r+b')
    locked = False
    try:
        if os.fstat(handle.fileno()).st_size == 0:
            handle.write(b'0'); handle.flush()
        handle.seek(0)
        try:
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            locked = True
        except OSError as exc:
            raise RuntimeError('A coleta já está em execução.') from exc
        yield
    finally:
        if locked:
            handle.seek(0)
            if os.name == 'nt':
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()

def coletor_ativo(pasta):
    try:
        with trava_coleta(pasta): return False
    except RuntimeError:
        return True

def solicitar_pausa(pasta):
    pasta.mkdir(parents=True, exist_ok=True)
    (pasta / 'PARAR').touch()
    if not coletor_ativo(pasta):
        return mensagem_estado(estado(pasta))
    return 'Pausa solicitada. Aguarde a confirmação de que a coleta parou.'

def retomar(pasta, motor_dir):
    if coletor_ativo(pasta):
        return 'O coletor ainda está ativo. Aguarde a pausa terminar antes de retomar.'
    if not (motor_dir / 'pje_links_motor.py').is_file():
        raise ValueError('Não foi encontrado o motor do PJe na pasta informada.')
    (pasta / 'PARAR').unlink(missing_ok=True)
    exe = Path(sys.executable)
    if exe.name.lower() == 'pythonw.exe': exe = exe.with_name('python.exe')
    with (pasta/'execucao.log').open('ab') as saida, (pasta/'erros.log').open('ab') as erros:
        proc = subprocess.Popen([str(exe), '-X', 'utf8', '-u', str(ROOT/'coletar_pecas.py'),
                                 '--motor-dir', str(motor_dir)], cwd=ROOT,
                                stdout=saida, stderr=erros,
                                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
    (pasta/'processo.pid').write_text(str(proc.pid), encoding='ascii')
    return 'Retomada iniciada. Os arquivos já conferidos serão reaproveitados.'

def estado(pasta):
    ativo = coletor_ativo(pasta)
    p = pasta/'progresso.json'
    dados = json.loads(p.read_text(encoding='utf-8')) if p.exists() else {}
    situacao = ('Pausando — aguarde a consulta atual terminar' if (pasta/'PARAR').exists()
                else 'Em execução') if ativo else 'Parada — dados salvos; pode retomar'
    if not ativo and dados.get('estado_execucao') == 'concluida': situacao = 'Coleta documental concluída'
    if not ativo and dados.get('estado_execucao') == 'finalizada_com_pendencias': situacao = 'Rodada encerrada com pendências'
    if not ativo and dados.get('estado_execucao') == 'erro': situacao = 'Parada após erro — confira o registro de erros'
    return {'ativo':ativo, 'situacao':situacao, **dados}

def mensagem_estado(dados):
    if not dados['ativo']:
        if dados.get('estado_execucao') == 'erro':
            return 'A coleta já está parada após um erro. Pode fechar o painel e desligar; o progresso salvo será reaproveitado na retomada.'
        return 'Coleta parada. Pode fechar o painel e desligar; o progresso salvo será reaproveitado na retomada.'
    if dados['situacao'].startswith('Pausando'):
        return 'Pausa solicitada. Aguarde a operação atual terminar e o estado mudar para Parada.'
    return 'Coleta em execução. Para interromper, clique em Pausar.'

def interface(motor_dir):
    import tkinter as tk
    from tkinter import messagebox, ttk
    win=tk.Tk();win.title('Coleta do estudo TSE — outubro de 2026');win.geometry('590x330')
    quadro=ttk.Frame(win,padding=22);quadro.pack(fill='both',expand=True)
    titulo=tk.StringVar();contagem=tk.StringVar();mensagem=tk.StringVar()
    ttk.Label(quadro,textvariable=titulo,font=('Segoe UI',13,'bold'),wraplength=540).pack(anchor='w')
    ttk.Label(quadro,textvariable=contagem,justify='left',padding=(0,16)).pack(anchor='w')
    botoes=ttk.Frame(quadro);botoes.pack(anchor='w')
    def acao(func):
        try: mensagem.set(func());atualizar(False)
        except Exception as exc: messagebox.showerror('Coleta TSE',str(exc))
    ttk.Button(botoes,text='Pausar',command=lambda:acao(lambda:solicitar_pausa(PASTA))).pack(side='left',padx=(0,10))
    ttk.Button(botoes,text='Retomar',command=lambda:acao(lambda:retomar(PASTA,motor_dir))).pack(side='left',padx=(0,10))
    ttk.Button(botoes,text='Abrir pasta',command=lambda:os.startfile(PASTA)).pack(side='left')
    ttk.Label(quadro,textvariable=mensagem,wraplength=540,padding=(0,12)).pack(anchor='w')
    ttk.Label(quadro,text='Antes de desligar: clique em Pausar e aguarde “Parada”.\nFechar esta janela não interrompe a coleta.\nA retomada após reiniciar o computador é feita pelo botão Retomar.',wraplength=540).pack(anchor='w')
    def atualizar(reagendar=True):
        try:
            d=estado(PASTA);titulo.set(d['situacao']);mensagem.set(mensagem_estado(d))
            contagem.set(f"Processos consultados: {d.get('consultas_efetuadas',0)} / {d.get('total_alvos',0)}\nProcessos sem pendências de download: {d.get('processos_sem_pendencias_de_download',0)}\nPeças conferidas: {d.get('pecas_conferidas',0)}")
        except Exception as exc:mensagem.set(str(exc))
        if reagendar:win.after(1500,atualizar)
    atualizar();win.mainloop()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('acao',choices=['painel','pausar','retomar','status'],nargs='?',default='painel')
    p.add_argument('--motor-dir',type=Path,default=next((r for r in ROOT.parents if (r/'pje_links_motor.py').is_file()),ROOT))
    a=p.parse_args()
    if a.acao=='painel':interface(a.motor_dir)
    elif a.acao=='pausar':print(solicitar_pausa(PASTA))
    elif a.acao=='retomar':print(retomar(PASTA,a.motor_dir))
    else:print(json.dumps(estado(PASTA),ensure_ascii=False,indent=2))
