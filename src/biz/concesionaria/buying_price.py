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
    
    valid_years = [col for col in resultado.columns if col.isdigit() and pd.notna(resultado[col].values[0])]

    if valid_years:
        if año_str in valid_years:
            precio = resultado[año_str].values[0]
            return marca, modelo, float(precio), año_str, "exact"
        else:
            near_year = min(valid_years, key=lambda x: abs(int(x) - int(año_str)))
            precio = resultado[near_year].values[0]
            return marca, modelo, float(precio), near_year, "approximate"
        
    return marca, modelo, -1, None, "no_price"

'''
marca, modelo, año = "honda", "civic", "2008"
precio = get_price(marca.upper(), modelo.upper(), int(año))
print(f"El precio para un {marca.capitalize()} {modelo.capitalize()} del año {año} es: {precio}")
'''