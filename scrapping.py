from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

option = webdriver.ChromeOptions()
option.add_argument(" — incognito")

browser = webdriver.Chrome(executable_path="/Users/lamazere/Library/Application Support/Google/chromedriver", options=option)

browser.get("https://www.legifrance.gouv.fr/rechJuriJudi.do?reprise=true&page=1")

#search
s_input = input("What are you lookning for ? ")
search = browser.find_element_by_id("champ7")
search.send_keys(s_input)

#time period
t_input = input("Which year?")
time = browser.find_element_by_id("champDateDecision1A")
time.send_keys(t_input)

#lauch search
search_button = browser.find_element_by_name("bouton")
search_button.click()


i=2
all_links1=[]
all_links2=[]
all_linkslast=[]

def get_links(text,liste):
    links_elts = browser.find_elements_by_partial_link_text(text)
    links = [x.get_attribute('href') for x in links_elts]
    for link in links:
        liste.append(link)

while True:
    try:
        next_button = browser.find_element_by_xpath("""//*[@id="result"]/div[4]/ul/li[{}]/a""".format(i))
        get_links('Cour de cassation,',all_links1)
        i+=1
    except NoSuchElementException:
        break   
    next_button.click()

while True:
    try:
        get_links('Cour de cassation,',all_links2)
        next_button = browser.find_element_by_xpath("""//*[@id="result"]/div[4]/ul/li[4]/a""") 
    except NoSuchElementException:
        break   
    next_button.click()

browser.find_element_by_xpath("""//*[@id="result"]/div[4]/ul/li[5]/a""").click()
get_links('Cour de cassation,',all_linkslast) #search only decisions of "cour de cassation"

all_links = all_links1 + all_links2 + all_linkslast

pick_dir = input("name of directory ?")
path = "/Users/lamazere/Desktop/Pour mémoire/%s" %pick_dir

#create file of scraped texts
os.mkdir(path)
os.chdir(path)

i=1
for links in all_links[1:100]:
    page = requests.get(links)
    parse = BeautifulSoup(page.content, 'html.parser') #parses the pages
    text = parse.find("contenu").get_text().replace("\n"," ")
    open("text{}.txt".format(i),"w").write(text)
    i+=1