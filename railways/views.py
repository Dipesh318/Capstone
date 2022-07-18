from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db.models import Count, F, Avg
from django.core.paginator import Paginator
from django.conf import settings

from .models import *
import datetime  
from datetime import date 
import calendar 
import random
#stripe.api.key = settings.STRIPE_SECRET_KEY

today = date.today()

alp = ["A","B","H"]
# Create your views here.

def findDay(year, month, day):    
    born = datetime.date(year, month, day) 
    return born.strftime("%A") 


def index(request):
    return render(request,"railways/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "railways/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "railways/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "railways/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "railways/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "railways/register.html")


def book(request):
    pass

def check_train(request):
    result = city.objects.all()
    if request.method == "POST":
        start = request.POST['from']
        end = request.POST['to']
        trainResult = trains.objects.filter(origin__in = city.objects.filter(cityName = start), destination__in = city.objects.filter(cityName = end))
        print(type(trainResult[0]))
        return render(request,"railways/train.html",{
        'cities' : result,
        'trains' : trainResult
    })
    return render(request,"railways/train.html",{
        'cities' : result
    })

def cancel(request):
    if request.method == "POST":
        pnr = request.POST['pnr']
        print(pnr)
        result = passenger.objects.filter(PNR = pnr)
        if len(result) < 1 :
            return render(request,"railways/error.html",{
                'message' : f"Ticket(s) with PNR : {pnr} not found"
            })
        totalTicket = len(result)
        amount = passenger.objects.filter(PNR = pnr).aggregate(Avg('cost'))
        price = amount['cost__avg']
        passenger.objects.filter(PNR = pnr).delete()
    
        return render(request,"railways/cancel.html",{
            'passengers' : f"{totalTicket} Ticket(s) with PNR : {pnr}, Rs{price} Will be refunded with in 7 working days "
        })
    return render(request,"railways/cancel.html")

def check_pnr(request):
    if request.method == "POST":
        pnr = request.POST['pnr']
        print(pnr)
        result = passenger.objects.filter(PNR = pnr)
        print(result)
        if len(result) < 1 :
            return render(request,"railways/error.html",{
                'message' : f"No booking found with PNR : {pnr}"
            })
        return render(request,"railways/pnr.html",{
            'passengers' : result
        })
    return render(request,"railways/pnr.html")

def seat(request):
    result = city.objects.all()
    if request.method == "POST":
        start = request.POST['from']
        end = request.POST['to']
        date = request.POST['date']
        if (datetime.date(int(date[0:4]),int(date[5:7]),int(date[8:]))<today):
            return render(request,"railways/error.html",{
            'message': "Date Should be greater than Current Date"
            })
        current_day = days.objects.filter(day=findDay(int(date[0:4]),int(date[5:7]),int(date[8:])))
        trainResult = trains.objects.filter(origin__in = city.objects.filter(cityName = start), destination__in = city.objects.filter(cityName = end), travelDays__in = current_day)
        print(trainResult)
        if (len(trainResult)<1):
            return render(request,"railways/error.html",{
            'message': "Train is not Scheduled for Selected Date"
            })
        seat_info=[] 
        for data in trainResult:
            tempData = booking.objects.filter(train = data, date = date)
            if len(tempData) < 1:
                createTrain = booking(train = data, date = date)
                createTrain.save()
            seat_info.append(booking.objects.get(train = data, date = date))
        print(seat_info)
        return render(request,"railways/seat.html",{
        'cities' : result,
        'trains' : seat_info,
        'start' : start,
        'end' :end
    })
    return render(request,"railways/seat.html",{
        'cities' : result
    })


def book(request,train,date):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    trainNumber = (train[-6:-1])
    trainResult = trains.objects.get(trainNo = trainNumber)
    return render(request,"railways/book.html",{
        'data' : booking.objects.get(train = trainResult, date = date)
    })


def booking_page(request,train,date,fname,lname,age,gender,seat,pnr,cost):
    trainNumber = (train[-6:-1])
    trainResult = trains.objects.get(trainNo = trainNumber)
    print(trainResult)
    book_ticket = booking.objects.get(train = trainResult, date = date)
    print(book_ticket)
    if seat == "Sleeper":
        booking.objects.filter(train = trainResult, date = date).update(Sleeper = F('Sleeper')-1)
        seat_count = booking.objects.get(train = trainResult, date = date)
        ans = seat_count.Sleeper
    elif seat == "AC_I":
        booking.objects.filter(train = trainResult, date = date).update(AC_I = F('AC_I')-1)
        seat_count = booking.objects.get(train = trainResult, date = date)
        ans = seat_count.AC_I
    elif seat == "AC_II":
        booking.objects.filter(train = trainResult, date = date).update(AC_II = F('AC_II')-1)
        seat_count = booking.objects.get(train = trainResult, date = date)
        ans = seat_count.AC_II
    elif seat == "AC_III":
        booking.objects.filter(train = trainResult, date = date).update(AC_III = F('AC_III')-1)
        seat_count = booking.objects.get(train = trainResult, date = date)
        ans = seat_count.AC_III
    
    seat = f"{seat[:2]}-{alp[random.randint(0,2)]}"+str(random.randint(1,72))
    check_Seat = passenger.objects.filter(train_info = book_ticket, seat = seat)
    if len(check_Seat) > 0:
        seat = f"{seat[:2]}-{alp[random.randint(0,2)]}"+str(random.randint(1,72))
        check_Seat = passenger.objects.filter(train_info = book_ticket, seat = seat)
    confirm_ticket = passenger(firstName = fname, lastName = lname, age = age, Gender = gender, PNR = pnr, seat = seat,cost = cost)
    passenger.objects.filter(PNR = pnr).update(cost = cost)
    confirm_ticket.save()
    confirm_ticket.train_info.add(book_ticket)
    return HttpResponse(ans)

def pay(request,pnr,price):
    print(price)
    passenger.objects.filter(PNR = pnr).update(cost = price)
    return HttpResponse("DOne")

def payment(request):
    pnr = request.POST['pnr']
    amount = passenger.objects.filter(PNR = pnr).aggregate(Avg('cost'))
    print(amount)
    price = amount['cost__avg']
    print(price)
    return render(request,"railways/checkout.html",{
        'price' : price
    })