from django.shortcuts import render,HttpResponse
from django.contrib import auth
import pyrebase,csv,io

config = {
    'apiKey': "AIzaSyB008ySUPzzGzmCUEzVXIQsHIu6C1pXKfg",
    'authDomain': "itravelerlk.firebaseapp.com",
    'databaseURL': "https://itravelerlk.firebaseio.com",
    'projectId': "itravelerlk",
    'storageBucket': "itravelerlk.appspot.com",
    'messagingSenderId': "1078899315418"
  }
firebase = pyrebase.initialize_app(config)

authfb = firebase.auth()
db = firebase.database()

def signIn(request):
    if request.session.is_empty():
        return render(request,'signIn.html')
    else:
        name = db.child('users').child(request.session['uid']).child('name').get().val()
        return render(request,'welcome.html',{'e':name})

def postsign(request):

    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authfb.sign_in_with_email_and_password(email,password)
    except:
        message = "Invalid Credentials"
        return render(request,"signIn.html",{'msg':message})
    session_id = user['localId']
    request.session['uid'] = str(session_id)
    usertype = db.child('users').child(session_id).child('type').get().val()
    name = db.child('users').child(request.session['uid']).child('name').get().val()
    if usertype == 'admin':
        return render(request,'welcome.html',{'e':name})
    return render(request,'signIn.html',{'msg':'You are not an environmentalist please use the mobile app.'})

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')

def signup(request):
    return render(request,'signUp.html')

def postsignup(request):
    
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authfb.create_user_with_email_and_password(email,password)
    except:
        message = 'Unable to create an account please try again later.'
        return render(request,'signUp.html',{'msg':message})
        
    uid = user['localId']
    data = {'name':name,'email':email}

    db.child('users').child(uid).set(data)

    return render(request,'signIn.html')

def downloadcsv(request,city):
    if request.session.is_empty():
        return render(request,'signIn.html',{'msg':'Please sign in First'})
    items =db.child('details').child('humidity').child(city).get()
    response = HttpResponse(content_type = 'text/csv')
    response['Content-Disposition'] = 'attachment; filename="tesla_stocks.csv"'
    writer = csv.writer(response,delimiter=',')
    writer.writerow(['key','values'])
    for item in items.each():
        writer.writerow([item.key(),item.val()])

    return response

def upload(request):
    if request.session.is_empty():
        return render(request,'signIn.html',{'msg':'Please sign in First'})
    template = 'upload.html'

    prompt = {
        'order':'order is order'
    }
    if request.method == "GET":
        return render(request,template,prompt)
    csv_file = request.FILES['file']
    if not csv_file.name.endswith('.csv'):
        return render(request,template,{'e':'this is not a csv file'})
    data_set = csv_file.read().decode('UTF-8')
    io_string = io.StringIO(data_set)
    next(io_string)
    data = {}
    i = 0
    for col in csv.reader(io_string,delimiter=','):
        data.update({i:float(col[4])})
        i+=1
    db.child('details').child('humidity').child('colombo').set(data)
    return render(request,'upload.html',{'d':'done'})

def humidity(request):
    if request.session.is_empty():
        return render(request,'signIn.html',{'msg':'Please sign in First'})
    cities =  db.child('details').child('humidity').get()
    name = db.child('users').child(request.session['uid']).child('name').get().val()
    town = []
    for city in cities.each():
        town.append(city.key())
    return render(request,'humidity.html',{'cities':town,'name':name})

def home(request):
    if request.session.is_empty():
        return render(request,'signIn.html',{'msg':'Please sign in First'})
    name = db.child('users').child(request.session['uid']).child('name').get().val()
    return render(request,'welcome.html',{'e':name})


def pollution(request):
    if request.session.is_empty():
        return render(request,'signIn.html',{'msg':'Please sign in First'})
    return render(request,'total-pollution.html')