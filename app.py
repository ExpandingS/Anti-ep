from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from difflib import get_close_matches
import time
import os

class Edu:
    answer={}
    def __init__(self,email,password):
        self.email=email
        self.password=password
        self.bot =webdriver.Firefox()
        print('Bot ready!')

    def login(self):
        bot=self.bot
        bot.get('https://www.educationperfect.com/app/#/login') #open login page
        print('opening webpage...')
        bot.minimize_window()
        while True: #Continue when loaded
            time.sleep(1)
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

    def tasktype(self): #find what type of question it is
        bot=self.bot
        url = bot.current_url
        #bot.maximize_window()
        print('                 ')
        print('Url is '+url)
        if url.find('list-starter') != -1: #if it is a list
            print('List detected... starting now.')
            ed.lists()

        elif url.find('maths')!= -1: #if it's maths.
            print('maths')
            ed.maths()
        else:
            print('Could not find challenge type') #unknown
            exit()


    def lists(self):
        bot=self.bot
        time.sleep(1)
        #enter list question code here
        print('doing list things')
      
        pages=False
        try:  #checks to see if it has multiple pages
           bot.find_element_by_id('full-list-switcher').click()
           bot.find_element_by_id('tutorial-hint-link').click()
           pages=True
           time.sleep(0.5)
        except:
            pages=False
        
        if pages == False:
            wordstring=bot.find_element_by_id('word-count').text #find word count
            cutoff=wordstring.find('wo')
            amount=int(wordstring[0:cutoff])
            print(amount)
        else:
            pagenum=bot.find_element_by_id('section-navigator-content').text
            loc=pagenum.find('f') 
            numpages=pagenum[loc+2:len(pagenum)]
            print(numpages) #amount of pages
            amount=int(numpages)*15  #15 questions per page
            print(amount)


        elem=[]
        wordlist=[]

        if pages == True:
            while len(wordlist) <= amount:  
                elem.extend(bot.find_elements_by_class_name('stats-item')) #gets selenium webelements


                for i in elem: #ADDS TO WORDLIST
                    meme=i.text
                    #print(wordlist)
                    if meme != '': #ignore blank lines
                        string=meme.replace('\n','!')
                        wordlist.append(string) # gets the words


                #print(elem)
                bot.find_elements_by_class_name('right')[0].click() #switches to next page
                elem=[] #resets the list
                time.sleep(0.1)


        else:
            elem.extend(bot.find_elements_by_class_name('stats-item'))
            for i in elem:
                meme=i.text
                #print(meme)
                if meme != '': #ignore blank lines
                    wordlist.append(meme.replace('\n','!')) # gets the words
                
        #print(wordlist)

        
        #print(wordlist)
        
        for i in wordlist:
            #print(i)
            split=i.find('!')
            question=i[0:split]  #finds the question and saves as 'question'
            leng=len(i)
            Answer=sanitiseInc(i[split+1:leng]) #finds answer
            #print('Question is: '+question)
            #print('answer is: '+Answer)

            self.answer[question]=Answer #append to dictionary.
        time.sleep(0.5)
        self.listquestions()

    def listquestions(self):
        bot=self.bot
        bot.find_elements_by_class_name('infinity')[0].click() #no breaks
        try:
            bot.find_element_by_id('full-list-switcher').click()
            time.sleep(0.1)
        except:
            pass
        bot.find_element_by_id('start-button-main').click() #start challenge
        time.sleep(1)
        finished=False
        #answers questions
        while finished == False:
        
            question=sanitiseInside(bot.find_element_by_id('question-block').text)  #finds question
            try:
                ans=sanitiseInc(self.answer[question])
            except: #if it can't find the question
                
                key=get_close_matches(question,[*self.answer]) #if question is slightly different
                time.sleep(0.5)
                try:
                    ans=self.answer[key[0]] #if this doesn't work, it can't resolve the key and will make a new one. (this line is still close matches)
                except:
                    bot.find_element_by_id('submit-button').click()
                    bot.find_element_by_id('submit-button').click() #goes ahead
                    correct=sanitiseInside(bot.find_element_by_id('correct-answer-field').text)  #finds correct answer
                    self.answer[question]=correct #adds to dictionary

            print(question)
            print(ans)
            imp=bot.find_elements_by_xpath('//*[@id="answer-text"]')[1]
            imp.send_keys(ans)
            submit=bot.find_element_by_id('submit-button')
            try:
                submit.click()
            except:
                try:
                    correct=sanitiseInc(bot.find_element_by_id('correct-answer-field').text) #corrects anwser
                    print('Wrong! Correcting...')
                except:
                    print('Finished!')
                    print('     ')
                    meme=input('Please navigate the the task you want to complete! Press enter when ready.')
                    meme.strip()
                    self.tasktype()
                    finished=True
                    break
                self.answer[question] = correct
                bot.find_element_by_id('continue-button').click()
                time.sleep(0.1)
            time.sleep(0.1)
            try:
                bot.find_elements_by_xpath('//*[@id="answer-text"]')[1]
            except:
                finished=True






    def maths(self):
        print('nothing for maths yet...')
        pass

def sanitiseInc(string):
    string.strip() #removes whitespace
    newstr=string #creates variable
    num=int(string.find(';')) #if there is multipule solutions, use the first.
    if num != -1:
        newstr=string[0:num] #use the first

    num=int(string.find(',')) #if there is multipule solutions, use the first. (this time with commas)
    if num != -1:
        newstr=string[0:num] #use the first

    num=int(string.find('(')) #if there is multipule solutions, use the first. (this time with parenthesis)
    if num != -1:
        newstr=string[0:num-1] #use the first

    num=int(string.find('|')) #if there is multipule solutions, use the first. (this time with pipes | )
    if num != -1:
        newstr=string[0:num-1] #use the first
        
    return newstr #returns the sanitised string.

def sanitiseInside(string):
    loc=string.find('(')
    string1=string
    string1.strip()
    if loc != -1:
        string1=string[0:loc-1]
    return string1

#do everything
username = input('Username/Email: ')
passwrd = input('Password: ')
print('         ')
ed = Edu(username,passwrd)
ed.login()
time.sleep(2)
#ed.bot.get('https://www.educationperfect.com/app/#/French/645239/187213/list-starter') #ONLY FOR DEBUGGING
meme=input('Please navigate the the task you want to complete! Press enter when ready.')
time.sleep(1)
ed.bot.maximize_window()
ed.tasktype()
