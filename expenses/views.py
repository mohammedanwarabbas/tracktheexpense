from django.http.response import HttpResponse
from django.shortcuts import render, redirect
#to allow only logged in users
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator

# Create your views here.
@login_required(login_url='/authentication/login/')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses,2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    context ={'expenses':expenses, 'page_obj':page_obj}
    return render(request, 'expenses/index.html',context)

@login_required(login_url='/authentication/login/')
def add_expense(request):
    categories = Category.objects.all()
    context ={'categories':categories, 'values':request.POST,}
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method=='POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount can\'t be blank')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, 'Description can\'t be blank')
            return render(request, 'expenses/add_expense.html', context)
        category = request.POST['category']
        # owner = 
        date = request.POST['expense_date']
        Expense.objects.create(amount=amount, date=date, description=description, owner=request.user, category=category)
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')

def expense_edit(request, id):
    expense = Expense.objects.get(id=id, owner=request.user)
    categories = Category.objects.all()
    context={'expense':expense, 'categories':categories}
    if request.method=='GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method=='POST':
        amount = request.POST['amount']
        if not amount:
            messages.error(request, 'Amount can\'t be blank')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        if not description:
            messages.error(request, 'Description can\'t be blank')
            return render(request, 'expenses/edit-expense.html', context)
        category = request.POST['category']
        date = request.POST['expense_date']
        expense.amount=amount
        expense.date=date
        expense.description=description
        expense.category=category
        expense.save()
        messages.success(request, 'Expense edited successfully')
        return redirect('expenses')

def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')




