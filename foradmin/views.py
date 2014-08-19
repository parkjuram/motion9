from django.shortcuts import render

def manage_shipping_view(request):
    return render(request, 'manage_shipping.html', {} )