from django.shortcuts import render
from django.contrib.auth import authenticate
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score

# Create your views here.
dataset = pd.read_csv('E:\Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

nltk.download('stopwords')
corpus = []
for i in range(0, 1000):
    review = re.sub('[^a-zA-Z]', ' ', dataset['Review'][i])
    review = review.lower()
    review = review.split()
    ps = PorterStemmer()
    review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
    review = ' '.join(review)
    corpus.append(review)

cv = CountVectorizer(max_features = 1500)
X = cv.fit_transform(corpus).toarray()
y = dataset.iloc[:, 1].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3, random_state = 42)

#MultinomialNB model
print("MultinomialNB")
classifier = MultinomialNB(alpha=0.1)
classifier.fit(X_train, y_train)


def home(request):
    return render(request,"index.html")

def registration(request):
    if request.POST:
        fname=request.POST["name"]
        lname=request.POST["lname"]
        phone=request.POST["phone"]
        email=request.POST["email"]
        pwd=request.POST["pass"]
        repass=request.POST["pass1"]
        add=request.POST["add"]
        print(email)
        user=User.objects.filter(username=email).exists()
        print(user)
        if not user:
            try:
                r=Registration.objects.create(fname=fname,lname=lname,email=email,contact=phone,password=pwd,address=add)
                r.save()
            except:
                messages.info(request, 'Sorry some error occured')
            else:
                try:
                    u=User.objects.create_user(username=email,password=pwd,is_superuser=0,is_active=1,is_staff=0,email=email)
                    u.save()
                except:
                    messages.info(request, 'Sorry some error occured')
                else:
                    messages.info(request, "Registration Succesful")
        else:
            messages.info(request, 'User already registered')
    return render(request,"registration.html")

def login(request):
    if request.POST:
        uname=request.POST["uname"]
        pwd=request.POST["pass"]
        user=authenticate(username=uname,password=pwd)
        if user is None:
            messages.info(request, 'Username or password is incorrect')
        else:
            userdata=User.objects.get(username=uname)
            if userdata.is_superuser == 1:
                return redirect("/adminhome")
            elif userdata.is_staff == 1:
                request.session["email"]=uname
                r = Hotels.objects.get(email=uname)
                request.session["id"]=r.id
                request.session["name"]=r.name
                return redirect("/hotelhome")
            else:
                request.session["email"]=uname
                r = Registration.objects.get(email=uname)
                request.session["id"]=r.id
                request.session["name"]=r.fname
                return redirect("/userhome")

    return render(request,"login.html")

def hotellogin(request):
    return render(request,"login.html")

def userhome(request):
    return render(request,"userhome.html")

def adminhome(request):
    return render(request,"adminhome.html")

def adminrequests(request):
    hotel=""
    data=Request.objects.all()
    hotels=Hotels.objects.all()
    if request.POST:
        hotid=request.POST["hotel"]
        hotel=Hotels.objects.get(id=hotid)
        id=request.POST["id"]
        req=Request.objects.get(id=id)
        req.hotel=hotel
        req.save()
    return render(request,"adminrequests.html",{"data":data,"hotels":hotels})

def adminuser(request):
    
    data=Registration.objects.all()
    return render(request,"adminuser.html",{"data":data})

def userhotel(request):
    data=Hotels.objects.all()
    
    return render(request,"userhotel.html",{"data":data})

def adminhotel(request):
    if request.POST:
        hname=request.POST["hname"]
        email=request.POST["email"]
        phone=request.POST["phone"]
        lic=request.POST["license"]
        date=request.POST["date"]
        add=request.POST["add"]
        image=request.FILES["image"]
        user=authenticate(name=hname,lic=license)
        if user is None:
            try:
                r=Hotels.objects.create(name=hname,dateopen=date,address=add,image=image,lic=lic,contact=phone,email=email,realrat=0)
                r.save()
            except Exception as e:
                messages.info(request, e)
            else:
                try:
                    u=User.objects.create_user(username=email,password=phone,is_superuser=0,is_active=1,is_staff=1,email=email)
                    u.save()
                except Exception as e:
                    messages.info(request, e)
                else:
                    messages.info(request, 'Registration successful')
        else:
            messages.info(request, 'Hotel already registered')

    return render(request,"adminhotel.html")


def userreview(request):
    return render(request,"userreview.html")

def about(request):
    return render(request,"about.html")


def remove(request):
    cid=request.GET.get("id")
    d=Registration.objects.get(id=cid)
    demail=d.email
    s=User.objects.filter(email=demail).delete()
    ct=Registration.objects.filter(id=cid).delete()
    return redirect("/adminuser")


def comment(request):
    rid=request.session["id"]
    pid=request.GET.get("id")
    user=Registration.objects.get(id=rid)
    data=Hotels.objects.filter(id=pid)
    if request.POST:
        rev=request.POST["review"]
        id=request.POST["hotel"]
        hotel=Hotels.objects.get(id=id)
        new_review = rev
        new_review = re.sub('[^a-zA-Z]', ' ', new_review)
        new_review = new_review.lower()
        new_review = new_review.split()
        ps = PorterStemmer()
        all_stopwords = stopwords.words('english')
        all_stopwords.remove('not')
        new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
        new_review = ' '.join(new_review)
        new_corpus = [new_review]
        new_X_test = cv.transform(new_corpus).toarray()
        new_y_pred = classifier.predict(new_X_test)

        rat=hotel.rating
        if rat == None:
            rat=0
        # print(new_y_pred[0])
        newRat = int(rat)+int(new_y_pred)
        hotel.rating = newRat
        hotel.save()
        try:
            r=Review.objects.create(hotelname=hotel,uname=user,review=rev)
            r.save()
        except:
            messages.info(request, 'some error occured')
        else:
            hotel2=Hotels.objects.get(id=id)
            rat1=hotel2.rating
            total=Review.objects.filter(hotelname=id).count()
            print(total)
            star=float(rat1) / int(total)
            star=round(star,2)
            # star1="{:.2f}".format(star)
            star=star * 5
            hotel2.realrat=round(star,2)
            hotel2.save()
        
    return render(request, "userhotelreview.html",{"data":data})

def review(request):
    rid=request.GET.get("id")
    data=Review.objects.filter(hotelname__id=rid)

    return render(request, "userreview.html",{"data":data})


def userrequest(request):
    uid=request.session["id"]
    user=Registration.objects.get(id=uid)
    if request.POST:
        condn=request.POST["condn"]
        r=Request.objects.create(user=user,request=condn)
        r.save()
    return render(request,"userrequest.html")

def uservrequest(request):
    uid=request.session["id"]
    data=Request.objects.filter(user=uid)
    
    return render(request,"uservrequest.html",{"data":data})

def adminhotelview(request):
    data=Hotels.objects.all()
    return render(request, "adminhotelview.html",{"data":data})

def removehotel(request):
    cid=request.GET.get("id")
    d=Hotels.objects.get(id=cid)
    demail=d.email
    print(demail)
    s=User.objects.get(email=demail).delete()
    ct=Hotels.objects.get(email=demail).delete()
    return redirect("/adminhotelview")


def adminhotelreview(request):
    
    pid=request.GET.get("id")
    
    data=Hotels.objects.filter(id=pid)
    return render(request,"adminhotelreview.html",{"data":data})

def commonhotel(request):
    data=Hotels.objects.all()
    return render(request,"commonhotel.html",{"data":data})

def hotelhome(request):
    return render(request,"hotelhome.html")


def adddish(request):

    rid=request.session["id"]
    if request.POST:
        dname=request.POST["dname"]
        price=request.POST["price"]
        print("hhhhh")
        im=request.FILES["img"]
        
        hotel=Hotels.objects.get(id=rid)
        # r=Dish.objects.create(dname=dname,hotelname=hotel,price=price,image=im)
        # r.save()
        try:
             r=Dish.objects.create(dishname=dname,hotelname=hotel,price=price,image=im)
             r.save()
        except Exception as e:
            messages.info(request, e)
    return render(request,"adddish.html")

def menu(request):
    rrid=0  
    rrid=request.session["id"]
    # rid=request.GET.get("id")
    # hotel=Hotels.objects.get(id=rrid)
    # name=hotel.name
    data=Dish.objects.filter(hotelname=rrid)
    return render(request,"menu.html",{"data":data})

def hotelreviews(request):
    rid=request.session["id"]
    data=Review.objects.filter(hotelname=rid)
    return render(request,"hotelreviews.html",{"data":data})

def usermenu(request):
    return render(request,"usermenu.html")

def adminmenu(request):
    return render(request,"adminmenu.html")

def commonmenu(request):
    return render(request,"commonmenu.html")

def special(request):
    rid=request.GET.get("id")
    data=Dish.objects.filter(hotelname__id=rid)

    return render(request, "usermenu.html",{"data":data})

def adspecial(request):
    rid=request.GET.get("id")
    data=Dish.objects.filter(hotelname__id=rid)

    return render(request, "adminmenu.html",{"data":data})



# def userhotelreview(request):
#     if request.POST:
#         rev=request.POST["review"]
#     return redirect("/userhotel")




