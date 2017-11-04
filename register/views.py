from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render
from django.core.validators import validate_email
import MySQLdb


def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("show tables")
        row = cursor.fetchall()
	return str(len(row))

def validUsername(username):
    with connection.cursor() as cursor:
        cursor.execute("select username from participants")
        row = cursor.fetchall()
    row=[i[0] for i in row]
    if username in row:
        return False
    return True
    
def validPhone(phone):
    x=str(phone)
    for i in x:
        if i not in '1234567890':
            return False
    return len(x)==10

def validEvent(events):
    return len(events)!=0

def valid(phone,username,events):
    return validUsername(username) and validPhone(phone) and validEvent(events)

def index(request, **kwargs):
    name="";college="";email="";message=""
    phone="";username="";events=[];userError='';phoneError='';eventError='';g=['',''];event=['Robowars','Maze Explorer','Pixelate','Modex','Hurdle Mania']
    if request.method=="POST":
        name = request.POST.get('fullname', '')
        college = request.POST.get('college', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', 0)
        username = request.POST.get('username', '')
        gender = request.POST.get('gender', '')
        password = request.POST.get('password', '')
        events = request.POST.getlist('event', '')
        if gender=='F':
            g[1]='checked'
        else:
            g[0]='checked'
        for i in range(len(event)):
            if event[i] in events:
                event[i]='checked'
            else:
                event[i]=''
        if not valid(phone,username,events):
            if not validUsername(username):
                userError="Username already exists!"
            if not validPhone(phone):
                phoneError="Invalid Phone Number!"
            if not validEvent(events):
                eventError="You must select atleast one event."
            print event
            return render(request, "technexRegister.html", {'name':name,'college':college,'email':email,'phone':phone,'username':username,'userError':userError,'phoneError':phoneError,'eventError':eventError,'event':event,'g':g})
        else:
            try:
                cursor=connection.cursor()
                cursor.execute('insert into participants(name,college,email,phone,username,password,gender) values("'+name+'","'+college+'","'+email+'",'+str(phone)+',"'+username+'","'+password+'","'+gender+'")')
                cursor.close()
                cursor=connection.cursor()
                cursor.execute('select id,name from roboticsEvent')
                row=cursor.fetchall()
                cursor.close()
                dic={}
                for i in row:
                    dic[i[1]]=i[0]
                x=[]
                for i in events:
                    x.append(dic[i])
                print x
                for i in x:
                    try:
                        cursor=connection.cursor()
                        cursor.execute('insert into register(eventid,username) values('+str(i)+',"'+username+'")')
                        cursor.close()
                    except:
                        pass
            except:
                db.rollback()
            message="Thank you for registering!"
            return render(request, "technexRegister.html", {'name':'','college':'','email':'','phone':'','username':'','userError':'','phoneError':'','eventError':'','message':message})
    else:
        return render(request, "technexRegister.html", {'name':"",'college':'','email':'','phone':'','username':'','userError':'','phoneError':'','eventError':''})
    
    
    
    
    