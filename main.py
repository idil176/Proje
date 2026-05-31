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
# Yıldızlı arka plan ve beyaz metinler için güncellenmiş CSS
yildizli_arka_plan = """
<style>
/* Ana arka planı hedefler */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1506318137071-a4e501166699?q=80&w=2070&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Üst menü çubuğunu şeffaf yapar */
header[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* Sekme panelinin arka planını koyu transparan yapar */
.stTabs [data-baseweb="tab-panel"] {
    background-color: rgba(0, 0, 0, 0.7) !important;
    padding: 20px;
    border-radius: 10px;
}

/* Koyu zemin üzerindeki tüm yazıları zorla BEYAZ yapar */
.stTabs [data-baseweb="tab-panel"] * {
    color: white !important;
}
</style>
"""
st.markdown(yildizli_arka_plan, unsafe_allow_html=True)
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
                # Element ve Yönetici Bilgisi Satırı
                st.markdown(f"**Element:** {burc_verileri[g]['element']} | **Yönetici Gezegen:** {burc_verileri[g]['yonetici']}")
                st.write(burc_verileri[g]['genel_analiz'])
                
                # Olumlu Özellikler ve Gölge Yanlar Panelleri
                st.success(f"✨ **Güçlü Yönler:** {', '.join(burc_verileri[g]['olumlu_ozellikler'])}")
                st.error(f"🪐 **Gölge Yanlar:** {', '.join(burc_verileri[g]['golge_yanlar'])}")

        with tab2:
            st.header(f"Ay: {a}")
            if a in burc_verileri:
                # Element ve Yönetici Bilgisi Satırı
                st.markdown(f"**Element:** {burc_verileri[a]['element']} | **Yönetici Gezegen:** {burc_verileri[a]['yonetici']}")
                st.write(burc_verileri[a].get('ay_analizi', "Bu burç için Ay analizi henüz eklenmemiş."))
                
                # Olumlu Özellikler ve Gölge Yanlar Panelleri
                st.success(f"✨ **Güçlü Yönler:** {', '.join(burc_verileri[a]['olumlu_ozellikler'])}")
                st.error(f"🪐 **Gölge Yanlar:** {', '.join(burc_verileri[a]['golge_yanlar'])}")

        with tab3:
            st.header(f"Yükselen: {y}")
            if y in burc_verileri:
                # Element ve Yönetici Bilgisi Satırı
                st.markdown(f"**Element:** {burc_verileri[y]['element']} | **Yönetici Gezegen:** {burc_verileri[y]['yonetici']}")
                st.write(burc_verileri[y].get('yukselen_analizi', "Bu burç için Yükselen analizi henüz eklenmemiş."))
                
                # Olumlu Özellikler ve Gölge Yanlar Panelleri
                st.success(f"✨ **Güçlü Yönler:** {', '.join(burc_verileri[y]['olumlu_ozellikler'])}")
                st.error(f"🪐 **Gölge Yanlar:** {', '.join(burc_verileri[y]['golge_yanlar'])}")
    else:
        st.error("Konum bulunamadı!")