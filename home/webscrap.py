import requests
from bs4 import BeautifulSoup

class WebScrapping:
    def __init__(self, url):
        r = requests.get(url)
        with open("index.html", "w") as file:
            file.write(r.text)

    def des_format(self, des):
        ol = des.find_all(["p", "ol"])
        description_list = []
        for i in ol:
            string = i.get_text()
            string = string.replace("\n", " ")
            string = string.replace("\t", "")
            string = string.replace("ï¿½", "\"")
            description_list.append(string)
        return description_list

    def chapters(self, content):
        for lines in content:
            section = lines.find_all("h2")
            des = lines.find_all("div", {"class": "sectxt"})
            section_des = {}
            for i in range(len(des)):
                des[i] = self.des_format(des[i])
                section_des[section[i].text] = "\n".join(des[i])
            return section_des

    def scrap(self):
        with open("index.html", "r") as f:
            html = f.read()
        soup = BeautifulSoup(html, 'html.parser')
        content = soup.find_all("div", id="content")
        return self.chapters(content)
