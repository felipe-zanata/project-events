import os
import requests
import django


# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE','app.settings')

django.setup()
# Configure Django settings
from eventos.models import Estado  
import json

def obter_estados():
    url_estados = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"
    response = requests.get(url_estados)
    estados = response.json()
    return estados

def obter_cidades_por_estado(uf):
    url_cidades = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
    response = requests.get(url_cidades)
    cidades = response.json()
    return cidades

def gerar_dados_estados_cidades():
    estados = obter_estados()

    for estado in estados:
        uf = estado['sigla']
        nome_estado = estado['nome']

        estado_info = Estado(
            estado=nome_estado,
            sigla=uf,
            cidades=json.dumps([cidade['nome'] for cidade in obter_cidades_por_estado(uf)], ensure_ascii=False)
        )
        estado_info.save()

def main():
    gerar_dados_estados_cidades()

if __name__ == "__main__":
    main()
