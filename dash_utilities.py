import pandas as pd
import itertools
import locale


def generate_graph_df(
    kaufpreis,
    Eigenkapital,
    Tilgungsrate,
    Sollzins,
    Sollzinsbindung,
    Sondertilgung_rate=0.05,
    Grunderwerbsteuer_rate=0.06,
    Maklerprovison_rate=0.0357,
    Notarkosten_rate=0.015,
    Grundbucheintrag_rate=0.005,
    Start_Date='2024-12-01'
):

    Date=pd.to_datetime(Start_Date)
    Faktor = 12
    Nettodarlehen = kaufpreis*(1+Grunderwerbsteuer_rate+Maklerprovison_rate+Notarkosten_rate+Grundbucheintrag_rate)-Eigenkapital
  
    
    aktuelle_Nettodarlehen=Nettodarlehen
    Sondertilgung=Nettodarlehen*Sondertilgung_rate
    Fest_Monatsrate = round(((Tilgungsrate+Sollzins)*Nettodarlehen)/Faktor)

    
    def get_Tilgungszahlung_Zinszahlung(Fest_Monatsrate,aktuelle_Nettodarlehen,Sollzins,Faktor):
        Zinszahlung = aktuelle_Nettodarlehen*Sollzins/Faktor
        Tilgungszahlung=Fest_Monatsrate-Zinszahlung
        return Zinszahlung,Tilgungszahlung
    
    def get_cumu(List):
        return list(itertools.accumulate(List))

    Zinszahlung_List=[0]
    Tilgungszahlung_List=[0]
    Sondertilgunszahlung_List=[0]
    totaltilgungszahlung_List=[0]
    aktuelle_Nettodarlehen_List =[aktuelle_Nettodarlehen]
    Date_List=[0]
    Years_List=[0]

    for i in range(Sollzinsbindung):
        for j in range(12):
            
            Date = Date + pd.DateOffset(months=1)
            Zinszahlung,Tilgungszahlung=get_Tilgungszahlung_Zinszahlung(Fest_Monatsrate,aktuelle_Nettodarlehen,Sollzins,Faktor)
            Date_List.append(Date.strftime("%b %Y"))
            Years_List.append(0.08333)

            if aktuelle_Nettodarlehen>0:
                Zinszahlung_List.append(round(Zinszahlung))
                Tilgungszahlung_List.append(round(Tilgungszahlung))
                
                if j==11:
                    aktuelle_Nettodarlehen=aktuelle_Nettodarlehen-Tilgungszahlung-Sondertilgung
                    Sondertilgunszahlung_List.append(Sondertilgung)

                    
                else:
                    aktuelle_Nettodarlehen=aktuelle_Nettodarlehen-Tilgungszahlung
                    Sondertilgunszahlung_List.append(0)
                if aktuelle_Nettodarlehen>0:
                    aktuelle_Nettodarlehen_List.append(round(aktuelle_Nettodarlehen))
                else:
                    aktuelle_Nettodarlehen_List.append(0)
                totaltilgungszahlung=Nettodarlehen-aktuelle_Nettodarlehen
                totaltilgungszahlung_List.append(round(totaltilgungszahlung))
            
            else:
                Zinszahlung_List.append(0)
                Tilgungszahlung_List.append(0)
                Sondertilgunszahlung_List.append(0)
                #if j==11:
                #    Years_List.append(1)
                #else:
                #    Years_List.append(0)

                aktuelle_Nettodarlehen_List.append(0)
                totaltilgungszahlung_List.append(round(Nettodarlehen))
                



    def get_rate(List,Nettodarlehen):
        return [[round(el/Nettodarlehen,4) for el in List]]


    # Creating a DataFrame from a dictionary
    data = {
        'Date': Date_List,
        'Zinszahlung_List': Zinszahlung_List,
        'Zinszahlung_List_Cumu':get_cumu(Zinszahlung_List),
        'Tilgungszahlung_List': Tilgungszahlung_List,
        'Tilgungszahlung_List_Cumu': get_cumu(Tilgungszahlung_List),
        'Sondertilgunszahlung_List': Sondertilgunszahlung_List,
        'Sondertilgunszahlung_List_Cumu': get_cumu(Sondertilgunszahlung_List),
        'totaltilgungszahlung_List':totaltilgungszahlung_List,
        'aktuelle_Nettodarlehen_List':aktuelle_Nettodarlehen_List,
        'Years_List':get_cumu(Years_List)
    }
    
    df = pd.DataFrame(data)#,index=Date_List)
    #df.index.name = 'date'    
    return df



def convert_to_chinese(years_month):
    def convert_month(date_str):
        month_mapping = {
        "Jan": "一月",
        "Feb": "二月",
        "Mar": "三月",
        "Apr": "四月",
        "May": "五月",
        "Jun": "六月",
        "Jul": "七月",
        "Aug": "八月",
        "Sep": "九月",
        "Oct": "十月",
        "Nov": "十一月",
        "Dec": "十二月"
    }


        # Parse the input and convert the month
        month, year = date_str.split()
        chinese_month = month_mapping[month]
        result = f"{year} {chinese_month}"
        return result
    
    return [0]+[ convert_month(date_str) for date_str in years_month[1:]]

if __name__ == '__main__':
    
    kaufpreis=568000
    Eigenkapital=113600
    Maklerprovison_rate=0.0249
    Notarkosten_rate=0.015
    Grundbucheintrag_rate=0.005
    Sondertilgung_rate=0.05
    Tilgungsrate=0.01
    Sollzins=0.0366
    Sollzinsbindung=20


    df=generate_graph_df(
        kaufpreis=kaufpreis,
        Eigenkapital=Eigenkapital,
        Maklerprovison_rate=Maklerprovison_rate,
        Notarkosten_rate=Notarkosten_rate,
        Grundbucheintrag_rate=Grundbucheintrag_rate,
        Sondertilgung_rate=Sondertilgung_rate,
        Tilgungsrate=Tilgungsrate,
        Sollzins=Sollzins,
        Sollzinsbindung=Sollzinsbindung
    )

    df.to_csv('with_repayment.csv', index=False)  # Set index=False to exclude the index column

    df=generate_graph_df(
        kaufpreis=kaufpreis,
        Eigenkapital=Eigenkapital,
        Maklerprovison_rate=Maklerprovison_rate,
        Notarkosten_rate=Notarkosten_rate,
        Grundbucheintrag_rate=Grundbucheintrag_rate,
        Sondertilgung_rate=0,
        Tilgungsrate=Tilgungsrate,
        Sollzins=Sollzins,
        Sollzinsbindung=Sollzinsbindung
    )

    df.to_csv('without_repayment.csv', index=False)  # Set index=False to exclude the index column
