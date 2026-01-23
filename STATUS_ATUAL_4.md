# STATUS ATUAL DO PROJETO - VEO AUTOMATOR
**Atualizado em:** 22/Jan/2026 - 13:00

---

## DIRETRIZES DE COMUNICACAO

1. **Fale de forma narrada**, como se estivesse conversando
2. **Entenda o codigo como se fosse voce que tivesse feito**
3. **Arquivo correto:** `/mnt/c/Users/cesar/veo-automator/automator.py`
4. **Mudancas incrementais** - uma coisa de cada vez
5. **Explique ANTES de fazer** - o usuario precisa aprovar
6. **NAO chute solucoes** - investigue com dados reais (logs, F12, etc)
7. **Explicacoes CLARAS e SIMPLES** - frases curtas, direto ao ponto

---

## O QUE E ESSE PROJETO

Ferramenta que automatiza criacao de videos no Google Flow (Veo 3.1).

- **URL do Flow:** https://labs.google/fx/pt/tools/flow
- **Builder local:** http://localhost:5000
- **Rodar:** `python app.py` no CMD do Windows

---

## STATUS ATUAL: FUNCIONANDO 100%

### OPCAO 1: Texto para video (SEM imagem)
- Usuario NAO anexa imagem no builder
- Cena 1: `configure_and_generate()`
- Cenas 2, 3, 4...: `gerar_cena_seguinte()`
- **STATUS: FUNCIONANDO**

### OPCAO 2: Frames para video (COM imagem)
- Usuario anexa imagem de personagem no builder
- Cena 1: `configure_and_generate()` - faz upload da imagem
- Cenas 2, 3, 4...: `gerar_cena_seguinte()` - FAZ UPLOAD DA IMAGEM NOVAMENTE
- **STATUS: FUNCIONANDO**

---

## FLUXO COMPLETO

1. Abre Chrome com perfil `FLOW_{email}`
2. Navega para o Flow
3. Detecta se precisa login
4. Se precisa: email -> "Seguinte" -> senha (digitacao humana) -> "Seguinte"
5. Clica em "Novo projeto"
6. Gera cenas UMA POR UMA
7. Espera tempo ALEATORIO (40-60 segundos) entre cada cena
8. Navegador fica aberto no final (usuario baixa manualmente)

---

## METODOS PRINCIPAIS

| Metodo | O que faz |
|--------|-----------|
| `setup_chrome()` | Abre Chrome com perfil FLOW_{email} |
| `fazer_login_email()` | Preenche email e clica Seguinte/Avancar/Next |
| `fazer_login_senha()` | Preenche senha (digitacao humana) e clica Seguinte |
| `configure_and_generate()` | Setup completo + gera primeira cena |
| `gerar_cena_seguinte()` | Gera cenas 2, 3, 4... (com imagem se tiver) |
| `digitar_como_humano()` | Digita caractere por caractere |
| `run(scenes)` | Metodo principal que orquestra tudo |

---

## TRATAMENTO DE ERROS

- **3 tentativas** em cada cena
- **Tentativa 1:** cola o prompt
- **Tentativa 2:** digita como humano (velocidade normal)
- **Tentativa 3:** digita como humano (velocidade lenta)
- Aguarda 20 segundos apos clicar para verificar "Falha na geracao"

---

## CORRECOES FEITAS (22/Jan/2026)

1. **Botao Seguinte/Avancar/Next** - Adicionado "Seguinte" (portugues de Portugal)
2. **Clique com JavaScript** - Evita erro "element click intercepted"
3. **Tempo aleatorio** - 40-60 segundos entre cenas
4. **Removido download** - Usuario baixa manualmente
5. **Removido lotes de 2** - Agora gera cena por cena
6. **Frames para video completo** - Cenas 2, 3, 4... agora fazem upload da imagem

---

## ESTRUTURA DE PASTAS

- **Windows:** `C:\Users\cesar\veo-automator\`
- **WSL:** `/mnt/c/Users/cesar/veo-automator/`
- **Editar sempre:** `/mnt/c/Users/cesar/veo-automator/automator.py`

---

## COMO TESTAR

1. CMD do Windows: `cd C:\Users\cesar\veo-automator`
2. Rodar servidor: `python app.py`
3. Abrir navegador: http://localhost:5000
4. Preencher dados e iniciar

---

## PROJETO CONCLUIDO

- Texto para video: OK
- Frames para video: OK
- Login automatico: OK
- Retry em caso de erro: OK
- Download: Manual (usuario baixa depois)
