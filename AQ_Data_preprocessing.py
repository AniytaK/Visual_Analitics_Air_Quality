##Air Quality Data
#Values for Berlin

import pandas as pd
from datetime import datetime
from meteostat import Point, Daily, Monthly

# Data per Hour since 2013 to 2022
# Agregated Data, where for each day (month) from 2013 to 2022,
# the daily (monthly) value is calculated as the average of 24 (30-31) individual values.

#NO2
def lade_NO2():
    df_NO2 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_NO2_dataGroup1.parquet")
    df_NO2['Value'].replace(-999.00, pd.NA, inplace=True)
    df_NO2['Value'] = df_NO2['Value'].ffill()
    return df_NO2

def lade_aver_NO2():
    df_NO2 = lade_NO2()
    df_NO2_new = df_NO2[["Start", "Value"]].copy()
    df_NO2_new['Start'] = pd.to_datetime(df_NO2_new['Start'])
    # Set the 'Start' column as the index
    df_NO2_new.set_index('Start', inplace=True)
    # Resample the dataframe to daily frequency, calculating the mean of 'Value' for each day
    daily_averages_NO2 = df_NO2_new.resample('D').mean().reset_index()
    return daily_averages_NO2

def lade_aver_month_NO2():
    df_NO2 = lade_NO2()
    df_NO2_new = df_NO2[["Start", "Value"]].copy()
    df_NO2_new['Start'] = pd.to_datetime(df_NO2_new['Start'])
    # Now, set the 'Start' column as the index
    df_NO2_new.set_index('Start', inplace=True)
    # Resample the dataframe to monthly frequency, calculating the mean of 'Value' for each month
    monthly_averages_NO2 = df_NO2_new.resample('M').mean().reset_index()
    return monthly_averages_NO2

#O3
def lade_O3():
    df_O3 = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE062_O3_dataGroup1.parquet")
    df_O3['Value'].replace(-999.00, pd.NA, inplace=True)
    df_O3['Value'] = df_O3['Value'].ffill()
    return df_O3

def lade_aver_O3():
    df_O3 = lade_O3()
    df_O3_new = df_O3[["Start", "Value"]].copy()
    df_O3_new['Start'] = pd.to_datetime(df_O3_new['Start'])
    df_O3_new.set_index('Start', inplace=True)
    daily_averages_O3 = df_O3_new.resample('D').mean().reset_index()
    return daily_averages_O3

def lade_aver_month_O3():
    df_O3 = lade_O3()
    df_O3_new = df_O3[["Start", "Value"]].copy()
    df_O3_new['Start'] = pd.to_datetime(df_O3_new['Start'])
    df_O3_new.set_index('Start', inplace=True)
    monthly_averages_O3 = df_O3_new.resample('M').mean().reset_index()
    return monthly_averages_O3

#SO2
def lade_SO2():
    df_SO2 = pd.read_parquet(
        "D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_SO2_dataGroup1.parquet")
    df_SO2['Value'].replace(-999.00, pd.NA, inplace=True)
    df_SO2['Value'] = df_SO2['Value'].ffill()
    return df_SO2

def lade_aver_SO2():
    df_SO2 = lade_SO2()
    df_SO2_new = df_SO2[["Start", "Value"]].copy()
    df_SO2_new['Start'] = pd.to_datetime(df_SO2_new['Start'])
    df_SO2_new.set_index('Start', inplace=True)
    daily_averages_SO2 = df_SO2_new.resample('D').mean().reset_index()
    return daily_averages_SO2

def lade_aver_month_SO2():
    df_SO2 = lade_SO2()
    df_SO2_new = df_SO2[["Start", "Value"]].copy()
    df_SO2_new['Start'] = pd.to_datetime(df_SO2_new['Start'])
    df_SO2_new.set_index('Start', inplace=True)
    monthly_averages_SO2 = df_SO2_new.resample('M').mean().reset_index()
    return monthly_averages_SO2

#CO
def lade_CO():
    df_CO = pd.read_parquet("D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_CO_dataGroup1.parquet")
    df_CO['Value'].replace(-999.00, pd.NA, inplace=True)
    df_CO['Value'] = df_CO['Value'].ffill()
    return df_CO

def lade_aver_CO():
    df_CO = lade_CO()
    df_CO_new = df_CO[["Start", "Value"]].copy()
    df_CO_new['Start'] = pd.to_datetime(df_CO_new['Start'])
    df_CO_new.set_index('Start', inplace=True)
    daily_averages_CO = df_CO_new.resample('D').mean().reset_index()
    return daily_averages_CO

def lade_aver_month_CO():
    df_CO = lade_CO()
    df_CO_new = df_CO[["Start", "Value"]].copy()
    df_CO_new['Start'] = pd.to_datetime(df_CO_new['Start'])
    df_CO_new.set_index('Start', inplace=True)
    monthly_averages_CO = df_CO_new.resample('M').mean().reset_index()
    return monthly_averages_CO

#PM 2.5
def lade_PM2_5():
    df_PM2_5 = pd.read_parquet(
        "D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_PM2_dataGroup1.parquet")
    df_PM2_5['Value'].replace(-999.00, pd.NA, inplace=True)
    df_PM2_5['Value'] = df_PM2_5['Value'].ffill()
    return df_PM2_5

def lade_aver_PM2_5():
    df_PM2_5 = lade_PM2_5()
    df_PM2_5_new = df_PM2_5[["Start", "Value"]].copy()
    df_PM2_5_new['Start'] = pd.to_datetime(df_PM2_5_new['Start'])
    df_PM2_5_new.set_index('Start', inplace=True)
    daily_averages_PM2_5 = df_PM2_5_new.resample('D').mean().reset_index()
    return daily_averages_PM2_5

def lade_aver_month_PM2_5():
    df_PM2_5 = lade_PM2_5()
    df_PM2_5_new = df_PM2_5[["Start", "Value"]].copy()
    df_PM2_5_new['Start'] = pd.to_datetime(df_PM2_5_new['Start'])
    df_PM2_5_new.set_index('Start', inplace=True)
    monthly_averages_PM2_5 = df_PM2_5_new.resample('M').mean().reset_index()
    return monthly_averages_PM2_5

#PM 10
def lade_PM10():
    df_PM10 = pd.read_parquet(
        "D:/Studium/3_HS 2023/Visual Analitics/Projekt/Daten/DE/Berlin/ParquetFiles/E1a/SPO.DE_DEBE065_PM1_dataGroup1.parquet")
    df_PM10['Value'].replace(-999.00, pd.NA, inplace=True)
    df_PM10['Value'] = df_PM10['Value'].ffill()
    return df_PM10

def lade_aver_PM10():
    df_PM10 = lade_PM10()
    df_PM10_new = df_PM10[["Start", "Value"]].copy()
    df_PM10_new['Start'] = pd.to_datetime(df_PM10_new['Start'])
    df_PM10_new.set_index('Start', inplace=True)
    daily_averages_PM10 = df_PM10_new.resample('D').mean().reset_index()
    return daily_averages_PM10

def lade_aver_month_PM10():
    df_PM10 = lade_PM10()
    df_PM10_new = df_PM10[["Start", "Value"]].copy()
    df_PM10_new['Start'] = pd.to_datetime(df_PM10_new['Start'])
    df_PM10_new.set_index('Start', inplace=True)
    monthly_averages_PM10 = df_PM10_new.resample('M').mean().reset_index()
    return monthly_averages_PM10

#Data cleaning for PCP
def lade_data_for_pcp():
    monthly_averages_NO2 = lade_aver_month_NO2()
    monthly_averages_O3 = lade_aver_month_O3()
    monthly_averages_CO = lade_aver_month_CO()
    monthly_averages_SO2 = lade_aver_month_SO2()
    monthly_averages_PM2_5 = lade_aver_month_PM2_5()
    monthly_averages_PM10 = lade_aver_month_PM10()
    #Weather Data
    start = datetime(2013, 1, 1)
    end = datetime(2022, 12, 31)
    berlin = Point(52.5200, 13.4050, 70)
    data = Monthly(berlin, start, end)
    data = data.fetch()
    data_1 = data[["tavg", "wspd"]].copy()
    data_1.fillna(13, inplace=True)
    data_1['ID'] = range(1, len(data_1) + 1)
    data_1.set_index(("ID"), inplace=True)
    #combine of 2 Data sources
    df_m = [monthly_averages_NO2["Value"], monthly_averages_O3["Value"], monthly_averages_CO["Value"],
            monthly_averages_SO2["Value"], monthly_averages_PM2_5["Value"], monthly_averages_PM10["Value"]]
    pollutants = ["NO2", "O3", "CO", "SO2", "PM 2.5", "PM 10"]

    comb_df_m = pd.concat(df_m, axis=1, keys=pollutants)
    comb_df_m['ID'] = range(1, len(comb_df_m) + 1)

    comb_df_m.set_index(("ID"), inplace=True)
    comb_df_m.fillna(0.1, inplace=True)
    df_final = pd.concat([comb_df_m, data_1], axis=1)
    df_final['Jahr'] = ((df_final.index - 1) // 12) + 2013  # Jahr beginnt bei 2013 und erhöht sich alle 12 Monate
    df_final['Monat'] = ((df_final.index - 1) % 12) + 1  # Monate von 1 bis 12
    columns_to_convert = ['NO2', 'O3', 'CO', 'SO2', 'PM 2.5', 'PM 10']

    for column in columns_to_convert:
        df_final[column] = pd.to_numeric(df_final[column])
    spalten = df_final.columns.tolist()
    spalten.remove('Jahr')
    spalten.remove("Monat")
    spalten.insert(0, 'Jahr')
    spalten.insert(1, "Monat")
    df_final = df_final[spalten]
    return df_final

def lade_data_for_AQI():
    daily_averages_PM2_5 = lade_aver_PM2_5()
    daily_averages_PM10 = lade_aver_PM10()
    daily_averages_O3 = lade_aver_O3()

    AQI_data = [daily_averages_O3["Start"], daily_averages_O3["Value"], daily_averages_PM2_5["Value"],
                daily_averages_PM10["Value"]]
    pollutants = ["Date", "O3", "PM 2.5", "PM 10"]

    comb_df = pd.concat(AQI_data, axis=1, keys=pollutants)
    comb_df['ID'] = range(1, len(comb_df) + 1)

    comb_df.set_index(("ID"), inplace=True)
    comb_df.fillna(0.1, inplace=True)
    comb_df["Date"] = pd.to_datetime(comb_df["Date"])
    comb_df["AQI"] = comb_df["PM 2.5"] + comb_df["PM 10"] + comb_df["O3"]
    return comb_df



