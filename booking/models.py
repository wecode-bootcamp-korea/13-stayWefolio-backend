from django.db    import models

from user.models  import User

class Booking(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    room         = models.ForeignKey("hotel.Room", on_delete=models.CASCADE, related_name='bookings')
    date_from    = models.DateField()
    date_to      = models.DateField()
    phone_number = models.CharField(max_length=40)
    adult        = models.IntegerField()
    child        = models.IntegerField(default=0)
    infant       = models.IntegerField(default=0)
    demand       = models.TextField()
    price        = models.DecimalField(max_digits=18, decimal_places=2)
    discount     = models.DecimalField(max_digits=18, decimal_places=2)
    total        = models.DecimalField(max_digits=18, decimal_places=2)
    
    class Meta:
        db_table = 'bookings'

class BookedRoom(models.Model):
    room    = models.ForeignKey("hotel.Room", on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)

    class Meta:
        db_table = 'booked_rooms'
