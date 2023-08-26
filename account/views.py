from django.shortcuts import render, redirect
from .forms import CreateUserForm
from django.contrib import messages
from Crypto.PublicKey import RSA
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def register_page(request):
    if request.user.is_authenticated:
        return redirect('cert_app:home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                obj = form.save(commit=False)
                if obj.is_teacher == True:
                    keyPair = RSA.generate(bits=1024)
                    obj.e_key = hex(keyPair.e)
                    obj.d_key = hex(keyPair.d)
                    obj.n_key = hex(keyPair.n)
                    obj.save()
                obj.save()               
                user = form.cleaned_data.get('user_name')
                messages.success(request, 'Account was created for ' + user)
                return redirect('account_app:login')
        context = {'form':form}
    return render(request, 'account/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            user_name = request.POST.get('user_name')
            password =request.POST.get('password')

            user = authenticate(request, user_name=user_name, password=password)

            if user is not None:
                login(request, user)
                return redirect('cert_app:home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'account/login.html', context)

def logout_(request):
    logout(request)
    return redirect('account_app:login')