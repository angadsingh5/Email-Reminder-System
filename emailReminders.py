import requests 
import smtplib

'''
Change these to your credentials and name
'''
your_name = "KTP Reminders"
your_email = "ktpumd.alerts@gmail.com"
your_password = "ajkhlgqvodsgtiwk"

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(your_email, your_password)
print('here...')

# Read the google sheet from api spreadsheets 

r = requests.get("https://api.apispreadsheets.com/data/J5wBSWKpXa3le3gw/")

if r.status_code == 200:
	# SUCCESS
	data = r.json()["data"]
	print("SUCCESS")
else:
	# ERROR
	data=None
	print("ERROR")
  
# Loop through the emails
for idx in range(len(data)):

    # Get each records name, email, subject and message
    name = data[idx]["Name"].strip()
    email = data[idx]["Email"].strip()
    subject = data[idx]["Subject"].strip()
    message = data[idx]["Message"].strip()
    status = data[idx]["Status"].strip()

    if status != "complete":
        # Create the email to send
        full_email = ("From: {0} <{1}>\n"
                  "To: {2} <{3}>\n"
                  "Subject: {4}\n\n"
                  "{5}"
                  .format(your_name, your_email, name, email, subject, message))

        # In the email field, you can add multiple other emails if you want
        # all of them to receive the same text
        try:
            server.sendmail(your_email, [email], full_email)
            print('Email to {} successfully sent!\n\n'.format(email))
        except Exception as e:
            print('Email to {} could not be sent :( because {}\n\n'.format(email, str(e)))

# Close the smtp server
server.close()