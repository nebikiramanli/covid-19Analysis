import pandas as  pd 
import numpy as np 
import folium 
from flask import Flask,render_template
import matplotlib.pyplot as plt

corona_df=pd.read_csv("CovidAnaliz\\datasheet2_3rd_Jan_2021.csv", engine="python", sep=',', quotechar='"', error_bad_lines=False)
corona_graf_df=pd.read_csv("CovidAnaliz\\datasheet_6_Jan_2021.csv")

def Grafiksel(corona_graf_df):
    globalCases=corona_graf_df[["Cases - cumulative total","Name"]].head(6)
    globalDeath=corona_graf_df[["Deaths - cumulative total","Name"]].head(10)
    weekDeath=corona_graf_df[["Name","Deaths - newly reported in last 7 days"]].head(6)
    dayDeath=corona_graf_df[["Name","Deaths - newly reported in last 24 hours"]].head(6)
    plt.figure(figsize=(15,8))
    plt.ticklabel_format(style='plain')
    plt.bar(globalCases["Name"],globalCases["Cases - cumulative total"],color='r')
    plt.xlabel("Ülke")
    plt.ylabel("Onaylanan Değer")
    plt.title("Dünya ve İlk 5 Ülke Tanımlanan Vaka Sayısı")
    plt.savefig('books_read.png')
    plt.show()
    plt.figure(figsize=(13,8))
    plt.ticklabel_format(style='plain')
    plt.plot(globalDeath["Name"],globalDeath["Deaths - cumulative total"],color="red")
    plt.xlabel("Ülke")
    plt.ylabel("Ölüm Sayıları")
    plt.title("Dünya Genelinde ve Ülkelerde Ölüm Sayıları")
    plt.show()
    weeklabels=weekDeath["Name"]
    weeksizes=weekDeath["Deaths - newly reported in last 7 days"]
    daylabels=dayDeath["Name"]
    daysizes=dayDeath["Deaths - newly reported in last 24 hours"]
    fig,y=plt.subplots()
    y.pie(daysizes,labels=daylabels,autopct='%1.1f%%')
    y.axis('equal')
    plt.title("Günlük Ölüm Bildirimlerin Oranları")
    fig,x=plt.subplots()
    x.pie(weeksizes,labels=weeklabels,autopct='%1.1f%%')
    x.axis('equal')
    plt.title("Hafatalık Ölüm Bildirimleri Oranları")
    plt.show()


print("Covid 19 Veri Analizine Hoşgeldiniz\n")
print("**************Menü************")
print("1 ->>>>>> Covid 19 Verilerinin Grafiksel Dağılımı")
print("2 ->>>>>> Covid 19 Verilerinin Dünya Haritası  Dağılımı")
secim=int(input())
if secim==1:
    Grafiksel(corona_graf_df)
    
else:
    pass

def find_confirmed(n=15):
    ulke_df=corona_df.groupby('WHO_Region').sum()[['Cases_cumulative_total','Deaths_cumulative_total']]
    top_df=ulke_df.nlargest(n,'Cases_cumulative_total')[['Cases_cumulative_total']]
    return top_df

top_df=find_confirmed()
veri_ciftleri=[(WHO_Region,Cases_cumulative_total) for WHO_Region,Cases_cumulative_total in zip(top_df.index,top_df['Cases_cumulative_total'])]

corona_df=corona_df[['Lat','Long_','Cases_cumulative_total']]
corona_df=corona_df.dropna()

corona_map=folium.Map(location=[38.96,35.24],tiles="Stamen toner",zoom_start=8)


def cember_yapici(x):
    folium.Circle(location=[x[0],x[1]], radius=float(x[2]/10),color='red',popup='Onayli Vaka Sayisi:{}'.format(x[2])).add_to(corona_map)

corona_df.apply(lambda x:cember_yapici(x),axis=1)

html_map=corona_map._repr_html_()
app=Flask(__name__)
@app.route('/')

def home():
    return render_template("home.html",table=top_df,cmap=html_map,pairs=veri_ciftleri)


if __name__=="__main__":
    app.run(debug=True)