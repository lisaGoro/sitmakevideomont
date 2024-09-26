import datetime
import random

import django.contrib.auth
import pytz
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from datetime import *
from pathlib import Path
import os
from shutil import copy2
from django.core.cache import cache

import settings
from testapp1.models import *


def getProfile(user):
    return Profile.objects.filter(user=user)[0]


def getGroup(user):
    return getProfile(user).group.groupname


def getSkills(user):
    if len(Skills.objects.filter(user=user)) > 0:
        return Skills.objects.filter(user=user)[0]
    else:
        return None


def getTgCode(user):
    if len(Telegram_Code.objects.filter(user=getProfile(user))) > 0:
        return Telegram_Code.objects.filter(user=getProfile(user))[0]
    else:
        new_tg_code = Telegram_Code(user=getProfile(user))
        new_tg_code.save()
        getTgCode(user)


def index_page(request):
    return render(request, 'index.html', {'username': request.user.username})


@csrf_exempt
def check_login(request):
    if is_ajax(request):
        allusernames = User.objects.all()
        for i in allusernames:
            if i.username == request.POST.get("login"):
                return JsonResponse({'text': "IsLogin"})
            return JsonResponse({'text': 'IsNotLogin'})


def reg_page(request):
    return render(request, 'reg.html')


# def newreg(request):
#     if request.method == 'POST':
#         print("\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
#         print("                         New register user!                            ")
#         print("name: " + request.POST.__getitem__("name"))
#         print("email: " + request.POST.__getitem__("email"))
#         print("password: " + request.POST.__getitem__("password"))
#         print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n")
#
#         user = User.objects.create_user(request.POST.__getitem__("name"), request.POST.__getitem__("email"), request.POST.__getitem__("password"))
#         user.save()
#         return render(request, 'regcomplete.html')

def auth_page(request):
    return render(request, 'auth.html')


# def login_page(request):
#     if request.method == 'POST':
#         user = authenticate(username=request.POST.__getitem__("NameOrEmail"), password=request.POST.__getitem__("password"))
#         if user is not None:
#             login(request, user)
#             print("\n=============Success Authentication!!!=========")
#             print("Username (or email): " + request.user.get_username())
#             print("Group:" + getProfile(request.user).group)
#             print("===============================================\n")
#
#
#     return render(request, 'loginFailed.html')

def logout_page(request):
    print("\n===============Success Logout!!!===============")
    print("Username (or email): " + request.user.get_username())
    logout(request)
    print("To: " + str(request.user))
    print("===============================================\n")

    return HttpResponseRedirect("/index/")


def profile_page(request):
    if getGroup(request.user) != "Client" and getGroup(request.user) != "Admin":
        return HttpResponseRedirect('/worker')
    Prof = Profile.objects.filter(user=request.user)[0]
    firstname = Prof.first_name
    secondname = Prof.second_name
    email = Prof.email
    telegram_id = Prof.telegram_id
    date_reg = request.user.date_joined.strftime("%d.%m.%Y")

    ordersSent = Order.objects.filter(creator=request.user) & Order.objects.filter(status="sent")
    ordersSentArr = []
    for i in ordersSent:
        ordersSentArr.append([i.name, i.id])
    print(ordersSentArr)
    ordersInWork = Order.objects.filter(creator=request.user) & Order.objects.filter(status="inwork")
    ordersInWorkArr = []
    for i in ordersInWork:
        ordersInWorkArr.append([i.name, i.id])
    ordersComplete = Order.objects.filter(creator=request.user) & Order.objects.filter(status="complete")
    ordersCompleteArr = []
    for i in ordersComplete:
        ordersCompleteArr.append([i.name, i.id])
    ordersCanceled = Order.objects.filter(creator=request.user) & Order.objects.filter(status="canceled")
    ordersCanceledArr = []
    for i in ordersCanceled:
        ordersCanceledArr.append([i.name, i.id])
    countallorders = len(ordersCanceledArr)+len(ordersCompleteArr)+len(ordersInWorkArr)+len(ordersSentArr)
    return render(request, 'profile.html', {'username': request.user.get_username(), 'firstname': firstname,
                                            'secondname': secondname, 'email': email, 'telegram': telegram_id,
                                            'datereg': date_reg, 'orderssent': ordersSentArr,
                                            'ordersinwork': ordersInWorkArr, 'orderscomplete': ordersCompleteArr,
                                            'orderscanceled': ordersCanceledArr, 'countallorders': countallorders})


def is_ajax(requset):
    return requset.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@csrf_exempt
def messanger_page(request):
    if is_ajax(request) and request.method == 'POST':
        print(request.POST)
        if request.POST.get('text').find("WAIT_NEW_MESSAGES#") > -1:
            last_id = request.POST.get('text').split("WAIT_NEW_MESSAGES#")[1]
            tz = pytz.timezone("Etc/GMT-4")

            try:
                last_id = int(last_id)

                messages_to_send_text = []
                messages_to_send_date = []
                all_messages_for_refresh = (
                        (Message.objects.filter(author=request.user.get_username()) & Message.objects.filter(
                            address=request.POST.get('address'))) |
                        (Message.objects.filter(author=request.POST.get('address')) & Message.objects.filter(
                            address=request.user.get_username())))
                for i in all_messages_for_refresh:

                    if i.id > last_id:
                        messages_to_send_text.append(i.text)
                        messages_to_send_date.append(tz.normalize(i.date.astimezone(tz)).strftime("%H:%M"))
                        last_id = i.id
                return JsonResponse({'text': messages_to_send_text, 'time': messages_to_send_date,
                                     'last_id': str(last_id)})
            except:
                pass
        else:
            new_message = Message(text=request.POST['text'], author=request.user.get_username(),
                                  address=request.POST.get('address'))
            new_message.save()
            return JsonResponse({'text': request.POST.get('text'), 'time': datetime.now().strftime("%H:%M"),
                                 'last_id': str(new_message.id)})

    if request.method == 'GET':
        if request.GET.get('user') == None:
            return HttpResponseRedirect('/userlist/')
        all_messages = ((Message.objects.filter(author=request.user.get_username()) & Message.objects.filter(
            address=request.GET.get('user'))) |
                        (Message.objects.filter(author=request.GET.get('user')) & Message.objects.filter(
                            address=request.user.get_username())))
        text_and_time = []
        tz = pytz.timezone("Etc/GMT-4")
        last_id = 0

        for i in all_messages:
            mess_date_utc4 = tz.normalize(i.date.astimezone(tz))  # Перевод времени в другой часовой пояс. ЭТО РАБОТАЕТ!
            if i.address == request.user.get_username():
                is_inner = True
            else:
                is_inner = False
            last_id = i.id
            text_and_time.append([i, mess_date_utc4.strftime("%H:%M"), is_inner])
        return render(request, 'messanger.html',
                      {'username': request.GET.get('user'), 'text': text_and_time, 'last_id': last_id})


def userlist_page(request):
    all_users = User.objects.all()
    users_and_messages = []

    for user in all_users:
        user_messages = (Message.objects.filter(author=user) & Message.objects.filter(address=request.user)) | (
                Message.objects.filter(author=request.user) & Message.objects.filter(address=user))
        if len(user_messages) > 0 and user != request.user:
            last_message = user_messages[len(user_messages) - 1]
            users_and_messages.append([user.get_username(), last_message])
    print(users_and_messages)
    return render(request, 'userlist.html', {'data': users_and_messages})


def Design_page(request):
    return render(request, 'Design.html', {'username': request.user.username})


@csrf_exempt
def login_page(request):
    if is_ajax(request) and request.method == "POST":
        user = authenticate(username=request.POST.get("login"),
                            password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            print("\n=============Success Authentication!!!=========")
            print("Username (or email): " + request.user.get_username())
            print("===============================================\n")
            if getGroup(request.user) == "Worker":
                return JsonResponse({'text': 'NiceWorkLogin'})
            elif getGroup(request.user) == "Client" or getGroup(request.user) == "Admin":
                return JsonResponse({'text': 'NiceClientLogin'})
        else:
            return JsonResponse({'text': "NotLogin"})
    if request.method == "GET":
        return render(request, 'login.html')


def Prog_page(request):
    return render(request, 'Prog.html', {'username': request.user.username})


def VidEd_page(request):
    return render(request, 'VidEd.html', {'username': request.user.username})


@csrf_exempt
def signin(request):
    if is_ajax(request):
        email = request.POST.get('email')
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = User.objects.create_user(username, email, password)
        user.save()
        group = UserGroup.objects.filter(groupname="Client")[0]
        prof = Profile(user=user, first_name=username, email=email, group=group)
        prof.save()

        print("\n|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        print("                         New register user!                            ")
        print("name: " + request.POST.get("login"))
        print("email: " + request.POST.get("email"))
        print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n")
        # user = authenticate(username, password)
        login(request, user)

        default_ava_url = os.path.join(Path(__file__).resolve().parent, "static/img/default.png")
        new_ava_url = os.path.join(Path(__file__).resolve().parent, "static/avatars", user.username + ".png")
        copy2(default_ava_url, new_ava_url)

        return JsonResponse({'text': 'NiceSignin'})


def neworder(request):
    print(getGroup(request.user))
    if getGroup(request.user) != "Client" and getGroup(request.user) != "Admin":

        return HttpResponseRedirect("/incorrectacc/")
    return render(request, "formaplication.html")


@csrf_exempt
def upload_files(request):
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')
        uploaded_files = []
        urls_files = []

        for file in files:
            while True:
                i = 0
                randfilename = str(random.randint(100000000, 999999999)) + file.name[-4:]
                file_path = os.path.join(Path(__file__).resolve().parent, "static/loadFiles", randfilename)
                if not os.path.exists(file_path):
                    break
                i += 1
                if i > 10000:
                    return JsonResponse({'message': 'error, can not generate file name'})
            with open(file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            uploaded_files.append(file.name)
            urls_files.append(randfilename)
        return JsonResponse({'message': uploaded_files, 'urls': urls_files})


@csrf_exempt
def remove_files(request):
    if is_ajax(request):
        url = request.POST.get('removeFile')
        print(url)
        url = os.path.join(Path(__file__).resolve().parent, "static/loadFiles", url)
        os.remove(url)
        print(url)
        return JsonResponse({"message": "ok"})


@csrf_exempt
def create_order(request):
    if is_ajax(request):
        datearr = str(request.POST.get("date")).split('-')
        timearr = str(request.POST.get("time")).split(':')
        deadline = timezone.datetime(int(datearr[0]), int(datearr[1]), int(datearr[2]), int(timearr[0]),
                                     int(timearr[1]))
        newOrder = Order(creator=request.user, name=request.POST.get("name"), about=request.POST.get("description"),
                         deadline=deadline)
        newOrder.save()
        return JsonResponse({'message': 'ok'})


def worker_page(request):
    if getGroup(request.user) != "Worker" and getGroup(request.user) != "Admin":
        return HttpResponseRedirect('/profile/')

    username = getProfile(request.user).user
    firstname = getProfile(request.user).first_name
    secondname = getProfile(request.user).second_name
    if not getSkills(request.user):
        newSkillTable = Skills(user=request.user)
        newSkillTable.save()
    skills_item = getSkills(request.user)
    all_bools = skills_item.getAll()
    print(all_bools)
    return render(request, "worker.html",
                  {'username': username, 'firstname': firstname, 'secondname': secondname,
                   'skills': all_bools})


def orders_page(request):
    if getGroup(request.user) != "Worker" and getGroup(request.user) != "Admin":
        return HttpResponseRedirect('/incorrectacc/')

    all_orders = Order.objects.filter(status="sent")
    all_names_creators = []
    for i in all_orders:
        deltadays = int(str(i.deadline.date() - timezone.now().date()).split(" ")[0])
        all_names_creators.append(
            [i.name, i.creator, i.created_time.strftime("%d.%m.%Y"), i.created_time.strftime("%H:%M"), deltadays])
    return render(request, "Orders.html", {'names_creators': all_names_creators})


def incorrent_acc(request):
    print(getProfile(request.user).group)
    if getProfile(request.user).group.groupname == "Client":
        return render(request, "NotInWorkerAccount.html")
    elif getProfile(request.user).group.groupname == "Worker":
        return render(request, "NotInClientAccount.html")
    else:
        return render(request, "NotInAccount.html")


def wsettings_page(request):
    if getGroup(request.user) != 'Worker' and getGroup(request.user) != 'Admin':
        return HttpResponseRedirect("/incorrectacc/")
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        secondname = request.POST.get('secondname')
        prof = getProfile(request.user)
        prof.first_name = firstname
        prof.second_name = secondname
        prof.save()

        return HttpResponseRedirect("/profile/")

    prof = getProfile(request.user)
    return render(request, "wsettings.html", {'firstname': prof.first_name, 'secondname': prof.second_name})


def save_skills(request):
    if is_ajax(request):
        all_skills = request.POST.getlist('skills[]')
        for i in range(len(all_skills)):
            if all_skills[i] == "false":
                all_skills[i] = False
            elif all_skills[i] == "true":
                all_skills[i] = True
        print(all_skills)
        skillsItem = getSkills(request.user)
        skillsItem.setAll(all_skills)
        skillsItem.save()
        return JsonResponse({})


@csrf_exempt
def upload_avatar(request):
    if request.method == 'POST':
        file = request.FILES.getlist('file')[0]
        print(file)
        file_path = os.path.join(Path(__file__).resolve().parent, "static/avatars", request.user.username + ".png")
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return JsonResponse({'message': 'ok'})


def csettings_page(request):
    if getGroup(request.user) != "Client" and getGroup(request.user) != "Admin":
        return HttpResponseRedirect("/incorrectacc/")
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        secondname = request.POST.get("secondname")
        prof = getProfile(request.user)
        prof.first_name = firstname
        prof.second_name = secondname
        prof.save()
    prof = getProfile(request.user)
    return render(request, "settings.html", {'firstname': prof.first_name, 'secondname': prof.second_name})


def history_page(request):
    if getGroup(request.user) != "Worker" and getGroup(request.user) != "Admin":
        return HttpResponseRedirect('/incorrectacc/')

    all_orders = ((Order.objects.filter(status="canceled") | Order.objects.filter(status="complete"))
                  & Order.objects.filter(worker=request.user.username))
    all_names_creators = []
    for i in all_orders:
        status = i.status
        all_names_creators.append(
            [i.name, i.creator, i.created_time.strftime("%d.%m.%Y"), i.created_time.strftime("%H:%M"), status])
    return render(request, "orderHistory.html", {'names_creators': all_names_creators})


def contacts_page(request):
    return render(request, "contacts.html", {'username': request.user.username})


def help_page(request):
    return render(request, "help.html", {'username': request.user.username})


def new_help(request):
    if request.method == "POST":
        topic = request.POST.get("topic")
        description = request.POST.get("description")
        callback = request.POST.get("callback")
        if request.user.username != "":
            prof = getProfile(request.user)
            new_help = Help(topic=topic, description=description, callback=callback, user=prof)
        else:
            new_help = Help(topic=topic, description=description, callback=callback)
        new_help.save()
        return render(request, "good_help.html")


def change_telegram(request):
    if request.method == "GET":
        return render(request, 'change_telegram.html')

    if request.method == "POST":
        if request.POST.get('code_1'):

            entered_code = request.POST.get('code_1') + request.POST.get('code_2') + request.POST.get(
                'code_3') + request.POST.get('code_4') + request.POST.get('code_5')

            try:
                entered_code = int(entered_code)
            except:
                return render(request, 'change_telegram2.html', {'errors': 'yes'})

            tg_code = getTgCode(request.user)
            if tg_code.code == entered_code and (timezone.now() - tg_code.time).seconds < 600:
                prof = getProfile(request.user)
                prof.telegram_id = getTgCode(request.user).maybe_tg_id
                prof.save()
                return HttpResponseRedirect('/profile/')

            else:
                return render(request, 'change_telegram2.html', {'errors': 'yes'})

        if request.POST.get('telegram_id'):
            telegram_id = request.POST.get('telegram_id')
            rand_code = random.randint(10000, 99999)
            print('Telegram code: ' + str(rand_code))
            # Отправляем код в тг челу
            tg_code = getTgCode(request.user)
            tg_code.code = rand_code
            tg_code.time = timezone.now()
            tg_code.maybe_tg_id = telegram_id
            tg_code.save()
            return render(request, 'change_telegram2.html', {'errors': 'no'})
def admin_page(request):
    if getGroup(request.user) == "Admin":
        return render(request, "admin_panel.html")
    else:
        return HttpResponseRedirect("/index/")
def sales_page(request):
    if getGroup(request.user) == 'Admin':
        return render(request, 'sales.html')

def order_page(request):
    # if getGroup(request.user) != "Client" and getGroup(request.user) != "Admin":
    #     return HttpResponseRedirect('/worker')
    order = (Order.objects.filter(creator=request.user) & Order.objects.filter(id=request.GET.get("order_id")))[0]
    datedeadline = order.deadline.strftime("%d.%m.%Y %H:%M")
    print(1111, order.worker)
    if order.status=="sent": status="Ожидает подтверждения"
    else:
        if order.status=="inwork": status="Принят в работу"
        else:
            if order.status=="complete":  status="Выполнен"
            else:
                if order.status=="canceled": status="Отменен"
    # match status:
    #     case "sent":
    #         print("Ожидает подтверждения")
    #     case "inwork":
    #         print("Принят в работу")
    #     case "complete":
    #         print("Выполнен")
    #     case "canceled":
    #         print("Отменен")
    return render(request, 'order.html', {'orderid': order.id, 'ordername': order.name, 'orderstatus': status,
                                          'orderabout': order.about, 'orderdeadline': datedeadline,
                                          'orderworker': order.worker})
@csrf_exempt
def edit_order(request):
    print(1000000000000)
    if is_ajax(request):

        # datearr = str(request.POST.get("date")).split('-')
        # timearr = str(request.POST.get("time")).split(':')
        # deadline = timezone.datetime(int(datearr[0]), int(datearr[1]), int(datearr[2]), int(timearr[0]),
        #                              int(timearr[1]))
        # newOrder = Order(creator=request.user, name=request.POST.get("name"), about=request.POST.get("description"),
        #                  deadline=deadline)
        # newOrder.save()
        return JsonResponse({'message': 'ok'})