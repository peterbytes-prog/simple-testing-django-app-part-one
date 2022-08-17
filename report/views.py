from django.shortcuts import render
from transaction.models import Transaction


def index(request):
    transactions = Transaction.objects.all()
    return render(request, 'report/index.html', {'transactions': transactions})
