import src.modules.scrap_indec as scri
import src.modules.fred_api as fred
from api_key import apiKey
from glob import glob
import os
import pandas as pd
import plotly.graph_objects as go
import locale
import webbrowser
from src.modules.dics_and_dates import presidencias, eventos_internacionales, eventos_relevantes, sequias, DIC_MESES
locale.setlocale(locale.LC_ALL, 'es_ES')

def capitaliza_serie_historica(serie_historica_bc:pd.DataFrame, serie_cpi_usa:pd.DataFrame):
    df = serie_cpi_usa.merge(serie_historica_bc, how="right",on=["Año","Mes"] )
    ipc_usa = df.pop("ipc_usa")
    df.insert(3, "ipc_usa", ipc_usa)

    def capitalizar_series(df:pd.DataFrame, serie:pd.Series):
        ultimo_mes_base_100 = df["ipc_usa"].iloc[-1] / df["ipc_usa"]
        df[f"{serie}_usd_constantes"] = df[serie]*(ultimo_mes_base_100)
        return df
    df = df\
        .pipe(capitalizar_series, serie="Importaciones")\
        .pipe(capitalizar_series, serie="Exportaciones")\
        .pipe(capitalizar_series, serie="Saldo comercial")
    return df

def get_balanza_comercial(serie_historica_bc:pd.DataFrame,
                          serie_cpi_usa:pd.DataFrame,
                          acumulado:bool
                          ):
    df = capitaliza_serie_historica(serie_historica_bc, serie_cpi_usa)
    ultimo_mes = df.Mes.iloc[-1]
    if acumulado:
        df = df[df["Mes"] <= str(ultimo_mes)]
        df = df.groupby(["Año"], as_index=True).sum(numeric_only=True)
        df = df.drop("ipc_usa",axis=1)
    else:
        df.index = pd.to_datetime(df.Año.astype(str) + "-" + df.Mes.astype(str), format="%Y-%m")
    return df

def plot_agregado_mensual(serie_historica_bc:pd.DataFrame, serie_cpi_usa:pd.DataFrame):
    balanza = get_balanza_comercial(serie_historica_bc, serie_cpi_usa, acumulado=False)
    new_date = [d.strftime('%b-%y').replace(
        ".", "").lower() for d in balanza.index]
    x = new_date
    primer_mes = DIC_MESES[balanza.index[0].month]
    ultimo_mes = balanza.Mes.iloc[-1]
    primer_anio = balanza.index[0].year
    ultimo_anio = balanza.Año.iloc[-1]
    title_text = f"Serie histórica de la balanza comercial. {primer_mes.capitalize()} {primer_anio}-{DIC_MESES[int(ultimo_mes)]} {ultimo_anio}<br><sup>A dólares constantes"
    dtick = False
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=balanza.Exportaciones_usd_constantes / 1_000_000,
        marker = dict(color="rgba(238,178,9,1)"),
        name="Exportaciones",
        hovertemplate="%{y:,.0f} millones de US$",
        line_width=2.5,
    ))

    fig.add_trace(go.Scatter(
        x=x,
        y=balanza.Importaciones_usd_constantes / 1_000_000,
        name="Importaciones",
        hovertemplate="%{y:,.0f} millones de US$",
        line_width=2.5,
        marker = dict(color="rgba(163,133,165,1)"),
    )
    )
    fig.add_trace(go.Bar(
        x=x,
        y=balanza['Saldo comercial_usd_constantes'] /
        1_000_000,
        name="Saldo",
        hovertemplate="%{y:,.0f} millones de US$",
        marker = dict(color="rgba(47, 86, 152,1)")
    )
    )
    for presidencia in presidencias:
        inicio =  pd.to_datetime(presidencia['inicio'])
        fin =  pd.to_datetime(presidencia['fin'])
        inicio_transformado = inicio.strftime('%b-%y').replace(
            ".", "").lower()
        fin_transformado = fin.strftime('%b-%y').replace(
            ".", "").lower()
        nombre = presidencia['nombre']
        fig.add_vline(x=inicio_transformado, line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
        midpoint = (inicio + (fin - inicio) / 2).strftime('%b-%y').replace(
            ".", "").lower()
        fig.add_annotation(x=midpoint, y=8_500, text=str(nombre), showarrow=False)
    for evento in eventos_internacionales:
        fecha = pd.to_datetime(evento['fecha']).strftime('%b-%y').replace(
            ".", "").lower()
        # fig.add_shape(x0=fecha,x1=fecha,y0=0,y1=3_000 ,line_width=1, line_dash="longdashdot", line_color="Black",opacity=1,
        #               )
        fig.add_annotation(x=fecha, y=0, text=str(evento["nombre"]), showarrow=True,textangle=0, font_color="black", opacity = 1,ay=70,ax=0)

    fig.update_layout(
        template="none",
        separators=",.",
        font_family="verdana",
        title_text=title_text,
        hovermode="x unified",
        legend=dict(
            yanchor="top", orientation="h",
            y=-.12,
            xanchor="left",
            x=0.34
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_yaxes(tickformat=",", 
                    dtick=dtick, 
                    title_text="Millones de US$")
    fig.update_xaxes(
        nticks=10,
        # tickangle=-90,
    )
    fig.add_annotation(x=0,xref="paper",yref="paper", y=-.1, text="@martinbasualo0. Fuente: INDEC y FRED", showarrow=False)
    return fig

def plot_agregado_anual(serie_historica_bc:pd.DataFrame, serie_cpi_usa:pd.DataFrame):
    balanza = get_balanza_comercial(serie_historica_bc, serie_cpi_usa, acumulado=True)
    ultimo_mes = get_balanza_comercial(serie_historica_bc, serie_cpi_usa, acumulado=False).Mes.iloc[-1]
    x = balanza.index
    primer_anio = balanza.index[0]
    ultimo_anio = balanza.index[-1]
    title_text = f"Serie histórica de la balanza comercial {primer_anio}-{ultimo_anio}. Acumulado hasta {DIC_MESES[int(ultimo_mes)]}<br><sup>A dólares constantes"
    dtick = False
        
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x,
        y=balanza.Exportaciones_usd_constantes / 1_000_000,
        marker = dict(color="rgba(238,178,9,1)"),
        name="Exportaciones",
        hovertemplate="%{y:,.0f} millones de US$",
        line_width=2.5,
    ))

    fig.add_trace(go.Scatter(
        x=x,
        y=balanza.Importaciones_usd_constantes / 1_000_000,
        name="Importaciones",
        hovertemplate="%{y:,.0f} millones de US$",
        line_width=2.5,
        marker = dict(color="rgba(163,133,165,1)"),
    )
    )
    fig.add_trace(go.Bar(
        x=x,
        y=balanza['Saldo comercial_usd_constantes'] /
        1_000_000,
        name="Saldo",
        hovertemplate="%{y:,.0f} millones de US$",
        marker = dict(color="rgba(47, 86, 152,1)")
    )
    )
    for presidencia in presidencias:
        inicio =  pd.to_datetime(presidencia['inicio']).year
        fin =  pd.to_datetime(presidencia['fin']).year
        nombre = presidencia['nombre']
        fig.add_vline(x=inicio, line_width=1, line_dash="dash", line_color="Black",opacity=0.5)
        midpoint = (inicio + (fin - inicio) / 2)
        fig.add_annotation(x=midpoint,yref="paper", y=0.95, text=str(nombre), showarrow=False)
    for evento in eventos_relevantes:
        fecha = pd.to_datetime(evento['fecha']).year
        fig.add_annotation(x=fecha, y=0, text=str(evento["nombre"]), showarrow=True,textangle=0, font_color="black", opacity = 1,ay=70,ax=0)
     
    fig.update_layout(
        template="none",
        separators=",.",
        font_family="verdana",
        title_text=title_text,
        hovermode="x unified",
        legend=dict(
            yanchor="top", orientation="h",
            y=-.12,
            xanchor="left",
            x=0.34
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_yaxes(tickformat=",", 
                    dtick=dtick, 
                    title_text="Millones de US$")
    fig.update_xaxes(
        nticks=10,
        # tickangle=-90,
    )
    fig.add_annotation(x=0,xref="paper",yref="paper", y=-.1, text="@martinbasualo0. Fuente: INDEC y FRED", showarrow=False)
    return fig


def genera_plots_inflacionados():
    for i in glob("downloads/*", recursive = True): os.remove(i)
    scri.scrap_excels_index_ica_digital()
    serie_historica_bc = pd.read_excel("downloads/plot_agregado.xlsx",dtype={"Año":str, "Mes":str})\
    [["Año","Mes","Importaciones", "Exportaciones","Saldo comercial"]]
    serie_cpi_usa = fred.get_cpi_fred(apiKey)
    plot_agregado_anual(serie_historica_bc, serie_cpi_usa).write_html("output/serie_historica_acumulada_usd_constantes.html")
    plot_agregado_mensual(serie_historica_bc, serie_cpi_usa).write_html("output/serie_historica_mensual_usd_constantes.html")
    get_balanza_comercial(serie_historica_bc, serie_cpi_usa, acumulado=False).to_excel("/output/serie_historica.xlsx")
    output_dir = os.path.abspath("output")
    webbrowser.open(os.path.join(output_dir, "serie_historica_acumulada_usd_constantes.html"), new=2)
    webbrowser.open(os.path.join(output_dir, "serie_historica_mensual_usd_constantes.html"), new=2)

if "__name__" == "__main__":
    genera_plots_inflacionados()  
    