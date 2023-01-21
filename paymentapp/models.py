from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Checkout(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length = 150)
    phone  = models.CharField(max_length = 11)
    email = models.EmailField()
    full_addres = models.TextField()
    order_summary  = models.TextField(blank=True, null=True)
    
    
    
    def __str__(self):
        return self.user.username


class BkashPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentID  = models.CharField(max_length = 150)
    createTime = models.CharField(max_length=150)
    orgName  = models.CharField(max_length = 150)
    transactionStatus  = models.CharField(max_length = 150)
    amount = models.CharField(max_length = 150)
    currency = models.CharField(max_length = 150)
    intent = models.CharField(max_length = 150)
    merchantInvoiceNumber = models.CharField(max_length = 150)
    
    class Meta:
        verbose_name = 'BkashPayment'
        verbose_name_plural = 'BkashPayments'

    def __str__(self):
        return self.paymentID


class BkashPaymentExecute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    paymentID  = models.CharField(max_length = 150)
    createTime  = models.CharField(max_length = 150)
    updateTime  = models.CharField(max_length = 150)
    trxID  = models.CharField(max_length = 150)
    transactionStatus  = models.CharField(max_length = 150)
    amount  = models.CharField(max_length = 150)
    currency  = models.CharField(max_length = 150)
    intent  = models.CharField(max_length = 150)
    merchantInvoiceNumber  = models.CharField(max_length = 150)
    customerMsisdn  = models.CharField(max_length = 150)
    

    class Meta:
        verbose_name_plural = 'BkashPaymentExecute'

    def __str__(self):
        return  self.paymentID
    