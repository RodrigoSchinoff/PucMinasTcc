import pandas as pd
import datetime

df = pd.read_excel('PETR4_5Minutos.xlsx',usecols="A,B,E,F,G")

def GeraDataFrame(): 
    df['Hora'] = pd.to_datetime(df['Data Hora']).dt.time
    df['Data'] = pd.to_datetime(df['Data Hora']).dt.date
    df['Perc'] = df['Fechamento'] / df['Média Móvel E [17]']
    
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)


def GeraClassificacao():
    vData = '2020-01-01'
    vLonge = 'N'
    vVoltou = 'N'
    vIndexLonge = 0

    for index, row in df[::-1].iterrows():
        
        if vData != row['Data'] and vLonge == 'S' and vVoltou == 'N':
            df.loc[vIndexLonge, 'AbriuLongeMedia'] = ''
        
        
        if row['Hora'] <= datetime.time(hour=10, minute= 15) and vData != row['Data']: 
            if (row['Perc'] >= 1.01 or row['Perc'] <= 0.99):
                df.loc[index, 'AbriuLongeMedia'] = 'S'
                vIndexLonge = index
                vData = row['Data']
                vLonge = 'S'
                vVoltou = 'N'
                df.loc[index, 'RetornouMedia'] = ''  
                
        elif row['Hora'] <= datetime.time(hour=10, minute= 55) and vData == row['Data']:
            if vLonge == 'S' and vVoltou == 'N' and (row['Perc'] < 1.01 and row['Perc'] > 0.99):
                df.loc[index, 'RetornouMedia'] = 'S'
                vVoltou = 'S'
                df.loc[index, 'AbriuLongeMedia'] = ''
                
        else:
            df.loc[index, 'AbriuLongeMedia'] = ''
            df.loc[index, 'RetornouMedia'] = ''
            

def RetornoMedias():
    print(df.query('AbriuLongeMedia == "S" or RetornouMedia == "S"'))
    

GeraDataFrame()
GeraClassificacao()
RetornoMedias()


