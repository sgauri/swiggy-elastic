from django.db import models
from .search import UpdateLocationIndex


class TimeStamp(models.Model):
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Menu(TimeStamp):
	item = models.CharField(max_length=80)
	price = models.PositiveIntegerField()
	restaurant = models.ForeignKey('Restaurant', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return "{}-{}-{}".format(self.restaurant, self.item, self.price)


class Restaurant(TimeStamp):
	r_name = models.CharField(max_length=100)
	email = models.EmailField()
	address = models.TextField()
	pin = models.CharField(max_length=6)
	gstn = models.CharField(max_length=40)
	lon = models.DecimalField(max_digits=9, decimal_places=6)
	lat = models.DecimalField(max_digits=9, decimal_places=6)

	def __str__(self):
		return self.r_name


class Driver(TimeStamp):
	name = models.CharField(max_length=60)
	address = models.TextField()
	mobile = models.CharField(max_length=10)
	lon = models.DecimalField(max_digits=9, decimal_places=6)
	lat = models.DecimalField(max_digits=9, decimal_places=6)

	def __str__(self):
		return self.name


class Customer(TimeStamp):
	name = models.CharField(max_length=100)
	address = models.TextField()
	pin = models.CharField(max_length=6)
	email = models.EmailField()
	mobile = models.CharField(max_length=10)

	def __str__(self):
		return self.name


class UpdateLocation(models.Model):
	driver = models.ForeignKey('Driver', on_delete=models.SET_NULL, null=True, blank=True)
	lat = models.DecimalField(max_digits=9, decimal_places=6)
	lon = models.DecimalField(max_digits=9, decimal_places=6)
	add_time = models.DateTimeField()

	def __str__(self):
		return "{}-{}-{}".format(self.driver, self.lat, self.lon)

	def indexing(self):
		obj = UpdateLocationIndex(
			meta={'id':self.id},
			driver_id = self.driver.id,
			driver=self.driver.name,
			add_time=self.add_time,
			pin = {'lat':self.lat,'lon':self.lon,}

		)
		obj.save(index='geo')
		return obj.to_dict(include_meta=True)