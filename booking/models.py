from django.db    import models

from user.models  import User

class Payment(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        db_table = 'payments'

class Booking(models.Model):
    user                          = models.ForeignKey(User, on_delete=models.CASCADE)
    room                          = models.ForeignKey("hotel.Room", on_delete=models.CASCADE, related_name='bookings')
    date_from                     = models.DateField()
    date_to                       = models.DateField()
    name                          = models.CharField(max_length=40, null=True)
    phone_number                  = models.CharField(max_length=40)
    email                         = models.EmailField(null=True)
    adult                         = models.IntegerField()
    child                         = models.IntegerField(default=0)
    infant                        = models.IntegerField(default=0)
    option_breakfast              = models.BooleanField(default=False)
    option_pickup                 = models.BooleanField(default=False)
    demand                        = models.TextField()
    price                         = models.DecimalField(max_digits=18, decimal_places=2)
    discount                      = models.DecimalField(max_digits=18, decimal_places=2)
    total                         = models.DecimalField(max_digits=18, decimal_places=2)
    payment                       = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    terms_information_collection  = models.BooleanField(default=True)
    terms_information_third_party = models.BooleanField(default=True)
    terms_information_refund      = models.BooleanField(default=True)
    terms_marketing               = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'bookings'

class BookedRoom(models.Model):
    room    = models.ForeignKey("hotel.Room", on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        db_table = 'booked_rooms'
