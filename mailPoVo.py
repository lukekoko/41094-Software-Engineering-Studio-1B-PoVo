import os
import smtplib
import base64
##def sendEmail():
#with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    #smtp.ehlo()
    #smtp.starttls()
    #smtp.ehlo()
#    
 #   smtp.login('povotest1@gmail.com', 'povotest123')
#    
 #   subject = 'Test email'
 #   body = 'test email'
#    
 #   msg = f'Subject: {subject}\n\n{body}'
#    
 #   smtp.sendmail('povotest1@gmail.com', 'ianhuang7991@gmail.com', msg)
def sendConfirmationEmail(email, name):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login('povotest1@gmail.com', 'povotest123')
            
            enc = base64.b64encode(email);
            
            
            subject = 'Welcome to Povo!'
            body = """
            Hi %s
            
            Thank you for signing up with PoVo
            
            Please click on this link to confirm your email:
            
            http://66.70.188.73/confirmation?acc=%s
            
            PoVo
            Australia's donation exchange place
            """%(name, enc)
            message = 'Subject: {}\n\n{}'.format(subject, body)
            server.sendmail('povotest1@gmail.com', email ,message)
            server.quit()
            print("Success: Email sent!")
        except:
            print("Email failed to send.")
            
def sendConfirmAd(email, name):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login('povotest1@gmail.com', 'povotest123')
            
            enc = base64.b64encode(email);
            
            
            subject = 'Your ad has successfully been posted!'
            body = """
            Hi %s,
            Your ad has successfully been posted!
            
            Please click on this link to view your your ad:
            
            http://66.70.188.73/advertisement/view
            
            PoVo
            Australia's donation exchange place
            """%(name)
            message = 'Subject: {}\n\n{}'.format(subject, body)
            server.sendmail('povotest1@gmail.com', email ,message)
            server.quit()
            print("Success: Email sent!")
        except:
            print("Email failed to send.")
            
def sendConfirmApp(email, name):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login('povotest1@gmail.com', 'povotest123')
            
            enc = base64.b64encode(email);
            
            
            subject = 'Your appointment has successfully been created!'
            body = """
            Hi %s,
            
            Your appointment has successfully been created!
            
            Please click on this link to view your your ad:
            
            http://66.70.188.73//myappointments
            
            PoVo
            Australia's donation exchange place
            """%(name)
            message = 'Subject: {}\n\n{}'.format(subject, body)
            server.sendmail('povotest1@gmail.com', email ,message)
            server.quit()
            print("Success: Email sent!")
        except:
            print("Email failed to send.")