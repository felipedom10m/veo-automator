# 🏆 IMPLEMENTAÇÃO - VEO AUTOMATOR PWA

## 📌 O Que Vamos Construir

Uma **aplicação web PWA** (funciona no celular e desktop) com design dourado premium que automatiza a criação de vídeos no Veo 3 (Google Flow).

---

## 🎯 PASSO 1: Criar Estrutura Base do Projeto

**O que vou fazer:**
1. Criar pastas e arquivos do projeto
2. Criar `requirements.txt` com dependências Python
3. Instalar dependências (Flask, Selenium)

**Estrutura:**
```
novo-projeto/
├── app.py                    # Servidor Flask
├── automator.py              # Lógica de automação Selenium
├── requirements.txt          # Dependências Python
├── templates/
│   └── index.html            # Interface web
├── static/
│   ├── style.css             # Estilos (design dourado)
│   ├── script.js             # Funcionalidades JavaScript
│   ├── manifest.json         # Configuração PWA
│   └── service-worker.js     # PWA offline support
└── README.md                 # Documentação
```

**Como testar:**
```bash
pip3 install -r requirements.txt
```

**Resultado esperado:**
✅ Estrutura de pastas criada
✅ Dependências instaladas

---

## 🎯 PASSO 2: Criar Interface Web com Design Dourado

**O que vou fazer:**
1. Criar `templates/index.html` - Interface responsiva
2. Criar `static/style.css` - Design dourado premium (ouro claro + ouro escuro)
3. Criar `static/script.js` - Funcionalidades (adicionar cenas, validações)

**Interface terá:**
- 🎨 Design responsivo (mobile + desktop)
- 🏆 Cores douradas harmônicas
- 📱 Dropdown para selecionar perfil FLOW
- 🖼️ Seletor de imagem de referência
- 📁 Seletor de pasta destino
- ➕ Botão "Adicionar Cena" (dinâmico)
- 🚀 Botão "Iniciar Automação"
- 📊 Área de logs em tempo real

**Como testar:**
```bash
python3 app.py
```
Acessar: `http://localhost:5000`

**Resultado esperado:**
✅ Interface abre no navegador
✅ Design dourado responsivo
✅ Consegue adicionar múltiplas cenas

---

## 🎯 PASSO 3: Configurar PWA (Progressive Web App)

**O que vou fazer:**
1. Criar `static/manifest.json` - Configuração do app
2. Criar `static/service-worker.js` - Funcionamento offline
3. Adicionar meta tags PWA no HTML
4. Criar ícones para instalação (192x192 e 512x512)

**Como testar:**
1. Abrir no celular: `http://[IP-DO-PC]:5000`
2. No Chrome mobile: Menu → "Adicionar à tela inicial"
3. Ícone aparece na tela do celular como app

**Resultado esperado:**
✅ Pode instalar como app no celular
✅ Funciona como aplicativo nativo

---

## 🎯 PASSO 4: Detectar Perfis FLOW do Chrome

**O que vou fazer:**
1. Criar função em `automator.py` que:
   - Busca perfis em `/mnt/c/Users/cesar/AppData/Local/Google/Chrome/User Data/`
   - Filtra apenas perfis que começam com `FLOW_`
   - Retorna lista: `["FLOW_1_Patricia", "FLOW_2_Cliente2", ...]`

2. Criar endpoint Flask `/api/get-profiles` que retorna JSON com perfis

3. Atualizar `script.js` para:
   - Fazer requisição ao endpoint
   - Popular dropdown com os perfis encontrados

**Como testar:**
1. Abrir interface
2. Ver dropdown populado com perfis FLOW

**Resultado esperado:**
✅ Dropdown mostra: FLOW_1_Patricia (e outros se existirem)

---

## 🎯 PASSO 5: Coletar Dados da Interface e Validar

**O que vou fazer:**
1. Criar endpoint Flask `/api/start-automation` (POST)
2. Coletar dados do formulário:
   - Perfil FLOW selecionado
   - Caminho da imagem (opcional)
   - Caminho da pasta destino
   - Lista de prompts (cenas)

3. Validações:
   - Pelo menos 1 cena preenchida
   - Perfil selecionado
   - Pasta destino válida

**Como testar:**
1. Preencher interface
2. Clicar "Iniciar Automação"
3. Ver no terminal se dados chegaram corretamente

**Resultado esperado:**
✅ Dados coletados e validados
✅ Mensagem de erro se faltar algo

---

## 🎯 PASSO 6: Abrir Chrome com Perfil FLOW Selecionado

**O que vou fazer:**
1. No `automator.py`, criar função `open_chrome_with_profile(profile_name)`
2. Usar Selenium para:
   - Localizar caminho do perfil (ex: Profile 57)
   - Abrir Chrome com esse perfil usando ChromeOptions
   - Aguardar Chrome abrir

**Como testar:**
1. Selecionar FLOW_1_Patricia
2. Clicar "Iniciar Automação"
3. Chrome abre com perfil da Patrícia (já logado)

**Resultado esperado:**
✅ Chrome abre com conta correta
✅ Já está logado no Google

---

## 🎯 PASSO 7: Navegar até Flow e Acessar Veo 3

**O que vou fazer:**
1. Adicionar código Selenium para:
   - Acessar `https://labs.google/fx/pt/tools/flow`
   - Aguardar página carregar
   - Localizar botão "Create with Flow"
   - Clicar no botão
   - Aguardar interface do Veo 3 aparecer

**Como testar:**
1. Iniciar automação
2. Ver Chrome navegando automaticamente
3. Interface do Veo 3 abre

**Resultado esperado:**
✅ Página Flow abre
✅ Clica em "Create with Flow"
✅ Interface Veo 3 aparece

**⚠️ IMPORTANTE:** Você vai precisar tirar **prints** da interface do Veo 3 para eu mapear os elementos (campos, botões)

---

## 🎯 PASSO 8: Mapear Interface do Veo 3 (VOCÊ VAI AJUDAR)

**O que vou precisar de você:**
1. Acessar manualmente o Veo 3
2. Tirar prints mostrando:
   - Campo onde cola o prompt
   - Botão para adicionar imagem (se houver)
   - Como fazer upload da imagem
   - Botão para gerar vídeo
   - Onde aparece o vídeo gerado
   - Botão de download

**O que vou fazer:**
1. Analisar os prints
2. Usar DevTools do Chrome (F12) para identificar:
   - IDs dos elementos
   - Classes CSS
   - XPaths
3. Mapear cada elemento no código

**Resultado esperado:**
✅ Todos elementos mapeados
✅ Sei exatamente onde clicar

---

## 🎯 PASSO 9: Automatizar Criação de 1 Vídeo (SEM Imagem)

**O que vou fazer:**
1. Implementar função que:
   - Localiza campo de prompt
   - Cola o texto
   - Clica em "Gerar vídeo"
   - Aguarda vídeo ser gerado (pode demorar)
   - Detecta quando vídeo está pronto

2. Enviar logs em tempo real para interface:
   - "Colando prompt da cena 1..."
   - "Gerando vídeo..."
   - "Vídeo pronto!"

**Como testar:**
1. Adicionar 1 cena (sem imagem)
2. Iniciar automação
3. Ver logs na tela
4. Vídeo é gerado no Veo 3

**Resultado esperado:**
✅ Vídeo gerado automaticamente
✅ Logs aparecem em tempo real

---

## 🎯 PASSO 10: Automatizar Criação de Vídeo COM Imagem

**O que vou fazer:**
1. Adicionar lógica para:
   - Verificar se há imagem fornecida
   - Clicar em "Adicionar imagem" (botão que você vai me mostrar)
   - Fazer upload da imagem
   - Cola prompt
   - Gera vídeo

**Como testar:**
1. Adicionar 1 cena + selecionar imagem
2. Iniciar automação
3. Vídeo gerado com imagem de referência

**Resultado esperado:**
✅ Imagem anexada corretamente
✅ Vídeo usa a imagem de referência

---

## 🎯 PASSO 11: Gerar 2 Vídeos por Cena

**O que vou fazer:**
1. Modificar lógica para:
   - Gerar primeiro vídeo
   - Aguardar finalização
   - Limpar campos
   - Repetir processo (mesmo prompt + imagem)
   - Gerar segundo vídeo
   - Aguardar finalização

**Como testar:**
1. Adicionar 1 cena
2. Iniciar automação
3. Ver 2 vídeos sendo gerados

**Resultado esperado:**
✅ 2 vídeos gerados com mesmo prompt
✅ Logs mostram "Gerando vídeo 1/2" e "Gerando vídeo 2/2"

---

## 🎯 PASSO 12: Download e Organização dos Vídeos

**O que vou fazer:**
1. Mapear botão de download (você vai me mostrar)
2. Implementar:
   - Clicar em download do vídeo 1
   - Aguardar download completar
   - Renomear para `cena-1-video-1.mp4`
   - Mover para pasta destino
   - Repetir para vídeo 2 (`cena-1-video-2.mp4`)

**Como testar:**
1. Gerar 1 cena (2 vídeos)
2. Ver vídeos baixados na pasta
3. Nomes corretos

**Resultado esperado:**
✅ Vídeos baixados automaticamente
✅ Renomeados: `cena-1-video-1.mp4`, `cena-1-video-2.mp4`
✅ Salvos na pasta escolhida

---

## 🎯 PASSO 13: Processar Múltiplas Cenas Automaticamente

**O que vou fazer:**
1. Criar loop que processa todas as cenas:
   ```
   Para cada cena:
     - Anexa imagem (se houver)
     - Cola prompt
     - Gera vídeo 1
     - Baixa e renomeia (cena-X-video-1.mp4)
     - Gera vídeo 2
     - Baixa e renomeia (cena-X-video-2.mp4)
     - Incrementa contador (X++)
   ```

2. Logs detalhados:
   - "Processando cena 1 de 5..."
   - "Processando cena 2 de 5..."

**Como testar:**
1. Adicionar 3+ cenas
2. Iniciar automação
3. Ver todas sendo processadas

**Resultado esperado:**
✅ Todas cenas processadas automaticamente
✅ Vídeos organizados: cena-1-video-1, cena-1-video-2, cena-2-video-1, cena-2-video-2...

---

## 🎯 PASSO 14: Tratamento de Erros e Robustez

**O que vou fazer:**
1. Adicionar try/catch em pontos críticos
2. Tratar erros comuns:
   - Elemento não encontrado (página mudou?)
   - Timeout (vídeo demorou muito)
   - Erro de download
   - Perfil não existe

3. Mostrar mensagens claras:
   - ❌ "Erro ao gerar vídeo da cena 3. Pulando..."
   - ⚠️ "Timeout aguardando vídeo. Tentando novamente..."

**Como testar:**
1. Testar cenários de erro
2. Ver mensagens apropriadas

**Resultado esperado:**
✅ Ferramenta não quebra com erros
✅ Mensagens claras do que aconteceu

---

## 🎯 PASSO 15: Melhorias Finais e Documentação

**O que vou fazer:**
1. Adicionar funcionalidades:
   - Botão "Pausar" automação
   - Botão "Cancelar" automação
   - Barra de progresso visual
   - Som de notificação quando terminar

2. Atualizar README.md com:
   - Como instalar
   - Como renomear perfis Chrome
   - Como usar a ferramenta
   - Exemplos

**Resultado esperado:**
✅ Ferramenta completa e polida
✅ Documentação clara

---

## 📋 Resumo Visual do Fluxo Final

```
[Celular ou Desktop]
  ↓
[Abre http://localhost:5000 ou instala PWA]
  ↓
[Seleciona perfil: FLOW_1_Patricia]
  ↓
[Adiciona cenas (+ Adicionar Cena)]
  ↓
[Seleciona imagem de referência (opcional)]
  ↓
[Seleciona pasta destino]
  ↓
[Clica "Iniciar Automação"]
  ↓
[Logs em tempo real mostram progresso]
  ↓
[Chrome abre e faz tudo sozinho]
  ↓
[Vídeos baixados e organizados na pasta]
  ↓
[Notificação: "Automação concluída! 🎉"]
```

---

## 🔧 Tecnologias

- **Python 3** + **Flask** (backend/servidor)
- **Selenium** (automação Chrome)
- **HTML/CSS/JavaScript** (interface)
- **PWA** (manifest.json + service worker)
- **WebSockets** (logs em tempo real - opcional)

---

## 📦 Arquivos que Vamos Criar

1. ✅ `app.py` - Servidor Flask
2. ✅ `automator.py` - Lógica de automação
3. ✅ `templates/index.html` - Interface
4. ✅ `static/style.css` - Design dourado
5. ✅ `static/script.js` - Funcionalidades
6. ✅ `static/manifest.json` - Configuração PWA
7. ✅ `static/service-worker.js` - PWA offline
8. ✅ `requirements.txt` - Dependências
9. ✅ `README.md` - Documentação (atualizado)
10. ✅ `IMPLEMENTACAO.md` - Este arquivo

---

## ⏱️ Estratégia de Trabalho (25 minutos por vez)

**Sessão 1 (agora):**
- Passos 1, 2, 3 (estrutura + interface + PWA)

**Sessão 2:**
- Passos 4, 5, 6 (perfis + validação + abrir Chrome)

**Sessão 3:**
- Passos 7, 8 (navegar Flow + mapear Veo - **VOCÊ VAI TIRAR PRINTS**)

**Sessão 4:**
- Passos 9, 10 (gerar vídeo sem/com imagem)

**Sessão 5:**
- Passos 11, 12 (2 vídeos + download)

**Sessão 6:**
- Passos 13, 14 (múltiplas cenas + erros)

**Sessão 7:**
- Passo 15 (melhorias finais)

---

**Próximo:** Começar PASSO 1 agora! 🚀
