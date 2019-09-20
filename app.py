from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Edu:
    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.bot =webdriver.Firefox()
        print('Bot ready!')
        print('         ')

    def login(self):
        bot=self.bot
        bot.get('https://www.educationperfect.com/app/#/login') #open login page
        print('opening webpage...')

        while True: #Continue when loaded
            time.sleep(2)
            try:
                bot.find_element_by_id('login-password')
                time.sleep(0.5)
                break
            except:
                print('Webpage loading...')

        #Put in credientals and submit form
        print('Logging in!')
        print('         ')
        emailInp= bot.find_element_by_id('login-username')
        passwrdInp= bot.find_element_by_id('login-password')
        emailInp.clear()
        passwrdInp.clear()
        emailInp.send_keys(self.email)
        passwrdInp.send_keys(self.password)
        passwrdInp.send_keys(Keys.RETURN)

    def tasktype(self):
        bot=self.bot
        url = bot.current_url
        print('                 ')
        print('Url is '+url)
        try:
            url.find('list-starter')
            print('List detected! starting now.')
            ed.lists()
        except:
            print('could not find question type.')


    def lists(self):
        #enter list question code here
        print('doing list things')





username = input('Username/Email: ')
passwrd = input('Password: ')
ed = Edu(username,passwrd)
ed.login()
meme=input('Please navigate the the task you want to complete! Press enter when ready.')
ed.tasktype()