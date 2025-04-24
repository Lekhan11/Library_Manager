from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
path('', LoginPage, name='login'),
path('home/', HomePage, name='home'),
path('issue_books/', IssueBooks, name='issue_books'),
path('update/', updateUser, name='update'),
path('add_book/', addBook, name='add_book'),
path('add_users/', addusers, name='add_users'),
path('logout/', Logout, name='logout'),
path('view_users/', viewUsers, name='view_users'),
path('view_users/update/<str:role>/<int:id>/', updateUser, name='update_user'),
path('view_users/delete/<str:role>/<int:id>/', deleteUser, name='delete_user'),
path('view_users/search', searchUser, name='search_user'),
path('return_book/', returnBook,name='return_book'),
path('view_books/', viewBooks, name='view_books'),
path('view_books/delete/<int:id>/', deleteBook, name='delete_book'),
path('view_books/update/<int:id>/', updateBook, name='update_book'),
path('view_books/search', searchBook, name='search_book'),
path('bulkadd',bulkAdd, name='bulk_add'),
path('bulkaddbooks',bulkAddBooks, name='bulkadd_books'),
path('settings',settings_view,name='settings'),
path('get-book-details/', get_book_details, name='get_book_details'),
path('get-user-role-due/',  get_user_role_due, name='get_user_role_due'),
path('fine/', fine , name='fine'),
path('get-user-fine/', get_user_fine, name='get_user_fine'),
path('pay-user-fine/', pay_user_fine, name='pay_user_fine'),
path('report/', report, name='report'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
