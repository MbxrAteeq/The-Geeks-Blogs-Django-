from django.shortcuts import render, HttpResponse
#from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib import messages
from blog.models import Blog, Contact
import math
# Create your views here.
def home(request):
    return render(request, 'index.html')


def blog(request):
    no_of_posts = 5
    page = (request.GET.get('page'))
    if page is None:
        page=1
    else:
        page = int(page)
    blogs = Blog.objects.all()
    length = len(blogs)
    blogs = blogs[(page-1)*no_of_posts: page*no_of_posts]
    if page>1:
        prev = page-1
    else:
        prev = None
    if page<math.ceil(length/no_of_posts):
        nxt = page + 1
    else:
        nxt = None
    context = {'blogs': blogs, 'prev' : prev, 'nxt' : nxt}
#    return HttpResponse("This is blog")
    return render(request, 'bloghome.html', context)

def blogpost(request, slug):
    blog = Blog.objects.filter(slug=slug).first
    context = {'blog': blog}
    return render(request, 'blogpost.html', context)
#    return HttpResponse(f"you are viewing {slug }")


def contact(request):
    if request.method=='POST':
        name= request.POST['name']
        email= request.POST['email']
        phone= request.POST['phone']
        desc= request.POST['desc']
        ins = Contact(name=name, email=email, phone=phone, desc=desc)
        ins.save()
        print('Data has been written in the database')
#    return HttpResponse("This is contact")
    return render(request, 'contact.html')

def search(request):
    query = request.GET["query"]
    if len(query)>80:
        allPosts=[]
    else:
        allPoststitle = Blog.objects.filter(title__icontains=query)
        allPostscontent = Blog.objects.filter(content__icontains=query)
        allPosts = allPoststitle.union(allPostscontent)
        context = {'allPosts': allPosts, 'query': query}
        return render(request, 'search.html', context)


def handleSignup(request):
    if request.method == 'POST':
       username = request.POST['username']
       fname = request.POST['fname']
       lname = request.POST['lname']
       email = request.POST['email']
       pass1 = request.POST['pass1']
       pass2 = request.POST['pass2']

       #check for errors

       #

       #create the user
       myuser = User.objects.create_user(username, email, pass1)
       myuser.first_name = fname
       myuser.last_name = lname
       myuser.save()
       messages.success(request, "Your Account has created successfully")

    else:
        return HttpResponse('404 - Not Allowed')