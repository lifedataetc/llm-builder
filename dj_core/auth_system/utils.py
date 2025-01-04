import string
import random
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

def generate_random_string(length):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

def update_user_password(user, plen=32):
    password = generate_random_string(plen)
    user.set_password(password)
    user.save()
    return password

def email_opt(user):
    password = update_user_password(user)
    email = user.email
    name = user.first_name.title() + user.last_name.title()
    context = {'name': name, 'password': password}
    subject = 'One Time Password for Morty'
    from_email = 'noreply@telperionscientific.com'
    msg = EmailMultiAlternatives(subject=subject, from_email=from_email, to=[email])
    html_message = render_to_string('accounts/password_email.html', context)
    msg.attach_alternative(html_message, "text/html")
    msg.send()
