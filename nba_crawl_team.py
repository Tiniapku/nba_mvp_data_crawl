from bs4 import BeautifulSoup as bs
import urllib2
import re
import unicodedata

url_base = "https://www.basketball-reference.com/leagues/NBA_"
year_list = [i for i in xrange(2018, 1989, -1)]
name_dict = {u'Boston Celtics': "BOS", u'Toronto Raptors':"TOR", u'New York Knicks':"NYK",
            u'Philadelphia 76ers':"PHI", u'Brooklyn Nets':"BRK", u'Cleveland Cavaliers':"CLE",
            u'Milwaukee Bucks':"MIL", u'Indiana Pacers':"IND", u'Chicago Bulls':"CHI", u'Detroit Pistons':"DET",
            u'Washington Wizards': "WAS", u'Atlanta Hawks': "ATL", u'Miami Heat':"MIA", u'Charlotte Hornets':"CHO",
            u'Orlando Magic':"ORL", u'Utah Jazz':"UTA", u'Oklahoma City Thunder': "OKC", u'Portland Trail Blazers':"POR",
            u'Denver Nuggets':"DEN", u'Minnesota Timberwolves':"MIN", u'Golden State Warriors':"GSW", u'Los Angeles Clippers':"LAC",
            u'Sacramento Kings':"SAC", u'Los Angeles Lakers':"LAL", u'Phoenix Suns':"PHO", u'San Antonio Spurs': "SAS", u'Houston Rockets': "HOU",
            u'Memphis Grizzlies':"MEM", u'New Orleans Pelicans':"NOP", u'Dallas Mavericks':"DAL",
            u'New Orleans Hornets': "NOH", u'New Jersey Nets': "NJN", u'Seattle SuperSonics':"SEA", u'Charlotte Bobcats': "CHA",
             u'New Orleans/Oklahoma City Hornets': "NOH", u'Vancouver Grizzlies': "VAN", u'Washington Bullets': "WSB"}
url_list = [url_base + str(y) + ".html" for y in year_list]
year = year_list[0]
#url_list = ["https://www.basketball-reference.com/leagues/NBA_2018.html"]
f = open('team_stats.csv', 'a')
#print url_list
for url in url_list:
    html = urllib2.urlopen(url)
    #h = unicodedata.normalize("NFKD", html.read())
    soup = bs(html.read(), 'lxml')
    i = 0
    div_stats_E = soup.find("table", {"id": "divs_standings_E"})
    for entry in div_stats_E.find_all('tr'):
        if i == 0:
            if year != 2018:
                i += 1
                continue
            else:
                content = "Year"
                for line in entry.find_all('th'):
                    if line.get_text() == "Eastern Conference":
                        content += "," + "Team_full,Team,Rank"
                    else:
                        content += "," + line.get_text()
                i += 1
                content += "\n"
                print content
                f.write(content.encode('utf-8'))
        else:
            content = "%s" %year
            for item in entry.find_all('th'):
                if item.has_attr('data-stat'):
                    s = item.get_text()
                    name = unicodedata.normalize("NFKD", s[:-5].strip('*')).strip(" ")
                    short = name_dict.get(name, "Others")
                    rank = re.search('\((\d+)\)', s[-5:]).group(1)
                    content += "," + name + "," + short + "," + rank
                    for line in entry.find_all('td'):
                        content += "," + line.get_text()
                    content += "\n"
                    print content
                    f.write(content.encode('utf-8'))
    div_stats_W = soup.find("table", {"id": "divs_standings_W"})
    j = 0
    for entry in div_stats_W.find_all('tr'):
        if j == 0:
            j += 1
            continue
        else:
            content = "%s" % year
            for item in entry.find_all('th'):
                if item.has_attr('data-stat'):
                    s = item.get_text()
                    name = unicodedata.normalize("NFKD", s[:-5].strip('*')).strip(" ")
                    short = name_dict[name]
                    rank = re.search('\((\d+)\)', s[-5:]).group(1)
                    content += "," + name + "," + short + "," + rank
                    for line in entry.find_all('td'):
                        content += "," + line.get_text()
                    content += "\n"
                    print content
                    f.write(content.encode('utf-8'))
    year -= 1
f.close()