from django.db import models

from user.models import User
#from booking.models import Booking

class Category(models.Model): 
    name = models.CharField(max_length=20)

    class Meta: 
        db_table = 'categories'

class Location(models.Model): 
    name = models.CharField(max_length=20)

    class Meta: 
        db_table = 'locations'

class Hotel(models.Model): 
    name               = models.CharField(max_length=200)
    english_name       = models.CharField(max_length=200)
    address            = models.CharField(max_length=200)
    introduction       = models.CharField(max_length=200)
    thumbnail_url      = models.URLField(max_length=1000)
    category           = models.ForeignKey(Category, on_delete=models.CASCADE)
    location           = models.ForeignKey(Location, on_delete=models.CASCADE)
    min_people         = models.IntegerField()
    max_people         = models.IntegerField()
    room_count         = models.IntegerField()
    checkin_time       = models.TimeField()
    checkout_time      = models.TimeField()
    longitude          = models.DecimalField(max_digits=12, decimal_places=7)
    latitude           = models.DecimalField(max_digits=12, decimal_places=7)
    phone_number       = models.CharField(max_length=200)
    email              = models.EmailField()
    description_title  = models.CharField(max_length=200)
    description_first  = models.TextField()
    description_second = models.TextField()
    description_third  = models.TextField()

    class Meta: 
        db_table = 'hotels'

class HotelImage(models.Model): 
    hotel     = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1000)
    
    class Meta: 
        db_table = 'hotel_images'

class Service(models.Model): 
    hotel    = models.ManyToManyField(Hotel, through='HotelService', related_name='services')
    name     = models.CharField(max_length=200)
    icon_url = models.URLField(max_length=1000)

    class Meta: 
        db_table = 'services'

class HotelService(models.Model): 
    hotel   = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'hotel_services'

class Tag(models.Model): 
    hotel = models.ManyToManyField(Hotel, through='HotelTag', related_name='tags')
    name  = models.CharField(max_length=200)

    class Meta: 
        db_table = 'tags'

class HotelTag(models.Model): 
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    tag   = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'hotel_tags'

class Room(models.Model): 
    hotel         = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    introduction  = models.TextField()
    min_people    = models.IntegerField()
    max_people    = models.IntegerField()
    area          = models.DecimalField(max_digits=18, decimal_places=2)
    price         = models.DecimalField(max_digits=18, decimal_places=2)
    name          = models.CharField(max_length=200)
    price_weekday = models.DecimalField(max_digits=18, decimal_places=2)
    price_weekend = models.DecimalField(max_digits=18, decimal_places=2)
    price_peak    = models.DecimalField(max_digits=18, decimal_places=2)
    stay_at_least = models.IntegerField()
    # booking       = models.ManyToManyField(User, through='Booking', related_name='rooms')

    class Meta: 
        db_table = 'rooms'

class RoomImage(models.Model): 
    room      = models.ForeignKey(Room, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=1000)

    class Meta: 
        db_table = 'room_images'

class Type(models.Model): 
    room = models.ManyToManyField(Room, through='RoomType', related_name='types')
    name = models.CharField(max_length=200)

    class Meta: 
        db_table = 'types'

class RoomType(models.Model): 
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'room_types'

class BedType(models.Model): 
    room = models.ManyToManyField(Room, through='Bed', related_name='bed_types')
    name = models.CharField(max_length=200)

    class Meta: 
        db_table = 'bed_types'

class Bed(models.Model): 
    room     = models.ForeignKey(Room, on_delete=models.CASCADE)
    bed_type = models.ForeignKey(BedType, on_delete=models.CASCADE)
    number   = models.IntegerField()

    class Meta: 
        db_table = 'beds'

class Facility(models.Model): 
    room     = models.ManyToManyField(Room, through='RoomFacility', related_name='facilities')
    name     = models.CharField(max_length=200)
    icon_url = models.URLField(max_length=1000)

    class Meta: 
        db_table = 'facilities'

class RoomFacility(models.Model): 
    room     = models.ForeignKey(Room, on_delete=models.CASCADE)
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE)

    class Meta: 
        db_table = 'room_facilities'

class HotelInformation(models.Model): 
    hotel                  = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    description            = models.CharField(max_length=200)
    detail_top             = models.TextField()
    detail_content         = models.TextField()
    detail_signature       = models.CharField(max_length=20)
    detail_signature_image = models.CharField(max_length=1000)
    special1               = models.CharField(max_length=20)
    special1_content       = models.TextField()
    special2               = models.CharField(max_length=20)
    special2_content       = models.TextField()
    special3               = models.CharField(max_length=20)
    special3_content       = models.TextField()

    class Meta: 
        db_table = 'hotel_informations'

class InfoLocation(models.Model): 
    info            = models.ForeignKey(HotelInformation, on_delete=models.CASCADE)
    place_name      = models.CharField(max_length=40)
    place_detail    = models.CharField(max_length=200)
    place_longitude = models.DecimalField(max_digits=12, decimal_places=7)
    place_latitude  = models.DecimalField(max_digits=12, decimal_places=7)

    class Meta: 
        db_table = 'info_locations'