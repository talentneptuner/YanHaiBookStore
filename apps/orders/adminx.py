import xadmin

from xadmin import views

from .models import Order, DeliveryOrder, Logistics, ReturnOrder
from opreation.models import UserMessage


class OrderAdmin(object):
    list_display = ['id', 'user', 'status', 'add_time']  # 展示的内容
    search_fields = ['user', 'status']  # 搜索时按以上字段搜索
    list_filter = ['status', 'add_time', 'total_price']  # 筛选器内容
    readonly_fields = ['id', 'user', 'status', 'total_price', 'add_time']
    ordering = ['-add_time']  # 排序


class DeliveryOrderAdmin(object):
    list_display = ['id', 'order', 'status', 'commodity']  # 展示的内容
    search_fields = ['status', 'commodity__name']  # 搜索时按以上字段搜索
    list_filter = ['status', 'add_time', 'order__status']  # 筛选器内容
    readonly_fields = ['id', 'order', 'commodity', 'address', 'nums', 'add_time', 'status']  # 只读
    ordering = ['-add_time']  # 排序


class LogisticsAdmin(object):
    list_display = ['id', 'Company', 'reciever', 'track_nums', 'delivery']  # 展示的内容
    search_fields = ['Company', 'reciever', 'id']  # 搜索时按以上字段搜索
    list_filter = ['Company', 'add_time']  # 筛选器内容
    readonly_fields = ['id']  # 只读
    ordering = ['-add_time']  # 排序


    def save_models(self):
        obj = self.new_obj
        obj.id = str(obj.delivery.id).replace('C', 'L')
        f = obj.delivery.is_out()
        if not obj.delivery.is_out():
            obj.delivery.status = 'ed'
            obj.delivery.save()
            obj.save()
            user_message = UserMessage()
            user_message.user = obj.delivery.order.user
            user_message.content = '您的货物' + str(obj.delivery.id)+','+str(obj.delivery.commodity.name) + '已出货'
            user_message.save()


class ReturnOrderAdmin(object):
    list_display = ['id', 'type', 'status','delivery','desc']  # 展示的内容
    search_fields = ['type', 'status', 'id']  # 搜索时按以上字段搜索
    list_filter = ['status', 'add_time']  # 筛选器内容
    readonly_fields = ['id','type','reason','tracking','delivery']  # 只读
    ordering = ['-add_time']  # 排序
    exclude = ['finish']
    list_editable = ['status', 're_status']

    def save_models(self):
        obj = self.new_obj
        if not obj.finish:
            if obj.status == 'reject':
                obj.finish = True
            if obj.status == 'accept' and obj.type == 'mc' and obj.re_status == 'ed':
                obj.delivery.order.user.wallet = obj.delivery.order.user.wallet + obj.delivery.get_totalprice()
                obj.delivery.order.user.save()
                obj.finish = True
            if obj.status == 'accept' and obj.type == 'm':
                obj.delivery.order.user.wallet = obj.delivery.order.user.wallet + obj.delivery.get_totalprice()
                obj.delivery.order.user.save()
                obj.finish = True
        obj.save()



xadmin.site.register(Order, OrderAdmin)
xadmin.site.register(DeliveryOrder, DeliveryOrderAdmin)

xadmin.site.register(Logistics, LogisticsAdmin)
xadmin.site.register(ReturnOrder, ReturnOrderAdmin)


class GlobalSettings(object):
    # 修改title
    site_title = '烟海书店后台管理'
    # 修改footer
    site_footer = 'YanHaiBookStore'
    # 收起菜单
    menu_style = 'accordion'


xadmin.site.register(views.CommAdminView, GlobalSettings)
