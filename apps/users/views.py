import json

from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

from .forms import RegisterForm, LoginForm, ForgetPwdForm, ModifyForm, AddressForm
from .models import UserProfile, EmailCode, Address
from opreation.models import ShopCartRecord,UserMessage
from orders.models import Order, DeliveryOrder,ReturnOrder
from utils.emailsend import send_email


# Create your views here.

class RegisterView(View):
    """注册界面的处理"""

    def get(self, request):

        return render(request, 'register.html')

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email')
            nickname = request.POST.get('nickname')

            if UserProfile.objects.filter(email=email) or UserProfile.objects.filter(nickname=nickname):
                return render(request, 'register.html', dict(msg='用户名或邮箱已存在'))

            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password2 != password1:
                return render(request, 'register.html', dict(msg='密码输入不一致'))

            code = request.POST.get('code')
            if not EmailCode.objects.filter(email=email, code=code, send_type="register"):
                return render(request, 'register.html', dict(msg='验证码不对'))
            user = UserProfile()
            user.email = email
            user.nickname = nickname
            user.is_active = 1
            user.password = make_password(password1)
            user.username = nickname
            user.save()
            return render(request, 'login.html')

        else:
            return render(request, 'register.html', dict(register_form=register_form))


class CustomBackend(ModelBackend):
    """自定义登录验证"""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):  # 检查密码
                return user
        except Exception:
            return None


class LoginView(View):
    """登录逻辑"""

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return render(request, 'index.html')
            else:
                return render(request, 'login.html', dict(msg="用户或密码错误"))

        else:
            return render(request, 'login.html', dict(login_form=login_form))


class LogoutView(View):
    """登出逻辑"""

    def get(self, request):
        logout(request)
        from django.urls import reverse
        return HttpResponseRedirect(reverse("index"), {})


class ForgetPwdView(View):
    """忘记密码"""

    def get(self, request):
        return render(request, 'forgetpwd.html')

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():

            email = request.POST.get("email")
            if not UserProfile.objects.filter(email=email):
                return render(request, "forgetpwd.html", dict(msg="没有查找到用户"))

            code = request.POST.get("code")
            if not EmailCode.objects.filter(send_type="forgetpwd", email=email, code=code):
                return render(request, "forgetpwd.html", dict(msg="验证码输入错误"))

            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 != password2:
                return render(request, "forgetpwd.html", dict(msg="密码不一致"))

            user = UserProfile.objects.get(email=email)
            user.password = make_password(password1)
            user.save()
            return render(request, "login.html")
        else:
            return render(request, "forgetpwd.html", dict(forgetpwd_form=forgetpwd_form))


class GetEmailCodeView(View):
    """发送验证码"""

    def post(self, request):
        email = request.POST.get("email")
        type = request.POST.get("type")
        if type == "modifyemail":

            if UserProfile.objects.filter(email=email):
                return HttpResponse('{"status":"fail"}', content_type='application/json')
        try:
            send_email(email, type)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        except:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UserCenterIndexView(View):

    def get(self, request):
        return render(request, "usercenter-index.html", dict(user=request.user))

    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            user = request.user
            birthday = request.POST.get("birthday")
            gender = request.POST.get("gender")
            tel = request.POST.get("tel")
            user.birthday = birthday
            user.tel = tel
            user.gender = gender
            user.save()
            return render(request, "usercenter-index.html", dict(msg="保存成功"))
        else:
            return render(request, "usercenter-index.html", dict(modify_form=modify_form))


class ModifyPwdView(View):
    """个人中心修改密码"""

    def post(self, request):
        oldpwd = request.POST.get('oldpass')
        newpwd = request.POST.get('newpass')
        user = request.user
        if not user.check_password(oldpwd):
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            user.password = make_password(newpwd)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')


class ModifyEmailView(View):
    """个人中心修改邮箱"""

    def post(self, request):
        email = request.POST.get("email")
        code = request.POST.get("code")
        if not EmailCode.objects.filter(send_type="modifyemail", email=email, code=code):
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        user = request.user
        user.email = email
        user.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')


class AddressListView(View):
    """个人地址展示"""

    def get(self, request):
        addresses = Address.objects.filter(user=request.user)
        return render(request, "usercenter-address.html", dict(addresses=addresses))


class AddAddressView(View):
    """添加或修改个人地址"""

    def get(self, request, address_id):
        if address_id == 0:
            return render(request, "usercenter-addaddress.html", dict(id=address_id))
        else:
            address = Address.objects.get(id=address_id)
            return render(request, "usercenter-addaddress.html", dict(address=address, id=address_id))

    def post(self, request, address_id):
        # id为0的话是添加，不为0则是修改
        if address_id == 0:
            content = request.POST.get("address")
            detail = request.POST.get("detail")
            name = request.POST.get("name")
            tel = request.POST.get("tel")
            contents = str(content).split('/')
            if len(contents) < 3 or detail == '' or name == '' or tel == '' or len(tel) > 11:
                return render(request, 'usercenter-addaddress.html', dict(id=address_id, msg="缺少必填字段或错误"))
            else:
                address = Address()
                address.province = contents[0]
                address.city = contents[1]
                address.region = contents[2]
                if len(contents) > 3:
                    address.town = contents[3]
                address.tel = tel
                address.name = name
                address.detail = detail
                address.user = request.user
                address.save()
                from django.urls import reverse
                return HttpResponseRedirect(reverse('users:addresslist'))
        else:
            content = request.POST.get("address")
            detail = request.POST.get("detail")
            name = request.POST.get("name")
            tel = request.POST.get("tel")
            contents = str(content).split('/')
            if len(contents) < 3 or detail == '' or name == '' or tel == '' or len(tel) > 11:
                return render(request, 'usercenter-addaddress.html', dict(id=address_id, msg="缺少必填字段或错误"))
            else:
                address = Address.objects.get(id=address_id)
                address.province = contents[0]
                address.city = contents[1]
                address.region = contents[2]
                if len(contents) > 3:
                    address.town = contents[3]
                address.tel = tel
                address.name = name
                address.detail = detail
                address.user = request.user
                address.save()
                from django.urls import reverse
                return HttpResponseRedirect(reverse('users:addresslist'))


class DeleteAddressView(View):

    def get(self, request, address_id):
        address = Address.objects.get(id=address_id)
        address.delete()
        from django.urls import reverse
        return HttpResponseRedirect(reverse('users:addresslist'))


class WalletView(View):
    """我的钱包"""

    def get(self, request):
        user = request.user
        return render(request, "usercenter-wallet.html", dict(user=user))

    def post(self, request):
        code = request.POST.get('code', '')
        paypass = request.POST.get('paypwd')
        if not EmailCode.objects.filter(email=request.user.email, code=code, send_type='modifypaypwd'):
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            user = request.user
            user.paypass = make_password(paypass)
            user.save()
            user_message = UserMessage()
            user_message.user = request.user
            user_message.content = '您的支付密码已经成功修改'
            user_message.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')


class CartView(View):
    """购物车"""

    def get(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        myshopcart = ShopCartRecord.objects.filter(user=request.user)
        return render(request, 'usercenter-cart.html', dict(myshopcart=myshopcart))


class ChangeCartView(View):
    """修改购物车的信息"""

    def get(self, request):
        id = request.GET.get('id')
        nums = request.GET.get('nums')
        record = ShopCartRecord.objects.get(id=id)
        record.nums = nums
        record.save()
        if int(record.nums) > record.commodity.stock:
            return HttpResponse('{"status":"success","msg":"buzu"}', content_type='application/json')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class DeteleCartView(View):
    """删除购物车信息"""

    def get(self, request, cart_id):
        record = ShopCartRecord.objects.get(id=cart_id)
        record.delete()
        from django.urls import reverse
        return HttpResponseRedirect(reverse('users:cart'))


class UnpaidOrderView(View):
    """用户未完成的订单"""

    def get(self, request):
        all_orders = Order.objects.filter(user=request.user, status='unpaid').order_by('-add_time')
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orders, 5, request=request)

        all_orders = p.page(page)
        return render(request, "usercenter-order-unpaid.html", dict(all_orders=all_orders))


class DeleteUnpaidOrderView(View):
    """删除未完成的订单"""

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        order.delete()
        from django.urls import reverse
        return HttpResponseRedirect(reverse('users:unpaidorder'))


class Pay1View(View):
    """从未完成订单前往付款界面"""

    def get(self, request):
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id=order_id)
        return render(request, 'pay.html', dict(order=order))


class PaidOrderView(View):
    """已付款的订单界面"""

    def get(self, request):
        all_orders = Order.objects.filter(user=request.user, status='paid').order_by('-add_time')
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orders, 5, request=request)

        all_orders = p.page(page)
        return render(request, "usercenter-order-paid.html", dict(all_orders=all_orders))

class ConfirmRecView(View):
    """确认收到货"""

    def get(self,request):
        p_id = request.GET.get('id')
        id = str(p_id).replace('订单编号：','').replace(' ','').replace('\n','')
        nums = Order.objects.filter(id=id).count()
        order = Order.objects.get(id=id)
        order.status = 'finished'
        order.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')


class FinshedOrderView(View):
    """已完成界面"""

    def get(self,request):
        all_orders = Order.objects.filter(user=request.user,status='finished').order_by('-add_time')
        # 进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orders, 5, request=request)

        all_orders = p.page(page)
        return render(request, "usercenter-order-finshed.html", dict(all_orders=all_orders))


class ReturnView(View):
    """退货"""

    def post(self,request):
        id = request.POST.get('orderid')
        type = request.POST.get('hav_get','mc')
        reason = request.POST.get('reason')
        delivery = DeliveryOrder.objects.get(id=id)
        record = ReturnOrder()
        record.id = delivery.id.replace('C','R')
        record.type = type
        record.delivery = delivery
        record.reason = reason
        record.save()
        from django.urls import reverse
        return HttpResponseRedirect(reverse('users:returnorder'))


class ReturnOrderView(View):
    """退单界面"""

    def get(self,request):
        all_orders = ReturnOrder.objects.filter(delivery__order__user=request.user).order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orders, 5, request=request)

        all_orders = p.page(page)
        return render(request,'usercenter-order-return.html',dict(all_orders=all_orders))


class AddReturnView(View):
    """登记单号"""

    def post(self,request):
        id = request.POST.get('orderid')
        express = request.POST.get('express')
        returnorder = ReturnOrder.objects.get(id=id)
        returnorder.tracking = express
        returnorder.re_status = 'ing'
        returnorder.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')


class MessageView(View):
    """用户信息"""

    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user).order_by('-send_time')
        for message in all_message:
            message.have_read = True
            message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 10, request=request)

        all_message = p.page(page)

        return render(request,'usercenter-message.html',dict(all_message=all_message))

