# myapp/views.py
import pickle
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from .models import Product


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
        #FLAW 2 injection
        #please note this flaw is already fixed, due to the function here is connected with other parts.
        #To ensure the web application and other flaws can be demostrated clearly, I fixed flaw here.
        #The flaw code before fixing should be the code directly put user input into query.

        #FLAW2 original CODE:
            # user = User.objects.raw("SELECT * FROM auth_user WHERE username = '{}'".format(username))[0]
        
        # Here, user input is directly placed into the SQL query, which opens up the possibility of SQL injection.

            
        #FLAW2: FIXED CODE:
            #This flaw is fixed by using Django ORM, which prevents SQL injection.
            user = User.objects.get(username=username)  #Django ORM prevents SQL injection
            if check_password(password, user.password): 
                django_login(request, user)
                return redirect('dashboard')
            
            else:
              
        #Flaw 1 Sensitive Data Exposure
            # https://docs.djangoproject.com/en/5.1/topics/auth/default/#using-the-views
            # Returning specific error messages like "Incorrect password"
                error_message = 'Incorrect password'
        except User.DoesNotExist:
            error_message = 'User not found'
        return render(request, 'login.html', {'error_message': error_message})
    
        #Fix 1 solution: returning generic error messages to avoid exposure
        # (also using authenticate in Django this time)

        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #   login(request, user)
        #   return redirect('dashboard')
        # else:
        #   return render(request, 'login.html', {'error_message': 'User or password incorrect'})
    return render(request, 'login.html')



@login_required
def dashboard(request):
    search_term = request.GET.get('search', '')
    products = Product.objects.filter(name__icontains=search_term)
    return render(request, 'dashboard.html', {'products': products})





def load_data(request):
    # Flaw 6: Insecure Deserialization
    data = request.POST.get('data') 
    try:
        loaded_data = pickle.loads(data)
    except Exception as e:
        return HttpResponse(f"Error loading data: {str(e)}")
    
    return render(request, 'dashboard.html', {'data': loaded_data})

# Fix 6: Avoiding insecure deserialization by using json
# def load_data(request):
#     data = request.POST.get('data') 
#     try:
#         loaded_data = json.loads(data) 
#     except json.JSONDecodeError as e:
#         return HttpResponse(f"Error loading data: {str(e)}")
    
#     return render(request, 'dashboard.html', {'data': loaded_data})
