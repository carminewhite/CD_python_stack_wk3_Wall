from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages

def index(request):
    if request.session._session:
        # for key, value in request.session.items():
        #     print('{} => {}'.format(key, value))
        context = {
            "f_name" : request.session['first_name'],
            "l_name" : request.session['last_name'],
            "email" : request.session['email'],
        }
    else:
        context = {}

    return render(request, "index.html", context)



def process_registration(request):
    errors = User.objects.reg_validator (request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        request.session['first_name'] = request.POST['fname']
        request.session['last_name'] = request.POST['lname']
        request.session['email'] = request.POST['email']
        return redirect ('/')

    else:
        User.objects.create(first_name = request.POST['fname'], last_name = request.POST['lname'], email = request.POST['email'], password = request.POST['password'])
        messages.success(request, "Successfully registered")
        request.session['first_name'] = request.POST['fname']

        return redirect("/reg_success")

def reg_success(request):
        context = {
            "user" : request.session['first_name']
        }
        return render(request, "success.html", context)

def process_login(request):
    errors = User.objects.login_validator (request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        request.session['login_email'] = request.POST['login_email']
        return redirect('/')
    else:
        request.session['login_email'] = request.POST['login_email']
        print(request.session['login_email'])
        return redirect('/log_success')


def log_success(request):
    if 'login_email' in request.session:
        my_user = User.objects.get(email = request.session['login_email'])
        my_user_id = my_user.id
        # print(my_user_id)
        request.session['user_id'] = my_user_id
        request.session['first_name'] = my_user.first_name
        return redirect("/wall")
    else:
        return redirect("/")

def destroy_session(request):
    request.session['first_name'] = ""
    request.session['last_name'] = ""
    request.session['email'] = ""
    request.session['login_email'] = ""
    request.session['user_id'] = ""
    return redirect('/')



##################  BEGIN WALL APP ROUTING ###################

def wall(request):
    context = {
        "all_messages" : Message.objects.all().order_by("-created_at"),
        "all_comments" : Comment.objects.all().order_by("-created_at"),
        "user_id" : request.session['user_id'],
        "f_name" : request.session['first_name']
    }
    print("First name: ", request.session['first_name'])
    return render(request, "wall.html", context)

def process_message(request):
    print(request.POST['post_message'])
    
    new_message = Message.objects.create(message_text = request.POST['post_message'], user = User.objects.get(id= request.session['user_id']))
    print(new_message)
    return redirect('/wall')

def process_comment(request):

    c = Comment.objects.create(comment_text = request.POST['post_comment'], user = User.objects.get(id= request.session['user_id']), message = Message.objects.get(id = request.POST['message_id']))
    return redirect('/wall')

def delete_comment(request):
    c = Comment.objects.get(id = request.POST['comment_id'])
    c.delete()
    return redirect('/wall')