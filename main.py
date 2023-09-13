import pandas as pd
import numpy as np

# Leitura dos arquivos CSV
escolas_df = pd.read_csv('escolas.csv', encoding='utf-8')
subprefeituras_df = pd.read_csv('subprefeituras.csv', encoding='utf-8')
material_didatico_df = pd.read_csv('material_didatico.csv', encoding='utf-8')

# Função para padronizar o nome do logradouro
def padronizar_logradouro(logradouro):
    logradouro = logradouro.upper()
    logradouro = logradouro.replace("R.", "RUA").replace("AV.", "AVENIDA")
    return logradouro

# Função para arredondar latitude e longitude para 5 casas decimais
def arredondar_lat_long(valor):
    return round(valor, 5)

# Aplicar padronização nos dataframes
escolas_df['nome_da_escola'] = escolas_df['nome_da_escola'].str.upper()
escolas_df['logradouro'] = escolas_df['logradouro'].apply(padronizar_logradouro)
escolas_df['bairro'] = escolas_df['bairro'].str.upper()

# Juntar os dataframes
escolas_material_df = escolas_df.merge(material_didatico_df, on='id_escola', how='inner')
escolas_material_subprefeitura_df = escolas_material_df.merge(subprefeituras_df, on='bairro', how='left')

# Arredondar latitude e longitude
escolas_material_subprefeitura_df['latitude'] = escolas_material_subprefeitura_df['latitude'].apply(arredondar_lat_long)
escolas_material_subprefeitura_df['longitude'] = escolas_material_subprefeitura_df['longitude'].apply(arredondar_lat_long)

# Renomear colunas para snake_case
escolas_material_subprefeitura_df = escolas_material_subprefeitura_df.rename(columns={
    'nome_da_escola': 'nome_da_escola',
    'id_escola': 'id_da_escola',
    'endereco': 'endereco',
    'bairro': 'bairro',
    'cep': 'cep',
    'telefone': 'telefone',
    'latitude': 'latitude',
    'longitude': 'longitude',
    'material_didatico': 'material_didatico',
    'quantidade': 'quantidade_de_material_didatico',
    'subprefeitura': 'subprefeitura'
})

# Ordenar pelo ID da escola
escolas_material_subprefeitura_df = escolas_material_subprefeitura_df.sort_values(by='id da escola')

# Salvar resultado em um arquivo CSV
escolas_material_subprefeitura_df.to_csv('escolas_material_didatico.csv', index=False, encoding='utf-8')

# Calcular quantidade total de material por subprefeitura
total_material_por_subprefeitura = escolas_material_subprefeitura_df.groupby('subprefeitura')['quantidade de material didatico'].sum().reset_index()

# Salvar resultado em um arquivo CSV
total_material_por_subprefeitura.to_csv('total_material_por_subprefeitura.csv', index=False, encoding='utf-8')
