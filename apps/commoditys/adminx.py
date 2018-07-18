import xadmin

from .models import CatagoryF, CatagoryS, CatagoryT, Commodity


class CatagoryFAdmin(object):
    list_display = ['name', 'add_time']  # 展示的内容
    search_fields = ['name']  # 搜索时按以上字段搜索
    list_filter = ['name', 'add_time']  # 筛选器内容


class CatagorySAdmin(object):
    list_display = ['name', 'add_time', 'cata_up']  # 展示的内容
    search_fields = ['name']  # 搜索时按以上字段搜索
    list_filter = ['name', 'cata_up__name']  # 筛选器内容


class CatagoryTAdmin(object):
    list_display = ['name', 'add_time', 'cata_up']  # 展示的内容
    search_fields = ['name']  # 搜索时按以上字段搜索
    list_filter = ['name', 'cata_up__name']  # 筛选器内容


class CommodityAdmin(object):
    list_display = ['name', 'price', 'author','stock','is_sale']  # 展示的内容
    search_fields = ['name','author','publisher']  # 搜索时按以上字段搜索
    list_filter = ['name', 'catagory__name','add_time']  # 筛选器内容
    list_editable = ['stock', 'is_sale','price']


xadmin.site.register(CatagoryF, CatagoryFAdmin)
xadmin.site.register(CatagoryS, CatagorySAdmin)
xadmin.site.register(CatagoryT, CatagoryTAdmin)
xadmin.site.register(Commodity, CommodityAdmin)


