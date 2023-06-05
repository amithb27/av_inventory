from django.core.mail import send_mail

send_mail(
    "Subject here",
    "Here is the message.",
    "manikantatez@gmail.com",
    ["manikantaprasadlopinti@gmail.com"],
    fail_silently=False,
)