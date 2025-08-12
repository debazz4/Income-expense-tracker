from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Expenses, Category
from django.contrib import messages
# Create your views here.
@login_required(login_url='/auth/login')
def index(request):
    return render(request, 'expenses/index.html')

def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST,
    }

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Enter amount')
            return render(request, 'expenses/add_expense.html', context)
        
        description = request.POST['description']
        category = request.POST['category']
        date = request.POST['date']

        Expenses.objects.create(owner=request.user, amount=amount, description=description,category=-category,
                                date=date)
        messages.success(request, 'Expense saved!')
        
    return render(request, 'expenses/add_expense.html', context)
