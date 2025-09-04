from django.shortcuts import render, redirect
from .models import Source, UserIncome
from django.core.paginator import Paginator
from userpreferences.models import UserPreferences
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse

# Create your views here.


def search_income(request):
    if request.method == 'POST':
        search_str = json.loads(request.body).get('searchText')
        income = UserIncome.objects.filter(
                amount__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
                date__istartswith=search_str, owner=request.user) | UserIncome.objects.filter(
                description__icontains=search_str, owner=request.user) | UserIncome.objects.filter(
                source__icontains=search_str, owner=request.user)
        data = income.values()
        return JsonResponse(list(data), safe=False)
    
@login_required(login_url='/auth/login')
def index(request):
    income = UserIncome.objects.filter(owner=request.user)
    sources = Source.objects.all()
    currency = UserPreferences.objects.get(user=request.user).currency
    if not currency:
        currency = "USD"
    paginator = Paginator(income, 10)
    page_number = request.GET.get('page')
    page_obj =  Paginator.get_page(paginator, page_number)
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
        'source': sources,
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

def income_edit(request, id):
    income = UserIncome.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'values': income,
        'sources': sources,
    }
    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Enter amount')
            return render(request, 'income/edit_income.html', context)
        
        description = request.POST['description']
        if not description:
            messages.error(request, 'Description required')
            return render(request, 'income/edit_income.html', context)
        
        source = request.POST['source']
        date = request.POST['income_date']

        income.owner=request.user 
        income.amount=amount
        income.description=description
        income.source=source
        income.date=date
        income.save()

        messages.success(request, 'Income Updated!')
        return redirect('income')
    
def income_delete(request, id):
    income = UserIncome.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income deleted successfully!')
    return redirect('income')
