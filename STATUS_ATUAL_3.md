# STATUS ATUAL DO PROJETO - VEO AUTOMATOR
**Atualizado em:** 23/Jan/2026 - 02:45

---

## DIRETRIZES DE COMUNICACAO

Programador, leia isso antes de comecar:

1. **Fale de forma narrada**, como se estivesse conversando. Nada de jogar codigo ou termos tecnicos sem explicar.

2. **Entenda o codigo como se fosse voce que tivesse feito**. Antes de mexer em qualquer coisa, leia o arquivo completo e entenda cada parte.

3. **O arquivo correto fica em:** `/mnt/c/Users/cesar/veo-automator/automator.py`
   - NAO confunda com `/home/cesar/novo-projeto/automator.py` que esta incompleto
   - Quando for implementar, edite o arquivo do Windows (/mnt/c/...)

4. **Faca mudancas incrementais** - uma coisa de cada vez, nao saia mudando tudo.

5. **Explique o que vai fazer ANTES de fazer** - o usuario precisa entender e aprovar.

---

## O QUE E ESSE PROJETO

O VEO AUTOMATOR e uma ferramenta que automatiza a criacao de videos no Google Flow (Veo 3.1). Em vez do usuario ficar la clicando manualmente, digitando prompts, esperando videos ficarem prontos, baixando um por um... a ferramenta faz tudo isso sozinha.

**URL do Flow:** https://labs.google/fx/pt/tools/flow
**Builder local:** http://localhost:5000
**Servidor:** roda com `python app.py` no CMD do Windows

---

## O QUE ESTA FUNCIONANDO (23/Jan/2026)

### Fluxo completo:
1. Abre Chrome com perfil `FLOW_{email}` (copia para pasta temporaria)
2. Navega para o Flow
3. Detecta se precisa login (botao "Crie com o Flow" ou "Create with Flow")
4. Faz login automatico (email + senha com digitacao humana)
5. Clica em "Novo projeto"
6. Gera multiplas cenas em lotes de 2 (cada cena = 2 videos)
7. Aguarda videos ficarem prontos (com contagem correta agora)
8. Tenta baixar videos

### Tratamento de falha implementado:
- Primeira cena (`configure_and_generate`): tem retry com 3 tentativas
- Cenas seguintes (`gerar_cena_seguinte`): AGORA TEM retry com 3 tentativas tambem
- Se falhar, digita o prompt da CENA ATUAL (nao da cena 1)

---

## O QUE FOI CORRIGIDO NESTA SESSAO (22-23/Jan/2026)

### 1. Contagem de videos gerando (CORRIGIDO)
**Problema:** Mostrava "16 gerando" quando eram so 4 videos
**Causa:** Buscava QUALQUER div com porcentagem na pagina toda
**Correcao:** Agora busca apenas `div[class*="sc-dd6abb21"]` (classe especifica)

```javascript
// ANTES (errado):
document.querySelectorAll('div')

// AGORA (certo):
document.querySelectorAll('div[class*="sc-dd6abb21"]')
```

### 2. Download de videos (CORRIGIDO)
**Problema:** Baixava o MESMO video 4 vezes em vez de 4 videos diferentes
**Causa:** Buscava QUALQUER botao de download na pagina toda
**Correcao:** Agora busca o botao DENTRO de cada container especifico

```javascript
// ANTES (errado):
document.querySelectorAll('button')

// AGORA (certo):
arguments[0].querySelector('button[class*="gCYjQM"]')
// onde arguments[0] = container do video atual
```

### 3. Retry nas cenas seguintes (IMPLEMENTADO)
**Problema:** Se cena 2, 3, 4... falhava, nao tinha retry
**Correcao:** Agora `gerar_cena_seguinte()` tem o mesmo tratamento de falha que a primeira cena:
- 3 tentativas
- Primeira tentativa: cola o prompt
- Segunda tentativa: digita como humano (velocidade normal)
- Terceira tentativa: digita como humano (velocidade lenta)
- Aguarda 20 segundos apos clicar para verificar "Falha na geracao"

---

## FLUXO DE GERACAO (LOTES DE 2 CENAS)

Cada cena gera 2 videos. O sistema trabalha em lotes de 2 cenas (4 videos por lote).

```
EXEMPLO: 6 CENAS

LOTE 1 (cenas 1 e 2):
1. configure_and_generate(cena1) -> gera 2 videos
2. gerar_cena_seguinte(cena2) -> gera mais 2 videos
3. aguardar_videos_prontos(4) -> espera 4 videos
4. baixar_videos(4) -> baixa os 4

LOTE 2 (cenas 3 e 4):
5. gerar_cena_seguinte(cena3) -> gera 2 videos
6. gerar_cena_seguinte(cena4) -> gera mais 2 videos
7. aguardar_videos_prontos(4) -> espera 4 videos
8. baixar_videos(4) -> baixa os 4

LOTE 3 (cenas 5 e 6):
9. gerar_cena_seguinte(cena5) -> gera 2 videos
10. gerar_cena_seguinte(cena6) -> gera mais 2 videos
11. aguardar_videos_prontos(4) -> espera 4 videos
12. baixar_videos(4) -> baixa os 4

FIM - 12 videos no total
```

---

## ELEMENTOS HTML DESCOBERTOS

### Container de cada video:
- **Classe:** `sc-7e665804-3 hVIKCb`
- **Tag:** DIV

### Indicador de porcentagem (video gerando):
- **Classe:** `sc-dd6abb21-1`
- **Texto:** "57%", "100%", etc

### Botao de download (CERTO):
- **Classe:** `gCYjQM` e `hFhuTI`
- **Texto:** `downloadBaixar`

### Botao de download (ERRADO - nao usar):
- **Classe:** `hNmoyJ`

### Opcao 720p no popup:
- **Tag:** DIV
- **Role:** `menuitem`
- **Texto:** contem "720p" ou "Tamanho original"

---

## PROBLEMA ATUAL - INSTABILIDADE DO GOOGLE FLOW

A ferramenta do Google Flow e MUITO instavel:
- As vezes gera o video normalmente
- As vezes da "Falha na geracao" sem motivo aparente
- As vezes inicia mas para no meio
- Oscila de forma imprevisivel

**Isso NAO e problema do codigo** - e limitacao da propria ferramenta do Google.

O retry ajuda, mas se o Google nao cooperar, nao tem o que fazer.

---

## O QUE FALTA IMPLEMENTAR

### Prioridade 1 - TESTAR DOWNLOAD
- [ ] Testar se o download de videos diferentes esta funcionando
- [ ] Verificar se baixa os 4 videos corretamente (nao o mesmo 4 vezes)

### Prioridade 2 - FRAMES PARA VIDEO (com imagem)
- [ ] Nas cenas seguintes (2, 3, 4...) tambem precisa fazer upload da imagem
- [ ] Atualmente so a primeira cena faz upload
- [ ] Modificar `gerar_cena_seguinte()` para suportar imagem

### Prioridade 3 - MELHORIAS
- [ ] Renomear arquivos baixados (cena1-video1.mp4, etc)
- [ ] Tratamento mais robusto de erros
- [ ] Log mais detalhado

---

## METODOS PRINCIPAIS DO CODIGO

```
setup_chrome()              -> Abre Chrome com perfil FLOW_{email}
fazer_login_email()         -> Preenche email e clica Avancar
fazer_login_senha()         -> Preenche senha (digitacao humana) e clica Avancar
configure_and_generate()    -> Setup completo + gera primeira cena (com retry)
gerar_cena_seguinte()       -> Gera cenas 2, 3, 4... (COM RETRY AGORA)
aguardar_videos_prontos()   -> Loop que detecta quando videos terminaram (CORRIGIDO)
baixar_videos()             -> Baixa videos um por um (CORRIGIDO)
digitar_como_humano()       -> Digita caractere por caractere
run(scenes)                 -> Metodo principal que orquestra tudo
```

---

## ESTRUTURA DE PASTAS

- **Pasta Windows:** `C:\Users\cesar\veo-automator\`
- **Pasta WSL (mesmo conteudo):** `/mnt/c/Users/cesar/veo-automator/`
- **Pasta do projeto no Linux:** `/home/cesar/novo-projeto/` (documentacao)

Quando for implementar, edite em `/mnt/c/Users/cesar/veo-automator/automator.py`

---

## COMO TESTAR

1. No CMD do Windows, vai pra pasta: `cd C:\Users\cesar\veo-automator`
2. Roda o servidor: `python app.py`
3. Abre o navegador em: http://localhost:5000
4. Preenche os dados e roda

---

## HISTORICO DE COMMITS

- `b8fd093` - Sistema de retry com digitacao humana implementado
- `03a27d9` - Automacao completa: Login + Criar projeto + Upload imagem + Gerar video
- `bbf0236` - Automacao funcionando: Login + Criar projeto
- `fd7b91b` - Primeira versao - Passos 1-4 concluidos

**Pendente:** Fazer commit das correcoes de download e retry nas cenas seguintes

---

## LEMBRETES FINAIS

- NAO use rebase (pode corromper codigo)
- Faca commit e push apos implementacoes importantes
- Sempre explique o que vai fazer antes de mexer no codigo
- Mudancas incrementais - uma coisa de cada vez
- A ferramenta do Google Flow e instavel - nao e culpa do codigo
