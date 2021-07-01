import os, sys  
sys.path.append('C:/windows/www/thriftplus/myproject/myproject/')
sys.path.append('C:/windows/www/thriftplus/myproject/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'myproject.settings'  
import django.core.handlers.wsgi  
application = django.core.handlers.wsgi.WSGIHandler()  
