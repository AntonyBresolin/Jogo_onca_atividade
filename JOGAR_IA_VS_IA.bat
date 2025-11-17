@echo off
REM Script para iniciar o jogo completo em 3 janelas separadas

echo ╔══════════════════════════════════════════════════════════════════════════╗
echo ║           JOGO DA ONÇA - IA com Minimax + Alpha-Beta                    ║
echo ╚══════════════════════════════════════════════════════════════════════════╝
echo.
echo Iniciando o jogo em 3 terminais separados...
echo.

REM Verifica se o Redis está rodando
docker ps | findstr redis >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠ Redis não está rodando! Iniciando Redis...
    docker-compose up -d
    timeout /t 3 >nul
) else (
    echo ✓ Redis já está rodando
)

echo.
echo Abrindo terminais:
echo   1. Controlador do jogo
echo   2. IA Onça
echo   3. IA Cachorros
echo.

REM Terminal 1 - Controlador
start "JOGO DA ONÇA - Controlador" cmd /k "cd /d %~dp0onca_py && echo ══════════════════════════════════════ && echo   CONTROLADOR DO JOGO && echo ══════════════════════════════════════ && echo. && python controlador.py o 100 30"

REM Aguarda 2 segundos para o controlador iniciar
timeout /t 2 >nul

REM Terminal 2 - IA Onça
start "JOGO DA ONÇA - IA Onça" cmd /k "cd /d %~dp0onca_py && echo ══════════════════════════════════════ && echo   IA JOGANDO COMO ONÇA && echo ══════════════════════════════════════ && echo. && python ia_jogador.py o"

REM Terminal 3 - IA Cachorros
start "JOGO DA ONÇA - IA Cachorros" cmd /k "cd /d %~dp0onca_py && echo ══════════════════════════════════════ && echo   IA JOGANDO COMO CACHORROS && echo ══════════════════════════════════════ && echo. && python ia_jogador.py c"

echo.
echo ✓ Todos os terminais foram abertos!
echo.
echo Observe o terminal do CONTROLADOR para ver o jogo acontecendo.
echo Os terminais das IAs mostram estatísticas detalhadas.
echo.
echo Pressione qualquer tecla para fechar esta janela...
pause >nul
