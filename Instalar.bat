@echo off
setlocal

rem Configurações
set VENV_NAME=venv
set REQUIREMENTS_FILE=requirements.txt

rem Criação da Virtual Environment
python -m venv %VENV_NAME%

rem Ativação da Virtual Environment
call %VENV_NAME%\Scripts\activate

rem Instalação dos requisitos
pip install -r %REQUIREMENTS_FILE%

rem Desativação da Virtual Environment
deactivate

endlocal
