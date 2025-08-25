# app.py
"""
Aplicación principal del Dashboard UPCH 2025
"""
import os
import sys
from dash import Dash
import dash_bootstrap_components as dbc

# Agregar el directorio actual al path de Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Importar módulos
    from data_processing import (
        leer_excel, 
        calcular_contadores, 
        procesar_datos_carreras,
        procesar_datos_modalidad,
        procesar_datos_universidades
    )
    from charts import (
        crear_grafico_comparativo,
        crear_grafico_carreras, 
        crear_grafico_universidades
    )
    from components import crear_tabla_modalidad
    from layout import crear_layout
    from styles import CUSTOM_CSS
except ImportError as e:
    print(f"Error al importar módulos: {e}")
    print("Asegúrate de que todos los archivos estén en el mismo directorio")
    sys.exit(1)


def crear_app():
    """Crea y configura la aplicación Dash"""
    app = Dash(__name__, external_stylesheets=[
        dbc.themes.CYBORG,
        "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap"
    ])
    
    # Inyectar CSS personalizado
    app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
''' + CUSTOM_CSS + '''
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
    
    return app


def main():
    """Función principal para ejecutar el dashboard"""
    # Leer y procesar datos
    df = leer_excel()
    
    # Calcular contadores principales
    contadores = calcular_contadores(df)
    
    # Procesar datos específicos
    df_carreras_count = procesar_datos_carreras(df)
    df_modalidad_count = procesar_datos_modalidad(df)
    df_universidades = procesar_datos_universidades(df)
    
    # Crear gráficos
    grafico_comparativo = crear_grafico_comparativo(contadores)
    grafico_carreras = crear_grafico_carreras(df_carreras_count)
    grafico_universidades = crear_grafico_universidades(df_universidades)
    
    # Crear componentes
    tabla_modalidad = crear_tabla_modalidad(df_modalidad_count)
    
    # Crear aplicación
    app = crear_app()
    
    # Configurar layout
    app.layout = crear_layout(
        contadores,
        grafico_comparativo,
        grafico_carreras,
        tabla_modalidad,
        grafico_universidades
    )
    
    return app


if __name__ == "__main__":
    app = main()
    port = int(os.environ.get("PORT", 8050))  # Render asigna el puerto
    app.run(host="0.0.0.0", port=port, debug=False)

app = main()
server = app.server