import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from videosurveillance_app.models import *


def login(request):
    return render(request, "loginindex.html")

def logout(request):
    auth.logout(request)
    return render(request, "loginindex.html")

def logincode(request):
    username=request.POST['textfield']
    password = request.POST['textfield2']
    # try:
    if True:
        ob=logintable.objects.get(username=username,password=password)
        if ob.type == 'admin':
            ob1=auth.authenticate(username='admin',password='admin')
            if ob1 is not None:
                auth.login(request,ob1)
            request.session['lid'] = ob.id
            return HttpResponse('''<script> alert("successfully login");window.location="/admin_home"</script>''')
        elif ob.type == 'security':
            ob1 = auth.authenticate(username='admin', password='admin')
            if ob1 is not None:
                auth.login(request, ob1)
            request.session['lid']=ob.id
            return HttpResponse('''<script>alert("successfully login");window.location="/security_home"</script>''')
        else:
            print("hhhhhhhhhhhhhhhhh")
            return HttpResponse('''<script>alert("invalid");window.location="/"</script>''')
    # except Exception as e:
    #     print(e)
    #     print("kkkkkkkkkkkkk")
    #     return HttpResponse('''<script>alert("invalid");window.location="/"</script>''')

def admin_home(request):
    return render(request,"admin1index.html")

@login_required(login_url='/')
def manage_security(request):
    ob=securitytable.objects.all()
    return render(request, "html pg/manag securty nd assgn wrk to scrty 1.html",{'val':ob})


def searchsecurity(request):
    name=request.POST['textfield']
    ob=securitytable.objects.filter(name__istartswith=name)
    return render(request, "html pg/manag securty nd assgn wrk to scrty 1.html",{'val':ob})



def edit_security(request,id):
    request.session['pp']=id
    ob=securitytable.objects.get(id=id)
    return render(request, "html pg/editsecurity.html",{"val":ob})


def editsecurity_code(request):
    try:
        name = request.POST['textfield']
        gender = request.POST['radiobutton']
        idproof = request.FILES['file']
        fs = FileSystemStorage()
        fp = fs.save(idproof.name, idproof)
        phone = request.POST['textfield2']
        email = request.POST['textfield3']

        ob1 = securitytable.objects.get(id=request.session['pp'])

        ob1.name = name
        ob1.gender = gender
        ob1.idproof = fp
        ob1.phone = phone
        ob1.email = email
        ob1.save()
        return HttpResponse('''<script>alert("successfully edited");window.location="/manage_security#about"</script>''')
    except:
        name = request.POST['textfield']
        gender = request.POST['radiobutton']
        phone = request.POST['textfield2']
        email = request.POST['textfield3']

        ob1 = securitytable.objects.get(id=request.session['pp'])

        ob1.name = name
        ob1.gender = gender
        ob1.phone = phone
        ob1.email = email
        ob1.save()
        return HttpResponse('''<script>alert("successfully edited");window.location="/manage_security#about"</script>''')


def delete_security(request,id):
    ob=securitytable.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted");window.location="/manage_security#about"</script>''')



def add_security(request):
    return render(request, "html pg/manag security 2.html")

def addsecuritycode(request):
    name=request.POST['textfield']
    gender=request.POST['radiobutton']
    idproof=request.FILES['file']
    fs=FileSystemStorage()
    fp=fs.save(idproof.name,idproof)
    phone=request.POST['textfield2']
    email=request.POST['textfield3']
    uname=request.POST['textfield4']
    password=request.POST['textfield5']

    ob=logintable()
    ob.username=uname
    ob.password=password
    ob.type='security'
    ob.save()

    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('videosurveillance012@gmail.com', 'pkqo faiz koek axek')
        print("login=======")
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Your password id : " + str(password) +"and Username :"+uname)
    print(msg)
    msg['Subject'] = 'anzen'
    msg['To'] = email
    msg['From'] = 'videosurveillance012@gmail.com'

    print("ok====")

    try:
        gmail.send_message(msg)
    except Exception as e:
        print("rrrrrrr",e)

    ob1=securitytable()
    ob1.LOGIN=ob
    ob1.name=name
    ob1.gender=gender
    ob1.idproof=fp
    ob1.phone=phone
    ob1.email=email
    ob1.save()




    return HttpResponse('''<script>alert("successfully Added");window.location="/manage_security#about"</script>''')


def assign_work1(request,id):
    request.session['pp']=id
    return render(request, "html pg/assign wrk to security 1.html")

def add_assignworkcode(request):
    work = request.POST['textfield2']
    details = request.POST['textfield3']
    date=request.POST['textfield4']

    ob=assignworktable()
    ob.security=securitytable.objects.get(id=request.session['pp'])
    ob.work=work
    ob.status='pending'
    ob.details=details
    ob.date=date
    ob.save()
    return HttpResponse('''<script>alert("successfully Assigned");window.location="/manage_security#about"</script>''')





def assign_work2(request):
    ob = assignworktable.objects.all()
    return render(request, "html pg/assign wrk to secty 2.html",{'val':ob})

def view_report(request):
    ob = reporttable.objects.all()
    return render(request, "html pg/view daily report.html",{'val':ob})

def view_feedback(request):
    ob = feedbacktable.objects.all()
    return render(request, "html pg/view feedback.html",{'val':ob})


def view_complaint(request):
    ob = complainttable.objects.all()
    return render(request, "html pg/view complaint nd reply 1.html",{'val':ob})

def searchcomplaint(request):
    date=request.POST['textfield']
    ob=complainttable.objects.filter(date=date)
    return render(request, "html pg/view complaint nd reply 1.html",{'val':ob})

def send_reply(request,id):
    request.session['rpl']=id
    return render(request, "html pg/send reply 2.html")

def sdrply(request):
    reply=request.POST['textfield']
    ob=complainttable.objects.get(id=request.session['rpl'])
    ob.reply=reply
    ob.date=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("successfully replied");window.location="/view_complaint#about"</script>''')


def add_camera1(request):
    ob = cameratable.objects.all()
    return render(request, "html pg/manage camera 1.html",{'val':ob})

def delete_camera(request,id):
    ob = cameratable.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted");window.location="/add_camera1#about"</script>''')


def add_camera2(request):
    return render(request, "html pg/manage camera 2.html")


def add_cameracode(request):
    cameranumber = request.POST['textfield']
    latitude = request.POST['textfield2']
    longitude = request.POST['textfield3']

    ob=cameratable()
    ob.camera_no=cameranumber
    ob.latitude=latitude
    ob.longitude=longitude
    ob.save()
    return HttpResponse('''<script>alert("successfully Added");window.location="/add_camera1#about"</script>''')


def view_notification(request):
    ob = alerttable.objects.all()
    return render(request, "html pg/view notification.html",{'val':ob})

def security_home(request):
    return render(request, "security1index.html")

def viewassign_work(request):
    ob=assignworktable.objects.filter(security__LOGIN__id=request.session['lid'])
    return render(request, "html pg/view assigned work.html",{'val':ob})


def updatework_status(request,id):
    request.session['nid']=id
    return render(request, "html pg/update work status.html")


def updt(request):
    a=request.POST['textfield']
    ob=assignworktable.objects.get(id= request.session['nid'])
    ob.status=a
    ob.date=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("successfully updated");window.location="/viewassign_work#about"</script>''')



def add_report(request,id):
    request.session['oo']=id
    return render(request, "html pg/add daily report.html")


def add_reportcode(request):
    report = request.POST['textfield']
    description = request.POST['textfield2']

    ob = reporttable()
    ob.assignwork = assignworktable.objects.get(id=request.session['oo'])
    ob.report = report
    ob.date = datetime.today()
    ob.description = description
    ob.save()
    return HttpResponse('''<script>alert("Report Added");window.location="/viewassign_work#about"</script>''')


def send_feedback(request):
    return render(request, "html pg/send feedback.html")

def sdfeedback(request):
    comments=request.POST['textfield']
    ob=feedbacktable()
    ob.security = securitytable.objects.get(LOGIN__id=request.session['lid'])
    ob.comments = comments
    ob.date=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("feedback added");window.location="/security_home"</script>''')



def view_reply(request):
    ob = complainttable.objects.all()
    return render(request, "html pg/view reply.html",{'val':ob})


def searchreply(request):
    date=request.POST['textfield']
    ob=complainttable.objects.filter(date=date)
    return render(request, "html pg/view reply.html",{'val':ob})

def send_complaint(request):
    return render(request, "html pg/send complaint and view reply.html")

def sdcmpt(request):
    complaint=request.POST['textfield']
    ob=complainttable()
    ob.security=securitytable.objects.get(LOGIN__id=request.session['lid'])
    ob.complaint=complaint
    ob.reply="pending"
    ob.date=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("complaint added");window.location="/ #about"</script>''')

def camera_info(request):
    obj = cameratable.objects.all()
    return render(request, "html pg/view camera info.html",{'val':obj})

def insertEmotions(request,emo,camid,img):
    obj = emotiontable()
    obj.emotion=emo
    obj.camera=cameratable.objects.get(id=camid)
    obj.image=img
    obj.date=datetime.today()
    obj.save()
    return HttpResponse('''<script>alert("added");window.location="/view_reply#about"</script>''')


def view_emotion(request):
    obj = emotiontable.objects.filter(emotion="fear")
    return render(request, "html pg/viewemotion.html",{'val':obj})





def view_alert(request):
    ob = alerttable.objects.all()
    return render(request, "html pg/view alert.html",{'val':ob})

