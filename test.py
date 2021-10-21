from random import randrange

num = randrange(100000, 1000000)

print(num)

# import datetime


# # start_date = "19/10/2021"

# start_date = str(datetime.datetime.now()).split(' ')[0][2:]

# date_1 = datetime.datetime.strptime(start_date, "%y-%m-%d")

# end_date = date_1 + datetime.timedelta(days=90)

# print(start_date)

# print(date_1)
# print(end_date)

# print(date_1 < end_date)

# import smtplib
# import ssl
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from templates.email import Email

# port = 587  # For starttls
# smtp_server = "smtp.gmail.com"
# sender_email = "t8910ech@gmail.com"
# receiver_email = "felixjordan312@gmail.com"
# password = "8910@tech"

# message = MIMEMultipart("alternative")
# message["Subject"] = "Verfication email."
# message["From"] = sender_email
# message["To"] = receiver_email

# message = """\
# Subject: Hi there

# This message is sent from Python."""

# link = "https://leetcode.com/problemset/all/"

# html = Email._email(link)

# part2 = MIMEText(html, "html")

# message.attach(part2)

# context = ssl.create_default_context()
# with smtplib.SMTP(smtp_server, port) as server:
#     server.ehlo()  # Can be omitted
#     server.starttls(context=context)
#     server.ehlo()  # Can be omitted
#     server.login(sender_email, password)
#     server.sendmail(sender_email, receiver_email, message)


# import razorpay
# import hashlib
# import hmac

# # generated_signature = hmac_sha256(
# #     'order_IAKHXtANe8KwkB' + "|" + 'pay_IAKHt6HcTynKiu', '7DQCW16JtDmORBaSxLrwArPh')

# secret = '7DQCW16JtDmORBaSxLrwArPh'

# signature = hmac.new(
#     key=secret,
#     msg='order_IAKHXtANe8KwkB' + "|" + 'pay_IAKHt6HcTynKiu',
#     digestmod=hashlib.sha256
# )

# if (signature == '5ed4bf66615c3468fa0a8eb684571dd14b5e14e146fef613c5ea8e9aed4f5a7e'):
#     print('payment is successful')


# import hashlib
# import hmac

# secret = '7DQCW16JtDmORBaSxLrwArPh'
# # assumes you're using requests for data/sig
# data = 'order_IAKHXtANe8KwkB' + "|" + 'pay_IAKHt6HcTynKiu'
# signature = '5ed4bf66615c3468fa0a8eb684571dd14b5e14e146fef613c5ea8e9aed4f5a7e'
# signature_computed = hmac.new(
#     key=secret.encode('utf-8'),
#     msg=data.encode('utf-8'),
#     digestmod=hashlib.sha256
# ).hexdigest()
# print(signature_computed)
# print(signature)
# if not hmac.compare_digest(signature, signature_computed):
#     print("Invalid payload")
