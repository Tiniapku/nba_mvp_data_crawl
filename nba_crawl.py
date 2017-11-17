from bs4 import BeautifulSoup as bs
import urllib2

url = "https://www.basketball-reference.com/awards/mvp.html"

html = urllib2.urlopen(url)

soup = bs(html.read(), 'lxml')
mvp_table = soup.find('table')
year_link = []
i = 0
f = open('nba_mvp.csv', 'a')
for entry in mvp_table.find_all('tr'):
    if i == 0:
        i += 1
        continue
    if i == 1:
        content = ""
        for line in entry.find_all('th'):
            content += line.get_text() + ","
        i += 1
        content += "\n"
        f.write(content)
        print content
    else:
        content = ""
        content += entry.th.get_text() + ","
        for item in entry.find_all('td'):
            if item['data-stat'] == "voting":
                year_link.append(item.a['href'])
            content += item.get_text() + ","
        content += "\n"
        f.write(content)
        print content
f.close()
print year_link