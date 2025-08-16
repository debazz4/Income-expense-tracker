from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Expenses, Category
from django.contrib import messages


# Create your views here.


@login_required(login_url='/auth/login')
def index(request):
    expenses = Expenses.objects.filter(owner=request.user)
    context = {
        'expenses': expenses,
    }
    return render(request, 'expenses/index.html', context)


def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST,
    }
    if request.method == "GET":
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Enter amount')
            return render(request, 'expenses/add_expense.html', context)
        
        description = request.POST['description']
        if not description:
            messages.error(request, 'Description required')
            return render(request, 'expenses/add_expense.html', context)
        
        category = request.POST['category']
        date = request.POST['expense_date']

        Expenses.objects.create(owner=request.user, amount=amount, description=description,category=category,
                                date=date)
        messages.success(request, 'Expense saved!')
        
    return redirect('expenses')

def expense_edit(request, id):
    expense = Expenses.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories,
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit_expense.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Enter amount')
            return render(request, 'expenses/edit_expense.html', context)
        
        description = request.POST['description']
        if not description:
            messages.error(request, 'Description required')
            return render(request, 'expenses/edit_expense.html', context)
        
        category = request.POST['category']
        date = request.POST['expense_date']

        expense.owner=request.user 
        expense.amount=amount
        expense.description=description
        expense.category=category
        expense.date=date
        expense.save()

        messages.success(request, 'Expense Updated!')
        return redirect('expenses')
    
def expense_delete(request, id):
    expense = Expenses.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')
    return redirect('expenses')
