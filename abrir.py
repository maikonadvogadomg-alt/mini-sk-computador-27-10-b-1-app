# -*- coding: utf-8 -*-
"""
MINI SK PARA PC — programa .exe LEVE (Python), sem Electron e sem tela preta.

Dois cliques: abre uma janelinha preta (é ela que liga tudo; pode minimizar)
e o Mini SK numa janela própria do Edge/Chrome. Por dentro ele liga:
  - o ⚡ Node (WebContainer) já com o lacre — funciona de primeira;
  - o 💻 Terminal do computador (cmd do Windows) no painel do terminal;
  - a ⇅ ponte e a 🔄 pasta viva: a árvore ligada numa pasta de verdade,
    Documentos\\Mini-SK\\NOME-DO-PROJETO (o que o terminal cria aparece na árvore);
  - o 🦙 Ollama, se estiver instalado.
Só o próprio computador acessa (127.0.0.1). Para desligar: feche a janelinha preta.
"""
import os, sys, json, time, base64, socket, shutil, hashlib, secrets, signal, codecs, threading, subprocess, webbrowser, mimetypes, socketserver, urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace', line_buffering=True)
except Exception:
    pass

WIN = os.name == 'nt'
NOME = 'Mini SK'
PORTA = int(os.environ.get('PORTA', '7790'))           # fixa: os projetos ficam guardados "por endereço"
PORTA_TERMINAL, PORTA_PONTE = PORTA + 1, PORTA + 2
ENDERECO = 'http://127.0.0.1:%d/' % PORTA
ORIGENS = ('http://127.0.0.1:%d' % PORTA, 'http://localhost:%d' % PORTA)
CODIGO = secrets.token_hex(16)

BASE = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(BASE, 'www')

# 🧰 ferramentas que vêm junto na pasta (Node e Python portáteis, baixados pelo INICIAR na 1ª vez):
# entram no PATH do 💻 terminal — npm, node e python funcionam sem instalar nada no Windows
FERRAMENTAS = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0] if not getattr(sys, 'frozen', False) else sys.executable)), 'ferramentas')
for _d in (os.path.join(FERRAMENTAS, 'node'), os.path.join(FERRAMENTAS, 'python'), os.path.join(FERRAMENTAS, 'python', 'Scripts')):
    if os.path.isdir(_d):
        os.environ['PATH'] = _d + os.pathsep + os.environ.get('PATH', '')


def pasta_documentos():
    if WIN:
        for v in ('USERPROFILE', 'HOMEPATH'):
            if os.environ.get(v):
                d = os.path.join(os.environ[v], 'Documents')
                if os.path.isdir(d):
                    return d
    return os.path.expanduser('~')


CASA = os.path.abspath(os.environ.get('DADOS_EM') or os.path.join(pasta_documentos(), 'Mini-SK'))
os.makedirs(CASA, exist_ok=True)
REGISTRO = os.path.join(CASA, 'registro.txt')


def log(*a):
    t = time.strftime('%d/%m/%Y %H:%M:%S') + ' ' + ' '.join(str(x) for x in a)
    try:
        with open(REGISTRO, 'a', encoding='utf-8') as f:
            f.write(t + '\n')
    except Exception:
        pass


for ext, tipo in {'.js': 'text/javascript', '.mjs': 'text/javascript', '.cjs': 'text/javascript', '.css': 'text/css',
                  '.json': 'application/json', '.webmanifest': 'application/manifest+json', '.svg': 'image/svg+xml',
                  '.wasm': 'application/wasm', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ico': 'image/x-icon',
                  '.md': 'text/markdown; charset=utf-8'}.items():
    mimetypes.add_type(tipo, ext)

# o que o Mini SK precisa saber para usar o terminal e a ponte do PC (igual ao programa antigo)
SHIM = ('<script>window.miniskPC={codigo:%s,pasta:%s,so:%s,portas:{app:%d,terminal:%d,ponte:%d},leve:true,'
        'ligarOllama:function(){return fetch("/__pc/ollama-ligar",{method:"POST"}).then(function(r){return r.text()})},'
        'desligarOllama:function(){return fetch("/__pc/ollama-desligar",{method:"POST"}).then(function(r){return r.text()})},'
        'abrirPasta:function(p){return fetch("/__pc/abrir-pasta",{method:"POST",body:JSON.stringify({p:p||""})}).then(function(r){return r.text()})}};</script>') % (
    json.dumps(CODIGO), json.dumps(CASA), json.dumps('win32' if WIN else sys.platform), PORTA, PORTA_TERMINAL, PORTA_PONTE)


# ───────────────────────── 🦙 Ollama ─────────────────────────
def ollama_ligado():
    try:
        with urllib.request.urlopen('http://127.0.0.1:11434/api/version', timeout=2.5) as r:
            return r.status == 200
    except Exception:
        return False


def ligar_ollama():
    if ollama_ligado():
        return 'já estava ligado'
    tentativas = [['ollama', 'serve']]
    if WIN and os.environ.get('LOCALAPPDATA'):
        tentativas.append([os.path.join(os.environ['LOCALAPPDATA'], 'Programs', 'Ollama', 'ollama.exe'), 'serve'])
    for cmd in tentativas:
        try:
            subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                             creationflags=(0x08000000 if WIN else 0))
        except Exception:
            continue
        for _ in range(8):
            time.sleep(1)
            if ollama_ligado():
                return 'liguei'
    return 'não achei o Ollama instalado'


def desligar_ollama():
    cmds = [['taskkill', '/f', '/im', 'ollama.exe'], ['taskkill', '/f', '/im', 'ollama app.exe']] if WIN else [['pkill', '-f', 'ollama']]
    for c in cmds:
        try:
            subprocess.run(c, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=(0x08000000 if WIN else 0))
        except Exception:
            pass
    return 'ok'


# ───────────────────────── 🖥 a tela (o Mini SK) ─────────────────────────
class Pagina(SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=SITE, **k)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache')
        # lacre de fábrica: o ⚡ Node (WebContainer) funciona sem recarregar
        self.send_header('Cross-Origin-Opener-Policy', 'same-origin')
        self.send_header('Cross-Origin-Embedder-Policy', 'credentialless')
        self.send_header('Cross-Origin-Resource-Policy', 'cross-origin')
        super().end_headers()

    def log_message(self, *a):
        pass

    def responder(self, cod, texto, tipo='text/plain; charset=utf-8'):
        corpo = texto.encode('utf-8')
        self.send_response(cod)
        self.send_header('Content-Type', tipo)
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_GET(self):
        caminho = urlparse(self.path).path
        if caminho in ('/', '/index.html'):
            try:
                with open(os.path.join(SITE, 'index.html'), encoding='utf-8') as f:
                    html = f.read()
            except OSError:
                return self.responder(404, 'não existe')
            i = html.lower().find('<head')
            if i >= 0:
                j = html.find('>', i) + 1
                html = html[:j] + SHIM + html[j:]
            return self.responder(200, html, 'text/html; charset=utf-8')
        return super().do_GET()

    def do_POST(self):
        caminho = urlparse(self.path).path
        if self.headers.get('Origin') not in ORIGENS and self.headers.get('Origin') is not None:
            return self.responder(403, 'fora')
        n = int(self.headers.get('Content-Length') or 0)
        corpo = self.rfile.read(n) if n else b''
        if caminho == '/__pc/ollama-ligar':
            return self.responder(200, ligar_ollama())
        if caminho == '/__pc/ollama-desligar':
            return self.responder(200, desligar_ollama())
        if caminho == '/__pc/abrir-pasta':
            try:
                p = json.loads(corpo.decode('utf-8') or '{}').get('p') or CASA
            except Exception:
                p = CASA
            alvo = os.path.abspath(p)
            if alvo != CASA and not alvo.startswith(CASA + os.sep):
                return self.responder(200, 'fora')
            os.makedirs(alvo, exist_ok=True)
            try:
                if WIN:
                    os.startfile(alvo)
                else:
                    subprocess.Popen(['xdg-open', alvo], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                return self.responder(200, str(e))
            return self.responder(200, '')
        return self.responder(404, 'não existe')


# ───────────────────────── ⇅ a ponte de arquivos ─────────────────────────
import re
PULAR = re.compile(r'(^|/)(node_modules|\.git|\.sk|\.gradle|\.cache)(/|$)')


def nome_proj(n):
    n = re.sub(r'[^\w.\- ]+', '_', str(n or 'projeto'))
    n = re.sub(r'^\.+', '', n)[:60]
    return n or 'projeto'


def dentro(proj, rel):
    raiz = os.path.abspath(os.path.join(CASA, nome_proj(proj)))
    p = os.path.abspath(os.path.join(raiz, str(rel or '')))
    if p != raiz and not p.startswith(raiz + os.sep):
        raise ValueError('caminho inválido: ' + str(rel))
    return raiz, p


def agora_ms():
    return int(time.time() * 1000)


class Ponte(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def cabecalhos(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Codigo')
        self.send_header('Access-Control-Allow-Private-Network', 'true')

    def json(self, cod, obj):
        corpo = json.dumps(obj, ensure_ascii=False).encode('utf-8')
        self.send_response(cod)
        self.cabecalhos()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_OPTIONS(self):
        self.send_response(204)
        self.cabecalhos()
        self.send_header('Content-Length', '0')
        self.end_headers()

    def corpo(self):
        n = int(self.headers.get('Content-Length') or 0)
        if n > 80e6:
            raise ValueError('grande demais')
        return json.loads((self.rfile.read(n) if n else b'{}').decode('utf-8') or '{}')

    def checar(self):
        if self.headers.get('X-Codigo') != CODIGO:
            self.json(403, {'erro': 'código errado'})
            return False
        return True

    def do_GET(self):
        if not self.checar():
            return
        u = urlparse(self.path)
        q = parse_qs(u.query)
        try:
            if u.path == '/ping':
                return self.json(200, {'ok': True, 'pasta': CASA, 'versao': 2, 'agora': agora_ms()})
            if u.path == '/listar':
                raiz, _ = dentro((q.get('projeto') or [''])[0], '')
                desde = float((q.get('desde') or ['0'])[0] or 0)
                lista, todos, total, cortou = [], [], 0, False
                agora = agora_ms()
                for d, pastas, arquivos in os.walk(raiz):
                    reld = os.path.relpath(d, raiz).replace(os.sep, '/')
                    pastas[:] = [x for x in pastas if not PULAR.search((x if reld == '.' else reld + '/' + x))]
                    for a in arquivos:
                        f = os.path.join(d, a)
                        rel = os.path.relpath(f, raiz).replace(os.sep, '/')
                        if PULAR.search(rel) or not os.path.isfile(f):
                            continue
                        st = os.stat(f)
                        todos.append(rel)
                        if st.st_mtime * 1000 <= desde or st.st_size > 5e6:
                            continue
                        if total + st.st_size > 30e6:
                            cortou = True
                            continue
                        total += st.st_size
                        with open(f, 'rb') as fh:
                            lista.append({'p': rel, 'b64': base64.b64encode(fh.read()).decode('ascii')})
                return self.json(200, {'ok': True, 'agora': agora, 'arquivos': lista, 'todos': todos, 'cortou': cortou})
            return self.json(404, {'erro': 'não existe'})
        except Exception as e:
            return self.json(500, {'erro': str(e)})

    def do_POST(self):
        if not self.checar():
            return
        u = urlparse(self.path)
        try:
            b = self.corpo()
            if u.path == '/enviar':
                n, pulados = 0, []
                for a in b.get('arquivos') or []:
                    try:
                        if PULAR.search(a.get('p', '')):
                            continue
                        _, p = dentro(b.get('projeto'), a.get('p'))
                        if a.get('pasta'):
                            os.makedirs(p, exist_ok=True)
                            n += 1
                            continue
                        os.makedirs(os.path.dirname(p), exist_ok=True)
                        dados = base64.b64decode(a['b64']) if a.get('b64') is not None else str(a.get('t') or '').encode('utf-8')
                        with open(p, 'wb') as fh:
                            fh.write(dados)
                        n += 1
                    except Exception as e:
                        pulados.append(str(a.get('p')) + ': ' + str(e))
                raiz, _ = dentro(b.get('projeto'), '')
                return self.json(200, {'ok': True, 'n': n, 'pulados': pulados, 'pasta': raiz, 'agora': agora_ms() + 1})
            if u.path == '/apagar':
                n = 0
                for rel in b.get('caminhos') or []:
                    try:
                        raiz, p = dentro(b.get('projeto'), rel)
                        if p == raiz:
                            continue
                        if os.path.isdir(p):
                            shutil.rmtree(p, ignore_errors=True)
                            n += 1
                        elif os.path.exists(p):
                            os.remove(p)
                            n += 1
                    except Exception:
                        pass
                return self.json(200, {'ok': True, 'n': n, 'agora': agora_ms() + 1})
            return self.json(404, {'erro': 'não existe'})
        except Exception as e:
            return self.json(500, {'erro': str(e)})


# ───────────────────────── 💻 o terminal do computador ─────────────────────────
# fala o mesmo "idioma" do ttyd (o do Termux): o painel do Mini SK funciona sem mudar nada
class Terminal(socketserver.BaseRequestHandler):
    def setup(self):
        self.trava = threading.Lock()
        self.vivo = True

    # --- websocket ---
    def ler(self, n):
        dados = b''
        while len(dados) < n:
            c = self.request.recv(n - len(dados))
            if not c:
                raise ConnectionError('fechou')
            dados += c
        return dados

    def quadro(self):
        b1, b2 = self.ler(2)
        op, mascara, n = b1 & 0x0F, b2 & 0x80, b2 & 0x7F
        if n == 126:
            n = int.from_bytes(self.ler(2), 'big')
        elif n == 127:
            n = int.from_bytes(self.ler(8), 'big')
        m = self.ler(4) if mascara else b'\0\0\0\0'
        dados = bytearray(self.ler(n))
        for i in range(len(dados)):
            dados[i] ^= m[i % 4]
        return op, bytes(dados)

    def enviar_quadro(self, op, dados):
        cab = bytes([0x80 | op])
        n = len(dados)
        if n < 126:
            cab += bytes([n])
        elif n < 65536:
            cab += bytes([126]) + n.to_bytes(2, 'big')
        else:
            cab += bytes([127]) + n.to_bytes(8, 'big')
        with self.trava:
            try:
                self.request.sendall(cab + dados)
            except OSError:
                self.vivo = False

    def mandar(self, t):
        t = str(t).replace('\r\n', '\n').replace('\n', '\r\n')
        self.enviar_quadro(2, b'0' + t.encode('utf-8'))

    def aperto(self):
        cab = b''
        while b'\r\n\r\n' not in cab:
            c = self.request.recv(4096)
            if not c:
                return False
            cab += c
            if len(cab) > 65536:
                return False
        linhas = cab.decode('latin-1').split('\r\n')
        h = {}
        for l in linhas[1:]:
            if ':' in l:
                k, v = l.split(':', 1)
                h[k.strip().lower()] = v.strip()
        origem = h.get('origin')
        if origem and origem not in ORIGENS:   # só a janela do próprio Mini SK pode usar
            self.request.sendall(b'HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n')
            return False
        chave = h.get('sec-websocket-key', '')
        aceite = base64.b64encode(hashlib.sha1((chave + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11').encode()).digest()).decode()
        resp = 'HTTP/1.1 101 Switching Protocols\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Accept: ' + aceite + '\r\n'
        if 'tty' in [x.strip() for x in h.get('sec-websocket-protocol', '').split(',')]:
            resp += 'Sec-WebSocket-Protocol: tty\r\n'
        self.request.sendall((resp + '\r\n').encode())
        return True

    # --- o "shell" ---
    def curto(self):
        rel = os.path.relpath(self.cwd, CASA)
        if rel == '.':
            return '📁 Mini-SK'
        if not rel.startswith('..') and not os.path.isabs(rel):
            return '📁 ' + rel.replace(os.sep, '/')
        return self.cwd

    def prompt(self):
        self.mandar('\r\n\x1b[32m' + self.curto() + '\x1b[0m> ')

    def trocar_linha(self, nova):
        self.mandar('\b \b' * len(self.buf))
        self.buf = nova
        self.mandar(self.buf)

    def parar(self):
        p = self.proc
        if not p:
            return
        try:
            if WIN:
                subprocess.run(['taskkill', '/pid', str(p.pid), '/T', '/F'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x08000000)
            else:
                os.killpg(p.pid, signal.SIGINT)
        except Exception:
            try:
                p.kill()
            except Exception:
                pass

    def expandir(self, alvo):
        alvo = re.sub(r'^/d\s+', '', alvo.strip(), flags=re.I).replace('"', '').replace("'", '')
        if not alvo:
            return os.path.expanduser('~')
        if re.match(r'^~/minisk(/|$)', alvo):
            alvo = os.path.join(CASA, re.sub(r'^~/minisk/?', '', alvo))
        elif re.match(r'^~(/|$)', alvo):
            alvo = os.path.join(os.path.expanduser('~'), alvo[2:])
        return os.path.abspath(os.path.join(self.cwd, alvo))

    def ler_saida(self, p):
        dec = codecs.getincrementaldecoder('utf-8')(errors='replace')
        while True:
            try:
                c = p.stdout.read1(4096) if hasattr(p.stdout, 'read1') else p.stdout.read(1)
            except Exception:
                c = b''
            if not c:
                break
            self.mandar(dec.decode(c))
        cod = p.wait()
        if self.proc is p:
            self.proc = None
            self.linha_proc = ''
            if cod:
                self.mandar('\r\n\x1b[33m[terminou com código %d]\x1b[0m' % cod)
            self.prompt()

    def rodar(self, linha):
        linha = linha.strip()
        if not linha:
            return self.prompt()
        self.hist.append(linha)
        self.hi = len(self.hist)
        # "cd pasta && comando": entra na pasta e roda o resto (os ⚡ Comandos prontos usam assim)
        junto = re.match(r'^cd\s+(.+?)\s*&&\s*(.+)$', linha, re.I)
        if junto:
            alvo = self.expandir(junto.group(1))
            if not os.path.isdir(alvo):
                self.mandar('\r\nPasta não existe: ' + alvo)
                return self.prompt()
            self.cwd = alvo
            self.hist.pop()
            return self.rodar(junto.group(2))
        cd = re.match(r'^cd(?:\s+(.*))?$', linha, re.I)
        if cd:
            alvo = self.expandir(cd.group(1) or '')
            if os.path.isdir(alvo):
                self.cwd = alvo
            else:
                self.mandar('\r\nPasta não existe: ' + alvo)
            return self.prompt()
        if re.match(r'^(cls|clear)$', linha, re.I):
            self.mandar('\x1b[2J\x1b[H')
            return self.prompt()
        env = dict(os.environ, FORCE_COLOR='1', npm_config_color='always', PYTHONIOENCODING='utf-8')
        try:
            if WIN:
                self.proc = subprocess.Popen('chcp 65001>nul & ' + linha, shell=True, cwd=self.cwd, env=env,
                                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                             creationflags=0x08000000)
            else:
                self.proc = subprocess.Popen(['/bin/bash', '-c', linha], cwd=self.cwd, env=env, start_new_session=True,
                                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        except Exception as e:
            self.proc = None
            self.mandar('\r\n' + str(e))
            return self.prompt()
        threading.Thread(target=self.ler_saida, args=(self.proc,), daemon=True).start()

    def tecla(self, t):
        if self.proc:   # um comando está rodando: o que você digita vai para ele
            for ch in t:
                if ch == '\x03':
                    self.mandar('^C')
                    self.parar()
                elif ch == '\r':
                    self.mandar('\r\n')
                    try:
                        self.proc.stdin.write((self.linha_proc + '\n').encode('utf-8'))
                        self.proc.stdin.flush()
                    except Exception:
                        pass
                    self.linha_proc = ''
                elif ch in ('\x7f', '\b'):
                    if self.linha_proc:
                        self.linha_proc = self.linha_proc[:-1]
                        self.mandar('\b \b')
                elif ch >= ' ':
                    self.linha_proc += ch
                    self.mandar(ch)
            return
        if t == '\x1b[A':
            if self.hi > 0:
                self.hi -= 1
                self.trocar_linha(self.hist[self.hi])
            return
        if t == '\x1b[B':
            if self.hi < len(self.hist):
                self.hi += 1
                self.trocar_linha(self.hist[self.hi] if self.hi < len(self.hist) else '')
            return
        if t.startswith('\x1b'):
            return
        i = 0
        while i < len(t):
            ch = t[i]
            if ch in ('\r', '\n'):
                self.mandar('\r\n')
                l, self.buf = self.buf, ''
                self.rodar(l)
                if self.proc:
                    return self.tecla(t[i + 1:])
            elif ch in ('\x7f', '\b'):
                if self.buf:
                    self.buf = self.buf[:-1]
                    self.mandar('\b \b')
            elif ch == '\x03':
                self.mandar('^C')
                self.buf = ''
                self.prompt()
            elif ch >= ' ':
                self.buf += ch
                self.mandar(ch)
            i += 1

    def handle(self):
        self.cwd, self.buf, self.hist, self.hi, self.proc, self.linha_proc, pronto = CASA, '', [], 0, None, '', False
        try:
            if not self.aperto():
                return
            pedacos = b''
            while self.vivo:
                op, dados = self.quadro()
                if op == 8:
                    break
                if op == 9:
                    self.enviar_quadro(10, dados)
                    continue
                if op == 0:
                    pedacos += dados
                    continue
                if op not in (1, 2):
                    continue
                dados, pedacos = pedacos + dados, b''
                if not dados:
                    continue
                if not pronto:
                    pronto = True
                    if dados[:1] == b'{':
                        self.mandar('\x1b[36m💻 Terminal do computador (' + ('Windows' if WIN else sys.platform) + ')\x1b[0m\r\n'
                                    'Digite um comando e Enter. Ctrl+C para parar. Pasta inicial: ' + CASA)
                        self.prompt()
                        continue
                if dados[:1] == b'0':
                    self.tecla(dados[1:].decode('utf-8', errors='replace'))
        except (ConnectionError, OSError, ValueError):
            pass
        finally:
            self.vivo = False
            self.parar()


class ServidorTerminal(socketserver.ThreadingTCPServer):
    daemon_threads = True
    allow_reuse_address = True


class ServidorHTTP(ThreadingHTTPServer):
    daemon_threads = True


# ───────────────────────── abrir a janela ─────────────────────────
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
                subprocess.Popen([c, '--app=' + ENDERECO, '--window-size=1366,900'])
                return
            except OSError:
                pass
    webbrowser.open(ENDERECO)


def main():
    if not os.path.isfile(os.path.join(SITE, 'index.html')):
        print('❌ Não achei o Mini SK (pasta www) dentro do programa.')
        input('Aperte Enter para fechar…')
        return
    if ja_ligado():
        print('✅ Já estava ligado. Abrindo a janela…')
        abrir_janela()
        return
    try:
        tela = ServidorHTTP(('127.0.0.1', PORTA), Pagina)
    except OSError:
        print('❌ A porta %d está ocupada por outro programa.' % PORTA)
        input('Aperte Enter para fechar…')
        return
    avisos = []
    try:
        ponte = ServidorHTTP(('127.0.0.1', PORTA_PONTE), Ponte)
        threading.Thread(target=ponte.serve_forever, daemon=True).start()
    except OSError:
        avisos.append('⚠ A porta %d (ponte) está ocupada — a árvore ligada não vai funcionar.' % PORTA_PONTE)
    try:
        term = ServidorTerminal(('127.0.0.1', PORTA_TERMINAL), Terminal)
        threading.Thread(target=term.serve_forever, daemon=True).start()
    except OSError:
        avisos.append('⚠ A porta %d (terminal) está ocupada — o terminal do computador não vai ligar.' % PORTA_TERMINAL)
    if WIN:
        os.system('title Mini SK (deixe esta janela aberta)')
    log('Mini SK ligado em', ENDERECO, '· pasta', CASA)
    print('━' * 56)
    print('  ✅  Mini SK — LIGADO')
    print('━' * 56)
    print('  ⚡ Node · 💻 Terminal do computador · 🔄 Pasta viva')
    print('  Pasta dos projetos: ' + CASA)
    print('  Abrindo a janela…  (se não abrir, use: %s)' % ENDERECO)
    for a in avisos:
        print('  ' + a)
    print('  Pode minimizar esta janelinha. Para DESLIGAR: feche ela.')
    print('━' * 56)
    threading.Timer(0.6, abrir_janela).start()
    threading.Thread(target=lambda: ligar_ollama() if shutil.which('ollama') or WIN else None, daemon=True).start()
    try:
        tela.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
