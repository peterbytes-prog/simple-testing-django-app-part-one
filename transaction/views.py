from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm


def index(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TransactionForm()
    return render(request, 'transaction/index.html', {'form': form})
