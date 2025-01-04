from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    html_template = loader.get_template('backoffice/dash_index.html')
    return HttpResponse(html_template.render({}, request))