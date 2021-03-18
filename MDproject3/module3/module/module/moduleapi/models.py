from django.db import models

# Create your models here.
class Md3Stock(models.Model):
    quantity = models.IntegerField(db_column='Quantity')  # Field name made lowercase.
    price = models.FloatField()
    days_range = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    search_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'md3stock'


class MyProjectMd3Stock(models.Model):
    quantity = models.BigIntegerField(db_column='Quantity')  # Field name made lowercase.
    price = models.FloatField()
    days_range = models.TextField()
    title = models.TextField()
    search_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'my_project_md3stock'


class MyProjectStock(models.Model):
    quantity = models.BigIntegerField()
    price = models.FloatField()
    days_range = models.TextField()
    title = models.TextField()
    open_price = models.FloatField()
    ratio = models.TextField()
    search_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'my_project_stock'


class MyProjectWeather(models.Model):
    temper = models.IntegerField()
    humid = models.TextField()
    high_temp = models.IntegerField()
    low_temp = models.IntegerField()
    title = models.TextField()
    wind = models.TextField()
    weather = models.TextField()
    search_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'my_project_weather'

class Savestockprice(models.Model):
    stock_title = models.CharField(max_length=50)
    time_day = models.IntegerField()
    time_hour = models.IntegerField()
    savepath = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'savestockprice'


class Savestockratio(models.Model):
    datacount = models.IntegerField()
    savepath = models.CharField(max_length=100)
    search_key = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'savestockratio'

class Saveweathertemp(models.Model):
    time_day = models.IntegerField()
    time_hour = models.IntegerField()
    savepath = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'saveweathertemp'


class Saveweathertempwithhumid(models.Model):
    title = models.CharField(max_length=50)
    time_day = models.IntegerField()
    time_hour = models.IntegerField()
    savepath = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'saveweathertempwithhumid'
        
class Stock(models.Model):
    quantity = models.IntegerField()
    price = models.FloatField()
    days_range = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    open_price = models.FloatField()
    ratio = models.CharField(max_length=10)
    search_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock'


class Weather(models.Model):
    temper = models.IntegerField()
    humid = models.CharField(max_length=10)
    high_temp = models.IntegerField()
    low_temp = models.IntegerField()
    title = models.CharField(max_length=20)
    wind = models.CharField(max_length=10)
    weather = models.CharField(max_length=20)
    search_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'weather'
