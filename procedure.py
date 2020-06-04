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
from printing import colors

#The next two lines are just to disable the stupid insecure request warning
from urllib3.exceptions import InsecureRequestWarning
packages.urllib3.disable_warnings(category = InsecureRequestWarning)

class Scraping_Kit():
    def __init__(self, email):
        self.target_email=email
        self.reprinter = Reprinter()
        db_json = {}
        db_json[email]={}

    def headless_selenium(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Firefox(options=options)

    def decapitate(self):
        self.driver.quit()

    def download(self, username, site_name, dp_url): 
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
        print(colors.fg.lightred, f"Searching for {username} in about a hundred social media sites:")
        ################# FIX PRINT
        self.results = sherlock(username, sites, print_found_only=True, color=False)
        self.exists = []
        # with open(username + ".csv", "w", newline='', encoding="utf-8") as csv_report:
            # writer = csv.writer(csv_report)
        for site in self.results:
            if self.results[site]['http_status']!=404 and self.results[site]['url_user'].strip()!="":
                print(colors.fg.lightgreen, self.results[site]['url_user'])
                if site in sites_we_need: 
                    self.exists.append(site)
                    # towrite=[site,results[site]['url_user']]
                    # writer.writerow(towrite)
        # return self.exists
        print(colors.reset)

    def instagram(self):
        if "Instagram" in self.exists:
            db_json[email]["Instagram"]={}
            #options = Options()
            #options.headless = True
            #driver = webself.driver.Firefox(options=options)
            self.reprinter.reprint("Processing Instagram\n",colors.fg.lightred)
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

                self.reprinter.reprint( "HD PHOTO (may not always be accurate): ",colors.fg.lightred)
                print(colors.fg.lightgreen,insta_data['graphql']['user']['profile_pic_url_hd'])
                print(colors.reset)
                filename = f"{insta_username}'s_insta_dp.jpg"
                # self.download(insta_username,"insta",dp_url)

                #json.dump(insta_data, open(data_file,"w+"), indent=4)
                # print(json.dumps(insta_data, indent=4))
                printme = yaml.safe_dump(insta_data, allow_unicode=True, default_flow_style=False)
                # print(printme)

    def facebook(self):
        if "Facebook" in self.exists:
            # print(self.results["Facebook"]["url_user"])
            self.reprinter.reprint("Processing Facebook\n",colors.fg.lightred)
            self.nofb = False
            self.driver.get("http://www.facebook.com")
            self.driver.find_element_by_xpath('//*[@id="email"]').send_keys("mydbmsproject2001@gmail.com")
            self.driver.find_element_by_xpath('//*[@id="pass"]').send_keys("g00dpassw0rd")
            self.driver.find_element_by_xpath('//*[@id="u_0_b"]').click()
            self.driver.find_element_by_id("userNavigationLabel").click()
            sleep(2)
            self.driver.find_element_by_class_name("_54nc").click()
            sleep(3)
            self.driver.delete_all_cookies()
            self.driver.get(self.results["Facebook"]["url_user"])
            self.driver.save_screenshot('logged_in.png')
            sleep(2)
            page = self.driver.page_source
            html = bs(page,'html.parser')
            name = html.find("a",{"class":"_2nlw _2nlv"})
            if name is not None:
                name=name.text
            about_keys=list(map(lambda x:x.text,html.find_all("span",{"role":"heading"})))
            about_keys=about_keys[:about_keys.index("Contact Information")]
            about=list(map(lambda x:x.text,html.find_all("ul")))
            about=about[1:len(about_keys)+1]
            likes=dict(zip(list(map(lambda x:x.text,html.find_all("th",{"class":"label"}))),list(map(lambda x:x.text,html.find_all("td",{"class":"data"})))))
            self.reprinter.reprint("ABOUT:",colors.fg.lightgreen)
            print()
            print(yaml.safe_dump(dict(zip(about_keys,about)), allow_unicode=True, default_flow_style=False))
            print()
            print("NAME : ", name)
            print()
            print("MIGHT LIKE:")
            print(yaml.safe_dump(likes, allow_unicode=True, default_flow_style=False))
            print(colors.reset)
        else:
            self.nofb = True

    def twitter(self):
        if "Twitter" in self.exists:
            # print(self.results["Twitter"]["url_user"])
            self.reprinter.reprint("Processing Twitter\n",colors.fg.lightred)
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
                  self.reprinter.reprint(f"LIVES IN : {location}\n",colors.fg.lightgreen)
                  print()
            except:
                pass


    def findName(self):
        if self.nofb:
            # print(self.target_email)
            wait = WebDriverWait(self.driver, 20)
            self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent%27')
            print(colors.fg.lightred,"Hunting for the Name :")
            self.reprinter.reprint("Headless initialized\n",colors.fg.lightgreen)
            sleep(5)
            self.driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
            self.driver.find_element_by_xpath('//input[@type="email"]').send_keys('mydbmsproject2001@gmail.com'+Keys.ENTER)
            self.reprinter.reprint("email done\n",colors.fg.lightgreen)
            sleep(3)
            self.driver.find_element_by_xpath('//input[@type="password"]').send_keys('g00dpassw0rd'+Keys.ENTER)
            wait.until(EC.presence_of_element_located((By.ID, "content")))
            self.reprinter.reprint("logged in\n",colors.fg.lightgreen)
            sleep(2)
            #Adding target as contact to google contacts
            self.driver.get("https://contacts.google.com/")
            self.reprinter.reprint("jumped to contacts\n",colors.fg.lightgreen)
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
                self.reprinter.reprint("Added contact and got google maps url\n",colors.fg.lightgreen)

                # Bounce to maps and get name
                maps_url = f"https://www.google.com/maps/contrib/{target_id}"
                self.reprinter.reprint("jumped to maps\n",colors.fg.lightgreen)
                self.reprinter.reprint(f"{colors.fg.lightgreen}Google maps url : {maps_url}\n")
                self.driver.get(f"https://www.google.com/maps/contrib/{target_id}")
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                name_page=self.driver.page_source
                name_soup=bs(name_page,'html.parser')
                name=name_soup.find("h1",{"role":"button","class":"section-profile-header-name section-profile-header-clickable-item"}).text
                print("Name : ",name)
                print(colors.reset)
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
