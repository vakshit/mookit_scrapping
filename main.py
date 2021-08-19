from selenium import webdriver
import yaml
from bs4 import BeautifulSoup
import re

conf = yaml.load(open("cred.yml"))

email = conf['email']
password = conf['password']
url = "https://hello.iitk.ac.in/index.php/user/login"
courseName = input("Enter Course Code: ")
n = int(input("Enter Number of lectures: "))
courseName = courseName.upper()

options = webdriver.ChromeOptions()
options.add_argument("start-maximized");
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=options, executable_path="/home/akshit/Desktop/VSCode/py/executables/chromedriver")
driver.get(url)
driver.find_element_by_id("edit-name").send_keys(email)
driver.find_element_by_id("edit-pass").send_keys(password)
driver.find_element_by_id("edit-submit").click()
driver.find_element_by_xpath('//*[@id="block-gavias-tico-main-menu"]/div/div/ul/li[2]/a').click() # click on courses
driver.find_element_by_partial_link_text(courseName).click() # click on the givern course
driver.find_element_by_xpath('//*[@id="edit-access-course"]').submit()

pagesource = driver.page_source
soup = BeautifulSoup(pagesource,'html.parser')
page = (soup.findAll('a'))

links = soup.find_all('a',attrs={'href': re.compile("^#/lecture")})
names = soup.find_all('div', attrs={'class': 'lectureInfoBoxText'})
weeks = soup.find_all('div', attrs={'class' : 'weekItem'})


f = open('out.csv', 'w')
f.writelines(f"Serial No.,Week No.,Lecture Name,Lecture Duration,Lecture Video Link\n")

temp = []
i = 1
for week in weeks:
    weekNum = week.findChildren()[2].get_text().strip()
    for it in week.findNextSibling().find_all('div', attrs={'class' : 'lectureItem'}):
        lecName = it.get_text().strip().splitlines()[0].replace(',', ' ')     # name
        lecDur = it.get_text().strip().splitlines()[2]      # duration
        lecLink = "https://hello.iitk.ac.in/mth102aa2021/"+it.find('a',attrs={'href': re.compile("^#/lecture")}).get('href')
        text = f"{i},{weekNum},{lecName},{lecDur},{lecLink}\n"
        temp.append(text)
        # f.writelines(text)
        i += 1
temp.reverse()

i = 1
for item in temp:
    f.writelines(item)
    i += 1
    if i > n:
        break


driver.close()
