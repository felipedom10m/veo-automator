#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VEO AUTOMATOR - Módulo de Automação
Lógica de automação com Selenium para controlar o Chrome e gerar vídeos no Veo 3
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

class VeoAutomator:
    """
    Classe principal para automação do Veo 3
    """

    def __init__(self, email, password, output_folder, image_path=None):
        """
        Inicializa o automatizador

        Args:
            email (str): Email do Google
            password (str): Senha do Google
            output_folder (str): Pasta onde os vídeos serão salvos
            image_path (str, optional): Caminho da imagem de referência
        """
        self.email = email
        self.password = password
        self.output_folder = output_folder
        self.image_path = image_path
        self.driver = None

    def setup_chrome(self):
        """
        Abre Chrome com perfil LIMPO (sem conflitos)
        """
        print(f"[LOG] Configurando Chrome...")

        import subprocess
        import tempfile

        # PASSO 1: Matar TODOS os processos do Chrome
        print("[LOG] Encerrando Chrome se estiver aberto...")
        try:
            subprocess.run(['taskkill', '/F', '/IM', 'chrome.exe'],
                          capture_output=True, shell=True)
            subprocess.run(['taskkill', '/F', '/IM', 'chromedriver.exe'],
                          capture_output=True, shell=True)
            time.sleep(2)
            print("[LOG] ✅ Chrome encerrado!")
        except Exception as e:
            print(f"[LOG] Aviso: {e}")

        # PASSO 2: Criar perfil temporário limpo
        temp_profile = os.path.join(tempfile.gettempdir(), "chrome_veo_automation")
        print(f"[LOG] Usando perfil limpo em: {temp_profile}")

        # PASSO 3: Configurar ChromeOptions
        chrome_options = Options()
        chrome_options.add_argument(f"--user-data-dir={temp_profile}")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        # Configurar downloads
        prefs = {
            "download.default_directory": self.output_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # PASSO 4: Iniciar Chrome
        try:
            print("[LOG] Iniciando Chrome...")
            import chromedriver_autoinstaller
            chromedriver_autoinstaller.install()

            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 60)
            print("[LOG] ✅ Chrome aberto!")

        except Exception as e:
            print(f"[ERRO] Falha ao abrir Chrome: {e}")
            raise

    def navigate_to_flow(self):
        """
        Navega até a página do Flow e clica em + Novo projeto
        """
        print("\n[LOG] === NAVEGANDO PARA FLOW ===")
        print("[LOG] URL: https://labs.google/fx/pt/tools/flow")

        self.driver.get("https://labs.google/fx/pt/tools/flow")
        print("[LOG] Aguardando página carregar (10 segundos)...")
        time.sleep(10)  # Dar tempo para página carregar completamente

        print(f"[LOG] Página carregada. Título: {self.driver.title}")
        print(f"[LOG] URL atual: {self.driver.current_url}")

        # Tentar várias estratégias para encontrar o botão "Novo projeto"
        print("\n[LOG] Procurando botão 'Novo projeto'...")

        # Estratégia 1: XPath com texto em português
        selectors = [
            ("XPATH - texto 'Novo projeto'", By.XPATH, "//button[contains(., 'Novo projeto')]"),
            ("XPATH - texto 'novo projeto' (minúsculo)", By.XPATH, "//button[contains(translate(., 'NOVO PROJETO', 'novo projeto'), 'novo projeto')]"),
            ("XPATH - qualquer botão", By.XPATH, "//button"),
            ("CSS - todos os botões", By.CSS_SELECTOR, "button"),
        ]

        botao_encontrado = False
        for nome, by_type, selector in selectors:
            try:
                print(f"[LOG] Tentando: {nome}...")
                elementos = self.driver.find_elements(by_type, selector)
                print(f"[LOG] Encontrados {len(elementos)} elemento(s)")

                if elementos:
                    # Listar todos os botões encontrados
                    for idx, elem in enumerate(elementos[:10], 1):  # Mostrar no máximo 10
                        try:
                            texto = elem.text.strip()
                            aria_label = elem.get_attribute('aria-label') or ''
                            print(f"[LOG]   Botão {idx}: texto='{texto}' aria-label='{aria_label}'")

                            # Verificar se é o botão que queremos
                            if 'novo' in texto.lower() and 'projeto' in texto.lower():
                                print(f"[LOG] ✅ ENCONTRADO! Clicando no botão...")
                                elem.click()
                                botao_encontrado = True
                                break
                        except:
                            continue

                if botao_encontrado:
                    break

            except Exception as e:
                print(f"[LOG] Erro com {nome}: {e}")
                continue

        if not botao_encontrado:
            print("\n[ERRO] ❌ NÃO ENCONTROU o botão 'Novo projeto'")
            print("[DICA] Tire um print da página e envie para análise")
            # Salvar screenshot para debug
            screenshot_path = os.path.join(self.output_folder, "debug_flow_page.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"[LOG] Screenshot salvo em: {screenshot_path}")
            raise Exception("Botão 'Novo projeto' não encontrado")

        print("[LOG] Aguardando página de criação carregar (10 segundos)...")
        time.sleep(10)
        print(f"[LOG] Página atual: {self.driver.current_url}")
        print("[LOG] ✅ NAVEGAÇÃO CONCLUÍDA!\n")

    def configure_veo_settings(self):
        """
        Configura modelo Veo 3.1 - Fast, 2 vídeos, 16:9
        """
        print("[LOG] Configurando Veo 3.1...")
        try:
            # Clicar em "Veo 3.1 - Fast" para abrir configurações
            veo_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Veo 3.1')]"))
            )
            veo_btn.click()
            time.sleep(2)

            # Selecionar Paisagem (16:9) - já vem selecionado geralmente
            # Selecionar Respostas por comando: 2
            try:
                respostas_dropdown = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Respostas por comando')]/..//select")
                respostas_dropdown.click()
                option_2 = self.driver.find_element(By.XPATH, "//option[contains(text(), '2')]")
                option_2.click()
                print("[LOG] Configurado para gerar 2 vídeos")
            except:
                print("[AVISO] Não conseguiu alterar número de respostas (pode já estar em 2)")

            # Fechar modal de configurações (clicar fora ou ESC)
            time.sleep(1)

        except Exception as e:
            print(f"[AVISO] Erro ao configurar Veo: {e}")

    def select_mode(self, has_image):
        """
        Seleciona modo: Frames para vídeo (com imagem) ou Texto para vídeo
        """
        if has_image:
            print("[LOG] Selecionando modo 'Frames para vídeo'...")
            try:
                frames_btn = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Frames para vídeo')]")
                frames_btn.click()
                time.sleep(1)
            except:
                print("[AVISO] Não encontrou opção 'Frames para vídeo'")
        else:
            print("[LOG] Modo 'Texto para vídeo' já selecionado")

    def upload_image(self):
        """
        Faz upload da imagem de referência
        """
        if not self.image_path or not os.path.exists(self.image_path):
            return

        print(f"[LOG] Fazendo upload de imagem: {self.image_path}")
        try:
            # Clicar no botão de upload (ícone inferior esquerdo)
            upload_btn = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )

            # Enviar caminho da imagem direto para o input file
            upload_btn.send_keys(self.image_path)
            time.sleep(2)

            # Verificar se aparece modal de aviso
            try:
                concordo_btn = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Concordo')]")
                concordo_btn.click()
                print("[LOG] Clicou em 'Concordo' no aviso")
                time.sleep(2)
            except:
                print("[LOG] Modal de aviso não apareceu")

        except Exception as e:
            print(f"[ERRO] Erro ao fazer upload da imagem: {e}")

    def generate_video(self, prompt, scene_number):
        """
        Gera 2 vídeos para uma cena no Veo 3

        Args:
            prompt (str): Texto do prompt
            scene_number (int): Número da cena
        """
        print(f"\n[LOG] === GERANDO CENA {scene_number} ===")

        try:
            # 1. Selecionar modo (Frames ou Texto)
            self.select_mode(has_image=bool(self.image_path))

            # 2. Configurar Veo 3.1 (apenas na primeira vez)
            if scene_number == 1:
                self.configure_veo_settings()

            # 3. Upload de imagem (se tiver)
            if self.image_path:
                self.upload_image()

            # 4. Colar prompt no campo
            print(f"[LOG] Colando prompt: {prompt[:50]}...")
            prompt_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'Crie um vídeo')]"))
            )
            prompt_field.clear()
            prompt_field.send_keys(prompt)
            time.sleep(1)

            # 5. Clicar na seta (→) para gerar
            print("[LOG] Iniciando geração...")
            generate_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Gerar' or contains(@class, 'generate')]"))
            )
            generate_btn.click()

            # 6. Aguardar geração (pode demorar)
            print("[LOG] Aguardando geração dos vídeos...")
            time.sleep(30)  # Tempo estimado de geração

            # 7. Baixar os 2 vídeos gerados
            self.download_videos(scene_number)

            print(f"[LOG] ✅ Cena {scene_number} concluída!")

        except Exception as e:
            print(f"[ERRO] Erro ao gerar cena {scene_number}: {e}")
            raise

    def download_videos(self, scene_number):
        """
        Baixa os 2 vídeos gerados e renomeia
        """
        print(f"[LOG] Baixando vídeos da cena {scene_number}...")

        try:
            # Localizar botões de download
            download_buttons = self.driver.find_elements(By.XPATH, "//button[@aria-label='Download' or contains(@class, 'download')]")

            for idx, btn in enumerate(download_buttons[:2], start=1):  # Apenas 2 vídeos
                btn.click()
                print(f"[LOG] Baixando vídeo {idx}/2")
                time.sleep(3)

                # Renomear arquivo baixado
                # TODO: Implementar renomeação automática dos arquivos baixados
                # De: video-12345.mp4 → Para: cena-X-video-Y.mp4

        except Exception as e:
            print(f"[ERRO] Erro ao baixar vídeos: {e}")

    def configure_and_generate(self, prompt):
        """
        Configura o projeto e inicia geração do vídeo

        Args:
            prompt (str): Texto do prompt da cena
        """
        try:
            has_image = bool(self.image_path and os.path.exists(self.image_path))

            # AGUARDAR PÁGINA CARREGAR COMPLETAMENTE
            print("[LOG] Aguardando página de criação carregar completamente...")
            time.sleep(8)  # Tempo para página carregar

            # PASSO 1: Decidir entre "Texto para vídeo" ou "Frames para vídeo"
            if has_image:
                print("[LOG] Imagem detectada. Mudando para 'Frames para vídeo'...")

                # Clicar no dropdown "Texto para vídeo"
                try:
                    print("[LOG] Procurando dropdown 'Texto para vídeo'...")
                    texto_video_dropdown = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Texto para vídeo')] | //div[contains(., 'Texto para vídeo') and @role='button']"))
                    )
                    texto_video_dropdown.click()
                    print("[LOG] ✅ Clicou no dropdown 'Texto para vídeo'")

                    # AGUARDAR modal abrir completamente
                    print("[LOG] Aguardando modal carregar (3 segundos)...")
                    time.sleep(3)

                    # ===== DEBUG: SALVAR HTML COMPLETO PARA ANÁLISE =====
                    print("[LOG] 🔍 MODO DEBUG: Salvando HTML da página...")
                    try:
                        html_completo = self.driver.page_source
                        debug_html_path = os.path.join(self.output_folder, "debug_modal_html.html")
                        with open(debug_html_path, 'w', encoding='utf-8') as f:
                            f.write(html_completo)
                        print(f"[LOG] 📄 HTML salvo em: {debug_html_path}")
                    except Exception as e:
                        print(f"[LOG] Erro ao salvar HTML: {e}")

                    # ===== DEBUG: INSPECIONAR TODOS ELEMENTOS COM "FRAMES" =====
                    print("[LOG] 🔍 Analisando TODOS elementos com 'Frames'...")
                    js_investigacao = """
                    // Procurar TODOS elementos que contenham "Frames"
                    let todosElementos = Array.from(document.querySelectorAll('*'));
                    let resultados = [];

                    todosElementos.forEach((el, idx) => {
                        let texto = el.textContent || '';
                        if (texto.includes('Frames') && el.offsetParent !== null) {
                            resultados.push({
                                indice: idx,
                                tag: el.tagName,
                                id: el.id || 'sem-id',
                                classes: el.className || 'sem-classe',
                                texto: texto.substring(0, 100),
                                role: el.getAttribute('role') || 'sem-role',
                                type: el.getAttribute('type') || 'sem-type',
                                dataType: el.getAttribute('data-type') || 'sem-data-type',
                                clicavel: el.onclick !== null || el.getAttribute('onclick') !== null,
                                temCursor: window.getComputedStyle(el).cursor === 'pointer'
                            });
                        }
                    });

                    return resultados;
                    """

                    elementos_frames = self.driver.execute_script(js_investigacao)
                    print(f"[LOG] 🔍 Encontrados {len(elementos_frames)} elementos com 'Frames':")
                    print("[LOG] " + "="*80)
                    for elem_info in elementos_frames:
                        print(f"[LOG] Elemento #{elem_info['indice']}:")
                        print(f"[LOG]   Tag: <{elem_info['tag']}>")
                        print(f"[LOG]   ID: {elem_info['id']}")
                        print(f"[LOG]   Classes: {elem_info['classes']}")
                        print(f"[LOG]   Role: {elem_info['role']}")
                        print(f"[LOG]   Type: {elem_info['type']}")
                        print(f"[LOG]   Data-Type: {elem_info['dataType']}")
                        print(f"[LOG]   Clicável: {elem_info['clicavel']}")
                        print(f"[LOG]   Cursor pointer: {elem_info['temCursor']}")
                        print(f"[LOG]   Texto: {elem_info['texto'][:80]}...")
                        print("[LOG]   " + "-"*78)
                    print("[LOG] " + "="*80)

                    # Selecionar "Frames para vídeo" - ESTRATÉGIA CORRETA
                    print("[LOG] Procurando opção 'Frames para vídeo' com role='option'...")

                    # ESTRATÉGIA CORRETA: Procurar por role="option" que contenha "Frames"
                    # Baseado na análise, o elemento correto tem:
                    # - role="option"
                    # - Clicável: True
                    # - Cursor pointer: True
                    # - Texto: "photo_sparkFrames para vídeo"

                    frames_option = None
                    try:
                        # Tentar pela classe específica encontrada
                        print("[LOG] Tentativa 1: Por classe 'sc-fbe1c021-2 jynkRM'...")
                        frames_option = self.driver.find_element(By.XPATH,
                            "//div[@role='option' and contains(@class, 'sc-fbe1c021-2') and contains(., 'Frames para vídeo')]")
                        print("[LOG] ✅ Encontrou pela classe específica!")
                    except:
                        print("[LOG] Não encontrou pela classe específica. Tentando role='option'...")
                        try:
                            # Buscar todos elementos com role="option"
                            opcoes = self.driver.find_elements(By.XPATH, "//div[@role='option']")
                            print(f"[LOG] Encontrou {len(opcoes)} elementos com role='option'")

                            for idx, opcao in enumerate(opcoes, 1):
                                texto = opcao.text.strip()
                                print(f"[LOG]   Opção {idx}: '{texto}'")

                                # Verificar se é a opção de Frames
                                if 'frames' in texto.lower() and 'vídeo' in texto.lower():
                                    frames_option = opcao
                                    print(f"[LOG] ✅ ENCONTROU opção 'Frames para vídeo'!")
                                    break
                        except Exception as e:
                            print(f"[LOG] Erro ao buscar por role='option': {e}")

                    # ESTRATÉGIA 2: JavaScript como fallback
                    if not frames_option:
                        print("[LOG] ⚠️ Tentando JavaScript para encontrar role='option' com 'Frames'...")
                        try:
                            js_code = """
                            // Buscar div com role="option" que contenha "Frames"
                            let opcoes = Array.from(document.querySelectorAll('div[role="option"]'));
                            let frames_elem = opcoes.find(el =>
                                el.textContent.includes('Frames') &&
                                el.textContent.includes('vídeo')
                            );
                            return frames_elem;
                            """
                            frames_option = self.driver.execute_script(js_code)
                            if frames_option:
                                print("[LOG] ✅ JavaScript encontrou elemento!")
                            else:
                                print("[LOG] ❌ JavaScript não encontrou elemento")
                        except Exception as e:
                            print(f"[LOG] Erro no JavaScript: {e}")

                    # CLICAR no elemento encontrado
                    if not frames_option:
                        # Salvar screenshot para debug
                        screenshot_path = os.path.join(self.output_folder, "debug_modal_frames.png")
                        self.driver.save_screenshot(screenshot_path)
                        print(f"[LOG] 📸 Screenshot salvo em: {screenshot_path}")
                        raise Exception("❌ NÃO encontrou opção 'Frames para vídeo' depois de todas tentativas")

                    # Tentar clicar normalmente primeiro
                    try:
                        print("[LOG] Tentando clicar normalmente...")
                        frames_option.click()
                        print("[LOG] ✅ Clicou com .click() normal!")
                    except Exception as e:
                        print(f"[LOG] .click() falhou: {e}. Tentando JavaScript...")
                        # Usar JavaScript para clicar
                        self.driver.execute_script("arguments[0].click();", frames_option)
                        print("[LOG] ✅ Clicou com JavaScript!")

                    print("[LOG] ✅ Selecionou 'Frames para vídeo'")
                    time.sleep(3)

                except Exception as e:
                    print(f"[ERRO] Erro ao mudar para 'Frames para vídeo': {e}")
                    raise

                # PASSO 2: Fazer upload da imagem
                print(f"[LOG] Fazendo upload da imagem: {self.image_path}")
                try:
                    # Aguardar a interface de "Frames para vídeo" carregar
                    print("[LOG] Aguardando interface 'Frames para vídeo' carregar...")
                    time.sleep(3)

                    # ===== DEBUG: INVESTIGAR BOTÃO DE UPLOAD (+) =====
                    print("[LOG] 🔍 Procurando botão '+' para fazer upload...")

                    # Investigar todos os botões visíveis
                    js_investigar_botoes = """
                    let botoes = Array.from(document.querySelectorAll('button'));
                    let resultados = [];

                    botoes.forEach((btn, idx) => {
                        if (btn.offsetParent !== null) {  // Apenas visíveis
                            resultados.push({
                                indice: idx,
                                id: btn.id || 'sem-id',
                                classes: btn.className || 'sem-classe',
                                ariaLabel: btn.getAttribute('aria-label') || 'sem-aria-label',
                                texto: btn.textContent.trim() || 'sem-texto',
                                type: btn.type || 'sem-type',
                                temIcone: btn.querySelector('svg') !== null
                            });
                        }
                    });

                    return resultados;
                    """

                    todos_botoes = self.driver.execute_script(js_investigar_botoes)
                    print(f"[LOG] 🔍 Encontrados {len(todos_botoes)} botões visíveis:")
                    print("[LOG] " + "="*80)

                    for btn_info in todos_botoes[:20]:  # Mostrar primeiros 20
                        print(f"[LOG] Botão #{btn_info['indice']}:")
                        print(f"[LOG]   ID: {btn_info['id']}")
                        print(f"[LOG]   Classes: {btn_info['classes'][:80]}...")
                        print(f"[LOG]   Aria-Label: {btn_info['ariaLabel']}")
                        print(f"[LOG]   Texto: {btn_info['texto'][:50]}")
                        print(f"[LOG]   Type: {btn_info['type']}")
                        print(f"[LOG]   Tem ícone SVG: {btn_info['temIcone']}")
                        print("[LOG]   " + "-"*78)
                    print("[LOG] " + "="*80)

                    # Procurar e clicar no botão "add" (+)
                    print("[LOG] Procurando botão 'add' (+) para adicionar frame...")

                    # ESTRATÉGIA: Procurar botão com texto "add" (ícone +)
                    # Baseado na análise: Botões #15 e #17 têm texto "add"
                    upload_btn = None

                    try:
                        # Procurar todos botões que contenham "add" no texto
                        print("[LOG] Procurando botões com texto 'add'...")
                        botoes_add = self.driver.find_elements(By.XPATH, "//button[contains(., 'add')]")
                        print(f"[LOG] Encontrou {len(botoes_add)} botão(ões) com 'add'")

                        # Filtrar apenas os visíveis e com type="submit"
                        for idx, btn in enumerate(botoes_add, 1):
                            try:
                                texto = btn.text.strip()
                                tipo = btn.get_attribute('type')
                                visivel = btn.is_displayed()
                                classes = btn.get_attribute('class')

                                print(f"[LOG]   Botão {idx}: texto='{texto}' | type='{tipo}' | visível={visivel}")

                                # Queremos o botão que tem APENAS "add" (não "add_photo_alternate")
                                # E que seja visível e type="submit"
                                if texto == 'add' and tipo == 'submit' and visivel:
                                    # Verificar se tem a classe específica do frame
                                    if 'sc-d02e9a37-1' in classes:
                                        upload_btn = btn
                                        print(f"[LOG] ✅ ENCONTROU botão 'add' correto! (#{idx})")
                                        break
                            except Exception as e:
                                print(f"[LOG] Erro ao verificar botão {idx}: {e}")
                                continue

                        # Se não encontrou pela classe, pegar o primeiro botão "add"
                        if not upload_btn and botoes_add:
                            for btn in botoes_add:
                                if btn.text.strip() == 'add' and btn.is_displayed():
                                    upload_btn = btn
                                    print("[LOG] ✅ Usando primeiro botão 'add' visível")
                                    break

                    except Exception as e:
                        print(f"[LOG] Erro ao procurar botão 'add': {e}")

                    # Se encontrou o botão, clicar nele
                    if upload_btn:
                        try:
                            print("[LOG] Clicando no botão '+' (add)...")
                            upload_btn.click()
                            print("[LOG] ✅ Clicou no botão '+'!")
                            time.sleep(2)
                        except Exception as e:
                            print(f"[LOG] Erro ao clicar: {e}. Tentando JavaScript...")
                            self.driver.execute_script("arguments[0].click();", upload_btn)
                            print("[LOG] ✅ Clicou com JavaScript!")
                            time.sleep(2)
                    else:
                        print("[LOG] ⚠️ Não encontrou botão 'add'. Tentando input direto...")

                    # Agora procurar o input[@type='file']
                    print("[LOG] Procurando input[@type='file']...")
                    upload_input = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                    )

                    # Enviar caminho da imagem
                    upload_input.send_keys(self.image_path)
                    print("[LOG] Upload iniciado. Aguardando imagem carregar...")

                    # AGUARDAR a imagem aparecer no preview (boa prática!)
                    print("[LOG] Aguardando preview da imagem aparecer...")
                    image_preview = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'blob:') or contains(@src, 'data:')]"))
                    )
                    print("[LOG] ✅ Imagem carregada e visível no preview!")
                    time.sleep(2)

                    # PASSO 3: Clicar em "Cortar e salvar"
                    print("[LOG] Procurando botão 'Cortar e salvar'...")
                    cortar_btn = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Cortar e salvar') or contains(., 'Cortar')]"))
                    )
                    cortar_btn.click()
                    print("[LOG] ✅ Clicou em 'Cortar e salvar'")
                    time.sleep(3)

                except Exception as e:
                    print(f"[ERRO] Erro ao fazer upload da imagem: {e}")
                    raise
            else:
                print("[LOG] Sem imagem. Mantendo 'Texto para vídeo'")

            # PASSO 4: Clicar no campo de texto e colar o prompt
            print(f"[LOG] Colando prompt: {prompt[:80]}...")
            try:
                print("[LOG] Procurando campo de texto...")
                prompt_field = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//textarea[contains(@placeholder, 'Crie um vídeo') or contains(@placeholder, 'vídeo')]"))
                )
                prompt_field.click()
                time.sleep(1)
                prompt_field.clear()
                prompt_field.send_keys(prompt)
                print("[LOG] ✅ Prompt colado!")
                time.sleep(2)

            except Exception as e:
                print(f"[ERRO] Erro ao colar prompt: {e}")
                raise

            # PASSO 5: Clicar na seta branca para gerar
            print("[LOG] Procurando seta branca para iniciar geração...")
            try:
                # Aguardar um pouco antes de procurar a seta (garantir que prompt foi colado)
                print("[LOG] Aguardando 3 segundos para garantir que o prompt foi processado...")
                time.sleep(3)

                # ===== DEBUG: INVESTIGAR BOTÕES APÓS COLAR PROMPT =====
                print("[LOG] 🔍 Investigando botões após colar o prompt...")
                js_botoes_geracao = """
                let botoes = Array.from(document.querySelectorAll('button'));
                let resultados = [];

                botoes.forEach((btn, idx) => {
                    if (btn.offsetParent !== null) {  // Apenas visíveis
                        let computedStyle = window.getComputedStyle(btn);
                        resultados.push({
                            indice: idx,
                            classes: btn.className || 'sem-classe',
                            ariaLabel: btn.getAttribute('aria-label') || 'sem-aria-label',
                            texto: btn.textContent.trim() || 'sem-texto',
                            type: btn.type || 'sem-type',
                            disabled: btn.disabled,
                            backgroundColor: computedStyle.backgroundColor,
                            color: computedStyle.color,
                            temIcone: btn.querySelector('svg') !== null,
                            temArrow: btn.textContent.includes('arrow')
                        });
                    }
                });

                return resultados;
                """

                botoes_atuais = self.driver.execute_script(js_botoes_geracao)
                print(f"[LOG] 🔍 Encontrados {len(botoes_atuais)} botões visíveis agora:")
                print("[LOG] " + "="*80)

                for btn_info in botoes_atuais[:25]:  # Mostrar primeiros 25
                    print(f"[LOG] Botão #{btn_info['indice']}:")
                    print(f"[LOG]   Classes: {btn_info['classes'][:80]}...")
                    print(f"[LOG]   Aria-Label: {btn_info['ariaLabel']}")
                    print(f"[LOG]   Texto: {btn_info['texto'][:50]}")
                    print(f"[LOG]   Type: {btn_info['type']}")
                    print(f"[LOG]   Disabled: {btn_info['disabled']}")
                    print(f"[LOG]   Background: {btn_info['backgroundColor']}")
                    print(f"[LOG]   Color: {btn_info['color']}")
                    print(f"[LOG]   Tem SVG: {btn_info['temIcone']}")
                    print(f"[LOG]   Tem 'arrow': {btn_info['temArrow']}")
                    print("[LOG]   " + "-"*78)
                print("[LOG] " + "="*80)

                # Procurar botão de gerar
                print("[LOG] Procurando botão com 'arrow_forward' ou 'Criar'...")
                generate_btn = None

                # ESTRATÉGIA 1: Procurar por texto "arrow_forward" ou contém "Criar"
                try:
                    botoes_candidatos = self.driver.find_elements(By.XPATH,
                        "//button[contains(., 'arrow_forward') or contains(., 'Criar')]")
                    print(f"[LOG] Encontrou {len(botoes_candidatos)} botão(ões) candidato(s)")

                    for idx, btn in enumerate(botoes_candidatos, 1):
                        texto = btn.text.strip()
                        disabled = btn.get_attribute('disabled')
                        aria = btn.get_attribute('aria-label') or 'sem-aria'
                        classes = btn.get_attribute('class')

                        print(f"[LOG]   Candidato {idx}: texto='{texto}' | disabled={disabled} | aria='{aria}'")

                        # Queremos o botão que contém "arrow_forward" e "Criar" E não está desabilitado
                        if 'arrow_forward' in texto and 'Criar' in texto and not disabled:
                            generate_btn = btn
                            print(f"[LOG] ✅ ENCONTROU botão de geração! (#{idx})")
                            break

                except Exception as e:
                    print(f"[LOG] Erro na estratégia 1: {e}")

                # ESTRATÉGIA 2: JavaScript para encontrar botão com classe específica
                if not generate_btn:
                    print("[LOG] Tentando JavaScript...")
                    try:
                        js_find_button = """
                        let botoes = Array.from(document.querySelectorAll('button'));
                        let botao_gerar = botoes.find(btn => {
                            let texto = btn.textContent || '';
                            return texto.includes('arrow_forward') &&
                                   texto.includes('Criar') &&
                                   !btn.disabled &&
                                   btn.offsetParent !== null;
                        });
                        return botao_gerar;
                        """
                        generate_btn = self.driver.execute_script(js_find_button)
                        if generate_btn:
                            print("[LOG] ✅ JavaScript encontrou botão!")
                        else:
                            print("[LOG] ❌ JavaScript não encontrou")
                    except Exception as e:
                        print(f"[LOG] Erro no JavaScript: {e}")

                # Clicar no botão se encontrou
                if not generate_btn:
                    raise Exception("❌ Não encontrou botão de geração após todas tentativas")

                # Tentar clicar
                try:
                    print("[LOG] Clicando no botão de gerar...")
                    generate_btn.click()
                    print("[LOG] ✅ Clicou na seta! Geração iniciada!")
                    time.sleep(3)
                except Exception as e:
                    print(f"[LOG] .click() falhou: {e}. Tentando JavaScript...")
                    self.driver.execute_script("arguments[0].click();", generate_btn)
                    print("[LOG] ✅ Clicou com JavaScript!")
                    time.sleep(3)

            except Exception as e:
                print(f"[ERRO] Erro ao clicar na seta de geração: {e}")
                raise

            print("[LOG] ✅ Configuração concluída! Vídeo em geração...")

        except Exception as e:
            print(f"[ERRO] Erro ao configurar e gerar: {e}")
            # Salvar screenshot para debug
            screenshot_path = os.path.join(self.output_folder, "debug_config_error.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"[LOG] Screenshot salvo em: {screenshot_path}")
            raise

    def google_login(self):
        """
        PASSO 2: Fazer login no Google
        """
        print("\n[LOG] === FAZENDO LOGIN NO GOOGLE ===")

        try:
            # 1. Clicar no botão "Create with Flow"
            print("[LOG] Procurando botão 'Create with Flow'...")
            create_btn = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Create with Flow')]"))
            )
            print("[LOG] Clicando em 'Create with Flow'...")
            create_btn.click()
            time.sleep(3)

            # 2. Preencher email
            print(f"[LOG] Preenchendo email: {self.email}")
            email_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='email']"))
            )
            email_field.clear()
            email_field.send_keys(self.email)
            time.sleep(1)

            # 3. Clicar em "Avançar" (primeira vez)
            print("[LOG] Clicando em 'Avançar' (email)...")
            avancar_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Avançar') or contains(., 'Next')]")
            avancar_btn.click()

            # 4. Aguardar página de senha carregar
            print("[LOG] Aguardando página de senha...")
            time.sleep(3)

            # 5. Preencher senha
            print("[LOG] Preenchendo senha...")
            password_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='password']"))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            time.sleep(1)

            # 6. Clicar em "Avançar" (segunda vez)
            print("[LOG] Clicando em 'Avançar' (senha)...")
            avancar_btn2 = self.driver.find_element(By.XPATH, "//button[contains(., 'Avançar') or contains(., 'Next')]")
            avancar_btn2.click()

            # 7. Aguardar login completar
            print("[LOG] Aguardando login completar...")
            time.sleep(5)

            print(f"[LOG] ✅ LOGIN CONCLUÍDO!")
            print(f"[LOG] URL atual: {self.driver.current_url}")

        except Exception as e:
            print(f"[ERRO] Erro ao fazer login: {e}")
            # Salvar screenshot para debug
            screenshot_path = os.path.join(self.output_folder, "debug_login_error.png")
            self.driver.save_screenshot(screenshot_path)
            print(f"[LOG] Screenshot salvo em: {screenshot_path}")
            raise

    def run(self, scenes):
        """
        VERSÃO INCREMENTAL - PASSO 2: Abrir Chrome, ir para Flow e fazer login (se necessário)
        """
        try:
            print("\n[LOG] 🎯 PASSO 1: Abrindo Chrome e navegando para Flow...")

            # 1. Abrir Chrome
            self.setup_chrome()

            # 2. Ir para o Flow
            print("\n[LOG] Navegando para https://labs.google/fx/pt/tools/flow")
            self.driver.get("https://labs.google/fx/pt/tools/flow")

            print("[LOG] Aguardando 5 segundos para página carregar...")
            time.sleep(5)

            print(f"\n[LOG] ✅ Página do Flow carregada!")
            print(f"[LOG] Título: {self.driver.title}")
            print(f"[LOG] URL: {self.driver.current_url}")

            # 3. Verificar se precisa fazer login
            print("\n[LOG] 🎯 PASSO 2: Verificando se precisa fazer login...")

            try:
                # Tentar encontrar botão "Create with Flow" (só aparece quando NÃO está logado)
                create_btn = self.driver.find_elements(By.XPATH, "//button[contains(., 'Create with Flow')]")

                if create_btn and len(create_btn) > 0:
                    # Botão existe = precisa fazer login
                    print("[LOG] ❌ Não está logado. Fazendo login...")
                    self.google_login()
                else:
                    # Botão não existe = já está logado
                    print("[LOG] ✅ Já está logado! Pulando etapa de login...")

            except Exception as e:
                print(f"[LOG] Erro ao verificar login: {e}")
                print("[LOG] Tentando fazer login mesmo assim...")
                self.google_login()

            print(f"\n[LOG] ✅ PRONTO! Pronto para continuar!")
            print(f"[LOG] Título da página: {self.driver.title}")
            print(f"[LOG] URL atual: {self.driver.current_url}")

            # 4. Clicar em "Novo projeto"
            print("\n[LOG] 🎯 PASSO 3: Clicando em 'Novo projeto'...")
            try:
                # Procurar botão "+ Novo projeto"
                novo_projeto_btn = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Novo projeto')]"))
                )
                print("[LOG] Botão 'Novo projeto' encontrado!")
                novo_projeto_btn.click()
                print("[LOG] ✅ Clicou em 'Novo projeto'!")

                # Aguardar página de criação carregar
                print("[LOG] Aguardando página de criação carregar (5 segundos)...")
                time.sleep(5)

                print(f"[LOG] ✅ Página de criação carregada!")
                print(f"[LOG] URL atual: {self.driver.current_url}")

            except Exception as e:
                print(f"[ERRO] Erro ao clicar em 'Novo projeto': {e}")
                # Salvar screenshot para debug
                screenshot_path = os.path.join(self.output_folder, "debug_novo_projeto_error.png")
                self.driver.save_screenshot(screenshot_path)
                print(f"[LOG] Screenshot salvo em: {screenshot_path}")
                raise

            # 5. Configurar projeto e gerar primeira cena
            print("\n[LOG] 🎯 PASSO 4: Configurando projeto e iniciando geração...")
            self.configure_and_generate(scenes[0])

            print(f"\n[LOG] ⏸️  AUTOMAÇÃO PAUSADA - Vídeo em geração!")
            print(f"[LOG] Aguardando geração dos 2 vídeos...")

            # NÃO FECHA O NAVEGADOR - deixa aberto para você ver
            input("[LOG] Pressione ENTER no CMD para fechar o navegador...")

        except Exception as e:
            print(f"\n[ERRO] ❌ Falhou: {str(e)}")
            raise

        finally:
            if self.driver:
                print("[LOG] Fechando navegador...")
                self.driver.quit()


def detect_flow_profiles():
    """
    Detecta perfis do Chrome que começam com FLOW_

    Returns:
        list: Lista de nomes de perfis FLOW
    """
    import json
    import glob

    # Caminho Windows nativo
    chrome_user_data = os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data")
    flow_profiles = []

    try:
        # Buscar todos os arquivos Preferences de cada Profile
        preferences_files = glob.glob(f"{chrome_user_data}\\Profile*\\Preferences")

        for pref_file in preferences_files:
            try:
                with open(pref_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                    # Extrair nome do perfil
                    profile_name = data.get('profile', {}).get('name', '')

                    # Filtrar apenas perfis que começam com FLOW_ (case-insensitive)
                    if profile_name.upper().startswith('FLOW_'):
                        flow_profiles.append(profile_name)

            except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
                # Ignorar perfis com erro
                continue

        # Ordenar alfabeticamente
        flow_profiles.sort()

        return flow_profiles

    except Exception as e:
        print(f"[ERRO] Erro ao detectar perfis: {e}")
        return []
