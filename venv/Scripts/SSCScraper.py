import re
import requests
from bs4 import BeautifulSoup

payload = {
    'username': 'Westernwaste',
    'password': 'sustainwwu',
    '__RequestVerificationToken': 'logindata'
}

url = "https://portal.ssc-inc.com/BillingHistory/Index?acctNumber=4101591"
my_list = []
count = 0

with requests.session() as s:
    resp = s.get(url)
    payload['__RequestVerificationToken'] = \
    BeautifulSoup(resp.content, 'html5lib').find('input', attrs={'name': '__RequestVerificationToken'})['value']
    response_post = s.post('https://portal.ssc-inc.com/User/Login?ReturnUrl=%2fUserLogin&action=submitlogin&type=login',
                           data=payload)
    response = s.get(url)

    soup = BeautifulSoup(response.text, 'html5lib')
    for link in soup.find_all('a'):
        x = link.get('href')
        if x is None:
            x = ""
        if re.search("^/BillingHistory/", x):
            my_list.append(link.get('href'))

print(soup.prettify())
print(payload['__RequestVerificationToken'])
print(my_list)
file = open("Acc4101591.txt", "w")
for link in my_list[1:]:
    url = "https://portal.ssc-inc.com" + link
    with requests.session() as s:
        resp = s.get(url)
        payload['__RequestVerificationToken'] = \
        BeautifulSoup(resp.content, 'html5lib').find('input', attrs={'name': '__RequestVerificationToken'})['value']

        response_post = s.post(
            'https://portal.ssc-inc.com/User/Login?ReturnUrl=%2fUserLogin&action=submitlogin&type=login', data=payload)
        response = s.get(url)
        soup = BeautifulSoup(response.text, 'html5lib')
        print(soup.prettify())
        divs = soup.find_all("table", class_="alternating-color right-align-last-column")

        rows = divs[0].find_all('tr')
        line = ""

        for row in rows[2:len(rows)]:
            line = ""
            for col in row.find_all('td'):
                x = col.contents[0]
                if x is None:
                    x = ""
                line += x + " "
            file.write(line)
            file.write("\n")
            print(line)

file.close()
