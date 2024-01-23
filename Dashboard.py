import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly import colors
import folium
import requests_cache
import openmeteo_requests
from retry_requests import retry
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
from AQ_Data_preprocessing import lade_aver_NO2
daily_averages_NO2 = lade_aver_NO2()

from AQ_Data_preprocessing import lade_aver_O3
daily_averages_O3 = lade_aver_O3()

from AQ_Data_preprocessing import lade_aver_SO2
daily_averages_SO2 = lade_aver_SO2()

from AQ_Data_preprocessing import lade_aver_CO
daily_averages_CO = lade_aver_CO()

from AQ_Data_preprocessing import lade_aver_PM2_5
daily_averages_PM2_5 = lade_aver_PM2_5()

from AQ_Data_preprocessing import lade_aver_PM10
daily_averages_PM10 = lade_aver_PM10()
data_frames_day = [daily_averages_NO2, daily_averages_O3, daily_averages_CO, daily_averages_SO2, daily_averages_PM2_5, daily_averages_PM10]

#Air Quality Data per Month
from AQ_Data_preprocessing import lade_aver_month_NO2
monthly_averages_NO2 = lade_aver_month_NO2()

from AQ_Data_preprocessing import lade_aver_month_O3
monthly_averages_O3 = lade_aver_month_O3()

from AQ_Data_preprocessing import lade_aver_month_SO2
monthly_averages_SO2 = lade_aver_month_SO2()

from AQ_Data_preprocessing import lade_aver_month_CO
monthly_averages_CO = lade_aver_month_CO()

from AQ_Data_preprocessing import lade_aver_month_PM2_5
monthly_averages_PM2_5 = lade_aver_month_PM2_5()

from AQ_Data_preprocessing import lade_aver_month_PM10
monthly_averages_PM10 = lade_aver_month_PM10()
data_frames_month = [monthly_averages_NO2, monthly_averages_O3, monthly_averages_CO, monthly_averages_SO2, monthly_averages_PM2_5, monthly_averages_PM10]

#Data for PCP
from AQ_Data_preprocessing import lade_data_for_pcp
df_final = lade_data_for_pcp()

#Data for Gauge-Chart
from AQ_Data_preprocessing import lade_data_for_AQI
daily_AQI = lade_data_for_AQI()
#_______________________________________________________________________________________________________________________

# FUNKTIONS
#Radar Chart to compare Pollutants Values per Day with WHO-Limits
def create_radar_chart_for_day(data_frames_day, pollutants, day, who_limits=None):
    # Standart WHO-Limits
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

#Map for geografical view
def create_map(daily_averages_PM10, date, location=(52.520008, 13.404954), zoom_start=6):
    map_object = folium.Map(location=location, zoom_start=zoom_start)

    df_day = daily_averages_PM10[daily_averages_PM10['Start'] == date]

    for index, row in df_day.iterrows():
        #PM10-Values
        pm10_value = row['Value']
        marker_location = location
        marker_objects = folium.Marker(location=marker_location,
                                       icon=folium.Icon(color="lightblue",
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
    palette = colors.sequential.BuPu_r
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

#Gauge Chart as daily values of AQI
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

def get_aqi_from_api(date):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)

    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": 52.52,
        "longitude": 13.41,
        "hourly": "european_aqi",
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]

    hourly = response.Hourly()
    hourly_european_aqi = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start=pd.to_datetime(hourly.Time(), unit="s"),
        end=pd.to_datetime(hourly.TimeEnd(), unit="s"),
        freq=pd.Timedelta(seconds=hourly.Interval()),
        inclusive="left"
    ), "european_aqi": hourly_european_aqi}

    hourly_dataframe = pd.DataFrame(data=hourly_data)
    hourly_dataframe_new = hourly_dataframe[["date", "european_aqi"]].copy()
    hourly_dataframe_new['date'] = pd.to_datetime(hourly_dataframe_new['date'])
    hourly_dataframe_new.set_index('date', inplace=True)

    # Berechnung des täglichen Durchschnitts der AQI-Werte
    daily_averages_aqi = hourly_dataframe_new.resample('D').mean().reset_index()
    return daily_averages_aqi

def get_aqi_from_api_value(daily_averages_aqi, selected_date):
    date_filter = daily_averages_aqi['date'] == pd.to_datetime(selected_date)
    if not date_filter.any():
        return None
    return daily_averages_aqi.loc[date_filter, 'european_aqi'].iloc[0]

def update_gauge_chart(daily_data, selected_date, is_api_data=False):
    if is_api_data:
        value = get_aqi_from_api_value(daily_data, selected_date)
    else:
        value = get_daily_AQI_value(daily_data, selected_date)

    if value is None:
        return None  # Missing values

    air_quality_text = get_air_quality_text(value)

    # Configuration for Gauge-Chart
    gauge_config = {
        'axis': {'range': [None, 500], 'tickwidth': 0.5, 'tickcolor': "black"},
        'bar': {'color': "black", 'thickness': 0.7},  # This color will be overridden by the steps
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

    # Gauge-Charts
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
                y=0.3,  # Verschiebung nach oben oder unten, um Überschneidungen zu vermeiden
                xref="paper",
                yref="paper",
                text=air_quality_text,
                showarrow=False,
                font=dict(size=15, color="black"),
                xanchor='center',  # Ausrichtung des Annotations-Textes
                yanchor='bottom'
            )
        ],
        autosize=False,
        width=350,
        height=260,
        margin=dict(l=10, r=10, b=100, t=60, pad=6)
    )
    return fig
#_______________________________________________________________________________________________________________________

#PCP
fixed_columns = ['Year', 'Month']
selectable_columns = ['NO2', 'O3', 'CO', 'SO2', 'PM 2.5', 'PM 10', 'tavg', 'wspd']
def create_parallel_coordinates_plot(df_final, selected_columns):
    seasonal_color_scale = [
    (0.00, "purple"), (1/12, "purple"), (2/12, "lightseagreen"), (3/12, "lightseagreen"), (4/12, "lightseagreen"),
    (5/12, "lightseagreen"), (6/12, "red"), (7/12, "red"), (8/12, "red"), (9/12, "orange"), (10/12, "orange"),
    (11/12, "orange"), (1.00, "purple")
    ]
    fig = px.parallel_coordinates(df_final,
                                  color='Month',
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
                    dbc.Col(html.H3('Air Quality',
                        className='text-left d-flex align-items-center',
                        style={'font-family': 'Source Sans Pro', 'font-size': '38px', 'font-weight': 'bold', 'color': '#FFFFFF'}),
                        width={'size': 5},
                        className='mt-1 d-flex align-items-end',),
                    dbc.Col(html.H3('A daily index developed to represent air quality',
                        className='text-left d-flex align-items-center',
                        style={'font-family': 'Source Sans Pro', 'font-size': '26px', 'color': '#FFFFFF',  'margin-bottom':'13px'}),
                        width={'size': 7}),
                ],
                    className='mt-1 d-flex align-items-end',
                    style={'background-image': 'linear-gradient(to right, #8CD0F1, #cc6bcc)', 'height': '60px', 'border-radius': '2px'}),

                html.Div(style={'height': '7px'}),

                dbc.Row([
                    dbc.Col([html.Div([
                        dcc.Input(
                            id='search-input',
                            type='text',
                            placeholder='Enter a City',
                            style={'marginRight': '15px', "height": "52px", 'font-family': 'Source Sans Pro', 'border-radius': '13px',
                                   'font-size': '22px'},
                        ),
                        html.Button(
                            '🔍',
                            id='search-button',
                            style={"height": "48px",
                                'marginRight': '7px',
                                'backgroundColor': 'white',
                                'border': 'none', 'borderRadius': '13px'}
                        ),
                    ]),], width={'size': 4},),
                    dbc.Col(html.Div([
                                dcc.DatePickerSingle(
                                    id='calender',
                                    date='2022-12-15',
                                    display_format='DD MMM YYYY',
                                    style={'marginLeft': '0px', 'margin-bottom':'10px', 'backgroundColor': 'white',
                                           'width': '100%', "height": "40px", 'margin-right': '5px',}
                                ),
                                html.Div(
                                    id='output-container',
                                    style={'width': '70%',})
                    ], style={'display': 'flex',
                                'flex-direction': 'row',
                                'justify-content': 'space-around',
                                'align-items': 'center',
                                'padding': '10px',
                                'border-radius': '13px',
                                'background-color': 'white',
                                "height": "50px"}
                    ),width={'size': 3},),
                    dbc.Col(html.Div([
                            html.Button(
                                '📧',
                                id='mail-button',
                                style={"height": "50px",
                                        'marginLeft': '220px',
                                       'backgroundColor': 'white',
                                       'border': 'none',
                                       'borderRadius': '13px'}),
                            html.Button(
                                '👤',  # Menschensymbol
                                id='account-button',
                                style={'marginLeft': '20px',
                                       "height": "50px",
                                       'backgroundColor': 'white',
                                       'border': 'none',
                                       'borderRadius': '13px'
                                }
                            ),
                    ]), width={'size': 5},),
                ],
                    #className = 'g-0',
                    style = {'background-color': "black", 'alignItems': 'center', 'height': '70px', 'border-radius': '2px'}),

                html.Div(style={'height': '10px'}),
                ########################################################################################################
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
                ########################################################################################################
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
        ]
    ),
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
# def show_gauge_chart(selected_date):
#     if not selected_date:
#         selected_date = daily_AQI['Date'].dt.strftime('%Y-%m-%d').max()
#
#     gauge_chart = update_gauge_chart(daily_AQI, selected_date)
#     if gauge_chart is not None:
#         return gauge_chart
#     else:
#         fig = go.Figure()
#         fig.add_annotation(text="Data is missing",
#                            xref="paper", yref="paper",
#                            x=0.5, y=0.5, showarrow=False,
#                            font=dict(size=16, color="red"))
#         return fig

def show_gauge_chart(selected_date):
    global daily_AQI
    is_api_data = False  # Flag, um zu überprüfen, ob die Daten von der API kommen

    # Prüfen, ob ein Datum ausgewählt wurde
    if not selected_date:
        # Wenn kein Datum ausgewählt wurde, verwenden Sie das neueste Datum aus dem CSV
        selected_date = daily_AQI['Date'].dt.strftime('%Y-%m-%d').max()
    else:
        # Umwandeln des ausgewählten Datums in das richtige Format
        selected_date = pd.to_datetime(selected_date)

    # Entscheiden, ob Daten aus dem CSV oder der API geholt werden sollen
    if selected_date > pd.to_datetime('2022-12-31'):  # Ersetzen Sie dies mit dem tatsächlichen letzten Datum im CSV
        # Abrufen der Daten von der API
        daily_data_from_api = get_aqi_from_api(selected_date)
        is_api_data = True
    else:
        # Daten aus dem CSV verwenden
        daily_data_from_api = daily_AQI

    # Gauge-Chart
    gauge_chart = update_gauge_chart(daily_data_from_api, selected_date, is_api_data)

    if gauge_chart is not None:
        return gauge_chart
    else:
        fig = go.Figure()
        fig.add_annotation(text="Data is missing",
                           xref="paper", yref="paper",
                           x=0.5, y=0.5, showarrow=False,
                           font=dict(size=16, color="red"))
        return fig


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
