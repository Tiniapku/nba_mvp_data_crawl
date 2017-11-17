import urllib2
from bs4 import BeautifulSoup as bs

year_link = ['https://www.basketball-reference.com/awards/awards_2017.html#mvp', 'https://www.basketball-reference.com/awards/awards_2016.html#mvp', 'https://www.basketball-reference.com/awards/awards_2015.html#mvp', 'https://www.basketball-reference.com/awards/awards_2014.html#mvp', 'https://www.basketball-reference.com/awards/awards_2013.html#mvp', 'https://www.basketball-reference.com/awards/awards_2012.html#mvp', 'https://www.basketball-reference.com/awards/awards_2011.html#mvp', 'https://www.basketball-reference.com/awards/awards_2010.html#mvp', 'https://www.basketball-reference.com/awards/awards_2009.html#mvp', 'https://www.basketball-reference.com/awards/awards_2008.html#mvp', 'https://www.basketball-reference.com/awards/awards_2007.html#mvp', 'https://www.basketball-reference.com/awards/awards_2006.html#mvp', 'https://www.basketball-reference.com/awards/awards_2005.html#mvp', 'https://www.basketball-reference.com/awards/awards_2004.html#mvp', 'https://www.basketball-reference.com/awards/awards_2003.html#mvp', 'https://www.basketball-reference.com/awards/awards_2002.html#mvp', 'https://www.basketball-reference.com/awards/awards_2001.html#mvp', 'https://www.basketball-reference.com/awards/awards_2000.html#mvp', 'https://www.basketball-reference.com/awards/awards_1999.html#mvp', 'https://www.basketball-reference.com/awards/awards_1998.html#mvp', 'https://www.basketball-reference.com/awards/awards_1997.html#mvp', 'https://www.basketball-reference.com/awards/awards_1996.html#mvp', 'https://www.basketball-reference.com/awards/awards_1995.html#mvp', 'https://www.basketball-reference.com/awards/awards_1994.html#mvp', 'https://www.basketball-reference.com/awards/awards_1993.html#mvp', 'https://www.basketball-reference.com/awards/awards_1992.html#mvp', 'https://www.basketball-reference.com/awards/awards_1991.html#mvp', 'https://www.basketball-reference.com/awards/awards_1990.html#mvp', 'https://www.basketball-reference.com/awards/awards_1989.html#mvp', 'https://www.basketball-reference.com/awards/awards_1988.html#mvp', 'https://www.basketball-reference.com/awards/awards_1987.html#mvp', 'https://www.basketball-reference.com/awards/awards_1986.html#mvp', 'https://www.basketball-reference.com/awards/awards_1985.html#mvp', 'https://www.basketball-reference.com/awards/awards_1984.html#mvp', 'https://www.basketball-reference.com/awards/awards_1983.html#mvp', 'https://www.basketball-reference.com/awards/awards_1982.html#mvp', 'https://www.basketball-reference.com/awards/awards_1981.html#mvp', 'https://www.basketball-reference.com/awards/awards_1980.html#mvp', 'https://www.basketball-reference.com/awards/awards_1979.html#mvp', 'https://www.basketball-reference.com/awards/awards_1978.html#mvp', 'https://www.basketball-reference.com/awards/awards_1977.html#mvp', 'https://www.basketball-reference.com/awards/awards_1976.html#mvp', 'https://www.basketball-reference.com/awards/awards_1975.html#mvp', 'https://www.basketball-reference.com/awards/awards_1974.html#mvp', 'https://www.basketball-reference.com/awards/awards_1973.html#mvp', 'https://www.basketball-reference.com/awards/awards_1972.html#mvp', 'https://www.basketball-reference.com/awards/awards_1971.html#mvp', 'https://www.basketball-reference.com/awards/awards_1970.html#mvp', 'https://www.basketball-reference.com/awards/awards_1969.html#mvp', 'https://www.basketball-reference.com/awards/awards_1968.html#mvp', 'https://www.basketball-reference.com/awards/awards_1967.html#mvp', 'https://www.basketball-reference.com/awards/awards_1966.html#mvp', 'https://www.basketball-reference.com/awards/awards_1965.html#mvp', 'https://www.basketball-reference.com/awards/awards_1964.html#mvp', 'https://www.basketball-reference.com/awards/awards_1963.html#mvp', 'https://www.basketball-reference.com/awards/awards_1962.html#mvp', 'https://www.basketball-reference.com/awards/awards_1961.html#mvp', 'https://www.basketball-reference.com/awards/awards_1960.html#mvp', 'https://www.basketball-reference.com/awards/awards_1959.html#mvp', 'https://www.basketball-reference.com/awards/awards_1958.html#mvp', 'https://www.basketball-reference.com/awards/awards_1957.html#mvp', 'https://www.basketball-reference.com/awards/awards_1956.html#mvp']

year = 2017
for url in year_link:
    html = urllib2.urlopen(url)

    soup = bs(html.read(), 'lxml')
    year_table = soup.find('table')
    i = 0
    f = open('nba_mvp_candidate_by_year.csv', 'a')
    for entry in year_table.find_all('tr'):
        if i == 0:
            i += 1
            continue
        if i == 1:
            i += 1
            if year == 2017:
                content = "year"
                for line in entry.find_all('th'):
                    content += "," + line.get_text()
                content += "\n"
                f.write(content)
                print content
        else:
            content = str(year)
            rank = entry.th.get_text()
            if rank[-1] == "T":
                rank = rank[:-1]
            content += "," + rank
            for item in entry.find_all('td'):
                content += "," + item.get_text()
            content += "\n"
            f.write(content)
            print content
    year -= 1
    f.close()