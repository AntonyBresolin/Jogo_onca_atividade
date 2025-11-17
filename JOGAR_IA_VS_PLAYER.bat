@echo off
chcp 65001 >nul
title Jogo da Onça - Jogador vs IA

echo ╔════════════════════════════════════════════════════╗
echo ║         JOGO DA ONÇA - JOGADOR vs IA               ║
echo ╚════════════════════════════════════════════════════╝
echo.
echo Escolha seu lado:
echo   [1] Jogar como ONÇA (IA joga com Cachorros)
echo   [2] Jogar como CACHORROS (IA joga com Onça)
echo.
set /p escolha="Digite 1 ou 2: "

if "%escolha%"=="1" (
    echo.
    echo ┌────────────────────────────────────────────────────┐
    echo │ Você escolheu: ONÇA                                │
    echo │ IA jogará com: CACHORROS                           │
    echo └────────────────────────────────────────────────────┘
    echo.
    echo Iniciando jogo...
    echo.
    
    REM Inicia o controlador em uma nova janela
    start "CONTROLADOR" cmd /k "cd /d %~dp0onca_py && python controlador.py 2"
    
    REM Aguarda 2 segundos para o controlador iniciar
    timeout /t 2 /nobreak >nul
    
    REM Inicia a IA jogando como Cachorros em uma nova janela
    start "IA - CACHORROS" cmd /k "cd /d %~dp0onca_py && python ia_jogador.py c"
    
    REM Aguarda 2 segundos
    timeout /t 2 /nobreak >nul
    
    REM Inicia você jogando como Onça (janela interativa com tutorial)
    start "VOCÊ - ONÇA" cmd /k "cd /d %~dp0onca_py && python player_humano.py o"
    
) else if "%escolha%"=="2" (
    echo.
    echo ┌────────────────────────────────────────────────────┐
    echo │ Você escolheu: CACHORROS                           │
    echo │ IA jogará com: ONÇA                                │
    echo └────────────────────────────────────────────────────┘
    echo.
    echo Iniciando jogo...
    echo.
    
    REM Inicia o controlador em uma nova janela
    start "CONTROLADOR" cmd /k "cd /d %~dp0onca_py && python controlador.py 2"
    
    REM Aguarda 2 segundos para o controlador iniciar
    timeout /t 2 /nobreak >nul
    
    REM Inicia a IA jogando como Onça em uma nova janela
    start "IA - ONÇA" cmd /k "cd /d %~dp0onca_py && python ia_jogador.py o"
    
    REM Aguarda 2 segundos
    timeout /t 2 /nobreak >nul
    
    REM Inicia você jogando como Cachorros (janela interativa com tutorial)
    start "VOCÊ - CACHORROS" cmd /k "cd /d %~dp0onca_py && python player_humano.py c"
    
) else (
    echo.
    echo ╔════════════════════════════════════════════════════╗
    echo ║ ERRO: Escolha inválida! Digite apenas 1 ou 2       ║
    echo ╚════════════════════════════════════════════════════╝
    timeout /t 3
    exit
)

echo.
echo ╔════════════════════════════════════════════════════╗
echo ║ Jogo iniciado! Verifique as janelas abertas        ║
echo ╚════════════════════════════════════════════════════╝
echo.
timeout /t 3
