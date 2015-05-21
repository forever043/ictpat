from django.core.mail import send_mass_mail

message1 = ('Subject here', 'Here is the message', 'from@example.com',
    ['first@example.com', 'other@example.com'])
message2 = ('Subject here', 'Here is the message', 'from@example.com',
    ['first@example.com', 'other@example.com'])
send_mass_mail([message1, message2], fail_silently=False)


smtplib.SMTPException

