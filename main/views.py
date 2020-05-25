from django.template.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from messenger.models import Team, Channel, Thread, ThreadIm, MessageIm, Message, Invitation
from account.models import Account
from django.http import JsonResponse
from messenger.serializers import AccountTeam
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
import json


class TeamList(generics.ListAPIView):
    serializer_class = AccountTeam
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        username = self.request.user.id
        User = Account.objects.get(id=username)
        team = User.team_set.all()
        return team[0].participants


class CreateTeam(View):
    def post(self, request):
        if request.user.is_authenticated:
            team = Team()
            team.name = request.POST.get('name')
            team.save()
            team.participants.add(request.user.id)
            team.save()
            channel = Channel()
            channel.name = 'Основной'
            channel.save()
            channel.team.add(team)
            channel.save()
            return redirect('/')
        else:
            return redirect('login')


class TeamR(View):

    def get(self, request):
        args = {}
        args.update(csrf(request))
        user = Account.objects.get(id=request.user.id)
        team = user.team_set.all()[0]
        args['team_name'] = team.name
        team_p = team.participants.all()
        args['len_team'] = len(team_p)
        args['participants'] = team_p
        args['name'] = user.last_name
        args['team_id'] = team.id
        for i in team_p:
            i.name = i.fio

        return render(request, 'main/team.html', args)


class Main(View):

    def get(self, request, **data):
        if request.user.is_authenticated:

            team = get_object(Team, data['id_team'])
            user = get_object(Account, request.user.id)

            if team.participants.filter(pk=user.pk).exists():
                channel = Channel.objects.filter(team=team)
                args = {}

                if 'id_channel' in data:
                    id_channel = data["id_channel"]
                else:
                    id_channel = channel[0].id
                channels = channel.get(id=id_channel)
                threads = Thread.objects.filter(channel=channels)
                for thread in threads:  # треды
                    sms = thread.message_set.filter(datetime=thread.last_message)[0]
                    thread.text = sms.text
                    thread.id_channel = channels.id
                    thread.partner = sms.sender.fio()
                args['team_id'] = team.id
                args['channel_id'] = id_channel
                args['traid'] = threads
                args['name_channel'] = channels.name
                args['channel'] = channel
                args['name'] = user.last_name
                args['user_id'] = user.id

                if 'id_traid' in data:  # собщния в чате
                    threa = threads.get(id=data['id_traid'])
                    sms = threa.message_set.all()
                    args['name_traid'] = threa.name
                    for smss in sms:
                        smss.name = smss.sender.fio()
                        smss.id_thread = smss.thread.id

                    args['sms'] = sms
                    args['thread_id'] = threa.id

                    return render(request, 'main/chat.html', args)

                return render(request, 'main/main.html', args)

        else:

            return redirect('/login/')


def get_object(model, pk):
    try:
        rr = model.objects.get(id=pk)
        return rr
    except ObjectDoesNotExist:
        raise False


class Im(View):  # личные сообщения
    def get(self, request, **data):
        if request.user.is_authenticated:
            user = Account.objects.get(id=request.user.id)
            threads = ThreadIm.objects.filter(participants=request.user.id)
            team = user.team_set.all()[0]
            args = {}

            args['team_id'] = team.id

            args.update(csrf(request))

            for thread in threads:
                try:
                    sms = thread.messageim_set.filter(datetime=thread.last_message)[0]
                    thread.text = sms.text
                    thread.partner = thread.participants.exclude(email=user)[0].fio()

                except:
                    thread.text = 'Начните беседу..'
                    thread.partner = thread.participants.exclude(email=user)[0].fio()
                thread.name = thread.participants.exclude(email=user)[0].fio()

            args["traid"] = threads
            args['name'] = user.last_name
            if 'id_traid' in data:
                team = user.team_set.all()[0]
                args['team_id'] = team.id
                threa = threads.get(id=data['id_traid'])
                args['thread_id'] = threa.id
                sms = threa.messageim_set.all()
                args['name_traid'] = threa.participants.exclude(email=user)[0].fio()
                for smss in sms:
                    smss.name = smss.sender.fio()
                    smss.id_thread = smss.thread.id

                args['sms'] = sms
                return render(request, 'main/chat2.html', args)

        return render(request, 'main/im.html', args)


class Ims(View):
    def post(self, request):  # создание нового чата
        if request.user.is_authenticated:

            data = json.loads(request.POST.get('sendData'))
            list = []
            list.append(request.user.id)
            for i in data:
                if int(i['value']) != int(request.user.id):
                    list.append(i['value'])

            if len(list) == 2:
                set = ThreadIm.objects.filter(participants=list[0], vid='LS')
                set = set.filter(participants=list[1])
                if len(set) == 0:
                    threadim = ThreadIm()
                    threadim.save()
                    threadim.participants.add(list[0])
                    threadim.participants.add(list[1])
                    threadim.save()
                    test = {}
                    test['id_threadim'] = threadim.id

                    return JsonResponse(test, status=200)



                else:
                    test = {}
                    test['id_threadim'] = set[0].id

                    return JsonResponse(test, status=200)

            elif len(list) > 2:  # групповой чат  сообщения
                threadim = ThreadIm()
                threadim.vid = 'GR'
                threadim.save()
                for i in list:
                    threadim.participants.add(i)
                threadim.save()
                test = {}
                test['id_threadim'] = threadim.id

                return JsonResponse(test, status=200)




        return HttpResponse('Error', status=200)



class ChannelNew(View):
    def post(self, request):
        if request.user.is_authenticated:
            user = get_object(Account, request.user.id)
            team = user.team_set.all()
            channel = Channel()
            channel.name = request.POST.get('text', '')
            channel.save()
            channel.team.add(team[0].id)
            channel.save()
            afres = {}
            afres['id'] = channel.id
            afres['name'] = channel.name

            return JsonResponse(afres)


class ThreadNew(View):

    def post(self, request):
        if request.user.is_authenticated:
            user = get_object(Account, request.user.id)
            team = user.team_set.all()
            channel = Channel.objects.get(id=request.POST.get('channel_id', ''))
            thread = Thread()
            thread.name = request.POST.get('name', '')
            thread.save()
            thread.channel.add(channel)
            thread.save()

            message = Message()
            message.sender = user
            message.thread = thread
            message.text = request.POST.get('text', '')
            message.save()

            afres = {}
            afres['tread_id'] = thread.id
            afres['tread_name'] = thread.name
            afres['channel_id'] = channel.id
            afres['partner'] = message.sender.fio()
            afres['text'] = message.text

            return JsonResponse(afres)

    pass


class Invitations(View):  # запрос на добавления участника

    def post(self, request):
        if request.user.is_authenticated:
            user = get_object(Account, request.user.id)
            team = user.team_set.get()
            inv = Invitation()
            inv.email = request.POST.get('email')
            inv.save()
            team.invitation.add(inv)
            return JsonResponse({"result": "Участник добавлен"}, status=200)
        else:
            return False


class Inteam(View):  ##запрос для присоединения к команде
    def post(self, request):
        if request.user.is_authenticated:
            user = Account.objects.get(id=request.user.id)
            id = request.POST.get('id')
            team = get_object(Team, id)
            if team:
                inv = team.invitation.filter(email=user.email)
                if inv:
                    team.participants.add(user)
                    team.save()
                    return JsonResponse({"ok": "1"}, status=200)
                else:
                    return JsonResponse({"result": "Вход не разрешон"}, status=200)

            else:
                return JsonResponse({"result": "Команда не найденна"}, status=200)


        else:
            return redirect('/')

# Create your views here.
