from django.template.loader import render_to_string
from dj_core.settings import *
from django.core.mail import EmailMultiAlternatives
from apps.backoffice.models import *
import apps.utils.pdf_maker.make_prequal as pm


def make_and_send_pq_letter(**kwargs):
    """Simple function to send out the PDF to applicants with agent CCed

    Inputs:
        Required: app_uuid - our internal 32 byte UUID for applications
        Optional: to - destination emails, defaults to available emails in the buyers list."""
    app_uuid = kwargs.get('app_uuid', False)
    if app_uuid == False:
        raise ValueError('Application UUID is required for sending the Pre-Qualification letter.')

    # build PDF
    else:
        app = Application.objects.get(app_uuid=app_uuid)
        pm.build_pre_qual_letter(app_uuid)
        pdf_path = str(BASE_DIR) + '/sess_data/{}/Pre-Qualification.pdf'.format(app_uuid)

        with open(pdf_path, 'rb') as f:
            data = f.read()

        buyers = app.answers['buyers']

        # process heading
        if len(buyers) == 2:
            name = list(map(lambda x: x.get('name'), app.answers['buyers']))
            name = name[0] + ' and ' + name[1]
        elif len(buyers) == 1:
            name = app.answers['buyers'][0]['name']
        elif len(buyers) > 2:
            name = list(map(lambda x: x.get('name'), app.answers['buyers']))
            name = ', '.join(name[:-1]) + ', and ' + name[-1]

    to = kwargs.get('to', False)

    if to == False:
        to = list(filter(None, map(lambda x: x.get('email', None), buyers)))
    else:
        to = [to]

    # send out pq email
    context = {'first_name': name, 'greeting': 'Dear ' + name + ','}
    subject = 'Mortgage Pre-Qualification Letter'
    from_email = 'noreply@telperionscientific.com'
    # TODO: make agent dynamic
    msg = EmailMultiAlternatives(subject=subject, from_email=from_email, to=to, cc=['john.vu@resmac.com'])
    html_message = render_to_string('backoffice/pq_email.html', context)
    msg.attach_alternative(html_message, "text/html")
    msg.attach('Pre-Qualification Letter.pdf', data, 'application/pdf')
    msg.send()

    # send out agent email
    context = {'first_name': 'John,', 'applicant': name, 'phone': app.answers['buyers'][0]['phone_number'],
               'email': app.answers['buyers'][0]['email']}
    subject = 'Pre-Qualification Letter Requested'
    from_email = 'noreply@telperionscientific.com'
    # TODO: make agent dynamic
    msg = EmailMultiAlternatives(subject=subject, from_email=from_email, to=['john.vu@resmac.com'])
    html_message = render_to_string('backoffice/lead_email.html', context)
    msg.attach_alternative(html_message, "text/html")
    msg.attach('Pre-Qualification Letter.pdf', data, 'application/pdf')
    msg.send()


    # add current data into the application object
    # app.downloaded_states.append({len(app.downloaded_states): app.process_for_output()})
    app.save()