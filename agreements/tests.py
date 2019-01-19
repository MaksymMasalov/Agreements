from django.test import TestCase, Client
from django.test.client import RequestFactory
from .models import Agreement, Period, Companie, Countrie
from django.contrib.auth.models import User
from datetime import date
from .calendar.views import calendar


class TestAgreement(TestCase):

   fixtures = ['agreements/fixtures/db.json']

   def setUp(self):
      self.factory = RequestFactory()

   def test_on_crossing_periods(self):
      first_period = Period.objects.create(agreement=Agreement.objects.get(
         pk=10), start_date=date(2018, 12, 25), end_date=date(2018, 12, 30))
      second_cross_first = Period.objects.create(
         agreement=Agreement.objects.get(pk=10), start_date=date(2018, 12, 26),
         end_date=date(2018, 12, 31))
      first_period.save()
      second_cross_first.save()
      print('ID first period '+str(first_period.id))
      print('second period didnt create')
      self.assertIs(second_cross_first.id, None)

   def test_on_get_request(self):
      client = Client()
      request = self.factory.get(
         '/agreements/calendar/?country=1&negotiator=1&company=1')
      request2 = self.factory.get(
         '/agreements/calendar/?negotiator=1,2&company=1&country=1,2')
      request3 = self.factory.get(
         '/agreements/calendar/?negotiator=1,2&company=2,1&country=1,2')
      response = calendar(request)
      response2 = calendar(request2)
      response3 = calendar(request3)
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response2.status_code, 200)
      self.assertEqual(response3.status_code, 200)
