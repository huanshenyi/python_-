import requests
from bs4 import BeautifulSoup
from pyecharts import Bar

ALL_DATA = []
def get_page(url):

    headers = {
        #
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode("UTF-8")
    soup = BeautifulSoup(text, 'lxml')
    table = soup.find('table', class_="week-index-table")
    trs = table.findAll("tr")[1:]
    for tr in trs:
        tds = tr.findAll("td")[0:2]
        #町を取得
        city_td = tds[0]
        city_1 = list(city_td.stripped_strings)[0]
        city_2 = list(city_td.stripped_strings)[1]
        city = city_1+city_2
        #最低気温を取得
        min_temp_td = tds[1]
        min_temp = list(min_temp_td.stripped_strings)[3]
        ALL_DATA.append({"city": city, "min_temp": min_temp})
        #print({"city": city, "min_temp": min_temp})



def main():
    url = "https://tenki.jp/week/2/"
    get_page(url)

    ALL_DATA.sort(key=lambda data: data['min_temp'])
    data=ALL_DATA[:]
    cities = list(map(lambda x: x['city'], data))
    temps = list(map(lambda x: x['min_temp'], data))


    chart = Bar("東北最低気温ランキング")
    chart.add('', cities, temps)
    chart.render("hokaido.html")

if __name__=="__main__":
    main()
