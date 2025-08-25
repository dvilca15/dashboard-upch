# data_processing.py
"""
Módulo para procesamiento de datos del dashboard UPCH
"""
import re
import pandas as pd
from config import UPCH, EXCEL_FILE, SHEET_NAME, CARRERAS_FILTRAR, UNIVERSIDADES_FILTRO, CARRERAS_MAPPING


def leer_excel():
    """Lee el archivo Excel con los datos"""
    return pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)


def limpiar_carrera(x):
    """Función para limpiar nombres de carreras"""
    if pd.isna(x):
        return None
    s = str(x).upper().strip()
    s = (s.replace("Á","A").replace("É","E").replace("Í","I")
           .replace("Ó","O").replace("Ú","U").replace("Ü","U")
           .replace("Ñ","N"))
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^A-Z0-9\s]", "", s)
    return s


def calcular_contadores(df):
    """Calcula los contadores principales para UPCH"""
    # Contadores 2M (Segundo Momento)
    df_filtrado_2m = df[df["IES 2M"] == UPCH]
    condicion_count_2m = (df_filtrado_2m["CONDICIÓN FINAL 2M"] == "SELECCIONADO").sum()
    becario_count_2m = df_filtrado_2m["BECARIO 2M"].isin(["BECARIO", "ACEPTO"]).sum()

    # Contadores 1M (Primer Momento)
    df_filtrado_1m = df[df["IES 1M"] == UPCH]
    condicion_count_1m = (df_filtrado_1m["CONDICIÓN FINAL 1M"] == "SELECCIONADO").sum()
    becario_count_1m = df_filtrado_1m["BECARIO 1M"].isin(["BECARIO", "ACEPTO"]).sum()

    # Métricas totales
    total_becarios = becario_count_1m + becario_count_2m
    crecimiento_becarios = ((becario_count_2m - becario_count_1m) / becario_count_1m) * 100 if becario_count_1m > 0 else 0

    return {
        'condicion_count_1m': condicion_count_1m,
        'condicion_count_2m': condicion_count_2m,
        'becario_count_1m': becario_count_1m,
        'becario_count_2m': becario_count_2m,
        'total_becarios': total_becarios,
        'crecimiento_becarios': crecimiento_becarios
    }


def procesar_datos_carreras(df):
    """Procesa los datos de carreras para becarios UPCH"""
    # Datos 1M
    df_1m_carr = df[
        (df["IES 1M"] == UPCH) &
        (df["BECARIO 1M"].isin(["BECARIO", "ACEPTO"]))
    ][["CARRERA ELEGIDA 1M"]].rename(columns={"CARRERA ELEGIDA 1M":"CARRERA"})

    # Datos 2M
    df_2m_carr = df[
        (df["IES 2M"] == UPCH) &
        (df["BECARIO 2M"].isin(["BECARIO", "ACEPTO"]))
    ][["CARRERA ELEGIDA 2M"]].rename(columns={"CARRERA ELEGIDA 2M":"CARRERA"})

    # Combinar datos
    df_carreras = pd.concat([df_1m_carr, df_2m_carr], ignore_index=True)
    df_carreras["CARRERA"] = df_carreras["CARRERA"].apply(limpiar_carrera)
    df_carreras = df_carreras.dropna(subset=["CARRERA"])
    
    # Filtrar carreras específicas
    df_carreras = df_carreras[df_carreras["CARRERA"].isin(CARRERAS_FILTRAR)]

    # Contar y procesar
    df_carreras_count = (
        df_carreras.groupby("CARRERA")
        .size()
        .reset_index(name="TOTAL")
    )

    # Aplicar mapeo de nombres largos
    df_carreras_count["CARRERA"] = df_carreras_count["CARRERA"].replace(CARRERAS_MAPPING)
    df_carreras_count = df_carreras_count.sort_values("TOTAL", ascending=True)

    return df_carreras_count


def procesar_datos_modalidad(df):
    """Procesa los datos de modalidad para becarios UPCH"""
    df_modalidad = pd.concat([
        df[(df["IES 1M"] == UPCH) & (df["BECARIO 1M"].isin(["BECARIO", "ACEPTO"]))][["MODALIDAD"]],
        df[(df["IES 2M"] == UPCH) & (df["BECARIO 2M"].isin(["BECARIO", "ACEPTO"]))][["MODALIDAD"]]
    ])

    df_modalidad_count = (
        df_modalidad.groupby("MODALIDAD")
        .size()
        .reset_index(name="TOTAL")
    )
    df_modalidad_count["PORCENTAJE"] = (df_modalidad_count["TOTAL"] / df_modalidad_count["TOTAL"].sum()) * 100
    df_modalidad_count["PORCENTAJE"] = df_modalidad_count["PORCENTAJE"].round(2).astype(str) + "%"
    df_modalidad_count = df_modalidad_count.sort_values("TOTAL", ascending=False)

    return df_modalidad_count


def procesar_datos_universidades(df):
    """Procesa los datos de universidades para comparación"""
    # Datos 1M
    df_uni_1m = df[(df["BECARIO 1M"].isin(["BECARIO", "ACEPTO"])) & 
                   (df["IES 1M"].isin(UNIVERSIDADES_FILTRO))][["IES 1M"]].rename(columns={"IES 1M": "UNIVERSIDAD"})
    
    # Datos 2M
    df_uni_2m = df[(df["BECARIO 2M"].isin(["BECARIO", "ACEPTO"])) & 
                   (df["IES 2M"].isin(UNIVERSIDADES_FILTRO))][["IES 2M"]].rename(columns={"IES 2M": "UNIVERSIDAD"})

    # Contar por momento
    conteo_1m = df_uni_1m.value_counts().reset_index(name="PRIMER MOMENTO")
    conteo_2m = df_uni_2m.value_counts().reset_index(name="SEGUNDO MOMENTO")

    # Combinar y procesar
    df_universidades = pd.merge(conteo_1m, conteo_2m, on="UNIVERSIDAD", how="outer").fillna(0)
    df_universidades = df_universidades.astype({"PRIMER MOMENTO": int, "SEGUNDO MOMENTO": int})
    df_universidades = df_universidades.set_index("UNIVERSIDAD").loc[UNIVERSIDADES_FILTRO].reset_index()

    # Ordenar por total
    df_universidades["TOTAL_BECARIOS"] = df_universidades["PRIMER MOMENTO"] + df_universidades["SEGUNDO MOMENTO"]
    df_universidades = df_universidades.sort_values("TOTAL_BECARIOS", ascending=True)

    return df_universidades