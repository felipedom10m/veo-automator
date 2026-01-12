# 🎬 Veo Automator - Automatizador de Vídeos para Instagram Reels

## 📋 O que é este projeto?

Uma ferramenta que automatiza a criação de vídeos no **Veo 3 (Google)** para produção de conteúdo para Instagram Reels, eliminando o trabalho manual repetitivo de gerar múltiplas cenas de vídeo.

---

## 😫 Qual é o problema que resolve?

### A Dor Atual:

Criar um vídeo de Reels (15s a 1min) requer:
- Dividir o vídeo em múltiplas cenas de 8 segundos (limite do Veo 3)
- Um vídeo de 40 segundos = aproximadamente 10 prompts = 20 vídeos (2 por cena)
- **Processo manual extremamente lento:**
  1. Acessar o Veo 3 no Google
  2. Fazer login na conta
  3. Copiar e colar o prompt da Cena 1
  4. Anexar imagem de referência
  5. Gerar 2 vídeos (para ter opções)
  6. Aguardar geração
  7. Baixar os vídeos
  8. Repetir para Cena 2, 3, 4... 10 vezes
  9. Organizar manualmente os arquivos

**Resultado:** 2 horas por dia só copiando e colando prompts! 😩

---

## ✅ Qual é a solução?

### O Prazer que Traz:

Uma ferramenta automatizada que faz **TUDO** sozinha:
- Login automático no Veo 3
- Processa todos os prompts de uma vez
- Gera 2 vídeos por cena automaticamente
- Baixa e organiza os vídeos com nomes padronizados
- Economiza horas de trabalho repetitivo

**De 2 horas de trabalho manual → para 5 minutos de configuração!** ⚡

---

## 🎨 Interface da Ferramenta

```
╔════════════════════════════════════════════════════╗
║          VEO AUTOMATOR - GERADOR DE VÍDEOS         ║
╚════════════════════════════════════════════════════╝

📧 Email: [___________________________________]

🔒 Senha: [___________________________________]

🖼️ Imagem de referência: [Selecionar arquivo] (opcional)

📁 Pasta de destino: [Selecionar pasta]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 CENAS DO VÍDEO

┌─ Cena 1 ──────────────────────────────────────────┐
│                                                    │
│  [Cole aqui o prompt da primeira cena]            │
│                                                    │
└────────────────────────────────────────────────────┘

        [➕ Adicionar nova cena]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

            [🚀 INICIAR AUTOMAÇÃO]
```

---

## ⚙️ Como Funciona?

1. **Você preenche:**
   - Email e senha da conta do Google (pode variar por cliente)
   - Imagem de referência da personagem (se houver)
   - Pasta onde os vídeos serão salvos

2. **Você adiciona as cenas:**
   - Clica em "+ Adicionar nova cena" quantas vezes precisar
   - Cola cada prompt no campo correspondente
   - Exemplo: 10 cenas = 10 campos preenchidos

3. **A ferramenta faz o resto:**
   - Abre o Chrome
   - Faz login no Veo 3
   - Processa cada cena automaticamente:
     - Cola o prompt
     - Anexa a imagem
     - Gera 2 vídeos
     - Aguarda o download
   - Renomeia e organiza os arquivos

4. **Resultado final:**
   - Vídeos salvos na pasta escolhida com nomes organizados:
     - `cena-1-video-1.mp4`
     - `cena-1-video-2.mp4`
     - `cena-2-video-1.mp4`
     - `cena-2-video-2.mp4`
     - E assim por diante...

---

## 🛠️ Tecnologias Utilizadas

- **Python** - Linguagem de programação
- **Selenium** - Automação do navegador Chrome
- **Tkinter** - Interface gráfica simples e intuitiva

---

## 🎯 Benefícios

✅ Economia de tempo (de horas para minutos)
✅ Elimina trabalho repetitivo
✅ Organização automática dos arquivos
✅ Suporte para múltiplas contas do Google
✅ Interface simples e fácil de usar
✅ Gera 2 vídeos por cena (para ter opções de escolha)

---

## 📦 Próximos Passos

Após a geração automática dos vídeos:
1. Revisar os vídeos gerados (escolher o melhor de cada cena)
2. Levar para o CapCut para edição final
3. Ajustar cortes, espaços e erros
4. Publicar no Instagram Reels! 🎉
