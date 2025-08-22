from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/auth/login')
def index(request):
    income = UserIncome.objects.filter(owner=request.user)
    source = Source.objects.all()
    currency = UserPreferences.objects.get(user=request.user).currency
    paginator = Paginator(income, 10)
    page_number = request.GET.get('page')
    page_obj =  Paginator.get_page(paginator, page_number)
    context = {
        'income': income,
        'page_obj': page_obj,
        'currrency': currency,
    }
    return render(request, 'income/index.html', context)

@login_required(login_url='/auth/login')
def add_income(request):
    sources = Source.objects.all()
    context = {
        'sources': sources,
        'values': request.POST,
    }
    if request.method == "GET":
        return render(request, 'income/add_income.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Enter amount')
            return render(request, 'income/add_income.html', context)
        
        description = request.POST['description']
        if not description:
            messages.error(request, 'Description required')
            return render(request, 'income/add_income.html', context)
        
        source = request.POST['source']
        date = request.POST['income_date']

        UserIncome.objects.create(owner=request.user, amount=amount, description=description,source=source,
                                date=date)
        messages.success(request, 'Income added!')
        
    return redirect('income')

# def expense_edit(request, id):
#     expense = Expenses.objects.get(pk=id)
#     categories = Category.objects.all()
#     context = {
#         'expense': expense,
#         'values': expense,
#         'categories': categories,
#     }
#     if request.method == 'GET':
#         return render(request, 'expenses/edit_expense.html', context)
    
#     if request.method == 'POST':
#         amount = request.POST['amount']

#         if not amount:
#             messages.error(request, 'Enter amount')
#             return render(request, 'expenses/edit_expense.html', context)
        
#         description = request.POST['description']
#         if not description:
#             messages.error(request, 'Description required')
#             return render(request, 'expenses/edit_expense.html', context)
        
#         category = request.POST['category']
#         date = request.POST['expense_date']

#         expense.owner=request.user 
#         expense.amount=amount
#         expense.description=description
#         expense.category=category
#         expense.date=date
#         expense.save()

#         messages.success(request, 'Expense Updated!')
#         return redirect('expenses')
    
# def expense_delete(request, id):
#     expense = Expenses.objects.get(pk=id)
#     expense.delete()
#     messages.success(request, 'Expense deleted successfully!')
#     return redirect('expenses')
