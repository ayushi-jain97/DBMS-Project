from django.http import HttpResponse
from django.db import connection
from django.http import HttpResponseRedirect

from django.shortcuts import render
import MySQLdb

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("show tables")
        row = cursor.fetchall()
	return str(len(row))
	
def valid(username,password):
    cursor=connection.cursor()
    cursor.execute('select * from management where rollnumber='+username+' and password="'+password+'"')
    row=cursor.fetchall()
    cursor.close()
    return len(row)==1 

def index(request, **kwargs):
    if request.method=='POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not valid(username,password):
            error="Username and password don't match!"
            return render(request, "home.html")
        else:
            request.session['admin_logged']=True
            return HttpResponseRedirect("/management")
    return render(request, "home.html", {})
