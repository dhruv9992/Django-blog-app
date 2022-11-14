from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from . models import Blog
from . forms import Edit_Blog


# Create your views here.
def index(request):
    blog = Blog.objects.all()
    
    for blogs in blog:
          print('inside.fuction',blogs.title, blogs.dsc)
    return render(request, 'home.html',{'blogs': blog})
    # return HttpResponse('this is page ')

def user_register(request):
    if request.method=='POST':
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2') 
        if pass1!=pass2:
             messages.warning(request,'password does not match')
             return redirect('register') 
        elif User.objects.filter(username=uname).exists():
           messages.warning(request,'username already taken')
           return redirect('register') 
        elif User.objects.filter(email=email).exists():
            messages.warning(request,'email already taken')
            return redirect('register') 
        else:
                   user = User.objects.create_user(first_name=fname,last_name=lname,username=uname,email=email,password=pass1)
                   user.save()
                   messages.success(request,'User has been registered succssfully')
                   return redirect('login')
    return render(request, ('register.html'))
    # return HttpResponse('this register page')

def user_login(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:   
            login(request, user)
            return redirect('/')
        else:
                messages.warning(request,'Invalid creadentials ')
                return redirect('login')    
    return render(request, ('login.html'))
    # return HttpResponse('this login page')
    
def user_logout(request):
    logout(request)
    return redirect('/')

def post_blog(request):
    if request.method=="POST":
       title = request.POST.get('title')
       desc = request.POST.get('Description')
       blog = Blog(title=title, dsc=desc, user_id=request.user)
       blog.save()
       messages.success(request, 'post has been submitted successfully')
       return redirect('post_blog')
    return render(request, 'blog_post.html')

def blog_detail(request,id):
    blog = Blog.objects.get(id=id)
    context = {'blog' :blog}
    return render(request, 'blog_detail.html',context)


def delete(request,id):
    blog = Blog.objects.get(id=id)
    blog.delete()
    messages.success(request, 'Post has been deleted')
    return redirect('/')

def edit(request,id):
    blog = Blog.objects.get(id=id)
    editblog = Edit_Blog(instance=blog)
    if request.method=='POST':
        form = Edit_Blog(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            messages.success(request, 'POST has been updated')
            return redirect('/')
        
    return render(request, 'edit_blog.html',{'edit_blog':editblog})

  

