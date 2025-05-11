import streamlit as st
import folium
from folium import Popup
from folium.plugins import AntPath
from streamlit_folium import st_folium
from folium.features import CustomIcon
import os
import pandas as pd


# === DATA (normaal importeer je dit uit je bestand of Excel) ===
vakanties = {
    1: [
        {"naam": "Landal Dwergter Sand", "coord": (52.899328, 7.972639), "aankomst": "07-07-2025", "vertrek": "11-07-2025", "prijs": "384,00€", "reistijd": "02:55", "url": "https://www.landal.nl/parken/dwergter-sand/accommodaties/6b"},
        {"naam": "Center parcs park Eifel", "coord": (50.257889, 6.976639), "aankomst": "11-07-2025", "vertrek": "14-07-2025", "prijs": "413,00€", "reistijd": "03:59", "url": "https://www.centerparcs.nl/nl-nl/duitsland/fp_HE_vakantiepark-park-eifel/cottages"},
        {"naam": "landal Vakantiepark Hochwald", "coord": (49.746126, 6.845690), "aankomst": "14-07-2025", "vertrek": "18-07-2025", "prijs": "795,00€", "reistijd": "01:01", "url": "https://www.landal.nl/parken/hochwald/accommodaties/6b1"},
        {"naam": "Center parcs Villages Nature Paris", "coord": (48.832250, 2.832722), "aankomst": "18-07-2025", "vertrek": "21-07-2025", "prijs": "496,00€", "reistijd": "03:54", "url": "https://www.centerparcs.nl/nl-nl/frankrijk/fp_VN_vakantiepark-villages-nature-paris/cottages"},
    ],
    2: [
        {"naam": "Landal Dwergter Sand", "coord": (52.899328, 7.972639), "aankomst": "07-07-2025", "vertrek": "11-07-2025", "prijs": "384,00€", "reistijd": "02:55", "url": "https://www.landal.nl/parken/dwergter-sand/accommodaties/6b"},
        {"naam": "Landal Winterberg", "coord": (51.250104, 8.505771), "aankomst": "11-07-2025", "vertrek": "14-07-2025", "prijs": "417,00€", "reistijd": "02:45", "url": "https://www.landal.nl/parken/winterberg/accommodaties/4u"},
        {"naam": "Village les Gottales", "coord": (50.370823, 5.862867), "aankomst": "14-07-2025", "vertrek": "18-07-2025", "prijs": "497,00€", "reistijd": "03:28", "url": "https://www.landal.nl/parken/village-les-gottales/accommodaties/2a"},
        {"naam": "Center parcs Villages Nature Paris", "coord": (48.832250, 2.832722), "aankomst": "18-07-2025", "vertrek": "21-07-2025", "prijs": "496,00€", "reistijd": "03:28", "url": "https://www.centerparcs.nl/nl-nl/frankrijk/fp_VN_vakantiepark-villages-nature-paris/cottages"},
    ],
    3: [
        {"naam": "Village les Gottales", "coord": (50.370823, 5.862867), "aankomst": "07-07-2025", "vertrek": "11-07-2025", "prijs": "347,00€", "reistijd": "03:02", "url": "https://www.landal.nl/parken/village-les-gottales/accommodaties/2a"},
        {"naam": "Center parcs Villages Nature Paris", "coord": (48.832250, 2.832722), "aankomst": "11-07-2025", "vertrek": "14-07-2025", "prijs": "489,00€", "reistijd": "03:30", "url": "https://www.centerparcs.nl/nl-nl/frankrijk/fp_VN_vakantiepark-villages-nature-paris/cottages"},
        {"naam": "Park Bostalsee", "coord": (49.628681, 7.060794), "aankomst": "14-07-2025", "vertrek": "18-07-2025", "prijs": "929,00€", "reistijd": "04:04", "url": "https://www.centerparcs.nl/nl-nl/duitsland/fp_BT_vakantiepark-park-bostalsee/cottages"},
        {"naam": "Landal Winterberg", "coord": (51.250104, 8.505771), "aankomst": "18-07-2025", "vertrek": "21-07-2025", "prijs": "517,00€", "reistijd": "03:27", "url": "https://www.landal.nl/parken/winterberg/accommodaties/4u"},
    ],
    4: [
        {"naam": "Landal Dwergter Sand", "coord": (52.899328, 7.972639), "aankomst": "07-07-2025", "vertrek": "11-07-2025", "prijs": "384,00€", "reistijd": "02:55", "url": "https://www.landal.nl/parken/dwergter-sand/accommodaties/6b"},
        {"naam": "Beach Park Travemünde", "coord": (54.006803, 10.887223), "aankomst": "11-07-2025", "vertrek": "14-07-2025", "prijs": "619,00€", "reistijd": "02:59", "url": "https://www.landal.nl/parken/travemunde/accommodaties/4b"},
        {"naam": "Vakantiepark Salztal Paradies", "coord": (51.644475, 10.543187), "aankomst": "14-07-2025", "vertrek": "18-07-2025", "prijs": "792,00€", "reistijd": "03:46", "url": "https://www.landal.nl/parken/salztal-paradies/accommodaties/2a"},
        {"naam": "Landal Winterberg", "coord": (51.250104, 8.505771), "aankomst": "18-07-2025", "vertrek": "21-07-2025", "prijs": "517,00€", "reistijd": "03:27", "url": "https://www.landal.nl/parken/winterberg/accommodaties/4u"},
    ],
    5: [
        {"naam": "Village les Gottales", "coord": (50.370823, 5.862867), "aankomst": "07-07-2025", "vertrek": "11-07-2025", "prijs": "347,00€", "reistijd": "03:02", "url": "https://www.landal.nl/parken/village-les-gottales/accommodaties/2a"},
        {"naam": "Center parcs Villages Nature Paris", "coord": (48.832250, 2.832722), "aankomst": "11-07-2025", "vertrek": "14-07-2025", "prijs": "489,00€", "reistijd": "03:30", "url": "https://www.centerparcs.nl/nl-nl/frankrijk/fp_VN_vakantiepark-villages-nature-paris/cottages"},
        {"naam": "Les Bois-Francs", "coord": (48.728389, 0.840083), "aankomst": "14-07-2025", "vertrek": "18-07-2025", "prijs": "857,00€", "reistijd": "02:01", "url": "https://www.centerparcs.nl/nl-nl/frankrijk/fp_BF_vakantiepark-les-bois-francs/cottages"},
        {"naam": "Roompot Noordzee Résidence Cadzand-Bad", "coord": (51.432947, 3.376430), "aankomst": "18-07-2025", "vertrek": "21-07-2025", "prijs": "874,00€", "reistijd": "04:51", "url": "https://www.landal.nl/parken/roompot-noordzee-residence-cadzand-bad/accommodaties/bungalow-4-comfort"},
    ],
    6: [
        {"naam": "Landal Winterberg", "coord": (51.250104, 8.505771), "aankomst": "07-07-2025", "vertrek": "11-07-2025", "prijs": "573,00€", "reistijd": "03:40", "url": "https://www.landal.nl/parken/winterberg/accommodaties/4u"},
        {"naam": "Vakantiepark Salztal Paradies", "coord": (51.644475, 10.543187), "aankomst": "11-07-2025", "vertrek": "14-07-2025", "prijs": "636,00€", "reistijd": "02:36", "url": "https://www.landal.nl/parken/salztal-paradies/accommodaties/2a"},
        {"naam": "Park Nordseeküste", "coord": (53.647839, 8.267665), "aankomst": "14-07-2025", "vertrek": "18-07-2025", "prijs": "502,00€", "reistijd": "03:12", "url": "https://www.centerparcs.nl/nl-nl/duitsland/fp_BK_vakantiepark-park-nordseekuste/cottages"},
        {"naam": "Waterpark de Bloemert", "coord": (53.145521, 6.677447), "aankomst": "18-07-2025", "vertrek": "21-07-2025", "prijs": "425,00€", "reistijd": "02:18", "url": "https://www.landal.nl/parken/de-bloemert/accommodaties/4b"},
    ],
    7:  [ 
        {"naam": "Landal Dwergter Sand", "coord": (52.899328, 7.972639), "aankomst": "07-07-2025", "vertrek": "11-07-2025", "prijs": "384,00€", "reistijd": "02:55", "url": "https://www.landal.nl/parken/dwergter-sand/accommodaties/6b"},
        {"naam": "Center parcs park Eifel", "coord": (50.257889, 6.976639), "aankomst": "11-07-2025", "vertrek": "14-07-2025", "prijs": "413,00€", "reistijd": "03:59", "url": "https://www.centerparcs.nl/nl-nl/duitsland/fp_HE_vakantiepark-park-eifel/cottages"},
        {"naam": "Village les Gottales", "coord": (50.370823, 5.862867), "aankomst": "14-07-2025", "vertrek": "18-07-2025", "prijs": "497,00€", "reistijd": "01:42", "url": "https://www.landal.nl/parken/village-les-gottales/accommodaties/2a"},
        {"naam": "Vakantiepark De Strabrechtse Vennen", "coord":(51.419159, 5.660626), "aankomst": "18-07-2025", "vertrek": "21-07-2025", "prijs": "531,00€", "reistijd": "01:58", "url": "https://www.landal.nl/parken/strabrechtse-vennen/accommodaties/4b3"}

    ],
    8: [
        {"naam": "Landal Dwergter Sand", "coord": (52.89932801940473, 7.972638939044459), "aankomst": "07-07-2025", "vertrek": "11-07-2025", "prijs": "329,00€", "reistijd": "02:55", "url": "https://www.landal.nl/parken/dwergter-sand/accommodaties/6b#filter:eyJhIjoiMDctMDctMjAyNSIsImQiOiIxMS0wNy0yMDI1IiwibmQiOjUsInN0Ijo5MjV9"},
        {"naam": "landal winterberg", "coord": (51.250104258366605, 8.505770970179324), "aankomst": "11-07-2025", "vertrek": "14-07-2025", "prijs": "417,00€", "reistijd": "02:45", "url": "https://www.landal.nl/parken/winterberg/accommodaties/4u#filter:eyJhIjoiMTEtMDctMjAyNSIsImQiOiIxNC0wNy0yMDI1IiwibmQiOjUsInN0Ijo5MjV9"},
        {"naam": "landal Wirfttal", "coord": (50.40179589840707, 6.520959575999275), "aankomst": "14-07-2024", "vertrek": "18-07-2024", "prijs": "641,00€", "reistijd": "02:58", "url": "https://www.landal.nl/parken/wirfttal/prijzen-en-beschikbaarheid#filter:eyJhIjoiMTQtMDctMjAyNSIsImQiOiIxOC0wNy0yMDI1Iiwic28iOiIyIiwic3QiOjkyNSwicyI6IjMifQ=="},
        {"naam": "Vakantiepark De Strabrechtse Vennen", "coord": (51.41915963603968, 5.660626570692307), "aankomst": "18-07-2025", "vertrek": "21-07-2025", "prijs": "531,00€", "reistijd": "01:58", "url": "https://www.landal.nl/parken/strabrechtse-vennen/accommodaties/4b3#filter:eyJhIjoiMTgtMDctMjAyNSIsImQiOiIyMS0wNy0yMDI1IiwibmQiOjUsInN0Ijo5MjV9"}
    ],
    9: [
        {"naam": "Landal Dwergter Sand", "coord": (52.89932801940473, 7.972638939044459), "aankomst": "07-07-2025", "vertrek": "11-07-2025", "prijs": "329,00€", "reistijd": "02:55", "url": "https://www.landal.nl/parken/dwergter-sand/accommodaties/6b#filter:eyJhIjoiMDctMDctMjAyNSIsImQiOiIxMS0wNy0yMDI1IiwibmQiOjUsInN0Ijo5MjV9"},
        {"naam": "landal Wirfttal", "coord": (50.40179589840707, 6.520959575999275), "aankomst": "11-07-2024", "vertrek": "18-07-2025", "prijs": "900,00€", "reistijd": "03:42", "url": "https://www.landal.nl/parken/wirfttal/prijzen-en-beschikbaarheid#filter:eyJhIjoiMDctMDctMjAyNSIsImQiOiIxNC0wNy0yMDI1Iiwic28iOiIyIiwic3QiOjk2OCwicyI6IjMifQ=="},
        {"naam": "Park Hochsauerland", "coord": (51.2413892921702, 8.685450860760298), "aankomst": "18-07-2025", "vertrek": "21-07-2025", "prijs": "537,00€", "reistijd": "03:04", "url": "https://www.centerparcs.nl/nl-nl/duitsland/fp_SL_vakantiepark-park-hochsauerland/cottages?market=nl&language=nl&c=CPE_PRODUCT&univers=cpe&type=PRODUCT_COTTAGES&item=SL&currency=EUR&group=housing&sort=price&asc=asc&page=1&nb=30&displayPrice=default&dateuser=1&facet[DISPO]=-1&facet[DATE]=2025-07-18&facet[DATEEND]=2025-07-21&facet[COUNTRYSITE][]=l2_SL&facet[MULTIPARTICIPANTS][0][adult]=2&facet[MULTIPARTICIPANTS][0][pet]=0&facet[PROMOCODE][portalCode]=partal_b2c"}
    ],
    10: [
        {"naam": "Landal Dwergter Sand", "coord": (52.89932801940473, 7.972638939044459), "aankomst": "07-07-2025", "vertrek": "14-07-2025", "prijs": "599,00€", "reistijd": "02:55", "url": "https://www.landal.nl/parken/dwergter-sand/prijzen-en-beschikbaarheid#filter:eyJhIjoiMDctMDctMjAyNSIsImFhIjowLCJhYiI6MCwiZCI6IjE0LTA3LTIwMjUiLCJuIjo3LCJzbyI6IjIiLCJzdCI6OTY4LCJzIjoiMyJ9"},
        {"naam": "landal Wirfttal", "coord": (50.40179589840707, 6.520959575999275), "aankomst": "14-07-2025", "vertrek": "18-07-2024", "prijs": "641,00€", "reistijd": "03:42", "url": "https://www.landal.nl/parken/wirfttal/prijzen-en-beschikbaarheid#filter:eyJhIjoiMTQtMDctMjAyNSIsImQiOiIxOC0wNy0yMDI1Iiwic28iOiIyIiwic3QiOjkyNSwicyI6IjMifQ=="},
        {"naam": "Park Eksel", "coord": (51.188300788507746, 5.392464527114761), "aankomst": "18-07-2024", "vertrek": "21-07-2024", "prijs": "525,00€", "reistijd": "02:03", "url": "https://www.landal.nl/parken/roompot-park-eksel/prijzen-en-beschikbaarheid#filter:eyJhIjoiMTgtMDctMjAyNSIsImFhIjowLCJhYiI6MCwiZCI6IjIxLTA3LTIwMjUiLCJuIjozLCJzbyI6IjIiLCJzdCI6OTI1LCJzIjoiMyJ9"}
    ]
}


# === UI ===
st.title("Zomervakantieplanner 2025")

vakantie_type = st.selectbox("Kies vakantiesoort", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# === KAART ===
# Voeg bovenaan toe
weesp = {"naam": "Startpunt: Sinnigvelderstraat, Weesp", "coord": (52.3075, 5.0422)}

# Voeg toe aan het begin van locaties
locaties = [weesp] + vakanties[vakantie_type] + [weesp]  # Start en eindpunt toevoegen

data = [
    {
        "Park": p["naam"],
        "Aankomst": p["aankomst"],
        "Vertrek": p["vertrek"],
        "Totaalprijs": p["prijs"],
        "Link": p["url"]
    }
    for p in vakanties[vakantie_type]
]



df = pd.DataFrame(data)
df.index += 1
df["Link"] = df["Link"].apply(lambda x: f"[Bekijk accommodatie]({x})")
st.subheader("Vakantieoverzicht")
st.dataframe(df.drop(columns="Link", errors="ignore"), use_container_width=True)

# Maak de kaart gebaseerd op Weesp
kaart = folium.Map(location=(51.28083911392615, 6.788471604666769), zoom_start=6)

# Markers
for plek in locaties:
    if "aankomst" in plek:
        popup_html = f"""
        <b>{plek['naam']}</b><br>
        Aankomst: {plek['aankomst']}<br>
        Vertrek: {plek['vertrek']}<br>
        Totaal prijs: {plek['prijs']}<br>
        <a href="{plek['url']}" target="_blank">Bekijk de accommodatie</a>
        """
    else:
        popup_html = f"<b>{plek['naam']}</b>"

    folium.Marker(
        location=plek["coord"],
        tooltip=plek["naam"],
        icon=folium.DivIcon(html=f'<div style="font-size: 24px;">🏠</div>'),
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(kaart)

# Reistijd-annotatie + lijnen (reistijd uit data alleen tussen vakantielocaties)
terug_reistijden = {
    "Landal Winterberg": "03:20",
    "Center parcs Villages Nature Paris": "05:03",
    "Roompot Noordzee Résidence Cadzand-Bad": "02:39",
    "Waterpark de bloemert": "01:56",
    "Vakantiepark De Strabrechtse Vennen": "01:44",
    "Park Hochsauerland": "03:34",
    "Park Eksel": "02:10"
}

for i in range(len(locaties) - 1):
    start = locaties[i]["coord"]
    end = locaties[i + 1]["coord"]
    if locaties[i + 1]["naam"].startswith("Startpunt"):
        # terugrit
        laatste = locaties[i]["naam"]
        reistijd = terug_reistijden.get(laatste, "03:00")
    else:
        reistijd = locaties[i + 1].get("reistijd", "")
    AntPath([start, end], dash_array=[10, 20], color='blue', weight=3).add_to(kaart)
    mid_lat = (start[0] + end[0]) / 2
    mid_lon = (start[1] + end[1]) / 2
    if reistijd:
        folium.Marker(
            location=(mid_lat, mid_lon),
            icon=folium.DivIcon(html=f'<div style="font-size: 18px; color: black;">{reistijd}</div>')
        ).add_to(kaart)


from datetime import timedelta

# === TOTAALPRIJS ===
# Strip euro-tekens en komma's voor optellen
prijzen = [float(p["prijs"].replace("€", "").replace(",", ".")) for p in vakanties[vakantie_type]]
totaal_prijs = sum(prijzen)

# === TOTALE REISTIJD ===
def parse_tijd(t):
    h, m = map(int, t.split(":"))
    return timedelta(hours=h, minutes=m)

# Verzamel reistijden tussen alle locaties
reistijden = []

# Tussen de vakantielocaties
reistijden += [plek["reistijd"] for plek in vakanties[vakantie_type][1:]]

# Sommeer alle tijden
totale_tijd = sum([parse_tijd(t) for t in reistijden], timedelta())
uren, rest = divmod(totale_tijd.seconds, 3600)
minuten = rest // 60

# === Tonen ===
st.markdown(f"**Totaalprijs vakantie:** €{totaal_prijs:,.2f}")
st.markdown(f"**Totale reistijd:** {uren} uur en {minuten} minuten")

# === Tonen in Streamlit ===
st_folium(kaart, width=800, height=600)

# === Hulpfunctie ===
import pandas as pd
from datetime import timedelta

# Hulpfunctie voor tijdconversie
def parse_tijd(t):
    h, m = map(int, t.split(":"))
    return timedelta(hours=h, minutes=m)

import pandas as pd
from datetime import timedelta

# --- Hulpfunctie ---
def parse_tijd(t):
    h, m = map(int, t.split(":"))
    return timedelta(hours=h, minutes=m)

# --- Gegevens per vakantiesoort ---
terugreistijd = {
    1: "05:03",
    2: "05:03",
    3: "03:20",
    4: "03:20",
    5: "02:39",
    6: "01:56",
    7: "01:41",
    8: "01:41",
    9: "03:34",
    10: "02:10"
}

# Voorbeelddata (gebruik je eigen vakanties-structuur)
vakantie_data = vakanties  # neem deze over uit je hoofdsysteem

st.subheader("Activiteiten per locatie")
activiteiten_per_park = {
    "Landal Dwergter Sand": [
        {
            "titel": "🌳 Wandelen en fietsen in het natuurgebied Dwergter Sand",
            "uitleg": "Direct vanaf het park kun je prachtige wandel- en fietsroutes volgen door bossen, heidevelden en langs vennetjes. Het gebied biedt diverse routes voor zowel beginners als gevorderden."
        },
        {
            "titel": "🏞️ Bezoek aan het Thülsfelder Talsperre recreatiegebied",
            "uitleg": "Op slechts 12 km afstand ligt dit stuwmeer waar je kunt wandelen, fietsen, zwemmen en picknicken. Er zijn ook avonturenpaden en een klimbos voor de avontuurlijke bezoekers."
        },
        {
            "titel": "🏰 Museumdorp Cloppenburg",
            "uitleg": "Op ongeveer 13 km afstand vind je dit openluchtmuseum met meer dan 50 historische gebouwen die het leven in het Oldenburger Münsterland van vroeger laten zien. Een educatief uitje voor het hele gezin."
        },
        {
            "titel": "🐾 Tier- und Freizeitpark Thüle",
            "uitleg": "Op ongeveer 9 km afstand ligt dit dieren- en attractiepark met meer dan 600 dieren en diverse attracties voor jong en oud. Een perfecte combinatie van dierentuin en pretpark."
        },
        {
            "titel": "🏰 Schloss Clemenswerth in Sögel",
            "uitleg": "Dit barokke jachtslot, gelegen op ongeveer 40 km afstand, is omringd door een stervormig park en biedt een kijkje in het leven van de adel in de 18e eeuw. Het complex omvat meerdere paviljoens en een museum."
        },
        {
            "titel": "🛍️ Stad Oldenburg",
            "uitleg": "Op ongeveer 40 minuten rijden ligt deze gezellige stad met een autovrij centrum, diverse winkels, cafés en restaurants. Bezoek ook het kasteel en het bijbehorende kunstmuseum."
        }
    ],
    "Center parcs park Eifel" : [
    {
        "titel": "🏎️ Bezoek de Nürburgring",
        "uitleg": "Op slechts 15 km afstand ligt het wereldberoemde racecircuit Nürburgring. Hier kun je het motorsportmuseum Ring°werk bezoeken of zelfs zelf rijden op het circuit tijdens speciale evenementen."
    },
    {
        "titel": "🏰 Ontdek Burg Eltz",
        "uitleg": "Een van de mooiste kastelen van Duitsland, Burg Eltz, ligt op ongeveer 50 km afstand. Het kasteel is prachtig gelegen in een bosrijke omgeving en biedt rondleidingen aan."
    },
    {
        "titel": "🌋 Verken het Vulkanpark",
        "uitleg": "Leer alles over de vulkanische geschiedenis van de Eifel in het Vulkanpark, met interactieve tentoonstellingen en wandelroutes langs oude vulkaankraters."
    },
    {
        "titel": "🐾 Wild- & Erlebnispark Daun",
        "uitleg": "Op ongeveer 30 km afstand vind je dit wildpark waar je met de auto doorheen kunt rijden en dieren zoals herten en lama’s van dichtbij kunt zien."
    },
    {
        "titel": "🎨 Bezoek het Eifelmuseum in Mayen",
        "uitleg": "Leer meer over de geschiedenis en cultuur van de Eifel in dit museum, met tentoonstellingen over vulkanisme, mijnbouw en lokale tradities."
    },
    {
        "titel": "🛶 Kanoën op de rivier de Ahr",
        "uitleg": "Geniet van een ontspannen kanotocht op de rivier de Ahr, die door pittoreske dorpjes en wijngaarden slingert."
    }
    ],
    "landal Vakantiepark Hochwald" : [
    {
        "titel": "🏰 Bezoek aan Trier",
        "uitleg": "Trier, de oudste stad van Duitsland, ligt op ongeveer 27 km afstand. Ontdek de rijke Romeinse geschiedenis met bezienswaardigheden zoals de Porta Nigra, het amfitheater en de keizerlijke thermen."
    },
    {
        "titel": "🛩️ Flugausstellung L.+P. Junior in Hermeskeil",
        "uitleg": "Slechts 15 km van het park bevindt zich dit luchtvaartmuseum met meer dan 40 vliegtuigen en een café in een echte Concorde."
    },
    {
        "titel": "🎿 Zomerrodelbaan en klimpark Erbeskopf",
        "uitleg": "Op ongeveer 30 km afstand kun je rodelen op een 747 meter lange baan en klimmen in het bosklimparcours."
    },
    {
        "titel": "💎 Edelsteenstad Idar-Oberstein",
        "uitleg": "Op ongeveer 50 km afstand ligt deze stad, bekend om zijn edelstenen. Bezoek de edelsteenmijnen en leer meer over de verwerking van edelstenen."
    },
    {
        "titel": "🔥 Brandweer Experience Museum",
        "uitleg": "Op ongeveer 15 km afstand kun je hier alles leren over de geschiedenis en het werk van de brandweer."
    },
    {
        "titel": "🌲 Wandelen en fietsen in Nationaal Park Hunsrück-Hochwald",
        "uitleg": "Op slechts 27 km van het park ligt dit prachtige nationale park met uitgestrekte bossen, heidevelden en rotsformaties. Het gebied biedt diverse wandel- en fietsroutes voor zowel beginners als gevorderden."
    }
    ],
    "Center parcs Villages Nature Paris": [
    {
        "titel": "🏰 Disneyland® Paris",
        "uitleg": "Op slechts 10 minuten rijden ligt het wereldberoemde Disneyland® Paris. Beleef de magie van attracties, shows en parades voor het hele gezin."
    },
    {
        "titel": "🏊 Aqualagon",
        "uitleg": "Binnen het park vind je Aqualagon, een tropisch zwemparadijs met glijbanen, een lazy river en een ‘Water Tree’ die 900 liter water uitstort."
    },
    {
        "titel": "🍷 Wijnproeverijen",
        "uitleg": "De regio staat bekend om zijn wijnen. Bezoek een lokale wijngaard voor een proeverij en leer meer over de Franse wijncultuur."
    },
    {
        "titel": "🛶 Wateractiviteiten",
        "uitleg": "Huur een kano, waterfiets of motorboot en verken de meren en waterwegen in de omgeving van het park."
    },
    {
        "titel": "🎭 Culturele uitstapjes naar Parijs",
        "uitleg": "Binnen 45 minuten ben je in het centrum van Parijs. Bezoek iconische bezienswaardigheden zoals de Eiffeltoren, het Louvre en de Notre-Dame."
    }
    ],
    "landal winterberg": [
    {
        "titel": "🚵 Bikepark Winterberg",
        "uitleg": "Een avonturenpark voor mountainbikers met 13 verschillende tracks, geschikt voor zowel beginners als professionals."
    },
    {
        "titel": "🐾 Wildpark Willingen",
        "uitleg": "Op ongeveer 18 km afstand kun je hier wilde dieren van dichtbij bekijken en genieten van een sprookjesachtig pad en een vogeltentoonstelling."
    },
    {
        "titel": "🏔️ Kahler Asten",
        "uitleg": "De bekendste berg van het Sauerland op ongeveer 5 km afstand. Biedt een toren met panoramisch uitzicht en een restaurant."
    },
    {
        "titel": "🛷 Zomerrodelbaan Winterberg",
        "uitleg": "Een 700 meter lange rodelbaan op rails, geschikt voor alle leeftijden. Gelegen op Erlebnisberg Kappe."
    },
    {
        "titel": "🧗 Klimbos Winterberg",
        "uitleg": "Een avontuurlijk klimbos met vijf verschillende parcoursen, snelle kabelbanen en wiebelige bruggen tussen de boomtoppen."
    }
    ],
    "Village les Gottales": [
    {
        "titel": "🌊 Watervallen van Coo",
        "uitleg": "Bezoek de hoogste watervallen van België en geniet van het indrukwekkende uitzicht. Je kunt er ook kajakken of met een stoellift omhoog gaan."
    },
    {
        "titel": "🏎️ Circuit Spa-Francorchamps",
        "uitleg": "Bezoek het beroemde Formule 1-circuit en ervaar een dag vol spanning en snelle bolides."
    },
    {
        "titel": "🏰 Abdij van Stavelot",
        "uitleg": "Ontdek de geschiedenis van een van de oudste kloosterfunderingen van België met drie musea in één."
    },
    {
        "titel": "🐾 Forestia",
        "uitleg": "Bezoek dit dierenpark midden in het bos en ontdek beren, elanden en lynxen."
    },
    {
        "titel": "🏞️ Ninglinspo Vallei",
        "uitleg": "Maak een prachtige wandeling door de enige bergrivier van België en geniet van de natuurlijke schoonheid."
    },
    {
        "titel": "🧗 Coo Adventure",
        "uitleg": "Voor de avontuurlijke vakantieganger biedt Coo Adventure activiteiten zoals klimmen, abseilen en mountainbiken."
    }],
    "Park Bostalsee" : [
    {
        "titel": "🌊 Watersporten op de Bostalsee",
        "uitleg": "Geniet van zeilen, windsurfen, kanoën, zwemmen en vissen op de 120 hectare grote Bostalsee. Er is ook een strandbad en een 7 km lang wandelpad rondom het meer."
    },
    {
        "titel": "🧗 Klimmen in het Hochseilgarten",
        "uitleg": "Beleef een avontuurlijke dag in het klimpark met diverse parcoursen voor jong en oud."
    },
    {
        "titel": "🏛️ Bezoek het Museum für Mode und Tracht",
        "uitleg": "Ontdek kleding en kleedgewoonten uit het verleden in dit unieke museum in Nohfelden."
    },
    {
        "titel": "🌌 Sterren kijken bij de Sternwarte Peterberg",
        "uitleg": "Bezoek het observatorium op de 584 meter hoge Peterberg voor een blik op het heelal."
    },
    {
        "titel": "🌿 Wandelen in het Buchwald",
        "uitleg": "Verken het Buchwald met zijn 250 jaar oude lariksen, een historische houtskooloven en de grootste Douglasspar van Zuidwest-Duitsland."
    }],
    "Beach Park Travemünde": [
    {
        "titel": "⚓ Viermaster Passat",
        "uitleg": "Bezoek dit historische zeilschip, een van de laatste viermasters ter wereld, dat nu dienstdoet als museumschip."
    },
    {
        "titel": "🛳️ Panoramaschip MS Hanse (naast het park)",
        "uitleg": "Maak een dagtocht per boot naar de Hanzestad Lübeck en geniet van het uitzicht op zee."
    },
    {
        "titel": "🏰 Lübeck",
        "uitleg": "Ontdek de historische binnenstad van Lübeck, een UNESCO-werelderfgoed, met zijn middeleeuwse architectuur en musea."
    },
    {
        "titel": "🐠 Ostseestation Travemünde",
        "uitleg": "Leer meer over het zeeleven van de Oostzee in dit interactieve aquarium en educatief centrum."
    },
    {
        "titel": "🌊 Brodtener Steilufer",
        "uitleg": "Maak een wandeling langs deze indrukwekkende klifkust met panoramisch uitzicht over de Oostzee."
    }],
    "Vakantiepark Salztal Paradies": [
    {
        "titel": "🏛️ Bezoek aan het Grenzlandmuseum",
        "uitleg": "Het Grenzlandmuseum in Bad Sachsa biedt inzicht in de geschiedenis van de Duitse deling en de impact ervan op de regio. Een educatieve ervaring voor geschiedenisliefhebbers."
    },
    {
        "titel": "⛪ Bezoek aan het Kloster Walkenried",
        "uitleg": "Het Kloster Walkenried is een voormalig cisterciënzerklooster en staat op de UNESCO-werelderfgoedlijst. Verken de gotische architectuur en leer meer over de geschiedenis van het klooster."
    },
    {
        "titel": "🏰 Stadsbezoek aan Wernigerode",
        "uitleg": "Wernigerode is een schilderachtige stad met vakwerkhuizen en een indrukwekkend kasteel. Het is een perfecte bestemming voor een dagtrip om de lokale cultuur en geschiedenis te ervaren."
    },
    {
        "titel": "🚤 Boottocht op de Odertalsperre",
        "uitleg": "Maak een ontspannen boottocht op het stuwmeer Odertalsperre en geniet van het uitzicht op de omliggende natuur. Een rustige activiteit om de dag mee af te sluiten."
    },
    {
        "titel": "🏘️  Bezoek aan Quedlinburg",
        "uitleg": "Quedlinburg is een historische stad met meer dan 1.000 vakwerkhuizen en staat op de UNESCO-werelderfgoedlijst. Dwaal door de geplaveide straatjes en geniet van de middeleeuwse sfeer."
    }],
    "Les Bois-Francs": [
    {
        "titel": "🏘️ Verken het middeleeuwse Verneuil-sur-Avre",
        "uitleg": "Dwaal door de geplaveide straatjes van Verneuil-sur-Avre en bewonder de vakwerkhuizen, de imposante Église de la Madeleine en de Tour Grise, een overblijfsel van het oude kasteel."
    },
    {
        "titel": "🕍 Bezoek de Abbaye Saint-Nicolas",
        "uitleg": "Ontdek deze voormalige benedictijnenabdij uit 1627, nu een cultureel centrum, met zijn historische architectuur en serene sfeer."
    },
    {
        "titel": "🏯 Bezoek het Château de Verneuil-sur-Avre",
        "uitleg": "Bewonder de overblijfselen van dit middeleeuwse kasteel, waaronder de imposante Tour Grise, en leer meer over de geschiedenis van de regio."
    },
    {
        "titel": "🚆 Maak een dagtocht naar Chartres",
        "uitleg": "Ontdek de stad Chartres met zijn beroemde kathedraal, charmante straatjes en diverse musea, op ongeveer een uur rijden van het vakantiepark."
    },
    {
        "titel": "🌊 Bezoek het Becquet de l’Iton",
        "uitleg": "Bekijk dit historische waterbouwkundige werk uit de 12e eeuw, dat diende om de waterstroom van de Iton te reguleren."
    },
    {
        "titel": "🌲 Verken het natuurgebied Forêt de Breteuil",
        "uitleg": "Maak een wandeling of fietstocht door dit uitgestrekte bosgebied, ideaal voor natuurliefhebbers en rustzoekers."
    }],
    "Roompot Noordzee Résidence Cadzand-Bad": [
    {
        "titel": "🐦  Bezoek aan natuurgebied Het Zwin",
        "uitleg": "Ontdek het unieke natuurgebied Het Zwin, bekend om zijn zilte vegetatie en rijke vogelpopulatie. Een gids kan je meenemen op een wandeling door dit bijzondere landschap."
    },
    {
        "titel": "🏙️ Dagtrip naar Brugge",
        "uitleg": "Maak een uitstapje naar het historische Brugge, op ongeveer een uur rijden. Verken de middeleeuwse straatjes, bezoek musea en geniet van de Vlaamse gastronomie."
    },
    {
        "titel": "🛍️ Bezoek aan Sluis",
        "uitleg": "Ontdek het charmante vestingstadje Sluis met zijn gezellige winkelstraten, historische wallen en diverse eetgelegenheden. Een ideale bestemming voor een ontspannen dagje uit."
    },
    {
        "titel": "🎨 Kunst en cultuur in Middelburg",
        "uitleg": "Verken de culturele hoofdstad van Zeeland, Middelburg. Bezoek musea, galerieën en historische gebouwen in deze levendige stad."
    },
    {
        "titel": "🛶 Zeilen of kajakken op de Westerschelde",
        "uitleg": "Voor de avontuurlijke reiziger zijn er mogelijkheden om te zeilen of kajakken op de Westerschelde. Ervaar de Zeeuwse wateren vanuit een uniek perspectief."
    }],
    "Park Nordseeküste": [
    {
        "titel": "🌊 Verken het UNESCO Werelderfgoed Waddenzee",
        "uitleg": "Maak een begeleide wadlooptocht en ontdek het unieke ecosysteem van de Waddenzee. Een bijzondere ervaring waarbij je over de zeebodem loopt tijdens eb."
    },
    {
        "titel": "⚓ Bezoek het Deutsches Marinemuseum in Wilhelmshaven",
        "uitleg": "Ontdek de maritieme geschiedenis van Duitsland in dit museum, waar je onder andere een echte onderzeeër kunt bezichtigen."
    },
    {
        "titel": "🌍 Bezoek het Klimahaus in Bremerhaven",
        "uitleg": "Een interactief museum waar je een reis rond de wereld maakt langs de achtste lengtegraad, met aandacht voor klimaat en duurzaamheid."
    },
    {
        "titel": "🐚 Bezoek het Nationalparkhaus Museum Fedderwardersiel",
        "uitleg": "Leer meer over de flora en fauna van de regio en het belang van het behoud van het Waddengebied in dit informatieve bezoekerscentrum."
    },
    {
        "titel": "🚉 Maak een dagtocht naar Bremerhaven",
        "uitleg": "Verken deze havenstad met attracties zoals het Deutsches Auswandererhaus en het Zoo am Meer, een dierentuin met uitzicht op de Noordzee."
    },
    {
        "titel": "🍽️ Geniet van lokale specialiteiten in Tossens",
        "uitleg": "Proef regionale gerechten in een van de gezellige restaurants in Tossens, zoals verse visgerechten of traditionele Duitse keuken."
    }],
    "Waterpark de Bloemert": [
        {
            "titel": "🏄 Watersport op het Zuidlaardermeer",
            "uitleg": "Geniet van zeilen, windsurfen, suppen of kanoën op het Zuidlaardermeer. Het park beschikt over een eigen jachthaven en zeilschool, en biedt diverse mogelijkheden voor bootverhuur."
        },
        {
            "titel": "🏛️ Bezoek aan Groningen",
            "uitleg": "Ontdek de bruisende stad Groningen, op slechts 20 km afstand. Bezoek het Groninger Museum, beklim de Martinitoren en geniet van de gezellige terrasjes op de Grote Markt."
        },
        {
            "titel": "🕊️ Bezoek aan Herinneringscentrum Kamp Westerbork",
            "uitleg": "Leer meer over de geschiedenis van de Tweede Wereldoorlog in dit indrukwekkende museum, gelegen op ongeveer 30 km van het park."
        },
        {
            "titel": "🪨 Bezoek aan het Hunebedcentrum in Borger",
            "uitleg": "Ontdek de geschiedenis van de hunebedbouwers en bewonder de grootste hunebedden van Nederland in dit informatieve centrum, op ongeveer 30 km afstand."
        },
        {
            "titel": "🌾 Bezoek aan Molenmuseum De Wachter in Zuidlaren",
            "uitleg": "Ontdek de werking van historische molens en proef versgebakken brood in dit museum, gelegen op slechts 3 km van het park."
        },
        {
            "titel": "🚶 Wandelen in het Noordlaarderbos",
            "uitleg": "Maak een ontspannen wandeling in het Noordlaarderbos, gelegen op slechts 10 minuten fietsen van het park. Onderweg kom je langs een hunebed verscholen tussen de bomen."
        }],
    "Vakantiepark De Strabrechtse Vennen": [
    {
        "titel": "🏰 Bezoek aan Kasteel Heeze",
        "uitleg": "Ontdek de geschiedenis en prachtige tuinen van dit middeleeuwse kasteel."
    },
    {
        "titel": "🚲 Wandelen en fietsen in de Strabrechtse Heide",
        "uitleg": "Verken de uitgestrekte heidevelden en bossen direct vanaf het park."
    },
    {
        "titel": "🏛️ Bezoek aan Museum Klok & Peel in Asten",
        "uitleg": "Leer meer over de natuur, cultuur en geschiedenis van de Peelregio en bewonder een van de grootste klokkencollecties ter wereld."
    },
    {
        "titel": "🏙️ Ontdek Eindhoven",
        "uitleg": "Op slechts 20 minuten rijden ligt Eindhoven, met moderne kunstmusea, designwinkels en gezellige eetgelegenheden in de binnenstad."
    },
    {
        "titel": "🛶 Kanoën op de Dommel",
        "uitleg": "Huur een kano en vaar over het rustige riviertje de Dommel, dat door een schilderachtig Brabants landschap slingert."
    },
    {
        "titel": "🦁 Bezoek aan Dierenrijk Nuenen",
        "uitleg": "Ontmoet diverse dieren in dit dierenpark."
    }],
    "Landal Wirfttal": [
    {
        "titel": "💧 Wandeling naar de Dreimühlen-waterval",
        "uitleg": "Deze schilderachtige waterval nabij Nohn is bereikbaar via een mooie wandelroute. Een perfecte plek voor natuurliefhebbers en fotografen."
    },
    {
        "titel": "⛰️ Wandeling naar de Hohe Acht",
        "uitleg": "Beklim de hoogste berg van de Eifel (747 m) en geniet van een panoramisch uitzicht vanaf de Kaiser Wilhelm-toren. Een populaire bestemming voor wandelaars en natuurliefhebbers."
    },
    {
        "titel": "⛪ Bezoek aan de Abdij van Maria Laach",
        "uitleg": "Deze prachtige abdij aan de Laacher See is een voorbeeld van romaanse architectuur. Combineer een bezoek aan de abdij met een wandeling rond het kratermeer."
    },
    {
        "titel": "🪨 Verkenning van de Teufelsschlucht (Duivelskloof)",
        "uitleg": "Deze indrukwekkende kloof met smalle doorgangen en hoge rotswanden biedt een avontuurlijke wandelervaring. Gelegen bij Irrel, is het een unieke geologische bezienswaardigheid."
    },
    {
        "titel": "🏛️ Bezoek aan de stad Trier",
        "uitleg": "Als de oudste stad van Duitsland biedt Trier een schat aan Romeinse overblijfselen, waaronder de Porta Nigra, het amfitheater en de keizerlijke thermen. Een culturele uitstap voor geschiedenisliefhebbers."
    },
    {
        "titel": "🌋 Wandelen in de Vulkaneifel en bezoek aan het Eifel Vulkanmuseum",
        "uitleg": "Verken de unieke geologie van de Vulkaneifel met zijn kratermeren (maaren) en vulkanische landschappen. Leer meer over de vulkanische geschiedenis van de regio in het interactieve museum."
    }],
    "Park Hochsauerland": [
    {
        "titel": "🪨 Bezoek aan de Bruchhauser Steine",
        "uitleg": "Bewonder deze indrukwekkende rotsformaties nabij Olsberg. Een korte wandeling brengt je naar de top, waar je wordt beloond met een panoramisch uitzicht over het Sauerland."
    },
    {
        "titel": "🏛️ Städtisches Museum Medebach",
        "uitleg": "Leer meer over de geschiedenis van Medebach en haar omgeving in dit lokale museum, gevestigd in een historisch gebouw uit de 18e eeuw. De collectie omvat archeologische vondsten en tentoonstellingen over het lokale leven door de eeuwen heen."
    },
    {
        "titel": "🏔️ Kahler Asten",
        "uitleg": "Een van de hoogste toppen van Sauerland (841,9 m) met een uitkijktoren en wandelpaden. Een must-see voor natuurliefhebbers en wandelaars."
    },
    {
        "titel": "⛪ Grafschaft Abdij",
        "uitleg": "Een historische abdij met prachtige barokke architectuur en serene tuinen. Perfect voor een rustige culturele uitstap."
    },
    {
        "titel": "🏰 Burg Altena",
        "uitleg": "Een middeleeuws kasteel met een interessant museum over riddercultuur. Ontdek de geschiedenis van de eerste jeugdherberg ter wereld, die hier gevestigd is."
    }],
    "Park Eksel": [
    {
        "titel": "🪟 Bezoek aan het GlazenHuis in Lommel",
        "uitleg": "Ontdek de kunst van glasblazen en bewonder moderne glaskunst in dit bijzondere museum en atelier."
    },
    {
        "titel": "👗 Bezoek aan het Modemuseum Hasselt",
        "uitleg": "Ontdek de evolutie van mode en textiel door de jaren heen in dit toonaangevende museum in het centrum van Hasselt."
    },
    {
        "titel": "⛪ Sint-Lambertuskerk",
        "uitleg": "Een historisch kerkgebouw met prachtige architectuur en een rijke geschiedenis, gelegen in het hart van Eksel."
    },
    {
        "titel": "🗼 Uitkijktoren Lommelse Sahara",
        "uitleg": "Beklim deze toren voor een panoramisch uitzicht over zandvlaktes, water en bossen. Een prachtig natuurgebied om ook te wandelen of te picknicken."
    },
    {
        "titel": "🚴‍♀️ Fietsen door de Bomen",
        "uitleg": "Een unieke fietservaring op 10 meter hoogte door de boomtoppen in Nationaal Park Bosland. Een van de meest iconische fietsroutes van België."
    }]   
}


for plek in vakanties[vakantie_type]:
    parknaam = plek["naam"]
    activiteiten = activiteiten_per_park.get(parknaam, []) or activiteiten_per_park.get(parknaam.lower(), []) or activiteiten_per_park.get(parknaam.title(), [])
    if activiteiten:
        st.markdown(f"### 📍 {parknaam}")
        for i, act in enumerate(activiteiten, 1):
            with st.expander(f"🔹 {i}. {act['titel']}"):
                st.markdown(act['uitleg'])
        st.markdown("---")
        
# --- Tabel samenstellen ---
rows = []
for soort, items in vakantie_data.items():
    prijs = sum(float(p["prijs"].replace("€", "").replace(",", ".")) for p in items)
    reistijd = sum([parse_tijd(p["reistijd"]) for p in items], timedelta()) + parse_tijd(terugreistijd[soort])
    uren, rest = divmod(reistijd.seconds, 3600)
    minuten = rest // 60
    totaal_min = int(reistijd.total_seconds() // 60)
    rows.append({
        "Vakantiesoort": soort,
        "Totaalprijs (€)": prijs,
        "Totale reistijd": f"{uren} uur {minuten} min",
        "Totale reistijd (min)": totaal_min  # voor sortering
    })

df = pd.DataFrame(rows).set_index("Vakantiesoort")

# --- Tabel tonen met sortering ---

st.subheader("Vakantieoverzicht (sorteerbaar)")
st.dataframe(df.drop(columns="Totale reistijd (min)"), use_container_width=True)