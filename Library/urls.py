from django.urls import path
from .views import *

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
path('return/', returnBook,name='return'),
]