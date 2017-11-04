from django.http import HttpResponse
from django.db import connection
from django.shortcuts import render
import MySQLdb

def my_custom_sql():
    with connection.cursor() as cursor:
        cursor.execute("show tables")
        row = cursor.fetchall()
	return str(len(row))
	


def index(request, **kwargs):
    cursor=connection.cursor()
    cursor.execute("select * from roboticsEvent")
    row1=cursor.fetchall()
    cursor.execute("select id,members.name,phone from roboticsEvent, memberPhone, members where convener=members.rollnumber and members.rollnumber=memberPhone.rollnumber and convener=memberPhone.rollnumber")
    row2=cursor.fetchall()
    cursor.execute("select id,members.name,phone from roboticsEvent, memberPhone, members where coconvener=members.rollnumber and members.rollnumber=memberPhone.rollnumber and coconvener=memberPhone.rollnumber")
    row3=cursor.fetchall()
    cursor.close()
    x=[]
    for i in range(len(row1)):
        y=list(row1[i])
        for j in row2:
            if row1[i][0]==j[0]:
                y.append([j[1],j[2]])
                break
        for j in row3:
            if row1[i][0]==j[0]:
                y.append([j[1],j[2]])
                break
        x.append(y)
    print x
    return render(request, "technexEvents.html", {'event_list':x})
