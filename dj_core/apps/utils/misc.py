import hashlib, random, string
from dj_core.settings import *
from apps.backoffice.models import *
from apps.utils.models import SessionData
import re


def email_validator(email: str) -> bool:
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    else:
        return False

def make_search_fp(in_num):
    fp = SALT_STR + in_num
    return hashlib.md5(fp.encode('utf-8')).hexdigest()

def update_or_create_session_data(session_key, session_type, payload):
    qs = SessionData.objects.filter(session_key=session_key)
    if len(qs) > 0:
        sd = qs.last()
        sd.session_data = payload
        sd.session_type = session_type
        sd.save()
    else:
        sd = SessionData.objects.create(session_key=session_key, session_type=session_type, session_data=payload)
        sd.save()
    return sd

def get_session_data(session_key, session_type):
    qs = SessionData.objects.filter(session_key=session_key).filter(session_type=session_type)
    return qs.last()

def create_or_get_buyer(data):
    phone_number = data['phone_number']
    num_fp = make_search_fp(phone_number)

    qs = Buyer.objects.filter(num_fp=num_fp)

    if len(qs) > 0:
        # we will overwrite email for consistency
        obj = qs.last()
        obj.email = data['email']
        obj.save()
        return obj

    else:
        name = data['name']
        email = data['email']
        buyer = Buyer.objects.create(
            mobile_number=phone_number,
            num_fp=make_search_fp(phone_number),
            email=data['email'],
            name=data['name']
        )
        buyer.save()

        return buyer


def make_uuid():
    tmp = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    qs = Application.objects.filter(app_uuid=tmp)
    if len(qs) > 0:
        return make_uuid()
    else:
        return tmp