from django.shortcuts import render 
from product.models import AdaptorProduct as Product
from django.conf import settings
from django.utils.translation import activate
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
import pdb

def home(request):
    content ={} 
    grids = Product.objects.filter(set_grid = 1)
    homes = Product.objects.filter(set_homepage = 1)
    content ={
        'grids':grids,
        'homes':homes
    }  
    content['mediaroot'] = settings.MEDIA_URL
    return render(request, 'home.html',content) 

def switch_language(request):
    content ={}   
    if 'django_language' in request.session: 
        if settings.LANGUAGE_CODE == 'en':
            activate('zh-hans')
            request.session['django_language'] = 'zh-hans'
            settings.LANGUAGE_CODE = 'zh-hans'
        else:
            activate('en')
            request.session['django_language'] = 'en'
            settings.LANGUAGE_CODE = 'en'
    else:
        activate('en')
        request.session['django_language'] = 'en'
        settings.LANGUAGE_CODE = 'en'

    return redirect('home') 