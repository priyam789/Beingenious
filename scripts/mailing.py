from google.appengine.api import mail

def send_mail(recipient, subject, body, html):
	sender_address = "noreply@be-ingenious.appspotmail.com"
	message = mail.EmailMessage(sender = sender_address, subject = subject)
	message.to = recipient
	message.body = body
	message.html = html

	message.send()

def activation_mail(email, fname, lname, link):
	recipient = "%s %s <%s>" %(fname, lname, email)
	subject = "Beingenious account verification - Do not reply"
	body = """Dear %s:
			Your request to create an account on Beingenious using this email id has been received.
			Please visit the following link to activate your account.
			%s
			Please note that the link will expire in 24 hrs. following which you will be required to fill in your details again.

			Regards
			Beingenious Team
			""" %(fname, link)
	html = """ <html><head></head><body> %s </body></html>""" %(body.replace('\n', '<br>'))
	send_mail(recipient, subject, body, html)

def forgotpass_mail(email, fname, lname, link):
	recipient = "%s %s <%s>" %(fname, lname, email)
	subject = "Beingenious account verification - Do not reply"
	body = """Dear %s:
			Your request to reset your password on Beingenious using this email id has been received.
			Please visit the following link to reset your password.
			%s
			Regards
			Beingenious Team
			""" %(fname, link)
	html = """ <html><head></head><body> %s </body></html>""" %(body.replace('\n', '<br>'))
	send_mail(recipient, subject, body, html)

