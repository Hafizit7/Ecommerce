from django.shortcuts import render, redirect
from django.views import View
from .forms import *
from django.core.exceptions import ObjectDoesNotExist
from store_app.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
# Create your views here.

class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        form = CheckoutForm()
        payment_form = PaymentMethodForm()
        order = Order.objects.get(user=request.user, ordered=False)
        context ={
            'form':form,
            'payment_form':payment_form,
            'order':order
        }
        return render(request, 'paymentapp/checkout.html',context)
    
    def post(self, request, *args, **kwargs):
        form = CheckoutForm(request.POST)
        payment_obj = Order.objects.filter(user=request.user, ordered=False)[0]
        payment_form = PaymentMethodForm(instance=payment_obj)
        
        if request.method == 'post' or request.method == 'POST':
            form = CheckoutForm(request.POST)
            pay_form = PaymentMethodForm(request.POST, instance=payment_obj)
            if form.is_valid() and pay_form.is_valid():
                name =form.cleaned_data.get('name')
                phone =form.cleaned_data.get('phone')
                email =form.cleaned_data.get('email')
                full_addres =form.cleaned_data.get('full_addres')
                order_summary =form.cleaned_data.get('order_summary')

                address  = Checkout(
                    user=request.user,
                    name=name,
                    phone=phone,
                    email=email,
                    full_addres=full_addres,
                    order_summary=order_summary
                )
                address.save()
                payment_obj.shipping_address = address
                pay_method = pay_form.save()



                if pay_method.payment_option == 'Cash on Delivery':
                    order_qs = Order.objects.filter(user=request.user, ordered=False)
                    order = order_qs[0]
                    order.ordered = True
                    order.payment_option = pay_method.payment_option
                    

                    order_items = CartProduct.objects.filter(user=request.user, ordered=False)
                    for order_item in order_items:
                        order_item.ordered = True
                        order_item.save()

                    order.save()
                    messages.success(request, "You order was successful")
                    return redirect('/')
                else:
                    return redirect('checkout')
            else:
                return redirect('checkout')



import requests
import json

app_key = "5nej5keguopj928ekcj3dne8p"
app_secret = "1honf6u1c56mqcivtc9ffl960slp4v2756jle5925nbooa46ch62"

def grant_token_function():
    token_url = "https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/token/grant"

    payload = {
    "app_key":f"{app_key}",
    "app_secret":f"{app_secret}"
    }

    headers = {
        "Content-Type":"application/json",
        "Accept":"application/json",
        "username":"testdemo",
        "password":"test%#de23@msdao"
    }

    token_response = requests.post(token_url, json=payload, headers=headers)
    token =json.loads(token_response.content)
   # print(token)
    id_tokens = token.get('id_token')
    return id_tokens

id_token = grant_token_function()
# print(id_token)



@login_required
@csrf_exempt
def create_bkash_payment(request, *args, **kwargs):
    id_token = grant_token_function()
    create_url = "https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/create"
    order = Order.objects.get(user=request.user, ordered=False)

    payload = json.dumps({
        "amount":f"{order.get_total()}",
        "currency": "BDT",
        "intent": "sale",
        "merchantInvoiceNumber":f"{order.id}",
    })

    headers = {
        "Accept": "application/json",
        "Authorization": f"{id_token}",
        "X-APP-Key":f"{app_key}",
        "Content-type": "application/json"
    }

    create_response = requests.post(create_url, data=payload, headers=headers)

    response =json.loads(create_response.content)
    # print(response)
    # id_tokens = token.get('id_token')
    # print(create_response.text)
    # return render(request, 'bkash-payment1.html',{'response':response})
    
    PaymentId=response['paymentID'] 
    createTime=response['createTime']
    orgName = response['orgName']
    transactionStatus = response['transactionStatus']
    amount = response['amount']
    currency = response['currency']
    intent = response['intent']
    merchantInvoiceNumber = response['merchantInvoiceNumber']
    
    BkashPayment.objects.create(user=request.user,paymentID =  PaymentId, createTime=createTime,orgName=orgName,  transactionStatus =  transactionStatus , amount=amount, currency= currency,  intent= intent,merchantInvoiceNumber=merchantInvoiceNumber )
    
    return JsonResponse(response)


@login_required
@csrf_exempt
def execute_bkash_payment(request):
    id_token = grant_token_function()
    length = BkashPayment.objects.filter(user=1).count()
    Id = BkashPayment.objects.filter(user=1)[length-1].paymentID    
    url = f"https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/execute/{Id}"

    headers = {
        "accept": "application/json",
        "Authorization": f"{id_token}",
        "X-APP-Key": "5nej5keguopj928ekcj3dne8p"
    }

    response_create = requests.post(url, headers=headers)

    response=json.loads(response_create.content)

    # if(array_key_exists("errorCode",$arr) && $arr['errorCode'] != '0000'){
    #     Session::put('errorMessage', $arr['errorMessage']);

    if response.get('errorCode') and response.get('errorCode') != '0000':
        text = response.get('errorMessage')
        messages.error(request, f"{text}")    
    else:
        paymentID=response.get('paymentID') 
        createTime=response.get('createTime')
        updateTime = response.get('updateTime')
        trxID = response.get('trxID')
        transactionStatus = response.get('transactionStatus')
        amount = response.get('amount')
        currency = response.get('currency')
        intent = response.get('intent')
        merchantInvoiceNumber = response.get('merchantInvoiceNumber')
        customerMsisdn = response.get('customerMsisdn')
        BkashPaymentExecute.objects.create(user=request.user,paymentID = paymentID, createTime=createTime,updateTime=updateTime,trxID=trxID, transactionStatus =  transactionStatus , amount=amount, currency= currency,  intent= intent,merchantInvoiceNumber=merchantInvoiceNumber, customerMsisdn=customerMsisdn )
        
        print(Id)

        order_qs = Order.objects.filter(user=request.user, ordered=False)
        order = order_qs[0]
        order.ordered = True
        order.orderId = order.id
        order.payment_option = 'Bkash'

        order_items = CartProduct.objects.filter(user=request.user, ordered=False)
        for order_item in order_items:
            order_item.ordered = True
            order_item.save()

        order.save()
        
        messages.success(request, "Your Payment successful done")

    return JsonResponse(response)












    