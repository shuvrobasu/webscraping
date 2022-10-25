# Original code by Pythonology
#https://www.youtube.com/watch?v=RvCBzhhydNk
#updated by Shuvro Basu

from bs4 import BeautifulSoup
import requests
from csv import writer
import os
import time
import sys

#importing os to clear screen before user input
os.system('cls')

#declare variables

noofitems = 0
counter = 0

def progress_spinner(status, cur_pos):
    #Code credit Yourun-proger at https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
    pos = ["|", "/", "-", "\\"]
    sys.stdout.write("%s: %s, [%s%s]\r" % (status, pos[cur_pos%4], cur_pos, '%'))
    sys.stdout.flush()

#input location to search from user and convert to lower case
loct = input("Enter location to search : ").lower()

if loct == None:
    #default to Amsterdam if no input provided
    loct = "Amsterdam"

#get url using requests
url= "https://www.pararius.com/apartments/" + loct +"?ac=1"
#tell user which url is being searched
print("Searching for :", url)

page = requests.get(url)

#beautiful soup at work
soup = BeautifulSoup(page.content, 'html.parser')
lists = soup.find_all('section', class_="listing-search-item")

#additional checks if there is something worth writing, tell the user if not
if len(lists) == 0:
    print("No listings found for your search " + loct)
else:
    noofitems = len(lists)

#generate dynamic filename
fname = "housing" + loct + ",csv"

with open(fname, 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['Title', 'Location', 'Price', 'Area',"Rooms"]
    thewriter.writerow(header)

    for list in lists:
        counter += 1
        title = list.find('a', class_="listing-search-item__link--title").text.replace('\n', '')
        location = list.find('div', class_="listing-search-item__sub-title").text.replace('\n', '')
        price = list.find('div', class_="listing-search-item__price").text.replace('\n', '')
        area = list.find('li', class_="illustrated-features__item--surface-area").text.replace('\n', '')
        rooms = list.find('li', class_="illustrated-features__item--number-of-rooms").text.replace('\n', '')

        info = [title, location, price, area, rooms]

        progress_spinner("Generating file  ", counter)
        time.sleep(0.5)
        thewriter.writerow(info)
