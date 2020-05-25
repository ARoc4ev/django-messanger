from django.shortcuts import HttpResponse
from django.template.context_processors import csrf
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import auth
from .form import RegisterForm
from messenger.models import Team
from account.models import Account

class Login(View):
    def get(self, request):

        if request.user.is_authenticated:
            return redirect('')

        else:
            args = {}
            args.update(csrf(request))

        return render(request, 'login/login.html', args)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        username = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(email=username, password=password)
        if user:
            auth.login(request, user)
            team = user.team_set.all()
            if team[0]:
                return render(request, 'main/main.html', {'name': user.first_name})


            else:
                return render(request, 'login/timchoice.html', {'name': user.first_name})



        else:
            args = {}
            args['login_error'] = 'Пользователь не найден'
            args.update(csrf(request))
            return render(request, 'login/login.html', args)

    def logout(request):
        auth.logout(request)
        return redirect("/login/")


class Register(View):

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        newuser = RegisterForm(request.POST)
        if newuser.is_valid():
            newuser.save()
            newuser = auth.authenticate(username=request.POST.get('email', ''),
                                        password=request.POST.get('password', ''))

            return render(request, "main/main.html")
        else:
            args = {}
            args.update()
            args['error'] = newuser.error_class
            args['form'] = newuser
            args.update(csrf(request))

            return render(request, 'login/login.html', args)


class Register2(View):

    def post(self, request):
        args = {}
        args.update(csrf(request))
        if request.user.is_authenticated:
            return redirect('')

        else:
            try:
                user = Account.objects.get(email=request.POST.get('email'))
                args['erroremail'] = 'Пользователь сданым Emal уже зарегистрирован  '
                return render(request, 'login/login.html', args)
            except Account.DoesNotExist:
                args['email'] = request.POST.get('email')

                if request.POST.get('password'):
                    newuser = RegisterForm(request.POST)
                    if newuser.is_valid():
                        newuser.save()
                        newuser = auth.authenticate(username=request.POST.get('email', ''),
                                                    password=request.POST.get('password', ''))
                        auth.login(request, newuser)

                        return redirect('/')

                    else:
                        args['error'] = newuser.error_class
                        return render(request, "login/register.html", args)
                else:
                    return render(request, 'login/register.html', args)








class Base(View):
    def get(self, request ):
        if request.user.is_authenticated:
            user = Account.objects.get(id=request.user.id)
            try:
                team = user.team_set.all()[0].id
                return redirect('/u/' + str(team ) + '/')
            except IndexError:
                args = {}
                args.update(csrf(request))

                return render(request, 'login/timchoice.html', args)







        else:
            return redirect('/login/')



# Create your views here.
