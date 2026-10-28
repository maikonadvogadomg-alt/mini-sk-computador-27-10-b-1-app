# 📋 Plano do projeto: Mini-SK-Computador-27-10-B (1)

_Gerado em 28/10/2026, 01:49:39 — sem IA, lendo os arquivos._

## 📊 Visão geral
| Item | Valor |
|---|---|
| Arquivos | 69 |
| Linhas | 14.057 |
| Telas/páginas | 1 |
| Rotas do backend | 0 |
| Chamadas do app | 3 |
| Tabelas do banco | 0 |
| Variáveis de ambiente | 8 |

**Linguagens:** JavaScript (58), Outros (3), Imagem (2), Python (1), Batch (Windows) (1), CSS (1), HTML (1), Markdown (1), JSON (1)

## 💡 O que fazer (em ordem)
1. 🧹 Tirar a Replit de 15 arquivo(s) (🏗️ Preparar → Fazer tudo)
2. 🔐 Criar um .env.example com: BASE_PATH, DADOS_EM, GITHUB_STEP_SUMMARY, LOCALAPPDATA, PONTE_BASE, PONTE_CODIGO, PONTE_PORTA, TESTE_SAIR (os valores você coloca no servidor, nunca no código)
3. 📝 Criar um README.md explicando como rodar
4. 🚫 Criar .gitignore (não mandar node_modules ao GitHub)

## 🚀 Por onde começa
- `www/index.html`

## 📱 Telas e páginas
| Endereço | Arquivo |
|---|---|
| `www/index.html` | www/index.html |

## 🖥️ Rotas do backend
_Nenhum encontrado._

## 📡 O que o app pede ao servidor
| Método | Endereço | Onde |
|---|---|---|
| POST | `/__pc/ollama-ligar` | abrir.py |
| POST | `/__pc/ollama-desligar` | abrir.py |
| POST | `/__pc/abrir-pasta` | abrir.py |

## 🔌 O que falta no backend
✅ Tudo que o app chama tem rota no projeto (ou o app não usa servidor).

## 🗄️ Banco de dados
_Nenhuma tabela encontrada._

## 🔐 Variáveis de ambiente (configurar no servidor)
- `BASE_PATH`
- `DADOS_EM`
- `GITHUB_STEP_SUMMARY`
- `LOCALAPPDATA`
- `PONTE_BASE`
- `PONTE_CODIGO`
- `PONTE_PORTA`
- `TESTE_SAIR`

_Só os nomes. Os valores (chaves, senhas) nunca vão no código nem no GitHub._

## 🤖 IA usada
- api.groq.com
- console.groq.com
- generativelanguage.googleapis.com
- openrouter.ai
- api.anthropic.com
- console.anthropic.com
- api.openai.com
- platform.openai.com

## 🌐 Serviços de fora que ele acessa
- aistudio.google.com
- api.anthropic.com
- api.exemplo.com
- api.expo.dev
- api.github.com
- api.groq.com
- api.npms.io
- api.openai.com
- api.perplexity.ai
- api.x.ai
- appassets.androidplatform.net
- cdn.jsdelivr.net
- cdn.tailwindcss.com
- console.anthropic.com
- console.groq.com
- console.x.ai
- esm.sh
- expo.dev
- generativelanguage.googleapis.com
- github.com
- mail.google.com
- ollama.com
- openapi.monica.im
- openrouter.ai
- platform.monica.im
- platform.openai.com
- raw.github.com
- registry.npmjs.org
- seu-usuario.github.io
- stuartk.com
- stuk.github.io
- u.expo.dev
- unpkg.com
- www.google.com
- www.npmjs.com
- www.perplexity.ai
- xxxx.supabase.co

## 🧹 Arquivos com coisa da Replit
- www/js/20-zip.js
- www/js/50-tree.js
- www/js/70-search.js
- www/js/80-ai.js
- www/js/86-terminal.js
- www/js/86c-termux.js
- www/js/88-inventario.js
- www/js/90-github.js
- www/js/95-pwa.js
- www/js/96b-eas.js
- www/js/96c-preparar.js
- www/js/97-analise.js
- www/js/lib/expo-core.js
- www/js/lib/plano-core.js
- www/js/lib/receita-core.js

## 🔁 Roteiro para recriar fora da Replit
1. Importar o projeto no Mini SK e tocar em 🏗️ Preparar → ✅ Fazer tudo (tira a Replit, cria os arquivos que faltam).
2. Não tem backend: o site sozinho basta (Netlify ou GitHub Pages).
3. Variáveis: cadastrar 8 variável(is) no servidor (lista acima).
4. Testar a prévia; se der erro, 🤖 Mandar os erros para a IA.
5. App: 📲 Instalável (PWA), 📦 APK ou 🖥️ Desktop (.exe) pelo 🏗️ Preparar.

## 🌳 Árvore de arquivos
```
├─ 📁 ferramentas/
│  └─ aqui-ficam-o-python-e-o-node.txt
├─ 📁 www/
│  ├─ 📁 css/
│  │  └─ app.css
│  ├─ 📁 icons/
│  │  ├─ icon-192.png
│  │  └─ icon-512.png
│  ├─ 📁 js/
│  │  ├─ 📁 lib/
│  │  │  ├─ 📁 lab/
│  │  │  │  ├─ 30-analise.js
│  │  │  │  └─ 50-comparar.js
│  │  │  ├─ 📁 picotador/
│  │  │  │  ├─ 00-base.js
│  │  │  │  ├─ 10-ler.js
│  │  │  │  ├─ 20-projetos.js
│  │  │  │  └─ 30-mensagens.js
│  │  │  ├─ acorn.min.js
│  │  │  ├─ expo-core.js
│  │  │  ├─ jszip.min.js
│  │  │  ├─ nacl-fast.min.js
│  │  │  ├─ plano-core.js
│  │  │  ├─ ponte-termux.cjs.txt
│  │  │  ├─ receita-core.js
│  │  │  └─ selar.js
│  │  ├─ 00-core.js
│  │  ├─ 04-conta.js
│  │  ├─ 10-fs.js
│  │  ├─ 20-zip.js
│  │  ├─ 30-highlight.js
│  │  ├─ 40-editor.js
│  │  ├─ 50-tree.js
│  │  ├─ 60-preview.js
│  │  ├─ 61-tsx.js
│  │  ├─ 70-search.js
│  │  ├─ 80-ai.js
│  │  ├─ 81-gasto.js
│  │  ├─ 83-voz.js
│  │  ├─ 84-ponte.js
│  │  ├─ 85-checkpoints.js
│  │  ├─ 86-terminal.js
│  │  ├─ 86b-node.js
│  │  ├─ 86c-termux.js
│  │  ├─ 86e-atalhos.js
│  │  ├─ 86f-pasta-viva.js
│  │  ├─ 86g-largura.js
│  │  ├─ 86h-node-extra.js
│  │  ├─ 87-links.js
│  │  ├─ 88-inventario.js
│  │  ├─ 89-config.js
│  │  ├─ 89b-cacador.js
│  │  ├─ 90-github.js
│  │  ├─ 91-acoes.js
│  │  ├─ 91b-publicar.js
│  │  ├─ 92-playground.js
│  │  ├─ 92c-importar.js
│  │  ├─ 93-conversa.js
│  │  ├─ 94-fatiador.js
│  │  ├─ 95-pwa.js
│  │  ├─ 96-apk.js
│  │  ├─ 96b-eas.js
│  │  ├─ 96c-preparar.js
│  │  ├─ 96d-exe-minisk.js
│  │  ├─ 96e-exe-python.js
│  │  ├─ 97-analise.js
│  │  ├─ 97b-cacabug.js
│  │  ├─ 97c-modularizar.js
│  │  ├─ 98-api.js
│  │  └─ 99-app.js
│  ├─ index.html
│  ├─ LEIA-ME.md
│  ├─ manifest.json
│  └─ sw.js
├─ abrir.py
├─ INICIAR-MINI-SK.bat
└─ LEIA-ME.txt
```
