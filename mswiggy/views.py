from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .models import Restaurant, Customer, Driver, UpdateLocation, Menu
from .search import query_for_driver_search

import json


@csrf_exempt
def restaurant_add(request):
	response_data = {}
	if request.method == "POST":
		data = json.loads(request.body.decode('utf-8'))
		print('data = ', data)
		if Restaurant.objects.filter(email=data['email']).exists():
			return JsonResponse('Email already exists', safe=False)
		restaurant = Restaurant(**data)
		restaurant.save()
		r_object = Restaurant.objects.filter(id=restaurant.id).values('r_name', 'lat', 'lon')
		try:
			response_data['obj'] = list(r_object)
		except Exception:
			response_data['error'] = "Invalid request"

	return JsonResponse(response_data)


@csrf_exempt
def restaurant_update(request):
	if request.method == "POST":
		data = json.loads(request.body.decode('utf-8'))
		if Restaurant.objects.filter(id=data['id']).exists():
			r = Restaurant.objects.get(id=data['id'])
			r.r_name = data['r_name']
			r.pin = data['pin']
			r.address = data['address']
			r.lon = data['lon']
			r.lat = data['lat']
			r.save()
			response = Restaurant.objects.filter(id=r.id).values('r_name', 'lat', 'lon')
			return JsonResponse({'new_restaurant':list(response)})
		return JsonResponse('Restaurant Does Not Exist', safe=False)
	return JsonResponse('Invalid Request', safe=False)


@csrf_exempt
def restaurant_delete(request):
	if request.method == "POST":
		data = json.loads(request.body.decode('utf-8'))
		if Restaurant.objects.filter(id=data['id']).exists():
			r = Restaurant.objects.get(id=data['id'])
			r.delete()
			return JsonResponse('Restaurant Deleted Successfully', safe=False)
		return JsonResponse('Restaurant Does Not Exist', safe=False)
	return JsonResponse('Invalid Request', safe=False)


@csrf_exempt
def driver_add(request):
	driver_data = {}
	if request.method == "POST":
		data = json.loads(request.body.decode('utf-8'))
		if Driver.objects.filter(mobile=data['mobile']).exists():
			return JsonResponse('Mobile number already exists', safe=False)
		d = Driver(**data)
		d.save()
		driver = Driver.objects.filter(id=d.id).values('name','mobile','lat','lon')
		driver_data['obj'] = list(driver)

	return JsonResponse(driver_data)


@csrf_exempt
def driver_location_update(request):
	if request.method == "POST":
		data = json.loads(request.body.decode('utf-8'))
		if Driver.objects.filter(mobile=data['mobile']).exists():
			driver = Driver.objects.get(mobile=data['mobile'])
			location = UpdateLocation(lat=data['lat'], lon=data['lon'], driver=driver)
			location.add_time = timezone.now()
			location.save()
			location_object = UpdateLocation.objects.filter(id=location.id).values('lat', 'lon')
			return JsonResponse({'location':list(location_object)})
		else:
			return JsonResponse('invalid mobile number or location data', safe=False)
	return JsonResponse('invalid data', safe=False)


@csrf_exempt
def create_menu(request):
	if request.method == "POST":
		data = json.loads(request.body.decode('utf-8'))
		rest = Restaurant.objects.get(id=data['restaurant'])
		menu = Menu(item=data['item'], price=data['price'], restaurant=rest)
		menu.created_on = timezone.now()
		menu.updated_on = timezone.now()
		menu.save()
		return JsonResponse('menu created successfully', safe=False)


@csrf_exempt
def order_place(request):
	if request.method == "POST":
		data = json.loads(request.body.decode('utf-8'))
		menu = Menu.objects.get(menu=data['menu'])
		restaurant = menu.restaurant
		lat1, lon1 = restaurant.lat, restaurant.lon
		drivers_list = query_for_driver_search(lat1, lon1)
		return JsonResponse({'drivers':drivers_list})
	return JsonResponse('Invalid request')