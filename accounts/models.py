from django.db import models
from django.contrib.auth.models import User


# Create your models here.

gender = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
)

states = (
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Assam','Assam'),
    ('Bihar','Bihar'),
    ('Chhattisgarh','Chattisgarh'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jharkhand','Jharkhand'),
    ('Karnataka','Karnataka'),
    ('Kerala','Kerala'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Maharashtra','Maharashtra'),
    ('Manipur','Manipur'),
    ('Meghalaya','Meghalaya'),
    ('Mizoram','Mizoram'),
    ('Nagaland','Nagaland'),
    ('Odisha','Odisha'),
    ('Rajasthan','Rajasthan'),
    ('Sikkim','Sikkim'),
    ('Tamil Nadu','Tamil Nadu'),
    ('Telangana','Telangana'),
    ('Tripura','Tripura'),
    ('Uttar Pradesh','Uttar Pradesh'),
    ('Uttarakhand','Uttarakhand'),
    ('West Bengal','West Bengal')
    )


user_type=(
    ('admin','admin'),
    ('service_provider','service_provider'),
    ('public','public'),
)

approval_choices=(
    ('2','Pending'),
    ('1','Approved'),
    ('3','Rejected')
)

class Users(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=200,null=True, blank=True)
    organization = models.CharField(max_length=250,null=True, blank=True)
    mob = models.CharField(max_length=12)
    sex = models.CharField(max_length=10,choices=gender,default='Male')
    house = models.CharField(max_length=100,null=True, blank=True)
    street1 =models.CharField(max_length=100,null=True, blank=True)
    street2 =models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    district = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True,choices=states, blank=True)
    pin = models.CharField(max_length=100,null=True,blank=True)
    age = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=20,choices=user_type)
    approval = models.CharField(max_length=20,choices=approval_choices,default='Pending')
    document = models.FileField(upload_to='documents',null=True, blank=True)

    def __str__(self):
        return self.name

class Service(models.Model):
    category = models.CharField(max_length=250)
    providers = models.IntegerField(null=True, blank=True)
    users = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.category


