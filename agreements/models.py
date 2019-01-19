from django.db import models
from django.contrib.auth.models import User


class Countrie(models.Model):
   code = models.CharField(max_length=3)
   name = models.CharField(max_length=50)

   def __str__(self):
      return '%s' % self.name


class Companie(models.Model):
   name = models.CharField(max_length=50)
   country = models.ForeignKey(Countrie, on_delete=models.CASCADE)

   def __str__(self):
      return '%s %s' % (self.name, self.country)


class Agreement(models.Model):
   start_date = models.DateField()
   end_date = models.DateField()
   credit = models.DecimalField(max_digits=19, decimal_places=2)
   debit = models.DecimalField(max_digits=19, decimal_places=2)
   company = models.ForeignKey(Companie, on_delete=models.PROTECT)
   negotiator = models.ForeignKey(User, on_delete=models.PROTECT)

   def __str__(self):
      return '%s' % self.company


class Period(models.Model):
   agreement = models.ForeignKey(Agreement, on_delete=models.CASCADE)
   loan_status = (
      ('New', 'New'),
      ('Active', 'Active'),
      ('Reconciliation', 'Reconciliation'),
      ('Closed', 'Closed')
   )
   status = models.CharField(max_length=14, choices=loan_status,
                             help_text='Period state')
   start_date = models.DateField()
   end_date = models.DateField()

   def save(self, *args, **kwargs):
      agreement = self.agreement

      # entry check
      if agreement.start_date > self.start_date or \
              agreement.end_date < self.end_date:
         raise ValueError('The period is not included in the agreement.')

      periods = Period.objects.filter(agreement=agreement).exclude(
          end_date__lt=self.start_date).exclude(
         start_date__gt=self.end_date)

      # crossing check
      if (periods):
         raise ValueError('Period should not overlap.')
      super(Period, self).save(*args, **kwargs)
