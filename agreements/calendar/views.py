from ..models import *
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Max


@api_view()
def calendar(request):
   result = {}
   country = [int(x) for x in request.GET.get('country').split(',')] \
       if request.GET.get('country') \
       else Countrie.objects.values_list('id', flat=True)

   negotiator = [int(x) for x in request.GET.get('negotiator').split(',')] \
       if request.GET.get('negotiator') \
       else User.objects.values_list('id', flat=True)

   company = [int(x) for x in request.GET.get('company').split(',')] \
       if request.GET.get('company') \
       else Companie.objects.values_list('id', flat=True)

   dates = Period.objects.filter(agreement__in=Agreement.objects.filter(
      company__in=Companie.objects.filter(
          country__in=Countrie.objects.filter(id__in=country)).filter(
          id__in=company)).filter(negotiator_id__in=negotiator)).values(
       'agreement_id').annotate(max_update_time=Max('end_date'))

   for period_max_date in dates:
      date = period_max_date['max_update_time']
      if date.year not in result:
         year = [0] * 12
         year[date.month - 1] += 1
         result = {date.year: year}
      else:
         year = result[date.year]
         year[date.month - 1] += 1
   return Response(result)
