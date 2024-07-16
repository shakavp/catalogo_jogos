import requests
import json
import time

from bs4 import BeautifulSoup
from urllib.request import urlopen

PS3 = "PS_3"
PS4 = "PS_4"
PS5 = "PS_5"
VITA = "VITA"
NINTENDO_3DS = "N3DS"
NINTENDO_SWITCH = "SWIT"

DAYS_1 = 1*24*60*60
HOURS_6 = 12*60*60

COMPLETE = ("Complete", "Completo")
NEW = ("New", "Novo")

GAMES = [
    (PS4, "Life Is Strange: True Colors (US)",
        r"https://www.pricecharting.com/game/playstation-4/life-is-strange-true-colors",
        NEW),
    (PS5, "Retunal (US)",
        r"https://www.pricecharting.com/game/playstation-5/returnal",
        COMPLETE),
    (PS5, "A Plague Tale: Requiem (US)",
        r"https://www.pricecharting.com/game/playstation-5/a-plague-tale-requiem",
        COMPLETE),
    (PS4, "South Park: The Stick Of Truth (US)",
        r"https://www.pricecharting.com/game/playstation-4/south-park-the-stick-of-truth",
        NEW),
    (PS3, "Max Payne 3 (US)",
        r"https://www.pricecharting.com/game/playstation-3/max-payne-3",
        COMPLETE),
    (NINTENDO_3DS, "Zelda Ocarina Of Time 3D (US)",
        r"https://www.pricecharting.com/game/nintendo-3ds/zelda-ocarina-of-time-3d",
        COMPLETE),
    (VITA, "Persona 4 Golden (US)",
        r"https://www.pricecharting.com/game/pal-playstation-vita/persona-4-golden",
        COMPLETE),
    (NINTENDO_SWITCH, "Pokemon Let's Go Pikachu (US)",
        r"https://www.pricecharting.com/game/nintendo-switch/pokemon-let%27s-go-pikachu",
        NEW),
    (PS5, "Persona 5 Tactica (US)",
        r"https://www.pricecharting.com/pt/game/playstation-5/persona-5-tactica",
        NEW),
    (PS5, "Alex Kidd In Miracle World DX (PAL)",
        r"https://www.pricecharting.com/pt/game/pal-playstation-5/alex-kidd-in-miracle-world-dx",
        NEW),
    (PS5, "Sea Of Stars (US)",
        r"https://www.pricecharting.com/pt/game/playstation-5/sea-of-stars",
        NEW),
    (PS5, "Sand Land (US)",
        r"https://www.pricecharting.com/pt/game/playstation-5/sand-land",
        NEW),
    (PS5, "Unicorn Overlord (US)",
        r"https://www.pricecharting.com/game/playstation-5/unicorn-overlord",
        NEW),
    (PS5, "Persona 3 Reload (US)",
        r"https://www.pricecharting.com/game/playstation-5/persona-3-reload",
        NEW),
    (PS5, "Marvel Spider-Man 2 (US)",
        r"https://www.pricecharting.com/game/playstation-5/marvel-spider-man-2",
        COMPLETE),
    (PS5, "The Last Of Us Part II (US)",
        r"https://www.pricecharting.com/game/playstation-5/the-last-of-us-part-ii-remastered",
        NEW),
    (PS5, "Stellar Blade (US)",
        r"https://www.pricecharting.com/game/playstation-5/stellar-blade",
        COMPLETE),
    (PS5, "Hogwarts Legacy (US)",
        r"https://www.pricecharting.com/game/playstation-5/hogwarts-legacy",
        COMPLETE),
    (PS4, "Tales Of Berseria (US)",
        r"https://www.pricecharting.com/game/playstation-4/tales-of-berseria",
        COMPLETE),
    (PS4, "Dishonored [Definitive Edition] (US)",
        r"https://www.pricecharting.com/game/playstation-4/dishonored-definitive-edition",
        COMPLETE)
]

use_bkp = False
with open("dolar.txt") as dolar_bkp:
    saved = dolar_bkp.read().strip().split(";")
    timestamp_now = int(time.time())
    if timestamp_now - int(saved[1]) <= HOURS_6:
        dolar_in_brl = float(saved[0])
        use_bkp = True

if not use_bkp:
    values_raw = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL").json()
    dolar_in_brl = float(values_raw['USDBRL']["bid"])

    with open("dolar.txt", 'w') as dolar_bkp:
        print(f"{dolar_in_brl};{int(time.time())}", file=dolar_bkp)

prices_us = []
names= []
bkp_dict = {}

with open("backup.txt") as bkp:
    for line in bkp:
        _l = line.strip().split(';')
        bkp_dict.update({_l[0]: (float(_l[1]), int(_l[2]))})

print("\n _________________________________________________________________________________")
print(f'{"| Game":<40}               |  USD Price  | BRL Price  |')
print(" —————————————————————————————————————————————————————————————————————————————————")

with open("backup.txt", "w") as bkp:
    for index, game in enumerate(sorted(GAMES, key=lambda tup: (tup[0], tup[1]))):
        saved = bkp_dict.get(game[1], None)
        use_bkp = False
        if saved:
            timestamp_now = int(time.time())
            if timestamp_now - saved[1] <= DAYS_1:
                price = saved[0]
                use_bkp = True
                print(f"{game[1]};{price};{saved[1]}", file=bkp)

        if not use_bkp:
            html = urlopen(game[2]).read().decode("utf-8")
            soup = BeautifulSoup(html, 'html.parser')

            try:
                price_str = soup.find("div", {"id": "full-prices"})
                price_str = price_str.find("td", text=game[3][0])
                price_str = price_str.find_next_sibling("td").text[1:]
                price = float(price_str)
            except AttributeError:
                price_str = soup.find("div", {"id": "full-prices"})
                price_str = price_str.find("td", text=game[3][1])
                price_str = price_str.find_next_sibling("td").text[1:]
                price = float(price_str)

            print(f"{game[1]};{price};{int(time.time())}", file=bkp)
            time.sleep(1)

        n_game = str(index + 1).zfill(3)
        price_brl = round(price * dolar_in_brl, 2)
        names.append(f'[{game[0]}] {game[1]}')
        prices_us.append(price)
        print(f"| {n_game}. [{game[0]}] {game[1]:<40} | US$ {price:7.2f} | R$ {price_brl:7.2f} |")

index_max = max(range(len(prices_us)), key=prices_us.__getitem__)

print(" —————————————————————————————————————————————————————————————————————————————————\n")
print(f"Max Value:   {names[index_max]} ({max(prices_us)})")
print(f"Total Value: US$ {sum(prices_us):.2f} | R$ {round(sum(prices_us) * dolar_in_brl, 2):.2f}")