from django.shortcuts import render
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

# Create your views here.
from .models import BookList, BookListDetail, UserFav
from .forms import BookListForm
from commoditys.models import Commodity
from opreation.models import ShopCartRecord



class MyBookListView(View):
    """我的书单功能"""

    def get(self, request):
        booklists = BookList.objects.filter(user=request.user)
        booklists = booklists.order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(booklists, 12, request=request)

        booklists = p.page(page)

        return render(request, 'usercenter-booklist-my.html', dict(booklists=booklists))


class DelBookListView(View):

    def get(self, request, booklist_id):
        booklist = BookList.objects.get(id=booklist_id)
        booklist.delete()
        from django.urls import reverse
        return HttpResponseRedirect(reverse('booklist:mybooklist'))


class EditBookListView(View):
    """书单添加修改操作"""

    def get(self, request, booklist_id):
        if booklist_id == 0:
            return render(request, 'usercenter-booklist-new.html', dict(booklist_id=booklist_id))
        else:
            booklist = BookList.objects.get(id=booklist_id)
            return render(request, 'usercenter-booklist-new.html', dict(booklist=booklist, booklist_id=booklist_id))

    def post(self, request, booklist_id):
        booklist_form = BookListForm(request.POST, request.FILES)
        if booklist_form.is_valid():
            if booklist_id == 0:
                booklist = BookList()
                booklist.user = request.user
                booklist.cover = request.FILES.get('cover')
                booklist.title = booklist_form.cleaned_data['title']
                booklist.tag1 = booklist_form.cleaned_data['tag1']
                booklist.tag2 = request.POST.get('tag2')
                booklist.desc = request.POST.get('desc')
                if request.POST.get('is_pub'):
                    booklist.is_pub = False
                booklist.save()
                from django.urls import reverse
                return HttpResponseRedirect(reverse('booklist:mybooklist'))
            else:
                booklist = BookList.objects.get(id=booklist_id)
                if request.FILES.get('cover'):
                    booklist.cover = request.FILES.get('cover')
                booklist.title = booklist_form.cleaned_data['title']
                booklist.tag1 = booklist_form.cleaned_data['tag1']
                booklist.tag2 = request.POST.get('tag2')
                booklist.desc = request.POST.get('desc')
                if request.POST.get('is_pub'):
                    booklist.is_pub = False
                booklist.save()
                from django.urls import reverse
                return HttpResponseRedirect(reverse('booklist:mybooklist'))
        else:
            return render(request, 'usercenter-booklist-new.html', dict(msg='缺少信息', booklist_id=booklist_id))


class AddBookView(View):
    """书单添加书籍"""

    def get(self, request):
        booklist_id = request.GET.get('booklist_id')
        commodity_id = request.GET.get('commodity_id')
        booklist = BookList.objects.get(id=booklist_id)
        commodity = Commodity.objects.get(id=commodity_id)
        if BookListDetail.objects.filter(booklist=booklist, commodity=commodity):
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            item = BookListDetail()
            item.commodity = commodity
            item.booklist = booklist
            item.save()
            booklist.set_booknums()
            booklist.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')


class SearchBookListView(View):
    """搜索书单"""

    def get(self, request):
        keyword = request.GET.get('keyword', '')
        sort = request.GET.get('sort', '')
        if keyword:
            booklists = BookList.objects.filter(
                Q(title__icontains=keyword) | Q(tag1__icontains=keyword) | Q(tag2__icontains=keyword) | Q(
                    user__nickname=keyword) & Q(book_nums__gt=0))
        else:
            booklists = BookList.objects.filter(book_nums__gt=0)
        recomend = booklists.order_by('-click_nums')[:5]
        if sort == 'click':
            booklists = booklists.order_by('-click_nums')
        elif sort == 'fav':
            booklists = booklists.order_by('-fav_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(booklists, 12, request=request)

        booklists = p.page(page)
        return render(request, 'booklists.html',
                      dict(keyword=keyword, recomend=recomend, booklists=booklists, sort=sort))


class BookListDetailView(View):
    """书单详情"""

    def get(self, request, booklist_id):
        booklist = BookList.objects.get(id=booklist_id)
        bookdetails = booklist.booklistdetail_set.all()
        recomend = BookList.objects.filter(book_nums__gt=0).order_by('-click_nums')[:5]
        own = 0
        has_fav = 0
        booklist.click_nums = booklist.click_nums + 1
        booklist.save()
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user, booklist=booklist):
                has_fav = 1
            else:
                has_fav = 0
            if booklist.user == request.user:
                own = 1
        return render(request, 'booklistdetail.html',
                      dict(booklist=booklist, bookdetails=bookdetails, own=own, recomend=recomend, has_fav=has_fav))


class DeleteDetailView(View):
    """删除书单项目"""

    def get(self, request, detail_id):
        detail = BookListDetail.objects.get(id=detail_id)
        booklist = detail.booklist
        detail.delete()
        booklist.set_booknums()
        booklist.save()
        from django.urls import reverse
        return HttpResponseRedirect(reverse('booklist:detail', args=(booklist.id,)))


class AddFavView(View):
    """添加收藏"""

    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        if int(fav_id) < 0:
            return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type='application/json')
        booklist = BookList.objects.get(id=fav_id)
        if booklist.user == request.user:
            return HttpResponse('{"status":"fail","msg":"这是你自己的书单"}', content_type='application/json')
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type='application/json')
        if UserFav.objects.filter(user=request.user, booklist=booklist):
            UserFav.objects.filter(user=request.user, booklist=booklist).delete()
            booklist.set_favnums()
            booklist.save()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFav()
            user_fav.booklist = booklist
            user_fav.user = request.user
            user_fav.save()
            booklist.set_favnums()
            booklist.save()
            return HttpResponse('{"status":"success","msg":"已收藏"}', content_type='application/json')


class MyFavView(View):
    """我的收藏"""
    def get(self,request):
        booklists = []
        userfavs = UserFav.objects.filter(user=request.user)
        for userfav in userfavs:
            booklists.append(userfav.booklist)
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(booklists, 12, request=request)

        booklists = p.page(page)
        return render(request,'usercenter-booklist-fav.html',dict(booklists=booklists))

class ToCartView(View):
    """全部加入购物车"""

    def get(self,request):
        booklist_id = request.GET.get('listid')
        booklist = BookList.objects.get(id=booklist_id)
        Details = booklist.booklistdetail_set.all()
        for detail in Details:
            record = ShopCartRecord();
            record.user = request.user
            record.commodity = detail.commodity
            record.nums = 1
            record.save()
        from django.urls import reverse
        return HttpResponseRedirect(reverse('users:cart'))
