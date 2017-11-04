from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render
import base64

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("show tables")
        row = cursor.fetchall()
	return str(len(row))
	


def index(request, **kwargs):
    selected_option = request.POST.get('sorting', None)
    with connection.cursor() as cursor:
        cursor.execute("select * from workshops order by date desc")
        workshop_list= cursor.fetchall()
    if selected_option=="2":
        with connection.cursor() as cursor:
            cursor.execute("select * from workshops order by date")
            workshop_list = cursor.fetchall()
    workshop_list=[list(i) for i in workshop_list]
    cursor=connection.cursor()
    cursor.execute("describe workshops")
    schema=cursor.fetchall()
    cursor.close()
    schema=[i[0] for i in schema]
    imageIndex=schema.index('image')
    print 
    print imageIndex
    for i in range(len(workshop_list)):
        print workshop_list[i][imageIndex]
        image_64_decode = base64.decodestring(workshop_list[i][imageIndex]) 
        image_result = open('./media/temp'+str(i), 'wb') # create a writable image and write the decoding result
        image_result.write(image_64_decode)
        workshop_list[i][imageIndex]='/media/temp'+str(i)
    return render(request, "calendar.html", {'workshop_list':workshop_list})
