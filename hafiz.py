import requests
import json

BKASH_CHECKOUT_APP_KEY = "5nej5keguopj928ekcj3dne8p"
BKASH_CHECKOUT_APP_SECRET = "1honf6u1c56mqcivtc9ffl960slp4v2756jle5925nbooa46ch62"
gtoken_url = 'https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/token/grant'


def grand_token():

    headers={
        'Content-Type':"application/json",
        'Accept':"application/json",
        'username':"testdemo",
        'password':"test%#de23@msdao",
    }
    
    Parameters={
        "app_key":"5nej5keguopj928ekcj3dne8p",
        "app_secret":"1honf6u1c56mqcivtc9ffl960slp4v2756jle5925nbooa46ch62"
    }

    response = requests.post(gtoken_url, json=Parameters, headers=headers)
    r = json.loads(response.content)
    token = r.get('id_token')
    return token

    # print(response.text)
print(grand_token())

def create_pyment():
    url= "https://checkout.sandbox.bka.sh/v1.2.0-beta/checkout/payment/create"

    headers={
        "Content-Type":"application/json",
        "Accept":"application/json",
        "Authorization":"eyJraWQiOiJmalhJQmwxclFUXC9hM215MG9ScXpEdVZZWk5KXC9qRTNJOFBaeGZUY3hlamc9IiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI4ZGU4ZjBlMC1mY2RjLTQyNzMtYjY4YS1iNDAwOWNjZjc3ZDEiLCJhdWQiOiI2NmEwdGZpYTZvc2tkYjRhMDRyY24wNjNhOSIsImV2ZW50X2lkIjoiOTc0N2JhZjUtNmFlMS00N2JlLThlY2UtOTVjMDE5NDZhMzdiIiwidG9rZW5fdXNlIjoiaWQiLCJhdXRoX3RpbWUiOjE2NzIxMTYyMjIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC5hcC1zb3V0aGVhc3QtMS5hbWF6b25hd3MuY29tXC9hcC1zb3V0aGVhc3QtMV9rZjVCU05vUGUiLCJjb2duaXRvOnVzZXJuYW1lIjoidGVzdGRlbW8iLCJleHAiOjE2NzIxMTk4MjIsImlhdCI6MTY3MjExNjIyMn0.eO1FigNVYFU0w3d3WU0v1Ed1r1Xmpe6hhgVW8E_pIU61iQKIrAx0I1CJ2roODvadm8fnKyD84mqrWow62jUomqqUaX4Lsx8ONgp_Lq-7lfFdtK50GaJaEsbJXmq6tpPwg8CcBMqhD7eZdJrfS7bDvOI73GEByFQ9wuYpDF7tjwPSAEGL_DP3dv7Ig1sY48l77dTkgBft7R--8yNOQ7zrefr2WrWQOUtIhYU2l856rGpSNyIiP4-6z6skInT09zE4ooLyYWCEjQGH-iLlUEoi_gmHbUfQmFYZTCfpImRTbdag4-xszivgrt8ZfR10UY52TrWs1PGig93HpNQ5uav4CA",
        "X-App-Key":"5nej5keguopj928ekcj3dne8p",
    }

    parameters = {
        "amount":"002",
        "currency":"BDT",
        "intent":"sale",
        "merchantInvoiceNumber":"hafiz",
    }

    response = requests.post(url, json=parameters, headers=headers)
    print(response.text)
create_pyment()

