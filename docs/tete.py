import json

# Substitua "caminho/do/arquivo.json" pelo caminho real do seu arquivo JSON
caminho_arquivo_json = "municipios.json"

# Abrir o arquivo JSON e carregar os dados
with open(caminho_arquivo_json, "r", encoding="utf-8") as arquivo_json:
    dados = json.load(arquivo_json)

# Agora, você pode trabalhar com os dados como um dicionário Python
# Por exemplo, você pode usar o código anterior para listar as cidades por UF

# Criar um dicionário para organizar as cidades por UF
cidades_por_uf = {}

for cidade in dados["data"]:
    uf = cidade["Uf"]
    nome_cidade = cidade["Nome"]

    # Adicionar a cidade à lista correspondente à UF
    if uf in cidades_por_uf:
        cidades_por_uf[uf].append(nome_cidade)
    else:
        cidades_por_uf[uf] = [nome_cidade]

# Imprimir as cidades por UF
for uf, cidades in cidades_por_uf.items():
    formato = '", "'.join(cidades)
    saida = f'["{formato}"]'
    print(f"Cidades em {uf}: {saida}")
    print()