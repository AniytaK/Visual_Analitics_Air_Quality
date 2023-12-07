#LIBRARIES
import pandas as pd
from dash import Dash, dcc, html, State
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly import colors
import folium
#_______________________________________________________________________________________________________________________

#DATA
#Air Quality Data per Hour
df_NO2 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_NO2_dataGroup1.parquet")
df_O3 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_O3_dataGroup1.parquet")
df_SO2 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_SO2_dataGroup1.parquet")
df_CO = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_CO_dataGroup1.parquet")
df_PM2_5 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_PM2_dataGroup1.parquet")
df_PM10 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_PM1_dataGroup1.parquet")
data_frames = [df_NO2, df_O3, df_CO, df_SO2, df_PM2_5, df_PM10]
pollutants = ["NO2", "O3", "CO", "SO2", "PM 2.5", "PM 10"]

#Air Quality Data per Day
from AQ_Data import lade_aver_NO2
daily_averages_NO2 = lade_aver_NO2()

from AQ_Data import lade_aver_O3
daily_averages_O3 = lade_aver_O3()

from AQ_Data import lade_aver_SO2
daily_averages_SO2 = lade_aver_SO2()

from AQ_Data import lade_aver_CO
daily_averages_CO = lade_aver_CO()

from AQ_Data import lade_aver_PM2_5
daily_averages_PM2_5 = lade_aver_PM2_5()

from AQ_Data import lade_aver_PM10
daily_averages_PM10 = lade_aver_PM10()
data_frames_day = [daily_averages_NO2, daily_averages_O3, daily_averages_CO, daily_averages_SO2, daily_averages_PM2_5, daily_averages_PM10]

#Air Quality Data per Month
from AQ_Data import lade_aver_month_NO2
monthly_averages_NO2 = lade_aver_month_NO2()

from AQ_Data import lade_aver_month_O3
monthly_averages_O3 = lade_aver_month_O3()

from AQ_Data import lade_aver_month_SO2
monthly_averages_SO2 = lade_aver_month_SO2()

from AQ_Data import lade_aver_month_CO
monthly_averages_CO = lade_aver_month_CO()

from AQ_Data import lade_aver_month_PM2_5
monthly_averages_PM2_5 = lade_aver_month_PM2_5()

from AQ_Data import lade_aver_month_PM10
monthly_averages_PM10 = lade_aver_month_PM10()
data_frames_month = [monthly_averages_NO2, monthly_averages_O3, monthly_averages_CO, monthly_averages_SO2, monthly_averages_PM2_5, monthly_averages_PM10]

from AQ_Data import lade_data_for_pcp
df_final = lade_data_for_pcp()

from AQ_Data import lade_data_for_AQI
daily_AQI = lade_data_for_AQI()
#_______________________________________________________________________________________________________________________

# FUNKTIONEN
#Radar Chart to compare Pollutants Values per Day with WHO-Limits
def create_radar_chart_for_day(data_frames_day, pollutants, day, who_limits=None):
    # Standard WHO-Limits
    if not who_limits:
        who_limits = [25, 100, 4, 40, 15, 45]

    # Data
    values = []
    for df, pollutant in zip(data_frames_day, pollutants):
        df_day = df[df["Start"] == day]
        if not df_day.empty:
            values.append(df_day["Value"].item())
        else:
            values.append(0)

    fig = go.Figure()
    #WHO-Limits
    fig.add_trace(go.Scatterpolar(
        r=who_limits,
        theta=pollutants,
        fill='toself',
        fillcolor='rgba(140, 208, 241, 0.5)',
        name='WHO Limits',
        #fillcolor="#98F5FF"
    ))

    # Current Values
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=pollutants,
        fill='toself',
        name='Current Value',
        fillcolor="rgba(204, 107, 204, 0.5)"
    ))

    # Layout
    fig.update_layout(title=f'Pollutants for {day}',
        polar=dict(
            radialaxis=dict(
                visible=True,
                gridcolor="white",
                gridwidth=2,
                range=[0, max(who_limits + values)]
            ),
            angularaxis = dict(
                gridcolor='white'),
        ),
        legend=dict(
            x=0.5,
            y=-0.1,
            xanchor='center',
            yanchor='middle',
            orientation='h'
        ))

    return fig
#________________________________________________________________________________________________________________________

#Map
def create_map(daily_averages_PM10, date, location=(52.520008, 13.404954), zoom_start=5):
    map_object = folium.Map(location=location, zoom_start=zoom_start)

    df_day = daily_averages_PM10[daily_averages_PM10['Start'] == date]

    for index, row in df_day.iterrows():
        # Extrahieren der PM10-Werte
        pm10_value = row['Value']
        marker_location = location
        marker_objects = folium.Marker(location=marker_location,
                                       icon=folium.Icon(color="green",
                                                        icon="cloud"),
                                       popup=f'PM10: {pm10_value}')

        marker_objects.add_to(map_object)

    return map_object
#_______________________________________________________________________________________________________________________

#Area Chart to show historical data
def create_area_chart(data_frames_month, pollutants):
    fig = px.area()

    # for df, pollutant in zip(data_frames_month, pollutants):
    #     fig.add_trace(go.Scatter(x=df['Start'], y=df['Value'], fill='tozeroy', mode='lines', name=pollutant))

    palette = colors.sequential.Purpor_r
    for i, (df, pollutant) in enumerate(zip(data_frames_month, pollutants)):
        color = palette[i % len(palette)]
        fig.add_trace(go.Scatter(
            x=df['Start'],
            y=df['Value'],
            fill='tozeroy',
            mode='lines',
            name=pollutant,
            line=dict(color=color)
        ))

    fig.update_layout(
        title="Pollutants Historical Data",
        xaxis_title="Date",
        yaxis_title="Value",
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(showgrid=True, gridcolor='#cccfcd', gridwidth=0.5, griddash='dot')
    )

    return fig
#_______________________________________________________________________________________________________________________

#Gauge Chart
def get_air_quality_text(value):
    if value <= 50:
        return "Good"
    elif value <= 100:
        return "Moderate"
    elif value <= 150:
        return "Unhealthy for Sensitive Groups"
    elif value <= 200:
        return "Unhealthy"
    elif value <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"

def get_daily_AQI_value(daily_AQI, selected_date):
    date_filter = daily_AQI['Date'] == pd.to_datetime(selected_date)
    if not date_filter.any():
        return None
    return daily_AQI.loc[date_filter, 'AQI'].iloc[0]

# Aktualisierte Funktion zur Erstellung des Gauge-Charts
def update_gauge_chart(daily_AQI, selected_date):
    value = get_daily_AQI_value(daily_AQI, selected_date)
    if value is None:
        return None  # Darstellung für fehlende Daten

    air_quality_text = get_air_quality_text(value)

    # Konfiguration für das Gauge-Chart
    gauge_config = {
        'axis': {'range': [None, 500], 'tickwidth': 0.5, 'tickcolor': "black"},
        'bar': {'color': "black", 'thickness': 0.8},  # This color will be overridden by the steps
        'bgcolor': "black",
        'borderwidth': 2,
        'bordercolor': "black",
        'steps': [
            {'range': [0, 50], 'color': '#8CD0F1'},
            {'range': [50, 100], 'color': '#99BCEA'},
            {'range': [100, 150], 'color': '#A6A8E2'},
            {'range': [150, 200], 'color': '#B293DB'},
            {'range': [200, 300], 'color': '#BF7FD3'},
            {'range': [300, 500], 'color': '#CC6BCC'}
        ],
    }

    # Erstellung des Gauge-Charts
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "AQI", 'font': {'size': 30, 'color': "black"}},
        gauge=gauge_config,
        number={'font': {'size': 30, 'color': "black"}}
    ))

    fig.update_layout(
        annotations=[
            go.layout.Annotation(
                x=0.5,
                y=0,
                xref="paper",
                yref="paper",
                text=air_quality_text,
                showarrow=False,
                font=dict(size=15, color="black")
            )
        ],
        autosize=False,
        width=350,  # Breite des Charts in Pixel
        height=260,  # Höhe des Charts in Pixel
        margin=dict(l=10, r=10, b=100, t=60, pad=6)
    )

    return fig
#_______________________________________________________________________________________________________________________

#PCP
fixed_columns = ['Jahr', 'Monat']
selectable_columns = ['NO2', 'O3', 'CO', 'SO2', 'PM 2.5', 'PM 10', 'tavg', 'wspd']
def create_parallel_coordinates_plot(df, selected_columns):
    seasonal_color_scale = [
    (0.00, "purple"), (1/12, "purple"), (2/12, "lightseagreen"), (3/12, "lightseagreen"), (4/12, "lightseagreen"), (5/12, "lightseagreen"), (6/12, "red"),
    (7/12, "red"), (8/12, "red"), (9/12, "orange"), (10/12, "orange"), (11/12, "orange"), (1.00, "purple")
    ]
    fig = px.parallel_coordinates(df_final,
                                  color='Monat',
                                  dimensions=fixed_columns + selected_columns,
                                  labels={column: column for column in df_final.columns},
                                  color_continuous_scale=seasonal_color_scale)
    return fig
#_______________________________________________________________________________________________________________________

# START APP

app = Dash(__name__, external_stylesheets=[dbc.themes.MORPH])

# LAYOUT SECTION: BOOTSTRAP
#-----------------------------------------------------------------------------------------------------------------------
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
                            style={'marginRight': '10px', "height": "50px", 'font-family': 'Source Sans Pro', 'border-radius': '13px'},
                                 ),
                        html.Button(
                            '🔍',  # Suchsymbol
                            id='search-button',
                            style={"height": "40px",
                                'backgroundColor': 'white',
                                'border': 'none', 'borderRadius': '10px'}
                ),
                    ]),
                    ], width={'size': 6},),
                    dbc.Col(html.Div([
                                dcc.DatePickerSingle(
                                    id='calender',
                                    date='2022-12-15',
                                    display_format='DD MMM YYYY',
                                    style={'marginLeft': '10px', 'backgroundColor': 'white', 'width': '100%', "height": "40px", 'margin-right': '5px',}
                                ),
                                html.Div(id='output-container', style={'width': '80%'})
                            ], style={
                                'display': 'flex',
                                'flex-direction': 'row',
                                'justify-content': 'space-around',
                                'align-items': 'center',
                                'padding': '10px',
                                'border-radius': '13px',
                                'background-color': 'white',
                                "height": "50px",
                                }
                    ),),
                    dbc.Col(html.Div([
                            html.Button(
                                '📧',
                                id='mail-button',
                                style={"height": "40px", 'backgroundColor': 'white','border': 'none', 'borderRadius': '10px'})
                        ])),
                ],
                    #className = 'g-0',
                    style = {'background-color': "black", 'alignItems': 'center', 'height': '70px', 'border-radius': '2px'}),

                html.Div(style={'height': '10px'}),
########################################################################################################################
                dbc.Row([
                    dbc.Col([
                        dbc.Row([dcc.Graph(id="half_donut")],
                                              style={'height': '260px', 'margin-top': '0px', 'margin-bottom': '0px',
                                                     'margin-right': '3px', 'border-radius': '13px', 'background-color':'white',
                                                     'boxShadow': '2px 2px 2px rgba(0, 0, 0, 0.25)', 'font-family': 'Source Sans Pro'},
                        ),
                html.Div(style={'height': '10px'}),
                        dbc.Row([
                            html.Iframe(id='map',
                                        height='270px',
                                        width="110%",
                                        style={'background-color':'white', 'border-radius': '13px','margin-right': '4px',
                                                'boxShadow': '2px 2px 2px rgba(0, 0, 0, 0.25)'}),
                        ]),
                    ], width=4),
                    dbc.Col([
                        dcc.Dropdown(
                                    id='select-columns',
                                    options=[{'label': col, 'value': col} for col in selectable_columns],
                                    value=selectable_columns[:6],
                                    multi=True,
                                    style={'width': '100%', 'margin-left': 'auto', 'margin-right': 'auto', }
                                ),
                        dcc.Graph(
                                id="PCP",
                                style={'height': '500px', 'margin-top': '0px', 'border-radius': '13px', 'background-color':'white',
                                       'boxShadow': '2px 2px 2px rgba(0, 0, 0, 0.25)'}),
                    ]),
                ]),
                html.Div(style={'height': '10px'}),
########################################################################################################################
                dbc.Row([
                    dbc.Col([
                        dbc.Row([
                                dcc.Graph(id="radar_chart")],
                                    style={'height': '350px', 'margin-top': '0px', 'margin-right': '3px',
                                           'border-radius': '13px', 'background-color':'white',
                                           'boxShadow': '2px 2px 2px rgba(0, 0, 0, 0.25)',
                                           'font-family': 'Source Sans Pro', 'font-size': '12px',}),
                    ], width=4),
                    dbc.Col([
                        dbc.Row([dcc.Graph(id='area-chart')],
                                              style={'height': '350px', 'margin-top': '0px','border-radius': '13px',
                                                     'background-color':'white', 'boxShadow': '2px 2px 2px rgba(0, 0, 0, 0.25)',
                                                     'font-family': 'Source Sans Pro', 'font-size': '12px',}
                        ),
                    ]),
                ]),
            ]),
        ]),
    ])


# CALLBACK FUNCTION
#-----------------------------------------------------------------------------------------------------------------------
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
        return selected_date


@app.callback(
    Output('area-chart', 'figure'),
    [Input('area-chart', 'clickData'),
     State('area-chart', 'figure')]
)
def toggle_trace(clickData, figure):
    if clickData:
        # Name des Schadstoffs, der in der Legende geklickt wurde
        pollutant_name = clickData['points'][0]['curveNumber']
        # Referenz auf die aktuelle Figur, die angezeigt wird
        fig = go.Figure(figure)
        # Iteriere durch die Daten (Traces) in der Figur und toggle die Sichtbarkeit
        for i, trace in enumerate(fig.data):
            # Wenn der Index des Schadstoffs mit dem geklickten Namen übereinstimmt
            if i == pollutant_name:
                # Toggle zwischen sichtbar und unsichtbar
                fig.data[i].visible = not fig.data[i].visible
    else:
        # Wenn kein Schadstoff geklickt wurde, zeige die Standardansicht
        fig = create_area_chart(data_frames_month, pollutants)

    return fig


@app.callback(
    Output('half_donut', 'figure'),
    [Input('calender', 'date')]
)
def show_gauge_chart(selected_date):
    if not selected_date:
        selected_date = daily_AQI['Date'].dt.strftime('%Y-%m-%d').max()

    gauge_chart = update_gauge_chart(daily_AQI, selected_date)
    if gauge_chart is not None:
        return gauge_chart
    else:
        # Alternativ kann hier ein Platzhalter-Chart oder eine Meldung zurückgegeben werden
        return go.Figure()

@app.callback(
    Output('PCP', 'figure'),
    [Input('select-columns', 'value')]
)
def update_plot(selected_columns):
    fig = create_parallel_coordinates_plot(df_final, selected_columns)
    return fig


# RUN THE APP
#-----------------------------------------------------------------------------------------------------------------------
if __name__=='__main__':
    app.run_server(debug=True, port=8020)
