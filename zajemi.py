import re
import orodja


vzorec_bloka = re.compile(
    r'<tr bgcolor.*?'
    r'</table>(</p>)?</td></tr>'
)

vzorec = re.compile(
    r'<tr bg.*/\d+/(?P<id>.*)">&nbsp;(?P<gora>.*)</a></td><td>&nbsp.*?">(?P<višina>.*?) m</a>.*" width="(?P<priljubljenost>.*?)%.*</tr>'
)

#ime_gorovja = re.compile(r'<title>(.*)</title>')

slovar_povezav = {"Goriško, Notranjsko in Snežniško hribovje" : "https://www.hribi.net/gorovje/gorisko_notranjsko_in_sneznisko_hribovje/26", "Julijske Alpe" : "https://www.hribi.net/gorovje/julijske_alpe/1", "Kamniško Savinjske Alpe" : "https://www.hribi.net/gorovje/kamnisko_savinjske_alpe/3", "Karavanke" : "https://www.hribi.net/gorovje/karavanke/11", "Pohorje in ostala severovzhodna Slovenija" : "https://www.hribi.net/gorovje/pohorje_in_ostala_severovzhodna_slovenija/4", "Polhograjsko hribovje in Ljubljana" : "https://www.hribi.net/gorovje/polhograjsko_hribovje_in_ljubljana/5", "Škofjeloško, Cerkljansko hribovje in Jelovica" : "https://www.hribi.net/gorovje/skofjelosko_cerkljansko_hribovje_in_jelovica/21", "Zasavsko - Posavsko hribovje in Dolenjska" : "https://www.hribi.net/gorovje/zasavsko_-_posavsko_hribovje_in_dolenjska/25"}

def uredi(blok, url):
    gora = vzorec.search(blok).groupdict()
    gora["id"] = int(gora["id"])
    gora["višina"] = int(gora["višina"])
    gora["priljubljenost"] = int(gora["priljubljenost"])
    for i in slovar_povezav.keys():
        if slovar_povezav[i] == url:
            imegorovja = i
    gora["gorovje"] = imegorovja
    return gora

def najdi(url):
    for i in slovar_povezav.keys():
        if slovar_povezav[i] == url:
            gorovje = i
    datoteka = f'gorovja/{gorovje}.html'
    orodja.shrani_spletno_stran(url, datoteka)
    vsebina = orodja.vsebina_datoteke(datoteka)
    for blok in vzorec_bloka.finditer(vsebina):
        yield uredi(blok.group(0), url)

seznam = []
for gorovje in slovar_povezav.values():
    for neki in najdi(gorovje):
        seznam.append(neki)  

orodja.zapisi_json(seznam, "obdelani-podatki/hribi.json")  
orodja.zapisi_csv(seznam, ["id", "gora", "višina", "priljubljenost", "gorovje"], "obdelani-podatki/hribi.csv")
