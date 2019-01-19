from django.shortcuts import render


def agreements(request):
   return render(request, 'agreements/admin.html', locals())
