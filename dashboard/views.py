from django.shortcuts import render
from django.http import HttpResponseRedirect
from collections import OrderedDict
from django.db import connection
import MySQLdb

def index(request, username):
    cursor=connection.cursor()
    cursor.execute('select * from participants where username="'+username+'"')
    row=cursor.fetchone()
    cursor.close()
    if request.method=='POST' and request.POST.get('logout'):
        request.session['participant:'+username]=False
        return HttpResponseRedirect('/home/')
    if row:
        cursor=connection.cursor()
        cursor.execute("describe participants")
        schema=cursor.fetchall()
        schema=[i[0] for i in schema]
        print row
        print schema
        row=[[schema[i],row[i]] for i in range(len(schema))]
        cursor.execute('select name from register, roboticsEvent where eventid=id and username="'+username+'"')
        registeredEvents=cursor.fetchall()
        cursor.close()
        registeredEvents=[i[0] for i in registeredEvents]
        if request.session.get('participant:'+username,None):
            return render(request, 'dashboard.html', {'username': username,'value_list':row,'registeredEvents':registeredEvents})
    return HttpResponseRedirect('/home/')

def settings(request, username):
    message=''
    success=''
    if request.method=='POST':
        old = request.POST.get('currentpass', '')
        new = request.POST.get('newpass', '')
        new2 = request.POST.get('confirmpass', '')
        cursor=connection.cursor()
        cursor.execute('select password from participants where username="'+username+'"')
        row=cursor.fetchone()
        cursor.close()
        if new==new2 and old==row[0]:
            try:
                cursor=connection.cursor()
                cursor.execute('update participants set password="'+new+'" where username="'+username+'"')
                cursor.close()
            except:
                pass
            message="Password changed successfully!"
            success='Yes'
        elif new!=new2:
            message="Passwords don't match!"
        elif old!=row[0]:
            message="Wrong Password! Try again."
        return render(request, 'settings.html', {'username': username,'message':message,'success':success})  
    else:
        return render(request, 'settings.html', {'username': username})

def feedback(request, username):
    cursor=connection.cursor()
    cursor.execute('select id,text from question where category="rating"')
    row1=cursor.fetchall()
    cursor.close()
    error=''
    success=''
    print row1
    rating_list=[i[1] for i  in row1]
    cursor=connection.cursor()
    cursor.execute('select id,text from question where category="best"')
    row2=cursor.fetchall()
    best_list=[i[1] for i in row2]
    cursor.execute('select id,text from question where category="suggestion"')
    row3=cursor.fetchall()
    cursor.close()
    suggestion_list=[i[1] for i in row3]
    if request.method=='POST':
        cursor=connection.cursor()
        cursor.execute('select count(*) from answers where username="'+username+'"')
        count=cursor.fetchone()
        cursor.close()
        count=count[0]
        print row1
        print row2
        if not count:
            for i in row1:
                x=request.POST.get(i[1], '')
                try:
                    cursor=connection.cursor()
                    cursor.execute('insert into answers values("'+username+'",'+str(i[0])+',"'+x+'")')
                    cursor.close()
                except:
                    pass
            for i in row2:
                x=request.POST.get(i[1], '')
                try:
                    cursor=connection.cursor()
                    cursor.execute('insert into answers values("'+username+'",'+str(i[0])+',"'+x+'")')
                    cursor.close()
                except:
                    pass
            for i in row3:
                x=request.POST.get(i[1],'')
                try:
                    cursor=connection.cursor()
                    cursor.execute('insert into answers values("'+username+'",'+str(i[0])+',"'+x+'")')
                    cursor.close()
                except:
                    pass
            error="Thank you for your time!"
            success='Yes'
        else:
            error="You have already submitted the feedback."
        return render(request, 'feedback.html', {'username': username,'rating_list':rating_list,'best_list':best_list,'error':error,'success':success,'suggestion_list':suggestion_list})
    else:
        return render(request, 'feedback.html', {'username': username,'rating_list':rating_list,'best_list':best_list,'suggestion_list':suggestion_list})

