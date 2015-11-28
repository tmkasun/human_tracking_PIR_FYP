from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def login(request):
    page_title = "Welcome to Knnector."
    context = {
        'page_title': page_title
    }
    return render(request, 'logins/content/index.html', context=context)


@require_http_methods(['POST'])
def submit(request):
    user = request.POST['user_email']
    password = request.POST['user_password']
    remember = False
    if request.POST.has_key('user_remember') and request.POST['user_remember'] == 'True':
        remember = True
    is_valid = _validate_user(user, password)
    if is_valid:
        return HttpResponseRedirect(reverse('maps:base'))
    raise Http404('Invalid username page not created yet.')


def _validate_user(user, password):
    if user == 'kasun@knnect.com' and password == 'kasun':
        return True
    return False


