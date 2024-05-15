@echo off
setlocal

rem Ative o ambiente virtual
call venv\Scripts\activate

rem Execute o comando para iniciar o servidor Django minimizado
start /MIN /B python manage.py runserver

rem Aguarde um curto período de tempo para o servidor iniciar
timeout /nobreak /t 5 >nul

rem Abrir a guia web no navegador padrão
start http://127.0.0.1:8000/

endlocal
