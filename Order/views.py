# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http.response import HttpResponse
from django.shortcuts import render
import json

# Create your views here.

def home(request):
    return HttpResponse('<div><center><h1>Delivery Cost Calculator</h1></center></div>')


def calculate_amount(request):
    if request.method == 'POST':
        payload = json.loads(request.body)
        order_items = payload['order_items']
        if len(order_items) == 0:
            return HttpResponse("Incorrect data", status=400)
        total = 0
        for i in order_items:
            total += i['quantity'] * i['price']
        distance = payload['distance'] / 1000
        delivery_cost = get_delivery_cost_of_item(distance)
        if 'offer' in payload and bool(payload['offer']):
            offer = payload['offer']
            if checkMin(offer['offer_val'], total) and offer['offer_type'] != 'DELIVERY':
                total += delivery_cost
                total -= offer['offer_val']
        else:
            total += delivery_cost
        response = {'order_total': total}
        return HttpResponse(str(response))
    else:
        print("Not a POST call")
        
        
def get_delivery_cost_of_item(distance):
    f = open('Config/delivery_cost.json', 'r')
    delivery_cost = json.load(f)
    for i in delivery_cost:
        if 'max' in i and i['max'] == True and distance >= i['from']:
            return i['price']
        elif distance >= i['from'] and distance < i['to']:
            return i['price']


def checkMin(offer, total):
    if total >= offer: return True
    return False