#!/usr/bin/python3

#NEEDED LIBRARIES
import sys
from os import path
from requests import get,session,packages
from bs4 import BeautifulSoup as bs,Comment
from sherlock import sherlock
from reprinter import Reprinter

#Just webdriver stuff
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

#Parsing
import json 
import yaml
import re
import csv
from time import sleep
from urllib.parse import unquote

#The next two lines are just to disable the stupid insecure request warning
from urllib3.exceptions import InsecureRequestWarning
packages.urllib3.disable_warnings(category = InsecureRequestWarning)

class Scraping_Kit():
    def __init__(self):
        # self.target_email=email
        check = '^[a-z0-9]+[\._]?[a-z0-9]+@\w+\.\w{2,3}$'
        ran_once=False
        self.target_email=""
        if ran_once:
            print("Invalid email please try again")
        while not re.search(check, self.target_email):
            self.target_email=input("Please enter target email : ")
            ran_once=True

    def headless_selenium(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def download(self, username,site_name,dp_url): 
        count = 0 
        filename = f"{username}'s_{site_name}_dp.jpg" 
        while True: 
            if not path.isfile(filename): 
                with open(filename, 'wb+') as handle: 
                    response = get(dp_url, stream=True)
                    if not response.ok: 
                        print(response)
                    for block in response.iter_content(1024): 
                        if not block: 
                            break 
                        handle.write(block) 
            else: 
                count += 1 
                filename = f"{username}'s_{site_name}_dp_{count}.jpg" 
                continue 
            print(f"{username}'s {site_name} dp downloaded!")
            break

    def hipb(self):
        #self.driver = self.headless_selenium()
        self.driver.get(f"https://haveibeenpwned.com/unifiedsearch/{self.target_email}")
        soup = bs(self.driver.page_source,'html.parser')
        data = json.loads(soup.find("body").text)
        # print(json.dumps(data,indent = 4).replace("\\\"","'"))
        printme = yaml.safe_dump(data["Breaches"], allow_unicode=True, default_flow_style=False)
        print(printme)

    def emailRep(self):
        headers={
        "User-Agent" : "python/emailrep.io",
        "Content-Type" : "application/json",
        "Key" : "9u880v5bumdu7m37c9zipnv3kwyq1bb3izmuxpwjjvrj3gnv"
        }
        email_rep_data = get(f"https://emailrep.io/{self.target_email}",headers=headers).content
        self.email_rep_data = json.loads(email_rep_data)
        printme = yaml.safe_dump(email_rep_data, allow_unicode=True, default_flow_style=False)
        print(printme)

    def sherly(self):
        sites_we_need = [
                         "Facebook",
                         "Instagram",
                         "Twitter",
                         "Linkedin",
                         "Medium",
                        ]
        try:
            sites_we_need.extend(list(i.title() for i in email_rep_data["details"]["profiles"]))
        except Exception as e:
            pass
        data = open("new_data.json")
        sites = json.load(data)
        username = self.target_email[:self.target_email.index('@')].replace(".","")
        print()
        print(f"Searching for {username} in about a hundred social media sites:")
        ################# FIX PRINT
        self.results = sherlock(username, sites, print_found_only=True, color=False)
        self.exists = []
        # with open(username + ".csv", "w", newline='', encoding="utf-8") as csv_report:
            # writer = csv.writer(csv_report)
        for site in self.results:
            if self.results[site]['http_status']!=404:
                print(self.results[site]['url_user'])
                if site in sites_we_need: 
                    self.exists.append(site)
                    # towrite=[site,results[site]['url_user']]
                    # writer.writerow(towrite)
        # return self.exists
        print()

    def instagram(self):
        if "Instagram" in self.exists:
            #options = Options()
            #options.headless = True
            #driver = webself.driver.Firefox(options=options)
            wait = WebDriverWait(self.driver, 20)
            self.driver.get(self.results["Instagram"]["url_user"])
            user_page = self.driver.page_source
            insta_soup = bs(user_page,'html.parser')
            if not insta_soup.find(text="Sorry, this page isn't available."):
                scripts = insta_soup.find('script', type="text/javascript", text=re.compile('window._sharedData'))
                stringified_json = scripts.text.replace('window._sharedData = ', '')[:-1]
                insta_data = json.loads(stringified_json)['entry_data']['ProfilePage'][0]
                insta_username = insta_data['graphql']['user']['username']

                if not path.isfile(f"{insta_username}'s_insta_data.json"):
                    data_file = f"{insta_username}'s_insta_data.json" 
                else:
                    data_file = f"{insta_username}'s_insta_data_1.json"

                print("HD PHOTO : ", insta_data['graphql']['user']['profile_pic_url_hd'])
                print()
                filename = f"{insta_username}'s_insta_dp.jpg"
                # self.download(insta_username,"insta",dp_url)

                #json.dump(insta_data, open(data_file,"w+"), indent=4)
                # print(json.dumps(insta_data, indent=4))
                printme = yaml.safe_dump(insta_data, allow_unicode=True, default_flow_style=False)
                # print(printme)
            else:
                print("Sorry this insta account does not exist")

    def facebook(self):
        if "Facebook" in self.exists:
            # print(self.results["Facebook"]["url_user"])
            self.nofb = False
            self.driver.get(self.results["Facebook"]["url_user"])
            sleep(3)
            page = self.driver.page_source
            html = bs(page,'html.parser')
            name = html.find("a",{"class":"_2nlw _2nlv"}).text
            print("NAME : ", name)
            about_keys=list(map(lambda x:x.text,html.find_all("span",{"role":"heading"})))
            about_keys=about_keys[:about_keys.index("Contact Information")]
            about=list(map(lambda x:x.text,html.find_all("ul")))
            about=about[1:len(about_keys)+1]
            print()
            print("ABOUT:")
            print(yaml.safe_dump(dict(zip(about_keys,about)), allow_unicode=True, default_flow_style=False))
            #print(list(map(lambda x:x.text,html.find_all("th",{"class":"label"}))))
            #print(list(map(lambda x:x.text,html.find_all("td",{"class":"data"}))))
            likes=dict(zip(list(map(lambda x:x.text,html.find_all("th",{"class":"label"}))),list(map(lambda x:x.text,html.find_all("td",{"class":"data"})))))
            print()
            print("MIGHT LIKE:")
            print(yaml.safe_dump(likes, allow_unicode=True, default_flow_style=False))
        else:
            self.nofb = True

    def twitter(self):
        if "Twitter" in self.exists:
            # print(self.results["Twitter"]["url_user"])
            self.driver.get(self.results["Twitter"]["url_user"])
            sleep(5)
            page = self.driver.page_source
            html = bs(page,'html.parser')
            try:
        #         TODO: Check what kind of exception raising if no location
        #         location = html.find("span",{"class":"ProfileHeaderCard-locationText u-dir"}).text
        #         birthday = html.find("span",{"class":"ProfileHeaderCard-birthdateText u-dir"}).text.strip()
        #         if birthday:
        #            birthday = birthday.replace('Born ', '')
        #         else:
        #             birthday = None
                  #profile_photo = html.find("img",{"class":"ProfileAvatar-image"}).attrs['src']
        #         page_title = html.find('title').text
        #         name = page_title[:page_title.find('(')].strip()
        #         biography = html.find("p",{"class":"ProfileHeaderCard-bio u-dir"}).text
        #         #website = html.find("a",{"class":"u-textUserColor","rel":"me nofollow noopener"}).text.strip()
        #         print(json.dumps(dict(
        #         twitter_name = name,
        #         twitter_username = username,
        #         twitter_birthday = birthday,
        #         biography = biography,
        #         profile_photo = profile_photo ), indent=4))
        #         #download(twit_username,"twitter",profile_photo)

                  location = html.find("span",{"class":"css-901oao css-16my406 r-111h2gw r-4qtqp9 r-1qd0xha r-ad9z0x r-zso239 r-bcqeeo r-qvutc0"}).text  
                  print("LIVES IN :", location)
                  print()
            except:
                pass


    def findName(self):
        if self.nofb:
            # print(self.target_email)
            reprinter = Reprinter()
            wait = WebDriverWait(self.driver, 20)
            self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
            print("Hunting for the Name :")
            reprinter.reprint("Headless initialized\n")
            sleep(5)
            self.driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
            self.driver.find_element_by_xpath('//input[@type="email"]').send_keys('mydbmsproject2001@gmail.com'+Keys.ENTER)
            reprinter.reprint("email done\n")
            sleep(3)
            self.driver.find_element_by_xpath('//input[@type="password"]').send_keys('g00dpassw0rd'+Keys.ENTER)
            wait.until(EC.presence_of_element_located((By.ID, "content")))
            reprinter.reprint("logged in\n")
            sleep(2)
            #Adding target as contact to google contacts
            self.driver.get("https://contacts.google.com/")
            reprinter.reprint("jumped to contacts\n")
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@title="Add new contact"]'))).click()
            #self.diver.find_element_by_xpath('//*[@title="Add new contact"]').click()
            sleep(2)
            wait.until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Create a contact"]'))).click()
            #wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'whsOnd zHQkBf'))).send_keys(target_email)
            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[4]/div/div[2]/span/div/div[2]/div[1]/div/div/div[6]/div/div/div[2]/div[1]/div[1]/div/div[1]/input'))).send_keys(self.target_email)
            #self.diver.find_element_by_xpath('/html/body/div[7]/div[4]/div/div[2]/span/div/div[2]/div[1]/div/div/div[6]/div/div/div[2]/div[1]/div[1]/div/div[1]/input').send_keys(target_email)
            wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@jsname="x8hlje"]'))).click()
            sleep(4)
            try:
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ONOzI")))
            except:
                self.driver.save_screenshot('test.png')
            page = self.driver.page_source
            target_contact_soup = bs(page,'html.parser')
            try:
                target_id = target_contact_soup.find('div',{"class":"NVFbjd LAORIe"}).attrs['data-sourceid']
                reprinter.reprint("Added contact and got google maps url\n")

                # Bounce to maps and get name
                maps_url = f"https://www.google.com/maps/contrib/{target_id}"
                reprinter.reprint("jumped to maps\n")
                reprinter.reprint(f"Google maps url : {maps_url}\n")
                self.driver.get(f"https://www.google.com/maps/contrib/{target_id}")
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                name_page=self.driver.page_source
                name_soup=bs(name_page,'html.parser')
                name=name_soup.find("h1",{"role":"button","class":"section-profile-header-name section-profile-header-clickable-item"}).text
                print("Name : ",name)
            except Exception as e:
                self.driver.save_screenshot('error.png')
                print("Sorry this email is not linked to a google account")


if __name__=="__main__":
    test = Scraping_Kit()
    test.headless_selenium()
    test.sherly()
    test.instagram()
    test.twitter()
    test.facebook()
    test.findName()
