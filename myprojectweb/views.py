
from django.shortcuts import render
from django.contrib import messages
from myapp.models import Post,Category
from django.contrib.auth.models  import  User
from django.contrib.auth  import  authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt 
#create a login page
def home(request):
    logout(request)
    
    return render(request,"index.html" )
@csrf_exempt   
def login_page(request):
    

    if request.method == "POST":
        
        username=request.POST["username"]
        pass1=request.POST["password"]
        user =authenticate(username=username, password=pass1)
        
        
        
        if user is not None:
            login(request,user)
            
            posts = Post.objects.all()
            cats = Category.objects.all() 

            data = {
                'posts': posts,
                'cats': cats
            }
            
            return render(request, 'blogging.html', data)
    
        else: 
            messages.info(request," incorrect id and password")
            
            return render(request,"index.html" )

    else:
        messages.info(request," not matching")
        return render(request,"signup.html" )
def post(request, url):
    post = Post.objects.get(url=url)
    

    
    return render(request, 'posts.html', {'post': post, })

#create signup page
def signup(request):
    return render(request,"signup.html")

def saveform(request):
    if request.method=="POST":
        first_name=request.POST["first_name"]
        last_name=request.POST["last_name"]
        username=request.POST["username"]
        email=request.POST["email"]
        pass1=request.POST["pass"]
        pass2=request.POST["pass2"]
        gender=request.POST["gender"]
        if pass1 ==pass2:
            
            if User.objects.filter(username=username).exists():
                print("user allreday refister")
                messages.info(request,"username allready taken try another username")
                return render(request,"signup.html")
            elif User.objects.filter(email=email).exists():
                messages.info(request," Email allready taken try another username")
                
                return render(request,"signup.html")
                    
                
            else:


                d=User.objects.create_user(username=username,email=email,password=pass1,first_name= first_name,last_name=last_name)
                d.save()
              
                return render(request,"index.html")
        else:
            
            messages.info(request," password not matching")
            return render(request,"signup.html")


        
    return render(request,"signup.html")

def category(request, url):
    cat = Category.objects.get(url=url)
    posts = Post.objects.filter(cat=cat)
    return render(request, "category.html", {'cat': cat, 'posts': posts})
