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
def sendConfirmationEmail(email):
        try:
            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            server.login('povotest1@gmail.com', 'povotest123')
            
            enc = base64.b64encode(email);
            
            
            subject = 'Welcome to Povo!'
            body = """
            Thank you for signing up with PoVo
            
            Please click on this link to confirm your email
            
            http://localhost/confirmation?acc=%s
            """%(enc)
            message = 'Subject: {}\n\n{}'.format(subject, body)
            server.sendmail('povotest1@gmail.com', email ,message)
            server.quit()
            print("Success: Email sent!")
        except:
            print("Email failed to send.")