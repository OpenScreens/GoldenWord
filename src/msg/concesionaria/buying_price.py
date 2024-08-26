import pandas as pd
from rapidfuzz import process, fuzz

df = pd.read_csv('dnrpa.csv', delimiter=';')

def get_price(marca_input, modelo_input, año_input):
    marca = process.extractOne(marca_input, df['Desc. marca'], scorer=fuzz.token_sort_ratio)[0]
    print(f"Brand found: {marca}")
    
    modelos_marca = df[df['Desc. marca'] == marca]['Desc. Modelo'].unique()
    modelo = process.extractOne(modelo_input, modelos_marca, scorer=fuzz.token_sort_ratio)[0]
    print(f"model found: {modelo}")
    
    año_str = str(año_input)

    resultado = df[(df['Desc. marca'] == marca) & (df['Desc. Modelo'] == modelo)]
    
    if not resultado.empty:
        if año_str in resultado.columns:
            precio = resultado[año_str].values[0]
            if pd.notna(precio):
                return marca, modelo, float(precio) 
            else:
                return 'There is no price available for that year.'
    else:
        return 'There is no vehicle specified.'

'''
prompt = 'i want a volkswagen gol 2004, what is the price?'
marca, modelo, año = "volkswagen", "gol", "2004"
precio = get_price(marca.upper(), modelo.upper(), int(año))
print(f"El precio para un {marca.capitalize()} {modelo.capitalize()} del año {año} es: {precio}")
'''