from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# Create your models here.


class Customer(models.Model):

    GENDER = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    )
    name = models.CharField(verbose_name="Name", max_length=100, null=True)
    email = models.EmailField(verbose_name="Email", max_length=100)
    password = models.CharField(verbose_name="Password", max_length=100)
    age = models.IntegerField(verbose_name="Age", null=True)
    contact_number = models.CharField(
        verbose_name="Contact Number", max_length=13, null=True)
    address = models.CharField(
        verbose_name="Address", max_length=200, null=True)
    city = models.CharField(verbose_name="City", max_length=50, null=True)
    state = models.CharField(verbose_name="State", max_length=50, null=True)
    gender = models.CharField(verbose_name="Gender",
                              max_length=1, choices=GENDER, null=True)
    image = models.ImageField(
        upload_to="customer/images", default="customer/images/custdefault.jpg")
    complete_info = models.BooleanField(
        verbose_name="Complete Registraiton", default=False)

    def __str__(self):
        return self.name

    def save(self, change_password=False, *args, **kwargs):
        if self.complete_info == False or change_password:
            hashed_password = make_password(self.password)
            self.password = hashed_password
        super(Customer, self).save(*args, **kwargs)

    def check_Customer_password(self, password):
        if check_password(password, self.password):
            return True
        return False
