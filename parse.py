import requests
from bs4 import BeautifulSoup
import sqlite3
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Razdel(Base):
    __tablename__ = 'razdel'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

class Tema(Base):
    __tablename__ = 'Tema'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    razdel_id = Column(Integer, ForeignKey('Razdel.id'), nullable=False)
    razdel = relationship("Razdel")











url = 'https://forum.criminal.ist/index.php'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

questions = soup.find_all('a', class_='subject mobile_subject')
b = []
b2 = []
for i in questions:
    ee = i.text
    ee = ee.strip()
    ee = ee.replace(" ", "")
    b2.append(ee)
    b.append(i['href'])

b2[0] = b2[0][:-1]
e = []
for i in b2:
    new_razdel = Razdel(name=i)

aaa = 0
for i in b:
    aaa += 1
    
    
    
    c = []
    url = i
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    questions = soup.find_all('span', class_='preview bold_text')
    for j in questions:
        cursor.execute("INSERT INTO Tema (name, razdel_id) VALUES (?, ?)", (j.text, aaa))
        href_value = j.find('a')['href']
        c.append(href_value)



    for q in c:

        d = []
        dd = []

        url = q
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        www = 1
        try:
            www = soup.find_all('a', class_='nav_page')[2]
            www = int(str(www).split(">")[1].split("<")[0])
        except Exception:
            pass



        for vv in range(www):
            ccc = str(15 * vv)
            if int(ccc) > 15:
                break

            parts = q.split(".")
            parts[-1] = str(ccc)
            result = ".".join(parts)
            url = result
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            questions = soup.find_all('div', class_='poster')
            for t in questions:
                username = t.find('a', title=lambda x: x and 'Просмотр профиля' in x).text
                d.append(username)
            for ii in d:
                if d.count(ii) > 3:
                    if not ii in dd:
                        dd.append(ii)



        e.append(len(dd))

connection.commit()
connection.close()



url = 'https://forum.criminal.ist/index.php'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
n = 0
questions = soup.find_all('div', class_='board_stats')
for i in questions:
    h = i.find('p')
    h = str(h).split(":")
    h = h[1].split("<")[0][1:]
    h = h.replace(',', '')
    n += int(h)


import matplotlib.pyplot as plt



fig, ax = plt.subplots()
ax.bar([str(n) + "всего сообщений", str(sum(e)) + "больше трех раз"], [n, sum(e)])

plt.show()


