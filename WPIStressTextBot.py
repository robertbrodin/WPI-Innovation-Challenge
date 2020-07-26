'''
The WPI Stress Text Service
Perceived Stress Scale (PSS) Text Bot - Stress Management Tool for College Students

@authors: Ishani Bedre and Robert Brodin

ipbedre@wpi.edu
rbrodin@wpi.edu

Date: 07/25/2020

The program will take user input, and send an email request to the WPI SDCC for an appointment.
As a prototype, we have not added push notifications/texting ability, we will need resources to purchase a phone number.

'''

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
import sys
import time

responses = []
questions = ["1. In the last month, how often have you been upset because of something that happened unexpectedly?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often",
            "2. In the last month, how often have you felt that you were unable to control the important things in your life?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often",
            "3. In the last month, how often have you felt nervous and “stressed”?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often",
            "4. In the last month, how often have you felt confident about your ability to handle your personal problems?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often",
            "5. In the last month, how often have you felt that things were going your way?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often",
            "6. In the last month, how often have you found that you could not cope with all the things that you had to do?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often",
            "7. In the last month, how often have you been able to control irritations in your life?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often",
            "8. In the last month, how often have you felt that you were on top of things?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often",
            "9. In the last month, how often have you been angered because of things that were outside of your control?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often",
            "10. In the last month, how often have you felt difficulties were piling up so high that you could not overcome them?\n0=Never\n1=Almost Never\n2=Sometimes\n3=Fairly Often\n4=Very Often"]


def responseAdd():

    try:
        answer = int(input("Answer: "))
        if (answer > -1 and answer <= 4):
            responses.append(answer)
            isNum = True
        else:
            print("Please enter a number 0-4")
            isNum = False
    except:
        print("Please enter a number 0-4")
        isNum = False
    return isNum

for x in range(0, 10):
   print(questions[x])
   isNum = False
   while not isNum:
       isNum = responseAdd()
       print(isNum)


# 4, 5, 7, 8 are flipped
flipNum = {"0": 4, "1": 3, "2": 2, "3": 1, "4": 0}

responses[3] = flipNum[str(responses[3])]
responses[4] = flipNum[str(responses[4])]
responses[6] = flipNum[str(responses[6])]
responses[7] = flipNum[str(responses[7])]

total = 0
for num in responses:
  total+=num
print("Your stress score score is " + str(total))

avg_college_score = 15.17

if total <= avg_college_score:
   print("The average college student scores 15. Your stress level is less than that of the average college student.")
elif total - avg_college_score <= 1:
   print("The average college student scores 15. Your stress level is around that of the average college student.")
elif total >= avg_college_score:
   print("The average college student scores 15. Your stress level is higher than that of the average college student.")


test = str(raw_input("Would you like some recommendations?"))
if test == "yes":
   print("links to stuff")
elif test == "no":
   print("OK")

counselors = str(raw_input("Would you like to set up a meeting with a WPI Counselor?"))

if counselors.lower() == 'yes':
   studentName = str(raw_input("Enter your name: "))
   studentEmail = str(raw_input("Enter your WPI email: "))
   studentPassword = str(raw_input("Enter your password: "))
   studentDate = str(raw_input("What day would you like to schedule your appointment for?"))

elif counselors.lower() == 'no':
   print("Okay! Thanks for using our text bot! Text 'STRESS' to take the test again.")




# Used for ease of changing the email that is being sent to the colleges. Reads a text file (txtFile) and returns a list of strings from the desired email to be sent text file.
def getEmailToSend(txtFile, name, date):
    lineList = ""
    fileToRead = open(txtFile, "r")
    filedata = fileToRead.read()
    fileToRead.close()

    filedata = filedata.replace("DATE", date)
    filedata = filedata.replace("NAME", name)

    f = open(txtFile, 'w')
    f.write(filedata)
    f.close()

    fileToRead = open(txtFile, "r")
    for line in fileToRead:
        lineList = lineList + line

    fileToRead.close()
    filedata = filedata.replace(name, "NAME")
    filedata = filedata.replace(date + ".", "DATE.")

    f = open(txtFile, 'w')
    f.write(filedata)
    f.close()

    return lineList

# Used to get a list of the college email addresses. Reads a text file (txtFile) and returns a list of strings of email addresses.
def getEmailAddresses(txtFile):
    emailList = []
    fileToRead = open(txtFile, "r")
    for email in fileToRead:
        # Creating a new variable to hold the email address, up until the dash. As well as the name!
        # When hitDash is set to true, stop appending to that variable and switch to a different variable.
        # I could have done this more efficiently but alas, it works and for this script that is what matters.
        emailAddress = ""
        name = ""
        hitDash = False
        for char in email:
            if(char == "-"):
                hitDash = True
            elif not hitDash:
                emailAddress+=char
            else:
                name+=char
        emailList.append(emailAddress)
        emailList.append(name)
    fileToRead.close()
    return emailList

# Used to send an email. Takes argument toAddr (email address to send email to), body (the content of the email). Function is void.
def sendEmail(fromAddr, password, toAddr, body, name, title):
    msg = MIMEMultipart()
    msg['From'] = name + " <" + fromAddr + ">"
    msg['To'] = toAddr
    msg['Subject'] = title # can make more specific, just testing for now.

    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromAddr, password)
    text = msg.as_string()
    server.sendmail(fromAddr, toAddr, text)
    server.quit()

# TODO: getEmailToSendWorks (reading from emailToSend.txt)
testList1 = getEmailToSend("emailToSend.txt", studentName, studentDate)
print testList1
testList = getEmailAddresses("collegeEmailAddresses.txt")
print testList

count = 0
email = []
name = []
while count < len(testList):
    if(count % 2 == 0):
        email.append(testList[count])
    else:
        name.append(testList[count].replace("\n", ""))
    count+=1
print email
print name

# TODO: Code works up until here! As of 11:37 AM
messages = []
for n in name:
    messages.append(getEmailToSend("emailToSend.txt", studentName, studentDate))

def getAccountInfo(txtFile):
    # Keys in the hashmap are name, email, password, and title
    userInfo = {}
    fileToRead = open(txtFile, "r")
    for line in fileToRead:
        key = ""
        value = ""
        hitDash = False
        for word in line:
            if (word == "-"):
                hitDash = True
            elif not hitDash:
                key += word
            else:
                value += word
        userInfo[key.strip().lower()] = (value.replace("\n", "")).lstrip()
    return userInfo

print messages
userInfo = getAccountInfo("accountInfo.txt")
print userInfo

counter = 0
for message in messages:
    sendEmail(studentEmail, studentPassword, email[counter], message, studentName,
              userInfo["title"])
    counter+=1
