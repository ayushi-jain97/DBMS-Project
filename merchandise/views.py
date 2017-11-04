from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.shortcuts import render
import base64
import time,datetime

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("select * from merchandise")
        row = cursor.fetchall()
	return row
	

def index(request, **kwargs):
    message=''
    display=''
    selected_option = request.POST.get('sorting', None)
    cursor=connection.cursor()
    cursor.execute("select * from merchandise order by price")
    cursor.close()
    merchandise_list= cursor.fetchall()
    if selected_option=="2":
        with connection.cursor() as cursor:
            cursor.execute("select * from merchandise order by price desc")
            merchandise_list = cursor.fetchall()
    print type(merchandise_list)
    item_list=[i[0] for i in merchandise_list]
    
    cursor=connection.cursor()
    cursor.execute("describe merchandise")
    schema=cursor.fetchall()
    cursor.close()
    schema=[i[0] for i in schema]
    imageIndex=schema.index('image')
    print 
    print imageIndex
    print merchandise_list
    merchandise_list=[list(i) for i in merchandise_list]
    for i in range(len(merchandise_list)):
        print merchandise_list[i][imageIndex]
        image_64_decode = base64.decodestring(merchandise_list[i][imageIndex]) 
        image_result = open('./media/temp'+str(i), 'wb') # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        merchandise_list[i][imageIndex]='/media/temp'+str(i)
    print 
    cursor=connection.cursor()
    cursor.execute("select * from members")
    x=cursor.fetchall()
    cursor.close()
    roll_list=[i[0] for i in x]
    print roll_list
    if request.method=='POST' and request.POST.get('order'):
        memberid = request.POST.get('rollnumber', '')
        size = request.POST.get('size', '')
        printname = request.POST.get('printName', '')
        itemid = request.POST.get('itemid', '')
        message="Order not placed!"
        ts=time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
        
        return HttpResponseRedirect('https://www.payumoney.com/paybypayumoney/#/166E8E61A4E75E5957433E16BA32499D')

        #return render(request, "merchandise.html", {'merchandise_list':merchandise_list,'item_list':item_list,'roll_list':roll_list,'message':message})
    return render(request, "merchandise.html", {'merchandise_list':merchandise_list,'item_list':item_list,'roll_list':roll_list})