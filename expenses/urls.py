from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='expenses'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('edit-expense/<int:id>/',views.expense_edit, name='expense-edit'),
    path('delete-expense/<int:id>/', views.expense_delete, name='expense-delete')
]