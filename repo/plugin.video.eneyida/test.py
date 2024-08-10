from bs4 import BeautifulSoup
import requests
r = requests.post("https://eneyida.tv/index.php?do=search", data={"do": "search", "subaction": "search", "story": "Пошук"})

soup = BeautifulSoup(r.content, 'html.parser')

for item in soup.find_all("article", class_="short"):
    print(item.find("a", class_="short_title").text)
