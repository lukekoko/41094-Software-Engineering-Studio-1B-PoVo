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
def sendConfirmationEmail(email, name, usertype):
        #try:
		server = smtplib.SMTP('smtp.gmail.com:587')
		server.ehlo()
		server.starttls()
		server.login('povotest1@gmail.com', 'povotest123')
		
		enc = base64.b64encode(email);
        
            
            
		if(usertype == 1): usertype_s = 'Charity'
		if(usertype == 2): usertype_s = 'Donor'
		else: usertype_s = 'Fuck'
	
		subject = 'Welcome to Povo!'
		body = """
		Hello %s ! Welcome to Povo, thank you for signing up for our service as a %s 
	
		Please click this link bellow to confirm your account
	
		http://localhost/confirmation?acc=%s
		""" % (name, usertype_s, enc)
	
		message = 'Subject: {}\n\n{}'.format(subject, body)
		server.sendmail('povotest1@gmail.com', email ,message)
		server.quit()
		print("Success: Email sent!")
        #except:
         #   print("Email failed to send.")