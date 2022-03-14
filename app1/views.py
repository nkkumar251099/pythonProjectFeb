import string

from django.shortcuts import render
from django.db import connection
from django.core.mail import send_mail
import random
# Create your views here.


def xyz(request):
    return render(request, "home.html")

def signUp(request):
    email = request.POST['email']
    psw = request.POST['pswname']
    cursor = connection.cursor()
    query1 = "select * from users where email  ='" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchall()
    if len(data) > 0:
        data = {"email":"Already SignedUP" , "password":""}
        return render(request, "first.html", data)
    else:
        otp = random.randint(100000, 999999)
        strotp = str(otp)
        query2 = "insert into users (email, password, otp) values (%s, %s, %s)"
        value2 = (email, psw, strotp)
        cursor.execute(query2, value2)
        print(cursor.rowcount)
        body = 'Your Otp for our portal you signed up with email ' + email + ' is '  + strotp
        send_mail('OTP For Verification', body, 'testcodeplanet@gmail.com', ['parth@codeplanet.co.in'])
        data = {"email":email}
        return render(request, "signupsuccess.html", data)

# Create your views here.
def signin(request):
    return render(request, "login.html")


def login(request):
    email = request.POST['email']
    psw = request.POST['psw']
    cursor = connection.cursor()
    query1 = "select * from users where email  ='" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data is None:
        data = {"email": "Not SignedUP", "password": ""}
        return render(request, "first.html", data)
    else:
        if data[2] == 0:
            data = {"email": "You are not verified user", "password": ""}
            return render(request, "first.html", data)
        if data[1] == psw:
            data = {"email": "Login Success", "password": ""}
            return render(request, "first.html", data)
        else:
            data = {"email": "Password is not correct", "password": ""}
            return render(request, "first.html", data)


def otpVerification(request):
    email = request.POST['email']
    otp = request.POST['otp']
    cursor = connection.cursor()
    query1 = "select * from users where email  ='" + email + "'"
    cursor.execute(query1)
    data = cursor.fetchone()
    if data is not None:
        if data[3] == otp:
            query2 = "update users set is_verify =1 where email  ='" + email + "'"
            cursor.execute(query2)
            if cursor.rowcount == 1 :
                print("OTP Verified Success")
                data = {"email": "OTP Verified Success"}
                return render(request, "first.html", data)
        else:
            data = {"email": "OTP is Not Correct"}
            return render(request, "first.html", data)


def generateShortURl():
    letters = string.ascii_letters + string.digits
    shortUrl = ''
    for i in range(6):
        shortUrl = shortUrl + ''.join(random.choice(letters))
    return shortUrl


def urlshortner(request):
    longLink = request.GET['link']
    customUrl = request.GET['customurl']
    if customUrl is None or customUrl == '':
        shortUrl = ''
    else:
        cursor = connection.cursor()
        query1 = "select * from links where short_link  ='" + customUrl + "'"
        cursor.execute(query1)
        data = cursor.fetchone()
        if data is not None:
            data = {"email": "Already Custom URL exist please try some other url"}
            return render(request, "first.html", data)
        else:
            query2 = "insert into links (long_link, short_link) values (%s, %s)"
            value =(longLink, customUrl)
            cursor.execute(query2, value)
            data = {"email": "Your URl is shortne with nano.co/"+customUrl}
            return render(request, "first.html", data)
    if shortUrl is not None or shortUrl != '':
        while True:
            shortUrl = generateShortURl()
            cursor = connection.cursor()
            query1 = "select * from links where short_link  ='" + shortUrl + "'"
            cursor.execute(query1)
            data = cursor.fetchone()
            if data is None:
                break
        query2 = "insert into links (long_link, short_link) values (%s, %s)"
        value =(longLink, shortUrl)
        cursor.execute(query2, value)
        data = {"email": "Your URl is shortne with nano.co/"+shortUrl}
        return render(request, "first.html", data)
