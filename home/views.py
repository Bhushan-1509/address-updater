from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Address
import re
# Create your views here
def index(request):
    if request.method == 'GET' and request.GET.get('search'):
        keyword = request.GET.get('search')
        records_1 = Address.objects.filter(reference_name__icontains=keyword)
        records_2 = Address.objects.filter(reference_name__contains=keyword)
        if records_1 or records_2:
            if records_1:
                return render(request, "index.html", context={'records': records_1})
            else:
                return render(request, "index.html", context={'records': records_2})
    if request.method == 'GET':
        addresses = Address.objects.all()
        return render(request, "index.html", context={'records': addresses})

    elif request.method == 'POST':
        reference_name = request.POST.get('referenceName')
        street_address = request.POST.get('streetAddress')
        apartment = request.POST.get('aptNumber')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postalCode')
        country = "India"
        if bool(re.match(r'^\d{6}$', postal_code)) is False and postal_code != "":
            addresses = Address.objects.all()
            return render(request, "index.html", context={'success': False, 'submission': False, 'msg': 'Pincode is incorrect !', 'records': addresses})

        if (reference_name != "" and street_address != "" and apartment != "" and city != "" and state != "0" and postal_code != "" and country != "") is False :
            addresses = Address.objects.all()
            return render(request, "index.html", context={'success': False, 'submission': False, 'msg': 'Please fill out all fields !', 'records': addresses})
        else:
            new_address = Address(reference_name=reference_name, street_address=street_address, apartment=apartment, city=city, state=state, postal_code=postal_code, country=country)
            existing_records = Address.objects.filter(reference_name__icontains=reference_name)
            if existing_records:
                addresses = Address.objects.all()
                return render(request, "index.html", context={'success': True, 'submission': True, 'msg': 'Already exists !', 'conflict': True,'records': addresses})
            result = new_address.save()
            addresses = Address.objects.all()
            return render(request, "index.html", context={'success': True, 'submission': True, 'msg': '', 'records': addresses})



def delete_address(request):
    if request.method == 'POST':
        reference_name = request.POST.get('hidden-ref-name')
        record = Address.objects.filter(reference_name__icontains=reference_name)
        if record:
            record.delete()
            return render(request, "delete.html")
        else:
            return render(request, "index.html", {"success":True, "submission":False, 'msg': 'Not able to delete address !', 'delete': 'NA'})

def update_address(request):
    if request.method == 'POST':
        reference_name = request.POST.get('hiddenRefName')
        street_address = request.POST.get('streetAddress')
        apartment = request.POST.get('aptNumber')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postalCode')
        print(request.POST)
        record = Address.objects.get(reference_name__icontains=reference_name)
        record.street_address = street_address
        record.apartment = apartment
        record.city = city
        record.state = state
        record.postal_code = postal_code
        record.country = "India"
        record.save()
        return render(request, "update.html")
