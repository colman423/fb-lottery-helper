import requests as req
from pyquery import PyQuery as pq

res = req.get("https://www.delish.com/food/g3758/best-food-trends-2016/")
doc = pq(res.text)
doc.make_links_absolute(base_url=res.url)

def run(food):
    for n in range(30):
        content = doc("#slide-{} > div.slideshow-slide-content".format(n))
        if food==content("div.slideshow-slide-hed").text():
            href = content("div.slideshow-slide-dek > p > a").attr("href") 
            print(href)
            return href