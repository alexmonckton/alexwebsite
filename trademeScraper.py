import requests
import csv
from bs4 import BeautifulSoup
from decimal import Decimal

class Product():
    def __init__(self, page, name, price):
        self.page = page
        self.name = name
        self.price = price
def Scrape():
    response = requests.get("https://www.trademe.co.nz/Browse/CategoryListings.aspx?mcatpath=gaming%2fplaystation-4%2fconsoles&rsqid=2be7fd63884343a2908b45ec2025b7c2-003&buy=buynow")
    soup = BeautifulSoup(response.text, "html.parser")
    itemlist = soup.findAll("div", {"class":"supergrid-listing"})
    allitems = []
    productlist = []
    pages = []
    i = 1
    for j in range(len(itemlist)):
        pages.append(i)
    while len(itemlist) > 0:
        allitems = allitems + itemlist
        i += 1
        response = requests.get("https://www.trademe.co.nz/Browse/CategoryListings.aspx?mcatpath=gaming%2fplaystation-4%2fconsoles&rsqid=2be7fd63884343a2908b45ec2025b7c2-003&buy=buynow&page=" + str(i))
        soup = BeautifulSoup(response.text, "html.parser")
        itemlist = soup.findAll("div", {"class":"supergrid-listing"})
        for j in range(len(itemlist)):
            pages.append(i)
    i = 0
    while i < len(allitems):
        title = allitems[i].find("div", {"class":"title"})
        if title != None:
            item_title = title.text.strip()
        else:
            allitems.remove(allitems[i])
            del(pages[i])
            continue
        item_price = allitems[i].find("div",{"class":"listingBuyNowPrice"}).text.strip().replace(",","")
        productlist.append(Product(pages[i], item_title, Decimal(item_price[1:])))
        i += 1
    productlist.sort(key=lambda x: x.price)
    return productlist

def GetAverage(productlist):
    total = 0
    for product in productlist:
        total += product.price
    return Decimal(total / len(productlist))

Scrape()

def ExportCSV(productlist):
    with open('trademe_ps4s.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["SN", "Title", "Price"])
        for i in range (len(productlist)):
            writer.writerow([str(i + 1), productlist[i].name, "$" + str(productlist[i].price)])