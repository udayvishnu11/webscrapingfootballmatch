from bs4 import BeautifulSoup as bs
import requests
import json


team_data = []

html_text = requests.get('http://www.collegehockeystats.net/1920/teamstats/ecachm').text
soup = bs(html_text, 'lxml')

links = soup.find_all("a", href=True)
k = []

for link in links:
    if "/1920/teamstats/" in link['href']:
        k.append(link['href'])


for link in k:
    player_numbers = []
    player_names = []

    html_text = requests.get(f'http://www.collegehockeystats.net{link}').text
    soup = bs(html_text, 'lxml')

    text = soup.find_all('td')
    for i in text:
        if len(str(i)) <= 13:
            player_numbers.append(i.text)

    s = player_numbers.index("##")


    for i in soup.find_all('strong'):
        if i.text != 'Player' and i.text != 'No.':
            player_names.append(i.text)


    team_nam = soup.find("i").text.split("\u00a0")
    team_name = team_nam[1][0:-1]

    home_label = soup.find('td', string="Home:")
    home_wins, home_lost, home_tie = 0, 0, 0

    if home_label:
        home_value_element = home_label.find_next('td')
        home_value_element_2 = home_value_element.find_next('td')

        home_value = home_value_element_2.text.strip()
        home_stats = home_value.split("-")
        home_wins, home_lost, home_tie = home_stats


    team_data.append({
        "players": [
            {
                "player_name": player_names[i],
                "player_number": player_numbers[i]
            }
            for i in range(s-1)
        ],
        "name": team_name,
        "home_wins": home_wins,
        "home_lost": home_lost,
        "home_tie": home_tie
    })


output_json = json.dumps(team_data, indent=2)
print(output_json)

