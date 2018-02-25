from igdb_api_python.igdb import igdb

import json, datetime

igdb = igdb("dfd4b285e76c0d3f97a549b2edd9467e")

#Consolas

'''
Wii:        5
PS3 :       9
360:        12
DS:         20
3DS:        37
PSP:        38
WiiU:       41
Vita:       46
PS4:        48
One:        49
Switch:     130

'''

all_games = { }

result = igdb.platforms({
    'ids': [9,12,37,41,46,48,49],
    'fields': ['name','games.name', 'games.aggregated_rating', 'games.first_release_date', 'games.screenshots', 'games.cover'],
    'expand': 'games'
})

for platform in result.body:
    for game in platform['games']:
        if str(game["id"]) in all_games:
            all_games[str(game["id"])]["platform"] = all_games[str(game["id"])]["platform"] + "," + platform['name']
        else:
            name = game["name"] if "name" in game else None
            rating = game["aggregated_rating"] if "aggregated_rating" in game else None
            release = datetime.datetime.fromtimestamp(int(game["first_release_date"]/1000)).strftime('%Y-%m-%d') if "first_release_date" in game else None
            tmp_s = game["screenshots"] if "screenshots" in game else None
            cover = game["cover"]["url"][2:].replace("t_thumb", "t_original") if "cover" in game else None

            screenshots = ""

            if tmp_s != None:
                for s in tmp_s:
                    url = s["url"][2:]
                    screenshots += url.replace("t_thumb", "t_original") + ","
                screenshots = screenshots[:-1]
            else:
                screenshots = None

            all_games[str(game["id"])] = \
                {"igdb" : str(game["id"]),
                 "name": name,
                 "rating": rating,
                 "release": release,
                 "screenshots": screenshots,
                 "cover": cover,
                 "platform": platform['name']
                 }

saved_games = []
pk = 1

for g in all_games.values():
    saved_games.append({"pk": pk, "model": "games.Game", "fields": g})
    pk += 1

with open('igdb.json', 'w') as fp:
    json.dump(saved_games, fp)
