@echo off
chcp 65001 > nul
REM ========================================
REM  VEO AUTOMATOR - INSTALADOR AUTOMÁTICO
REM ========================================
echo.
echo ========================================
echo  🏆 VEO AUTOMATOR - INSTALADOR
echo ========================================
echo.

REM Verificar se Python está instalado
echo [1/5] Verificando Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo 📥 Baixando Python 3.12...
    echo Por favor, aguarde...
    echo.

    REM Baixar Python usando PowerShell
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe' -OutFile '%TEMP%\python-installer.exe'}"

    echo.
    echo 🔧 Instalando Python...
    echo IMPORTANTE: Marque 'Add Python to PATH' durante a instalação!
    echo.
    start /wait %TEMP%\python-installer.exe /quiet InstallAllUsers=1 PrependPath=1

    REM Limpar instalador
    del %TEMP%\python-installer.exe

    echo.
    echo ✅ Python instalado! Reiniciando instalação...
    timeout /t 3 > nul

    REM Recarregar PATH
    call refreshenv 2> nul

    python --version > nul 2>&1
    if errorlevel 1 (
        echo.
        echo ⚠️ Python instalado, mas precisa reiniciar o terminal.
        echo Por favor, FECHE este terminal e execute INSTALAR.bat novamente.
        echo.
        pause
        exit /b 1
    )
)

python --version
echo ✅ Python encontrado!
echo.

REM Criar ambiente virtual
echo [2/5] Criando ambiente virtual...
if exist venv (
    echo ⚠️ Ambiente virtual já existe, pulando...
) else (
    python -m venv venv
    echo ✅ Ambiente virtual criado!
)
echo.

REM Ativar ambiente virtual
echo [3/5] Ativando ambiente virtual...
call venv\Scripts\activate.bat
echo ✅ Ambiente virtual ativado!
echo.

REM Instalar dependências
echo [4/5] Instalando dependências (Flask, Selenium)...
echo Por favor, aguarde...
python -m pip install --upgrade pip > nul 2>&1
pip install -r requirements.txt
echo ✅ Dependências instaladas!
echo.

REM Baixar ChromeDriver
echo [5/5] Baixando ChromeDriver...
python -c "import chromedriver_autoinstaller; chromedriver_autoinstaller.install()" 2> nul
if errorlevel 1 (
    echo ⚠️ ChromeDriver será baixado automaticamente quando necessário.
) else (
    echo ✅ ChromeDriver configurado!
)
echo.

REM Concluído
echo ========================================
echo  ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ========================================
echo.
echo 🚀 Próximo passo:
echo    Execute RODAR.bat para iniciar o servidor
echo.
echo ========================================
pause
