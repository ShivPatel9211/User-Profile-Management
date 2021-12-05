from django.shortcuts import render,redirect
from pyrebase import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Create your views here.
firebaseConfig = {
  "databaseURL": "https://profilemanager-d6377-default-rtdb.firebaseio.com",
  "apiKey": "AIzaSyBtpVRpuoFZwD-fb-GWXuT5v7nmInpJHDA",
  "authDomain": "profilemanager-d6377.firebaseapp.com",
  "projectId": "profilemanager-d6377",
  "storageBucket": "profilemanager-d6377.appspot.com",
  "messagingSenderId": "330925109644",
  "appId": "1:330925109644:web:f4991d92c5cefe89b5a6a9",
  "measurementId": "G-3Q799XMZZY"
}
# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()
# database=firebase.database()
cred = credentials.Certificate(r"E:\Python Project\User Profile Management\UserManagement\ProfileManager\security.json")
firebase_admin.initialize_app(cred)
db= firestore.client()
def index(request):
  if request.method=="POST":
    email=request.POST.get("email")
    password=request.POST.get("password")
    try:
      user= authe.sign_in_with_email_and_password(email, password)
      userid=user['localId']
      error = 'no'
      return redirect(f'/home/{userid}')
    except Exception as x:
      error ='yes'
      message="Invalid email or password,Please try again"
      context = {
        'error': error,
        'message': message,
      }
      return render(request,'index.html',context)
  return render(request, 'index.html')


def register(request):
  if request.method=="POST":
    email=request.POST.get("email")
    password=request.POST.get("password")
    try:
      if len(password)<6:
        error="yes"
        message="Password cannot be less then 6 characters"

        context = {
          'error': error,
          'message': message,
        }
        return render(request, 'register.html', context)
      elif email=="":
        error = "yes"
        message = "Email cannot be bank"

        context = {
          'error': error,
          'message': message,
        }
        return render(request, 'register.html', context)
      else:
        user=authe.create_user_with_email_and_password(email, password)
        userid=user['localId']
        db.collection('user').document(userid).set({
          'email':email,
          'picurl':'https://www.kindpng.com/picc/m/21-214439_free-high-quality-person-icon-default-profile-picture.png'
        })
      return redirect(f'/home/{userid}')
    except Exception as e:
      error='yes'
      message = "Something went wrong plz try again,or email already exists"
      context = {
        'error': error,
        'message':message,
      }
      return render(request,'register.html',context)
  return render(request,'register.html')
def home(request,userid):
  if request.method =="POST":
    name=request.POST['name']
    address = request.POST['address']
    DOB = request.POST['DOB']
    picurl = request.POST['url']
    if picurl == "":
      profilepic=db.collection('user').document(userid).get()
      pic =profilepic.to_dict()
      profilepic=pic['picurl']
    else:
      profilepic=picurl
    data={
      'name':name,
      'address':address,
      'DOB':DOB,
      'picurl':profilepic
    }
    db.collection('user').document(userid).update(data)
  userDetail=db.collection('user').document(userid).get()
  context=userDetail.to_dict()
  return render(request, 'home.html',context)



# retrive data
# result = db.collection('user').where('email','==','admin@admin.com').get()
# for i in result:
#   print(i.to_dict())
def resetPassword(request):
    return render(request, "resetPassword.html")


def postReset(request):
  email = request.POST.get('email')
  try:
    authe.send_password_reset_email(email)
    error = 'no'
  except:
    error = 'yes'
  context = {
    "error": error
  }
  return render(request, "resetPassword.html",context)

def logout(request):
  try:
    del request.session['uid']
  except:
    pass
  return render(request, "index.html")