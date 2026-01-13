# 🎬 VEO AUTOMATOR - INSTRUÇÕES PARA WINDOWS

## 📋 PASSO A PASSO COMPLETO

---

### PASSO 1: Copiar Pasta para Windows

**Você está no WSL agora**, então precisa copiar a pasta do projeto para o Windows:

1. **Abra o Explorador de Arquivos do Windows**

2. **Navegue até uma pasta Windows** (por exemplo: `C:\Users\cesar\Desktop`)

3. **Copie a pasta do projeto** de WSL para Windows:
   - No WSL, o caminho é: `/home/cesar/novo-projeto`
   - No Windows, isso fica em: `\\wsl$\Ubuntu\home\cesar\novo-projeto`
   - Copie toda a pasta para `C:\Users\cesar\Desktop\novo-projeto`

**OU** use este comando no WSL para copiar automaticamente:

```bash
cp -r /home/cesar/novo-projeto /mnt/c/Users/cesar/Desktop/novo-projeto
```

---

### PASSO 2: Instalar Dependências

**No Windows:**

1. **Abra a pasta** que você copiou:
   ```
   C:\Users\cesar\Desktop\novo-projeto
   ```

2. **Duplo clique** em: `INSTALAR.bat`

3. **Aguarde a instalação automática** de:
   - Python 3.12 (se não tiver instalado)
   - Flask
   - Selenium
   - ChromeDriver

4. **Quando aparecer "INSTALAÇÃO CONCLUÍDA"**, pode fechar a janela

---

### PASSO 3: Fechar TODOS os Chromes

**IMPORTANTE:** Antes de rodar o automator:

1. Feche **TODAS** as janelas do Google Chrome
2. Verifique no Gerenciador de Tarefas se não tem Chrome rodando
3. Isso é necessário para o Selenium conseguir abrir o Chrome com o perfil

---

### PASSO 4: Iniciar o Servidor

**No Windows:**

1. **Duplo clique** em: `RODAR.bat`

2. **Aguarde** o servidor iniciar (você verá: "SERVIDOR FLASK INICIADO")

3. **Acesse no navegador:**
   ```
   http://localhost:5000
   ```

---

### PASSO 5: Usar a Ferramenta

**Na interface web:**

1. **Selecione o Perfil do Chrome**
   - Escolha um perfil FLOW (ex: FLOW_1_Patricia)
   - Deve estar logado na conta Google

2. **Imagem de Referência** (opcional)
   - Clique em "Selecionar" e escolha uma imagem
   - Deixe em branco se não tiver imagem

3. **Pasta de Destino**
   - Digite o caminho completo:
   - Exemplo: `C:\Users\cesar\Videos\Veo-Output`

4. **Cenas**
   - Cole o prompt de cada cena
   - Clique em "Adicionar Nova Cena" para mais cenas

5. **Clique em "INICIAR AUTOMAÇÃO"**

---

## ⚠️ IMPORTANTE

### Limitações do Veo 3:
- Máximo **8 segundos** por vídeo
- Gera **2 vídeos** por cena
- Custo: **20 créditos** por geração

### Antes de Usar:
- ✅ Feche TODOS os Chromes abertos
- ✅ Perfil FLOW deve estar logado na conta Google
- ✅ Pasta de destino deve existir (crie antes se necessário)

---

## 🚨 RESOLUÇÃO DE PROBLEMAS

### Erro: "Python não encontrado"

**Solução:**
1. O INSTALAR.bat deve baixar Python automaticamente
2. Se não funcionar, baixe manualmente: https://www.python.org/downloads/
3. Durante instalação, marque: **"Add Python to PATH"**
4. Rode INSTALAR.bat novamente

---

### Erro: "Nenhum perfil FLOW encontrado"

**Solução:**
1. Abra o Google Chrome
2. Clique no ícone de perfil (canto superior direito)
3. Renomeie um perfil para começar com `FLOW_`
   - Exemplo: `FLOW_1_Patricia`
   - Exemplo: `FLOW_2`
4. Reinicie o servidor (feche e rode RODAR.bat novamente)

---

### Erro: "Chrome instance exited"

**Solução:**
1. Feche **TODOS** os Chromes (inclusive no Gerenciador de Tarefas)
2. Tente novamente
3. Se persistir, reinicie o computador

---

### Erro: "Não conseguiu conectar ao Chrome"

**Solução:**
- O Selenium está tentando abrir o Chrome com o perfil
- Certifique-se de que NENHUM Chrome está aberto
- Feche pelo Gerenciador de Tarefas se necessário

---

## 📝 NOTAS TÉCNICAS

**Requisitos:**
- Windows 10/11
- Python 3.12+ (instalado automaticamente)
- Google Chrome instalado
- Pelo menos 1 perfil Chrome renomeado para FLOW_

**Arquivos Importantes:**
- `INSTALAR.bat` - Instala tudo automaticamente
- `RODAR.bat` - Inicia o servidor Flask
- `app.py` - Backend Flask
- `automator.py` - Lógica do Selenium
- `templates/index.html` - Interface web

---

## 🎯 FLUXO RESUMIDO

1. ✅ Copiar pasta para Windows (`C:\Users\cesar\Desktop\novo-projeto`)
2. ✅ Duplo clique em `INSTALAR.bat`
3. ✅ Fechar TODOS os Chromes
4. ✅ Duplo clique em `RODAR.bat`
5. ✅ Acessar `http://localhost:5000`
6. ✅ Preencher formulário e clicar em "Iniciar"
7. ✅ Aguardar os vídeos serem gerados

---

**Desenvolvido com 🏆**