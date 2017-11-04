from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from dateutil.parser import parse
import datetime
from random import choice
from string import ascii_uppercase
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import transaction,connection
import base64


def validPhone(phone):
    x=str(phone)
    for i in x:
        if i not in '1234567890':
            return False
    return len(x)==10

def validRoll(rollnumber):
    x=str(rollnumber)
    for i in x:
        if i not in '1234567890':
            return False
    return len(x)==8

def validRating(rating):
    x=str(rating)
    try:
        y=int(x)
        if not (y>=0 and y<=10):
            return False
    except:
        return False
    return True

def invalidDate(date):
    try:
        parse(date)
    except Exception as e:
        print e
        return e
    return ''

def validateRoboticsEvent(schema,newdata):
    startdate=schema.index('date')
    technexdate=schema.index('technexDate')
    for i in range(len(newdata)):
        print newdata[i][technexdate]
        y=parse(newdata[i][technexdate])
        d = y.strftime('%Y-%m-%d')
        cursor=connection.cursor()
        cursor.execute("select enddate from technexRobotics where startdate="+'"'+d+'"')
        row=cursor.fetchall()
        cursor.close()
        print 
        print 'here',row
        if len(row)==1 and parse(newdata[i][startdate])>=parse(newdata[i][technexdate]) and parse(newdata[i][startdate])<=parse(row[0][0]):
            pass
        elif len(row)==1:
            return "Date should be between "+newdata[i][technexdate]+' and '+row[0][0]
        
def validateTechnexRobotics(schema,newdata):
    startdate=schema.index('startdate')
    enddate=schema.index('enddate')
    for i in range(len(newdata)):
        print newdata[i][startdate]+'here is date'
        if parse(newdata[i][startdate])>parse(newdata[i][enddate]):
            return "Start date should be less than end date."

def valid(request,tablename,schema,newdata):
    records=[zip(schema,i) for i in newdata]
    message=[]
    for i in range(len(newdata)):
        for j in range(len(schema)):
            if not newdata[i][j]:
                message.append((i,j,schema[j]+" is compulsory!"))
            else:
                if 'phone' in schema[j] and not validPhone(newdata[i][j]):
                    x='Invalid Phone!'
                    message.append((i,j,x))
                elif schema[j] in ['rollnumber','convener','coconvener','inchargeID'] and not validRoll(newdata[i][j]):
                    x=schema[j]+' is an 8 digit number!'
                    message.append((i,j,x))
                elif 'rating' in schema[j] and not validRating(newdata[i][j]):
                    x='Rating should be less than 10 and greater than 0'
                    message.append((i,j,x))
                elif 'date' in schema[j] and invalidDate(newdata[i][j]):
                    x=invalidDate(newdata[i][j])
                    message.append((i,j,x))
        if tablename=='roboticsEvent':
            x=validateRoboticsEvent(schema,[newdata[i]])
            if x:
                message.append((i,-1,x))
        elif tablename=='technexRobotics':
            x=validateTechnexRobotics(schema,[newdata[i]])
            if x:
                message.append((i,-1,x))
    return message

def index(request, **kwargs):
    cursor=connection.cursor()
    cursor.execute('show tables')
    row=cursor.fetchall()
    cursor.close()
    table_list=[i[0] for i in row if '_' not in i[0]]
    print table_list
    if request.method=='POST':
        request.session['admin_logged']=False
        return HttpResponseRedirect('/home/')
    else:
        if request.session.get('admin_logged',None):
            return render(request, "management.html", {'table_list':table_list})
        else:
            return HttpResponseRedirect('/home/')


def check(colname,datatype,val):
    if 'phone' in colname:
        if not validPhone(val):
            return "Phone number is invalid!"
        else:
            return False
        

def addNewRecord(request,tablename, record, x, editable): 
    cursor=connection.cursor()
    cursor.execute("describe "+tablename)
    schema=cursor.fetchall()
    cursor.close()
    print schema
    s=[i[0] for i in schema]
    schema=[(i[0],i[1]) for i in schema]
    data=''
    print 'here is record ',record
    for i in range(len(record[:-1])):
        if 'int' in schema[i][1]:
            data+=record[i]+','
        else:
            data+='"'+record[i]+'",'
    if 'int' in schema[-1][1]:
        data+=record[-1]
    else:
        data+='"'+record[-1]+'"'
    error=valid(request,tablename,s,[record])
    error=[i[2] for i in error]
    if not error:
        try:
            cursor=connection.cursor()
            cursor.execute("insert into "+tablename+' values('+data+')')
            if tablename=='members':
                mp=''.join(choice(ascii_lowercase) for i in range(6))
                cursor.execute("insert into memberPasswords values("+record[0]+',"'+mp+'"')
            cursor.close()
        except Exception as e:
            if e[0]==1452:
                y=e[1].split()[17][2:-2]+" entered doesn't exist in the database."
            elif e[0]==1062:
                key=e[1].split()[2][1:-1]
                y='Entry for '+key+' already exists.'
            else:
                y=e
            error.append(y)
            pass
    print error
    r=zip(s,record)
    if len(error):
        print 'here',r
        return render(request, "table.html", {'tablename':tablename,'schema':s,'row':x,'editable':editable[tablename],'error':error,'record':r})
    else:
        return HttpResponseRedirect("/management/"+tablename)

def editTable(request, tablename, editstring):
    cursor=connection.cursor()
    cursor.execute('select * from '+tablename)
    row=cursor.fetchall()
    cursor.close()
    editIndex=editstring.split('a')
    editIndex=[int(i) for i in editIndex]
    record_list=[];message=''
    cursor=connection.cursor()
    cursor.execute("describe "+tablename)
    schema=cursor.fetchall()
    cursor.close()
    schema=[i[0] for i in schema]
    for i in editIndex:
        record_list.append(row[i])
    records=[zip(schema,i) for i in record_list]
    if request.method=='POST':
        newrows=[]
        for i in schema:
            if i=='image':
                x=[]
                myfiles=request.FILES.getlist('image')
                print myfiles
                for myfile in myfiles:
                    image_read=myfile.read()
                    image_64_encode = base64.encodestring(image_read)
                    x.append(image_64_encode)
            else:
                x=request.POST.getlist(i)
            print i,x
            newrows.append(x)
        print request.FILES
        newdata=[]
        print "new:",newrows
        for i in range(len(newrows[0])):
            x=[]
            for j in range(len(newrows)):
                x.append(str(newrows[j][i]))
            newdata.append(x)
        print newdata
        newrecords=[zip(schema,i) for i in newdata]
        message_list=valid(request,tablename,schema,newdata)
        print message_list
        if not len(message_list):
            for i in range(len(newdata)):
                data=''
                query='';nquery=''
                for j in range(len(newdata[i][:-1])):
                    if type(record_list[i][j])==type(1):
                        data+=str(newdata[i][j])+','
                    else:
                        data+='"'+str(newdata[i][j])+'",'
                if type(record_list[i][-1])==type(1):
                    data+=str(newdata[i][-1])
                else:
                    data+='"'+str(newdata[i][-1])+'"'
                print data
                for j in range(len(schema)-1):
                    if type(record_list[i][j])==type(1):
                        query+=schema[j]+'='+str(record_list[i][j])+' and '   
                    else:
                        query+=schema[j]+'="'+str(record_list[i][j])+'" and '
                if type(record_list[i][-1])==type(1):
                    query+=schema[-1]+'='+str(record_list[i][-1])
                else:
                    query+=schema[-1]+'="'+str(record_list[i][-1])+'"'
                for j in range(len(schema)-1):
                    if type(record_list[i][j])==type(1):
                        nquery+=schema[j]+'='+str(newdata[i][j])+', '   
                    else:
                        nquery+=schema[j]+'="'+str(newdata[i][j])+'", '
                if type(record_list[i][-1])==type(1):
                    nquery+=schema[-1]+'='+str(newdata[i][-1])
                else:
                    nquery+=schema[-1]+'="'+str(newdata[i][-1])+'"'
                print nquery,query
                try:
                    cmd= "update "+tablename+" set "+nquery+" where "+query
                    print cmd
                    cursor=connection.cursor()
                    cursor.execute(cmd)
                    cursor.close()
                except Exception as e:
                    if e[0]==1452:
                        x=e[1].split()[17][2:-2]+" entered doesn't exist in the database."
                    elif e[0]==1062:
                        key=e[1].split()[2][1:-1]
                        x='Entry for '+key+' already exists.'
                    else:
                        x=e
                    message_list.append((i,-1,x))
            print message_list
            if len(message_list):
                return render(request, "editTable.html", {'tablename':tablename,'record_list':newrecords,'message_list':message_list})
            else:
                return HttpResponseRedirect('/management/'+tablename)
        else:
            return render(request, "editTable.html", {'tablename':tablename,'record_list':newrecords,'message_list':message_list})
    print records
    return render(request, "editTable.html", {'tablename':tablename,'record_list':records})

def showTable(request,tablename):
    cursor=connection.cursor()
    cursor.execute('select * from '+tablename)
    row=cursor.fetchall()
    cursor.execute("describe "+tablename)
    schema=cursor.fetchall()
    cursor.close()
    schema=[i[0] for i in schema]
    editable={'management':False,'answers':False,'memberPhone':True,'members':True,'merchandise':True,'participants':False,'postDesc':True,'question':True,'register':False,'roboticsEvent':True,'technexRobotics':True,'workshops':True,'supplier':True,'orders':False,'sponsor':True,'funds':True,'memberPasswords':False}
    x=[]
    for r in range(len(row)):
        y=[]
        y.append(r)
        z=[str(i) for i in row[r]]
        y.extend(z)
        x.append(y)
    rows=x
    emptyRecord=[(i,'') for i in schema]
    if request.method=='POST':
        editList=[]
        if request.POST.get("edit"):
            editIndex=request.POST.getlist("sno")
            editString='a'.join(editIndex)
            print editString
            return HttpResponseRedirect("/management/"+tablename+'/'+editString+'/')
        elif request.POST.get("delete"):
            record_list=[]
            delIndex=request.POST.getlist("sno")
            for i in delIndex:
                record_list.append(row[int(i)])
            print record_list
            for i in range(len(delIndex)):
                query=''
                for j in range(len(schema)-1):
                    if type(record_list[i][j])==type(1):
                        query+=schema[j]+'='+str(record_list[i][j])+' and '
                    else:
                        query+=schema[j]+'="'+str(record_list[i][j])+'" and '
                        
                if type(record_list[i][-1])==type(1):
                    query+=schema[-1]+'='+str(record_list[i][-1])
                else:
                    query+=schema[-1]+'="'+str(record_list[i][-1])+'"'
                print query
                try:
                    cursor=connection.cursor()
                    cursor.execute("delete from "+tablename+" where "+query)
                    cursor.close()
                except:
                    pass
            return HttpResponseRedirect('/management/'+tablename)
        elif request.POST.get("new"):
            record=[]
            for i in schema:
                if i=='image':
                    x=request.FILES['image']
                    image_read=x.read()
                    image_64_encode = base64.encodestring(image_read)
                    x=image_64_encode
                else:
                    x=request.POST.get(i)
                record.append(x.strip())
            return addNewRecord(request,tablename,record,rows,editable)
    return render(request, "table.html", {'tablename':tablename,'schema':schema,'row':rows,'editable':editable[tablename],'error':'','record':emptyRecord})




