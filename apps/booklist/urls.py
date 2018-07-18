from django.urls import path

from .views import EditBookListView,MyBookListView,DelBookListView,AddBookView,SearchBookListView,BookListDetailView
from .views import DeleteDetailView,AddFavView,MyFavView,ToCartView

app_name = 'booklist'
urlpatterns = [
    path('mybooklist/',MyBookListView.as_view(),name='mybooklist'),
    path('delbooklist/<int:booklist_id>/',DelBookListView.as_view(),name='delbooklist'),
    path('editbooklist/<int:booklist_id>/', EditBookListView.as_view(), name='editbooklist'),
    path('addbook/',AddBookView.as_view(),name='addbook'),
    path('search/',SearchBookListView.as_view(),name='search'),
    path('detail/<int:booklist_id>/',BookListDetailView.as_view(),name='detail'),
    path('deldetail/<int:detail_id>/',DeleteDetailView.as_view(),name='deltail'),
    path('addfav/',AddFavView.as_view(),name='add_fav'),
    path('myfav/',MyFavView.as_view(),name='myfav'),
    path('tocart/',ToCartView.as_view(),name='tocart'),

]
