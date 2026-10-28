# -*- coding: utf-8 -*-
"""
Mini-SK-Computador-27-10-B (teste 10280451) — programa .exe LEVE (Python), feito pelo Mini SK.

Não usa Electron: por isso é pequeno e não dá tela preta.
Você dá dois cliques, abre uma janelinha preta que "liga" o app,
e ele aparece numa janela própria do Edge/Chrome (modo app).
O site inteiro (pasta www) vai guardado DENTRO do .exe.

- Porta fixa (7864): é ela que guarda os seus dados. Não mude.
- Só o próprio computador acessa (127.0.0.1). Ninguém de fora entra.
- Se já estiver ligado, clicar de novo só abre a janela outra vez.
- Para fechar de vez: feche a janelinha preta.
"""
import os, sys, socket, shutil, subprocess, threading, webbrowser, mimetypes
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
except Exception:
    pass

NOME = 'Mini-SK-Computador-27-10-B (teste 10280451)'
PORTA = int(os.environ.get('PORTA', '7864'))
ENDERECO = 'http://127.0.0.1:%d/' % PORTA
# "lacre" já ligado de fábrica: o ⚡ Node (WebContainer) funciona no computador sem recarregar
ISOLAR = False

BASE = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(BASE, 'www')

for ext, tipo in {'.js': 'text/javascript', '.mjs': 'text/javascript', '.cjs': 'text/javascript', '.css': 'text/css',
                  '.json': 'application/json', '.webmanifest': 'application/manifest+json', '.svg': 'image/svg+xml',
                  '.wasm': 'application/wasm', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ico': 'image/x-icon',
                  '.md': 'text/markdown; charset=utf-8'}.items():
    mimetypes.add_type(tipo, ext)


class Pagina(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=SITE, **k)

    def send_head(self):
        caminho = self.translate_path(self.path)
        if not os.path.exists(caminho) and '.' not in os.path.basename(self.path.split('?')[0]):
            self.path = '/index.html'
        return super().send_head()

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        if ISOLAR:
            self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
            self.send_header('Cross-Origin-Embedder-Policy', 'credentialless')
            self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
        super().end_headers()

    def log_message(self, *a):
        pass


def ja_ligado():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', PORTA)) == 0


def abrir_janela():
    if os.environ.get('SEM_ABRIR'):
        return
    candidatos = [shutil.which('msedge'), shutil.which('chrome'),
                  r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
                  r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
                  r'C:\Program Files\Google\Chrome\Application\chrome.exe',
                  os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe')]
    for c in candidatos:
        if c and os.path.isfile(c):
            try:
                subprocess.Popen([c, '--app=' + ENDERECO, '--window-size=1250,880'])
                return
            except OSError:
                pass
    webbrowser.open(ENDERECO)


def main():
    if not os.path.isfile(os.path.join(SITE, 'index.html')):
        print('❌ Não achei o site (pasta www) dentro do programa.')
        input('Aperte Enter para fechar…')
        return
    if ja_ligado():
        print('✅ Já estava ligado. Abrindo a janela…')
        abrir_janela()
        return
    try:
        srv = ThreadingHTTPServer(('127.0.0.1', PORTA), Pagina)
    except OSError:
        print('❌ A porta %d está ocupada por outro programa.' % PORTA)
        input('Aperte Enter para fechar…')
        return
    if os.name == 'nt':
        os.system('title ' + NOME + ' (deixe esta janela aberta)')
    print('━' * 52)
    print('  ✅  %s — LIGADO' % NOME)
    print('━' * 52)
    print('  Abrindo a janela do app…  (se não abrir, use: %s)' % ENDERECO)
    print('  Pode minimizar esta janelinha.')
    print('  Para DESLIGAR: feche esta janelinha.')
    print('━' * 52)
    threading.Timer(0.6, abrir_janela).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
