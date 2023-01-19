import smtplib
from email.mime.text import MIMEText

def send_mail(customer, dealer, rating, comments):
  port = 2525
  smtp_server = "smtp.mailtrap.oi"
  # login = os.environ.get("MAILTRAP_LOGIN") <---this is probably a better way so it protects login credentials
  login = " see note" #UPDATE with Mailtrap username
  password = " see note" #UPDATE with Mailtrap pw
  message = f"<H3>New Submission</H3>\n<ul><li>Dealer: {dealer}</li>\n<li>Customer: {customer}</li>\n<li>Rating: {rating}</li>\n<li>Comments: {comments}</li></ul>"

  sender_email = "sender@example.com"
  receiver_email = "recipient@example.com" #This would be from email entered in form/ {recipient_email}
  msg = MIMEText(message, 'html')
  msg["Subject"] = "New Submission"
  msg["From"] = sender_email
  msg["To"] = receiver_email

  # THis sends the email
  with smtplib.SMTP(smtp_server, port) as server:
    # server.starttls()
    server.login(login, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    # server.quit()


