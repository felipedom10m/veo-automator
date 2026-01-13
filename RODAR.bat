@echo off
chcp 65001 > nul
REM ========================================
REM  VEO AUTOMATOR - INICIAR SERVIDOR
REM ========================================

echo.
echo ========================================
echo  🏆 VEO AUTOMATOR - SERVIDOR
echo ========================================
echo.

REM Verificar se ambiente virtual existe
if not exist venv (
    echo ❌ ERRO: Ambiente virtual não encontrado!
    echo.
    echo Por favor, execute INSTALAR.bat primeiro.
    echo.
    pause
    exit /b 1
)

REM Ativar ambiente virtual
echo 🔧 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Iniciar servidor Flask
echo.
echo ========================================
echo  🚀 INICIANDO SERVIDOR FLASK
echo ========================================
echo.
echo 📱 Acesse no navegador:
echo    http://localhost:5000
echo.
echo ⚠️ Para PARAR o servidor, pressione CTRL+C
echo ========================================
echo.

python app.py

REM Se o servidor parar
echo.
echo Servidor encerrado.
pause
