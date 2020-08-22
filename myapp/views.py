from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import send_mail
from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from datetime import datetime

from .forms import InterestForm, OrderForm, RegisterForm, FeedbackForm
from .models import Topic, Course, Student, Order


# Create your views here.
def index(request):
    # We are passing two extra context variables : topic_list and course_list
    top_list = Topic.objects.all().order_by('id')[:10]
    course_list = Course.objects.all().order_by('-price')[:5]
    if request.session.has_key('last_login'):
        lastLog = (request.session.get('last_login'))
    else:
        lastLog = "Your last login was more than an hour ago!"
    return render(request, 'myapp/index.html', {'top_list': top_list,'course_list' : course_list})


def about(request):
    # We are not passing any extra context variables because we are not using any variable inside html
    visitCount = request.COOKIES.get('about_visits')
    if visitCount == None:
        visitCount = 0
    else:
        visitCount = int(visitCount) + 1
    response = render(request, 'myapp/about.html', {'visitCount': visitCount})
    response.set_cookie(key="about_visits", value=visitCount, expires= 60 * 5)
    return response

def detail(request, top_no):
    # We are passing one extra context variables : topic
    topic = get_object_or_404(Topic, pk=top_no)
    courses = topic.courses.all()
    return render(request, 'myapp/detail.html', {'topic': topic})

def courses(request):
    courlist = Course.objects.all().order_by('id')
    return render(request, 'myapp/courses.html', {'course_list': courlist})


def place_order(request):
    msg = ''
    courlist = Course.objects.all()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            ordervalid = False
            order.save()
            form.save_m2m()
            for course in order.courses.all():
                if order.levels <= course.stages:
                    ordervalid = True
                else:
                    ordervalid = False
                    break
            if ordervalid:
                for course in order.courses.all():
                    if course.price > 150:
                        course.price = course.discount()
                        course.save()
                msg = 'Your course has been ordered successfully.'
            else:
                order.delete()
                msg = 'You exceeded the number of levels for this course.'
            return render(request, 'myapp/order_response.html', {'msg': msg})
    else:
        form = OrderForm()
        return render(request, 'myapp/placeorder.html', {'form': form, 'msg': msg,
                                                         'courlist': courlist})

def coursedetail(request, cour_id):
    course = get_object_or_404(Course, pk=cour_id)
    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            if form['interested'].value() == '1':
                print(course.interested)
                course.interested = course.interested + 1
                course.save()
            return redirect('myapp:index')
    elif request.method == 'GET':
        form = InterestForm()
        return render(request, 'myapp/coursedetail.html', {'form': form, 'course': course})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username + "  "+password)
        user = authenticate(username=username, password=password)
        if user:
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            else:
                response = HttpResponse("Please enable cookies and try again.")
            if user.is_active:
                login(request, user)
                response =  HttpResponseRedirect(reverse('myapp:myaccount'))
                date_time = str(datetime.now())
                request.session['last_login'] = date_time
                # This is commented to remove session cookie
                # and also we need to add (SESSION_EXPIRE_AT_BROWSER_CLOSE = True) into sesssion.py when browser is closed
                # request.session.set_expiry(60*60)
            else:
                response = HttpResponse('Your account is disabled.')
        else:
            response =  HttpResponse('Invalid login details.')
    else:
        response = render(request, 'myapp/login.html')
    response.delete_cookie(key='home')
    request.session.set_test_cookie()
    return response


@login_required
def user_logout(request):
    # logout(request)
    request.session.flush()
    return HttpResponseRedirect(reverse(('myapp:index')))


def myaccount(request):
    userid= request.user.id
    if userid != None:
        student = Student.objects.get(pk=userid)
        orders = Order.objects.filter(Student=student)
        topics = Topic.objects.filter(student=student)
        return render(request, 'myapp/myaccount.html', {'student': student, 'orders': orders, 'topics': topics})
    else:
        return HttpResponseRedirect(reverse('myapp:login'))


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            student = form.save()
            student.set_password(student.password)
            student.save()
            return render(request, 'myapp/register.html', {'form': RegisterForm(), 'msg': 'Registration Successful'})
        else:
            return render(request, 'myapp/register.html', {'form': RegisterForm(), 'msg': 'Error in registration'})
    else:
        form = RegisterForm()
        return render(request, 'myapp/register.html', {'form': form, 'msg': ''})

def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = Student.objects.filter(email=email)
            if user.exists():
                user = user.get(email = email)
                subject = "Password Reset Requested"
                user_email = user.email
                message = "Please use 123456@12 as your password"
                try:
                    user.set_password('123456@12')
                    user.save()
                    send_mail(subject, message, '', [user_email], fail_silently=False)
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return render(request, 'myapp/forgot_password.html', {'form': PasswordResetForm(), 'msg': 'Forgot passwprd email sent'})
            else:
                return render(request, 'myapp/forgot_password.html', {'form': PasswordResetForm(), 'msg': 'No records found for this email'})
    else:
        form = PasswordResetForm()
        return render(request, 'myapp/forgot_password.html', {'form': form})


@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            userid = request.user.id
            feedback.student = Student.objects.get(pk=userid)
            feedback.save()
        return render(request, 'myapp/feedback.html', {'form': FeedbackForm(), 'msg': 'Thanks for your valuable feedback'})
    else:
        form = FeedbackForm()
        return render(request, 'myapp/feedback.html', {'form': form})