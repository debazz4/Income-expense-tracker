from django.contrib import admin
from .models import Expenses, Category
# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('amount', 'description', 'category', 'date', 'owner')
    list_filter = ('category', 'date', 'owner')
    search_fields = ('description', 'category')
    ordering = ('-date',)

    list_per_page = 2

class CategoryAdmin(admin.ModelAdmin):    
    list_display = ('name', 'owner')
    search_fields = ('name', 'owner__username')
    ordering = ('name',)
admin.site.register(Expenses, ExpenseAdmin)
admin.site.register(Category)