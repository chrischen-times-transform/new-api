from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template, render_to_string
from django.contrib.auth.hashers import make_password
from passlib.handlers.django import django_pbkdf2_sha256
from django.core import mail
from django.utils.html import strip_tags
from django.db.models import Q
from hkshopu import models
import datetime
import re
import random

# Create your views here.

# 會員註冊頁面
def register(request):
    template = get_template('register.html')
    html = template.render()
    return HttpResponse(html)
# 檢查電子郵件是否已存在
def checkEmailExistsProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')

        if response_data['status'] == 0:
            users = models.User.objects.filter(email=email)
            if len(users) > 0:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件已存在!'

        if response_data['status'] == 0:
            response_data['ret_val'] = '該電子郵件沒有重複使用!'
    return JsonResponse(response_data)
# 確認電子郵件是否透過社群登入
def checkEmailIsAllowedLoginProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')

        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件未被使用!'

        if response_data['status'] == 0:
            if not(user.password):
                response_data['status'] = -2
                response_data['ret_val'] = '該電子郵件只可透過社群登入!'

        if response_data['status'] == 0:
            response_data['ret_val'] = '該電子郵件可正常登入!'
    return JsonResponse(response_data)
# 會員註冊
def registerProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'user_id': ''
    }
    if request.method == 'POST':
        # 取得欄位資料
        accountName = request.POST.get('account_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirmPassword = request.POST.get('confirm_password', '')
        firstName = request.POST.get('first_name', '')
        lastName = request.POST.get('last_name', '')
        phone = request.POST.get('phone', '')
        gender = request.POST.get('gender', '')
        birthday = request.POST.get('birthday', '')
        address = request.POST.get('address', '')
        region = request.POST.get('region', '')
        district = request.POST.get('district', '')
        street_name = request.POST.get('street_name', '')
        street_no = request.POST.get('street_no', '')
        floor = request.POST.get('floor', '')
        room = request.POST.get('room', '')
        # 判斷欄位資料是否符合要求格式
        if responseData['status'] == 0:
            if accountName:
                if not(re.match('^[A-Za-z]{3,45}$', accountName)):
                    responseData['status'] = -1
                    responseData['ret_val'] = '用戶名稱格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', email)):
                responseData['status'] = -2
                responseData['ret_val'] = '電子郵件格式錯誤!'

        if responseData['status'] == 0:
            if not(re.match('^(?!.*[^\x21-\x7e])(?=.{8,16})(?=.*[\W])(?=.*[a-zA-Z])(?=.*\d).*$', password)):
                responseData['status'] = -3
                responseData['ret_val'] = '密碼格式錯誤!'

        if responseData['status'] == 0:
            if confirmPassword != password:
                responseData['status'] = -4
                responseData['ret_val'] = '兩次密碼輸入不一致!'

        if responseData['status'] == 0:
            if firstName:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', firstName)):
                    responseData['status'] = -5
                    responseData['ret_val'] = '名字格式錯誤!'
            else:
                firstName = str(email).split('@')[0]

        if responseData['status'] == 0:
            if lastName:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', lastName)):
                    responseData['status'] = -6
                    responseData['ret_val'] = '姓氏格式錯誤!'

        if responseData['status'] == 0:
            if phone:
                if not(re.match('^[0-9]{8,10}$', phone)):
                    responseData['status'] = -7
                    responseData['ret_val'] = '手機號碼格式錯誤!'
        if responseData['status'] == 0:
            if gender:
                if not(re.match('^[M|F|O]{1}$', gender)):
                    responseData['status'] = -8
                    responseData['ret_val'] = '性別格式錯誤!'

        if responseData['status'] == 0:
            if birthday:
                if not(re.match('^[0-9]{2}\/[0-9]{2}\/[0-9]{4}$', birthday)):
                    responseData['status'] = -9
                    responseData['ret_val'] = '出生日期格式錯誤!'

        if responseData['status'] == 0:
            if address:
                if not(re.match('^[A-Za-z0-9\u4e00-\u9fa5]{1,95}$', address)):
                    responseData['status'] = -10
                    responseData['ret_val'] = '居住地址格式錯誤!'

        if responseData['status'] == 0:
            if region:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', region)):
                    responseData['status'] = -11
                    responseData['ret_val'] = '地域格式錯誤!'

        if responseData['status'] == 0:
            if district:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', district)):
                    responseData['status'] = -12
                    responseData['ret_val'] = '地區格式錯誤!'

        if responseData['status'] == 0:
            if street_name:
                if not(re.match('^[A-Za-z\u4e00-\u9fa5]{1,45}$', street_name)):
                    responseData['status'] = -13
                    responseData['ret_val'] = '街道名稱格式錯誤!'

        if responseData['status'] == 0:
            if street_no:
                if not(re.match('^[0-9\u4e00-\u9fa5]{1,45}$', street_no)):
                    responseData['status'] = -14
                    responseData['ret_val'] = '街道門牌格式錯誤!'

        if responseData['status'] == 0:
            if floor:
                if not(re.match('^[0-9\u4e00-\u9fa5]{1,45}$', floor)):
                    responseData['status'] = -15
                    responseData['ret_val'] = '樓層格式錯誤!'

        if responseData['status'] == 0:
            if room:
                if not(re.match('^[0-9\u4e00-\u9fa5]{1,45}$', room)):
                    responseData['status'] = -16
                    responseData['ret_val'] = '室格式錯誤!'
        # 判斷使用者是否使用相同電子郵件重複註冊
        if responseData['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
                responseData['status'] = -17
                responseData['ret_val'] = '該電子郵件已被使用!'
            except:
                pass
                
        if responseData['status'] == 0:
            models.User.objects.create(
                account_name=accountName, 
                email=email, 
                password=make_password(password), 
                first_name=firstName, 
                last_name=lastName, 
                phone=phone, 
                gender=gender, 
                birthday=birthday, 
                address=address, 
                region=region, 
                district=district, 
                street_name=street_name, 
                street_no=street_no, 
                floor=floor, 
                room=room
            )
            try:
                user = models.User.objects.get(email=email)
                responseData['user_id'] = user.id
                # 預設將使用者登入
                request.session['user'] = {
                    'id': user.id, 
                    'account_name': user.account_name, 
                    'email': user.email, 
                    'first_name': user.first_name, 
                    'last_name': user.last_name
                }
            except:
                pass
            responseData['ret_val'] = '註冊成功!'
    return JsonResponse(responseData)
# 產生並發送驗證碼到使用者電子郵件
def generateAndSendValidationCodeProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')
        # 檢查使用者是否登入
        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件未被使用!'

        if response_data['status'] == 0:
            # 產生帳號註冊驗證碼
            rand_str = ''
            needle = '0123456789'
            for j in range(4):
                rand_str += random.choice(needle)
            # 判斷資料表中是否已有使用者電子郵件和驗證碼，若沒有則新增，若有則更新
            try:
                user_validation = models.Email_Validation.objects.get(email=email)
                user_validation.validation_code = rand_str
                user_validation.save()
            except:
                models.Email_Validation.objects.create(
                    user_id=user.id, 
                    email=user.email, 
                    validation_code=rand_str
                )
            # 發送電子郵件，告知帳號註冊驗證碼
            subject = ''
            html_message = render_to_string('validation_mail.html', {'account_name': user.account_name, 'validation_code': rand_str})
            message = strip_tags(html_message)
            from_email = 'HKShopU'
            recipient_list = [user.email, ]
            mail.send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list)
            response_data['ret_val'] = '已寄出驗證碼!'
    return JsonResponse(response_data)
# 驗證電子郵件
def validateEmailProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 取得欄位資料
        email = request.POST.get('email', '')
        validation_code = request.POST.get('validation_code', '')
        # 確認電子郵件是否存在
        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件不存在!'
        # 確認電子郵件及驗證碼是否正確
        if response_data['status'] == 0:
            try:
                user_validation = models.Email_Validation.objects.get(email=email, validation_code=validation_code)
            except:
                response_data['status'] = -2
                response_data['ret_val'] = '電子郵件或驗證碼錯誤!'

        if response_data['status'] == 0:
            now = datetime.datetime.now()
            updated_at = user_validation.updated_at
            if (now - updated_at).min > datetime.timedelta(minutes=10):
                response_data['status'] = -3
                response_data['ret_val'] = '驗證碼已過期，請重新產生!'

        if response_data['status'] == 0:
            user.activated = 'Y'
            user.save()
            response_data['ret_val'] = '驗證成功!'
    return JsonResponse(response_data)
# 會員登入
def loginProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'user_id': ''
    }
    if request.method == 'POST':
        # 取得欄位資料
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        # 驗證使用者輸入的電子郵件與密碼是否正確
        if responseData['status'] == 0:
            if not(email) or not(password):
                responseData['status'] = -1
                responseData['ret_val'] = '電子郵件或密碼未填寫!'

        if responseData['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                responseData['status'] = -2
                responseData['ret_val'] = '電子郵件錯誤!'

        if responseData['status'] == 0:
            if not(user.password):
                responseData['status'] = -3
                responseData['ret_val'] = '此電子郵件僅透過社群帳號註冊使用，請選擇社群登入!'

        if responseData['status'] == 0:
            if not(django_pbkdf2_sha256.verify(password, user.password)):
                responseData['status'] = -4
                responseData['ret_val'] = '密碼錯誤!'

        if responseData['status'] == 0:
            request.session['user'] = {
                'id': user.id, 
                'account_name': user.account_name, 
                'email': user.email, 
                'first_name': user.first_name, 
                'last_name': user.last_name
            }
            responseData['user_id'] = user.id
            responseData['ret_val'] = '登入成功!'
    return JsonResponse(responseData)
# 社群登入
def socialLoginProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'user_id': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')
        googleAccount = request.POST.get('google_account', '')
        facebookAccount = request.POST.get('facebook_account', '')
        appleAccount = request.POST.get('apple_account', '')

        if responseData['status'] == 0:
            if googleAccount and email:
                try:
                    user = models.User.objects.get(email=email)
                    user.google_account = googleAccount
                    user.save()
                    responseData['user_id'] = user.id
                    responseData['ret_val'] = '已使用 Google 帳戶登入!'
                    responseData['status'] = 1
                except:
                    models.User.objects.create(
                        google_account=googleAccount, 
                        email=email
                    )
                    responseData['user_id'] = models.User.objects.order_by('-updated_at')[0].id
                    responseData['ret_val'] = '已使用 Google 帳戶註冊!'
                    responseData['status'] = -1

        if responseData['status'] == 0:
            if facebookAccount and email:
                try:
                    user = models.User.objects.get(email=email)
                    user.facebook_account = facebookAccount
                    user.save()
                    responseData['user_id'] = user.id
                    responseData['ret_val'] = '已使用 Facebook 帳戶登入!'
                    responseData['status'] = 2
                except:
                    models.User.objects.create(
                        facebook_account=facebookAccount, 
                        email=email
                    )
                    responseData['user_id'] = models.User.objects.order_by('-updated_at')[0].id
                    responseData['ret_val'] = '已使用 Facebook 帳戶註冊!'
                    responseData['status'] = -2

        if responseData['status'] == 0:
            if appleAccount:
                try:
                    user = models.User.objects.get(apple_account=appleAccount)
                    responseData['user_id'] = user.id
                    responseData['ret_val'] = '已使用 Apple 帳戶登入!'
                    responseData['status'] = 3
                except:
                    try:
                        user = models.User.objects.get(email=email)
                        user.apple_account = appleAccount
                        user.save()
                        responseData['user_id'] = user.id
                        responseData['ret_val'] = '已使用 Apple 帳戶登入!'
                        responseData['status'] = 3
                    except:
                        models.User.objects.create(
                            apple_account=appleAccount, 
                            email=email
                        )
                        responseData['user_id'] = models.User.objects.order_by('-updated_at')[0].id
                        responseData['ret_val'] = '已使用 Apple 帳戶註冊!'
                        responseData['status'] = -3
    return JsonResponse(responseData)
# 忘記密碼
def forgetPasswordProcess(request):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')

        if responseData['status'] == 0:
            if not(email):
                responseData['status'] = -1
                responseData['ret_val'] = '電子郵件未填寫!'

        if responseData['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                responseData['status'] = -2
                responseData['ret_val'] = '電子郵件錯誤或未被使用!'

        if responseData['status'] == 0:
            # 產生隨機字串
            seed = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+'
            i = 1
            while i > 0:
                randStrList = []
                for i in range(8):
                    randStrList.append(random.choice(seed))
                token = ''.join(randStrList)
                # 確認資料表中沒有重複的 Token
                users = models.User.objects.filter(forget_password_token=token)
                i = len(users)
            # 更新使用者的 Token
            user.forget_password_token = token
            user.save()
            # 發送忘記密碼通知信
            subject = 'HKShopU - 忘記密碼'
            htmlMessage = render_to_string('forget_password_mail.html', {'id': user.id, 'account_name': user.account_name, 'token': user.forget_password_token})
            message = strip_tags(htmlMessage)
            fromEmail = 'HKShopU'
            toEmail = [email, ]
            mail.send_mail(subject=subject, message=message, from_email=fromEmail, recipient_list=toEmail, html_message=htmlMessage)
            responseData['ret_val'] = '已發送重設密碼連結至您的電子郵件!'
    return JsonResponse(responseData)
# 會員密碼更新
def resetPasswordProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': ''
    }
    if request.method == 'POST':
        # 欄位資料
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        # 檢查電子郵件是否存在
        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(email=email)
            except:
                response_data['status'] = -1
                response_data['ret_val'] = '該電子郵件不存在或未被使用!'
        # 檢查密碼格式是否正確
        if response_data['status'] == 0:
            if not(re.match('^(?!.*[^\x21-\x7e])(?=.{8,16})(?=.*[\W])(?=.*[a-zA-Z])(?=.*\d).*$', password)):
                response_data['status'] = -2
                response_data['ret_val'] = '密碼格式錯誤!'
        # 檢查兩次密碼輸入是否一致
        if response_data['status'] == 0:
            if confirm_password != password:
                response_data['status'] = -3
                response_data['ret_val'] = '兩次密碼輸入不一致!'
        # 更新會員密碼
        if response_data['status'] == 0:
            user.password = make_password(password)
            user.save()
            response_data['ret_val'] = '密碼修改成功!'
    return JsonResponse(response_data)
# 使用者商店列表
def getUserShopListProcess(request, id):
    # 回傳資料
    responseData = {
        'status': 0, 
        'ret_val': '', 
        'shop_list': []
    }

    if request.method == 'GET':
        if responseData['status'] == 0:
            shops = models.Shop.objects.filter(user_id=id)
            if len(shops) == 0:
                responseData['status'] = 1
                responseData['ret_val'] = '您尚未建立任何商店!'
        
        if responseData['status'] == 0:
            for shop in shops:
                shopInfo = {
                    'id': shop.id, 
                    'user_id': shop.user_id, 
                    'shop_category_id': shop.shop_category_id, 
                    'shop_title': shop.shop_title, 
                    'shop_icon': shop.shop_icon, 
                    'shop_pic': shop.shop_pic, 
                    'shop_description': shop.shop_description, 
                    'paypal': shop.paypal, 
                    'visa': shop.visa, 
                    'master': shop.master, 
                    'apple': shop.apple, 
                    'android': shop.android, 
                    'is_ship_free': shop.is_ship_free, 
                    'ship_by_product': shop.ship_by_product, 
                    'ship_free_quota': shop.ship_free_quota, 
                    'fix_ship_fee': shop.fix_ship_fee, 
                    'fix_ship_fee_from': shop.fix_ship_fee_from, 
                    'fix_ship_fee_to': shop.fix_ship_fee_to, 
                    'created_at': shop.created_at, 
                    'updated_at': shop.updated_at
                }
                responseData['shop_list'].append(shopInfo)
            responseData['ret_val'] = '已取得您的商店清單!'
    return JsonResponse(responseData)
# 取得會員資料
def getUserListProcess(request):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'user_list': []
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            users = models.User.objects.all()
            if len(users) == 0:
                response_data['status'] = 1
                response_data['ret_val'] = '目前尚未存在任何會員!'
            
        if response_data['status'] == 0:
            for user in users:
                user_info = {
                    'id': user.id, 
                    'account_name': user.account_name, 
                    'google_account': user.google_account, 
                    'facebook_account': user.facebook_account, 
                    'apple_account': user.apple_account, 
                    'email': user.email, 
                    'password': user.password, 
                    'first_name': user.first_name, 
                    'last_name': user.last_name, 
                    'phone': user.phone, 
                    'gender': user.gender, 
                    'birthday': user.birthday, 
                    'address': user.address, 
                    'region': user.region, 
                    'district': user.district, 
                    'street_name': user.street_name, 
                    'street_no': user.street_no, 
                    'floor': user.floor, 
                    'room': user.room, 
                    'forget_password_token': user.forget_password_token, 
                    'activated': user.activated, 
                    'created_at': user.created_at, 
                    'updated_at': user.updated_at
                }
                response_data['user_list'].append(user_info)
            response_data['ret_val'] = '取得會員資料成功!'
    return JsonResponse(response_data)
# 取得單一用戶資料
def show(request, id):
    response_data = {
        'status': 0, 
        'ret_val': '', 
        'user_data': {}
    }
    if request.method == 'GET':
        if response_data['status'] == 0:
            try:
                user = models.User.objects.get(id=id)
            except:
                response_data['status'] = 1
                response_data['ret_val'] = '找不到此使用者編號的資料!'

        if response_data['status'] == 0:
            response_data['user_data']['id'] = user.id
            response_data['user_data']['account_name'] = user.account_name
            response_data['user_data']['google_account'] = user.google_account
            response_data['user_data']['facebook_account'] = user.facebook_account
            response_data['user_data']['apple_account'] = user.apple_account
            response_data['user_data']['email'] = user.email
            response_data['user_data']['first_name'] = user.first_name
            response_data['user_data']['last_name'] = user.last_name
            response_data['user_data']['phone'] = user.phone
            response_data['user_data']['gender'] = user.gender
            response_data['user_data']['birthday'] = user.birthday
            response_data['user_data']['address'] = user.address
            response_data['user_data']['region'] = user.region
            response_data['user_data']['district'] = user.district
            response_data['user_data']['street_name'] = user.street_name
            response_data['user_data']['street_no'] = user.street_no
            response_data['user_data']['floor'] = user.floor
            response_data['user_data']['room'] = user.room
            response_data['user_data']['activated'] = user.activated
            response_data['user_data']['created_at'] = user.created_at
            response_data['user_data']['updated_at'] = user.updated_at
            response_data['ret_val'] = '已取得使用者資料!'
    return JsonResponse(response_data)
