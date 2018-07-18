from django.urls import path

from .views import RegisterView, GetEmailCodeView, LoginView, LogoutView, ForgetPwdView, UserCenterIndexView,ModifyPwdView
from .views import ModifyEmailView,AddressListView,AddAddressView,DeleteAddressView,WalletView,CartView,ChangeCartView
from .views import DeteleCartView,UnpaidOrderView,DeleteUnpaidOrderView,Pay1View,PaidOrderView,ConfirmRecView,FinshedOrderView
from .views import ReturnView,ReturnOrderView,AddReturnView,MessageView


app_name = 'users'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('sendemail', GetEmailCodeView.as_view(), name="getcode"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('forgetpwd/', ForgetPwdView.as_view(), name="forgetpwd"),
    path('usercenterinfo/', UserCenterIndexView.as_view(), name="usercenter"),
    path('modifypwd/',ModifyPwdView.as_view(),name="modifypwd"),
    path('modifyemail/',ModifyEmailView.as_view(),name="modifyeamil"),
    path('addresslist/',AddressListView.as_view(),name="addresslist"),
    path('addaddress/<int:address_id>',AddAddressView.as_view(),name="addaddress"),
    path('deleteaddress/<int:address_id>',DeleteAddressView.as_view(),name="deleteaddress"),
    path('wallet/',WalletView.as_view(),name="wallet"),
    path('cart/',CartView.as_view(),name='cart'),
    path('changecart/',ChangeCartView.as_view(),name='changecart'),
    path('deletecart/<int:cart_id>',DeteleCartView.as_view(),name='deletecart'),
    path('unpaidorder/',UnpaidOrderView.as_view(),name='unpaidorder'),
    path('delunpaidorder/<str:order_id>/',DeleteUnpaidOrderView.as_view(),name='delunpaidorder'),
    path('pay1',Pay1View.as_view(),name='pay1'),
    path('paidorder/',PaidOrderView.as_view(),name="paidorder"),
    path('conrec/',ConfirmRecView.as_view(),name='conrec'),
    path('finishedorder/',FinshedOrderView.as_view(),name='finishedorder'),
    path('return/',ReturnView.as_view(),name='return'),
    path('returnorder/',ReturnOrderView.as_view(),name='returnorder'),
    path('addreturn/',AddReturnView.as_view(),name='addreturn'),
    path('message/',MessageView.as_view(),name='message'),
]
