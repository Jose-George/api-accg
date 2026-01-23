@echo off
:: Navega até a pasta do projeto
cd /d "C:\Users\kaymm\OneDrive\Área de Trabalho\api-accg-develop\api-accg"

:: Executa o comando usando o python do seu ambiente virtual (venv)
"C:\Users\kaymm\OneDrive\Área de Trabalho\api-accg-develop\venv\Scripts\python.exe" manage.py check_vencimentos

:: Pausa para você ver se deu erro ou sucesso (opcional, remova depois de testar)

:: pause