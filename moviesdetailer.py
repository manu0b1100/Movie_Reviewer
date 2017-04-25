import requests,bs4,re
from movienamecleaning import cleanit
import pandas as pd
class BuildMovieRatingSet:
    def __init__(self):
        self.movie_list=[]
        self.searchurl="https://www.google.co.in/search"
        self.piratebayurl="https://www.thepiratebay.org/browse/201/0/7/0"
        self.compareurl="https://www.rottentomatoes.com/m"

    def getPiratebayLinks(self):
        soup = bs4.BeautifulSoup(requests.get(self.piratebayurl).text, 'lxml')
        res = soup.find_all("a", class_="detLink")
        for r in res:
            temp_name=cleanit(r.contents[0])
            if temp_name!=None:
                self.movie_list.append({"name":temp_name})
                print(cleanit(r.contents[0]))

    def getRottenLinks(self):

        for l in self.movie_list:
            l["link"]=self.getRottenLink(l["name"])

    def getRottenLink(self,movie_name):

        payload = {"q": "site:rottentomatoes.com " + movie_name}
        res = requests.get(self.searchurl, params=payload)
        soup = bs4.BeautifulSoup(res.text, "lxml")
        #print(soup.prettify())
        div = soup.find_all("div", class_="g")
        for d in div:
            links = d.find_all("a")
            for li in links:
                #print('/'.join(re.findall(r'https.*', li['href'])[0].split('/')[0:4]) )
                if '/'.join(re.findall(r'https.*', li['href'])[0].split('/')[0:4]) == self.compareurl:
                    return '/'.join(re.findall(r'https.*', li['href'])[0].split('/')[0:5])
        return "https://www.rottentomatoes.com/m/top_gun"


    def get_scores(self):
        for l in self.movie_list:
            self.getScore(l)


    def getScore(self,l):
        soup = bs4.BeautifulSoup(requests.get(l["link"]).text, "lxml")
        span = soup.find_all("span", class_="meter-value superPageFontColor")
        print(span[0].find_all("span")[0].contents[0])
        l["critics"] = span[0].find_all("span")[0].contents[0]
       	#print(soup.find_all(lambda tag: tag.name == 'span' and tag.get('class') == ['superPageFontColor'])[0].contents[0])
        l["audience"] = soup.find_all(lambda tag: tag.name == 'span' and
                                                      tag.get('class') == ['superPageFontColor'])[0].contents[0]

    def run(self):
        self.getPiratebayLinks()
        self.getRottenLinks()
        self.get_scores()
        print(self.movie_list)


obj=BuildMovieRatingSet()
obj.run()

df=pd.DataFrame(obj.movie_list)
writer=pd.ExcelWriter('output.xlsx')
df.to_excel(writer,'Sheet1')
writer.save()
