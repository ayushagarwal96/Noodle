import smtplib

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("noodleportal819@gmail.com", "")  # enter password
message = "Message_you_need_to_send"
s.sendmail("noodleportal819@gmail.com", "prateekpvjain@gmail.com", message)
s.quit()
