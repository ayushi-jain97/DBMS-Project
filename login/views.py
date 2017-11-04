from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render
from collections import OrderedDict
from django.http import HttpResponseRedirect
import MySQLdb


def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("select * from merchandise")
        row = cursor.fetchall()
	return row

def valid(username,password):
    cursor=connection.cursor()
    cursor.execute('select * from participants where username="'+username+'" and password="'+password+'"')
    row=cursor.fetchall()
    cursor.close()
    return len(row)==1 

def index(request, **kwargs):
    if request.method=="POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if not valid(username,password):
            error="Username and password don't match!"
            return render(request, "login.html", {'error':error,'username':username})
        else:
            request.session['participant:'+username]=True
            return HttpResponseRedirect("/dashboard/"+username)
    return render(request, "login.html", {})
