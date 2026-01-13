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

            print(f"\n[LOG] ⏸️  AUTOMAÇÃO PAUSADA - Verifique a página e me diga o que apareceu!")

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
