#LIBRARIES
import pandas as pd
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import dash
import folium

# IMPORT DATA
#Air Quality Data
df_NO2 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_NO2_dataGroup1.parquet")
df_O3 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_O3_dataGroup1.parquet")
df_SO2 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_SO2_dataGroup1.parquet")
df_CO = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_CO_dataGroup1.parquet")
df_PM2_5 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_PM2_dataGroup1.parquet")
df_PM10 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_PM1_dataGroup1.parquet")
data_frames = [df_NO2, df_O3, df_CO, df_SO2, df_PM2_5, df_PM10]
pollutants = ["NO2", "O3", "CO", "SO2", "PM 2.5", "PM 10"]

# FUNKTIONEN
def create_radar_chart_for_day(data_frames, pollutants, day):

    data = []

    for df, pollutant in zip(data_frames, pollutants):
        df_day = df[df["Start"] == day]
        if not df_day.empty:
            values = df_day["Value"]
            data.append({"Schadstoff": pollutant, "Wert": values.item()})
    values = [entry["Wert"] for entry in data]
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[25, 100, 4, 40, 15, 45],
        theta=pollutants,
        fill='toself',
        name='WHO Limits'
    ))

    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=[entry["Schadstoff"] for entry in data],  # Extrahiere alle Schadstoffnamen in eine separate Liste
        fill='toself',
        name='Current Status'
    ))

    fig.update_layout(
        title=f'POLLUTANTS for {day}',
        legend=dict(
            x=0.5,  # x-Position in der Mitte
            y=-0.1,  # y-Position unterhalb des Diagramms
            xanchor='center',  # Zentriert die Legende basierend auf der x-Position
            yanchor='top',  # Verankert die Legende oben basierend auf der y-Position
            orientation='h'  # Setzt die Orientierung der Legende auf horizontal
        )
    )

    return fig


def create_map(df_PM10, date, location=(52.520008, 13.404954), zoom_start=5):
    map_object = folium.Map(location=location, zoom_start=zoom_start)

    # Filtern des DataFrames basierend auf dem Datum
    df_day = df_PM10[df_PM10['Start'] == date]

    for index, row in df_day.iterrows():
        # Extrahieren der PM10-Werte
        pm10_value = row['Value']
        marker_location = location

        # Markierungsobjekte mit folium.Marker() erzeugen
        marker_objects = folium.Marker(location=marker_location,
                                       popup=f'PM10: {pm10_value}')

        # Markierungen der Karte hinzufügen
        marker_objects.add_to(map_object)

    return map_object


def create_area_chart(data_frames, pollutants):
    fig = px.area()

    for df, pollutant in zip(data_frames, pollutants):
        fig.add_trace(go.Scatter(x=df['Start'], y=df['Value'], fill='tozeroy', mode='lines', name=pollutant))

    fig.update_layout(
        title="Area Chart für verschiedene Schadstoffe",
        xaxis_title="Datum",
        yaxis_title="Wert",
    )

    return fig


# START APP
#-------------------------------------------------------------------
app = Dash(__name__, external_stylesheets=[dbc.themes.QUARTZ])

# LAYOUT SECTION: BOOTSTRAP
#--------------------------------------------------------------------
app.layout = html.Div([
    dcc.Loading(
        id='loading',
        type='cube',
        color="#cc6bcc",
        children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.H3('Air Quality', className='text-left d-flex align-items-center',
                        style={'font-family': 'Source Sans Pro', 'font-size': '38px', 'font-weight': 'bold', 'color': '#FFFFFF'}),
                        width={'size': 5},
                        className='mt-1 d-flex align-items-end',),
                    dbc.Col(html.H3('A daily index developed to represent air quality', className='text-left d-flex align-items-center',
                        style={'font-family': 'Source Sans Pro', 'font-size': '26px', 'color': '#FFFFFF',  'margin-bottom':'13px'}),
                        width={'size': 7}),],
                    className='mt-1 d-flex align-items-end',
                    style={'background-image': 'linear-gradient(to right, #8CD0F1, #cc6bcc)', 'height': '60px', 'border-radius': '2px'}),

                html.Div(style={'height': '7px'}),

                dbc.Row([
                    dbc.Col([html.Div([
                        dcc.Input(
                            id='search-input',
                            type='text',
                            placeholder='Enter a City',
                            style={'marginRight': '10px', 'font-family': 'Source Sans Pro', 'border-radius': '13px'},
                                 ),
                        html.Button(
                    '🔍',  # Suchsymbol
                            id='search-button',
                            style={
                                'backgroundColor': 'white',
                                'border': 'none', 'borderRadius': '13px'}
                ),
                    ]),
                    ], width={'size': 6},),
                    dbc.Col(html.Div("One of three columns")),
                    dbc.Col(html.Div("One of three columns")),
                ],
                    className = 'g-0',
                    style = {'background-color': "black", 'alignItems': 'center', 'height': '50px', 'border-radius': '2px'}),

                html.Div(style={'height': '10px'}),

                dbc.Row([
                    dbc.Col([
                        dbc.Row([dcc.Graph(id="half_donut")],
                                        style={'height': '250px', 'margin-top': '0px','border-radius': '10px', 'backround-color':'white',
                                        'boxShadow': '2px 2px 2px rgba(255, 255, 255, 0.50)'}),

                    html.Div(style={'height': '10px'}),

                        dbc.Row([
                        html.Div([
                            dcc.DatePickerSingle(
                                id='calender',
                                date='2021-08-14',
                                display_format='DD MMM YYYY',
                                style={
                                    'backgroundColor': '#f03592',}
                            ),
                            html.Div(id='output-container')
                        ]),], style={'height': '250px', 'margin-top': '0px','border-radius': '10px', 'backround-color':'white',
                                        'boxShadow': '2px 2px 2px rgba(255, 255, 255, 0.50)'}
                        ),

                    html.Div(style={'height': '10px'}),

                        dbc.Row([
                            dcc.Graph(id="Helth_advice")],
                                style={'height': '210px', 'margin-top': '0px','border-radius': '10px', 'backround-color':'white',
                                       'boxShadow': '2px 2px 2px rgba(255, 255, 255, 0.50)'}),
                    ], width=2,),

                    dbc.Col([
                        dbc.Row([dcc.Graph(id="PCP")],
                                style={'height': '400px', 'margin-top': '0px','border-radius': '10px', 'backround-color':'white',
                                       'boxShadow': '2px 2px 2px rgba(255, 255, 255, 0.50)'}),

                    html.Div(style={'height': '10px'}),

                        dbc.Row([
                            dcc.Dropdown(
                                id='pollutant-dropdown',
                                options=[{'label': pollutant, 'value': pollutant} for pollutant in pollutants],
                                value=pollutants[0]
                            ),
                            dcc.Graph(id='area-chart')],
                                style={'height': '300px', 'margin-top': '0px','border-radius': '10px', 'backround-color':'white',
                                       'boxShadow': '2px 2px 2px rgba(255, 255, 255, 0.50)'}),],
                         width=6, ),

                    dbc.Col([
                        dbc.Row([
                            dcc.Graph(id="radar_chart")],
                                style={'height': '360px', 'margin-top': '0px', 'border-radius': '10px', 'backround-color':'transparent',
                                       'boxShadow': '2px 2px 2px rgba(255, 255, 255, 0.50)'}),

                    html.Div(style={'height': '20 px'}),

                        dbc.Row([
                            html.Iframe(id='map', height='350px', width="120%", style={'backround-color':'white', 'border-radius': '10px',
                                                                                      'boxShadow': '2px 2px 2px rgba(255, 255, 255, 0.50)'})
                ])
            ], width='4')
       ])
    ])
])])
# CALLBACK FUNCTION
#--------------------------------------------------------------------
@app.callback(
    Output('radar_chart', 'figure'),
    [Input('calender', 'date')]
)
def update_radar_chart(selected_day):
    return create_radar_chart_for_day(data_frames, pollutants, selected_day)

@app.callback(
    Output('map', 'srcDoc'),
    [Input('calender', 'date')]
)
def update_map(selected_day):
    map_object = create_map(df_PM10, selected_day)
    return map_object._repr_html_()

@app.callback(
    Output('output-container', 'children'),
    [Input('calender', 'date')]
)
def update_output(selected_date):
    if selected_date is not None:
        return f'Sie haben das folgende Datum ausgewählt: {selected_date}'


@app.callback(
    Output('area-chart', 'figure'),
    [Input('pollutant-dropdown', 'value')]
)
def update_chart(selected_pollutant):
    index = pollutants.index(selected_pollutant)
    df = data_frames[index]
    fig = create_area_chart([df], [selected_pollutant])
    return fig
# RUN THE APP
#--------------------------------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=8020)
