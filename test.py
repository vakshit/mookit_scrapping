from selenium import webdriver
import csv
import yaml
from bs4 import BeautifulSoup
import re

link_text = []
name_text = []
week_info = []

def get_week_info(links, names, weeks):

    for week in weeks:
        week_info.append(week.get_text().strip())

    for link in links:
        link_text.append(link.get('href'))

    for name in names:
        name_text.append(name.get_text().strip())

conf = yaml.load(open("cred.yml"))

email = conf['hello_iitk']['email']
password = conf['hello_iitk']['password']
url = "https://hello.iitk.ac.in/index.php/user/login"

options = webdriver.ChromeOptions()
options.add_argument("start-maximized");
# options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
driver = webdriver.Chrome(chrome_options=options, executable_path="chromedriver")
driver.get(url)
driver.find_element_by_name("name").send_keys(email)
driver.find_element_by_name("pass").send_keys(password)
driver.find_element_by_name("op").click()

driver.find_element_by_xpath('//*[@id="block-gavias-tico-main-menu"]/div/div/ul/li[2]/a').click()
driver.find_element_by_xpath('//*[@id="block-gavias-tico-tabs-2"]/div/ul/li[4]/a').click()
driver.find_element_by_xpath('//*[@id="block-gavias-tico-content"]/div/div/div/div/div[1]/div[3]/div/span/a').click()
driver.find_element_by_xpath('//*[@id="edit-access-course"]').submit()
course_name = driver.find_element_by_xpath('/html/body/app-root/div[1]/div/div[4]/div[1]/span').text
print(course_name)

pagesource = driver.page_source
soup = BeautifulSoup(pagesource,'html.parser')
page = (soup.findAll('a'))

links = soup.find_all('a',attrs={'href': re.compile("^#/lecture")})
names = soup.find_all('div', attrs={'class': 'lectureInfoBoxText'})
weeks = soup.find_all('div', attrs={'class' : 'weekItem'})

# test = soup.find('div', attrs={'class' : 'weekItem'})
# weekNum = test.findChildren()[2].get_text().strip()
# lecTitle = test.findNextSibling().find_all('span', attrs={'class' : 'weekListItemTitle'})[0].get_text().strip()
# print(weekNum)
# print(lecTitle.replace('•', ''))
# for it in test.findNextSibling().find_all('div', attrs={'class' : 'lectureItem'}):
#     # print(type(it.get_text().strip().splitlines()))
#     print(it.get_text().strip().splitlines()[0]) # title
#     print(it.get_text().strip().splitlines()[2])   # duration
#     print(it.find('a',attrs={'href': re.compile("^#/lecture")}).get('href'))

f = open('out.csv', 'w')
f.writelines(f"Serial No.,Week No.,Lecture Topic,Lecture Name,Lecture Duration,Lecture Video Link\n")

i = 1
for week in weeks:
    weekNum = week.findChildren()[2].get_text().strip()
    lecTitle = week.findNextSibling().find_all('span', attrs={'class' : 'weekListItemTitle'})[0].get_text().strip().replace('•', '')
    # print(weekNum)
    for it in week.findNextSibling().find_all('div', attrs={'class' : 'lectureItem'}):
        # print(type(it.get_text().strip().splitlines()))
        lecName = it.get_text().strip().splitlines()[0].replace(',', ' ')     # name
        lecDur = it.get_text().strip().splitlines()[2]      # duration
        lecLink = it.find('a',attrs={'href': re.compile("^#/lecture")}).get('href')
        # print(weekNum, lecTitle, lecName, lecDur, lecLink)
        text = f"{i},{weekNum},{lecTitle},{lecName},{lecDur},{lecLink}\n"
        f.writelines(text)
        i += 1
    # print(f'One outer loop completed \n')


driver.close()
