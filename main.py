import streamlit as st
import json
import ephem
import math
import datetime
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="astro_ai_app")

def veriyi_yukle():
    with open("burclar.json", "r", encoding="utf-8") as dosya:
        return json.load(dosya)

def burca_cevir(radyan_degeri):
    derece = (math.degrees(radyan_degeri) + 360) % 360
    burclar = ["Koç", "Boğa", "İkizler", "Yengeç", "Aslan", "Başak", 
               "Terazi", "Akrep", "Yay", "Oğlak", "Kova", "Balık"]
    return burclar[int(derece / 30) % 12]

def harita_hesapla(tarih, saat, enlem, boylam):
    gozlemci = ephem.Observer()
    tam_zaman = datetime.datetime.combine(tarih, saat)
    utc_zaman = tam_zaman - datetime.timedelta(hours=3) 
    gozlemci.date = utc_zaman.strftime('%Y/%m/%d %H:%M:%S')
    gozlemci.lat, gozlemci.lon = str(enlem), str(boylam)

    gunes_b = burca_cevir(ephem.Ecliptic(ephem.Sun(gozlemci)).lon)
    ay_b = burca_cevir(ephem.Ecliptic(ephem.Moon(gozlemci)).lon)

    lst, lat, eps = gozlemci.sidereal_time(), gozlemci.lat, math.radians(23.43929)
    pay = math.cos(lst)
    payda = -(math.sin(lst) * math.cos(eps) + math.tan(lat) * math.sin(eps))
    yukselen_b = burca_cevir(math.atan2(pay, payda))

    return gunes_b, ay_b, yukselen_b


st.set_page_config(page_title="Astroloji AI", page_icon="✨")
st.title("✨ Astroloji AI: Büyük Üçlü Analizi")

burc_verileri = veriyi_yukle()

col1, col2, col3 = st.columns(3)
with col1:
    secilen_tarih = st.date_input("Doğum Tarihi", min_value=datetime.date(1900, 1, 1), max_value=datetime.date.today())
with col2:
    secilen_saat = st.time_input("Doğum Saati", step=60)
with col3:
    secilen_sehir = st.text_input("Doğum Yeri")

if st.button("Analiz Et 🔮", use_container_width=True):
    konum = geolocator.geocode(secilen_sehir)
    if konum:
        g, a, y = harita_hesapla(secilen_tarih, secilen_saat, konum.latitude, konum.longitude)
        
        
        st.success(f"Analiz Tamamlandı! Konum: {konum.address}")
        
       
        tab1, tab2, tab3 = st.tabs(["☀️ Güneş Burcu", "🌙 Ay Burcu", "⬆️ Yükselen Burcu"])

        with tab1:
            st.header(f"Güneş: {g}")
            if g in burc_verileri:
                st.write(burc_verileri[g]['genel_analiz'])
                st.info(f"✨ **Güçlü Yönler:** {', '.join(burc_verileri[g]['olumlu_ozellikler'])}")

        with tab2:
            st.header(f"Ay: {a}")
            if a in burc_verileri:
                # JSON'da 'ay_analizi' anahtarı var mı kontrol et
                st.write(burc_verileri[a].get('ay_analizi', "Bu burç için Ay analizi henüz eklenmemiş."))

        with tab3:
            st.header(f"Yükselen: {y}")
            if y in burc_verileri:
                # JSON'da 'yukselen_analizi' anahtarı var mı kontrol et
                st.write(burc_verileri[y].get('yukselen_analizi', "Bu burç için Yükselen analizi henüz eklenmemiş."))
    else:
        st.error("Konum bulunamadı!")