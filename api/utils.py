from .models import Coordinate, Location, Category, Price, Parking, Transaction, ParkingSpot, Booking
from yookassa import Payment
import uuid
from django.utils import timezone

def update_parking_spots(parking):
    parking_spots = ParkingSpot.objects.filter(parking=parking, is_reserved=True, is_empty=False)
    for spot in parking_spots:
        active_bookings = Booking.objects.filter(parking_spot=spot, booking_end_time__lt=timezone.now())
        if active_bookings.exists():
            spot.is_reserved = False
            spot.is_empty = True
            spot.save()

def create_payment(booking):
    transactions = Transaction.objects.filter(booking=booking, transaction_status='pending')
    if transactions.exists():
        return Payment.find_one(transactions.payment_id)

    value = booking.total_price/100
    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
            "confirmation": {
            "type": "redirect",
            "return_url": "https://youtu.be/dQw4w9WgXcQ"
        },
            "capture": True,
            "description": booking.credentials
    }, uuid.uuid4())
    
    transaction = Transaction.objects.get_or_create(
        booking=booking,
        payment_id=payment.id,
        payment_url=payment.confirmation.confirmation_url,
        transaction_status='pending',
    )
    transaction[0].save()
    
    return payment

def get_payment_link(payment):    
    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url

def get_payment_id(payment):
    return payment.id


def get_payment_status(payment_id):
    payment = Payment.find_one(payment_id)
    return payment.status


# Написал ChatGPT
def load_parkings_from_ek(json_data):
    # Проход по каждой парковке в JSON
    for parking_data in json_data:
        try:
            # Создание координаты центра
            center_data = parking_data['center']['coordinates']
            center = Coordinate.objects.create(longitude=center_data[0], latitude=center_data[1])

            # Создание локации
            location_data = parking_data['location']['coordinates']
            location_type = parking_data['location']['type']
            location = Location.objects.create(type=location_type)

            if location_type != "Polygon":
                location.coordinates.set(
                    [Coordinate.objects.create(longitude=lon, latitude=lat) for lon, lat in location_data])
            else:
                location.coordinates.set(
                    [Coordinate.objects.create(longitude=lon, latitude=lat) for lon, lat in location_data[0]])

            # Создание категории
            category_data = parking_data['category']
            category, created = Category.objects.get_or_create(zone_purpose=category_data['zonePurpose'])

            # Создание парковочных мест
            spaces_data = parking_data['spaces']

            total_spots = 0
            empty_spots = 0
            handicapped_spots = 0
            if spaces_data.get('handicapped') is not None:
                total_spots = spaces_data['total']
                empty_spots = spaces_data['total']
                handicapped_spots = spaces_data['handicapped']

            # Создание цен
            prices = None
            if parking_data.get('zone') is not None:
                zone_data = parking_data['zone']

                prices_data = zone_data['prices']
                prices = [
                    Price.objects.create(vehicle_type=price_data['vehicleType'], min_price=price_data['price']['min'],
                                         max_price=price_data['price']['max']) for price_data in prices_data]

            # Создание парковки
            parking = Parking.objects.create(
                blocked=parking_data['blocked'],
                aggregating=parking_data['aggregating'],
                category=category,
                location=location,
                center=center,
                total_spots=total_spots,
                empty_spots=empty_spots,
                handicapped_spots=handicapped_spots
                # space=space
            )

            if prices is not None:
                parking.prices.set(prices)

            parking.save()
        except Exception:
            print("ad")
    # Готово! Данные загружены в базу данных Django.

def payment_status_handler(payment_id, payment_status):
    transaction = Transaction.objects.get(payment_id=payment_id)

    if payment_status == 'pending':
        transaction.transaction_status = 'pending'
    elif payment_status == 'waiting_for_capture':
        transaction.transaction_status = 'pending'
    elif payment_status == 'succeeded':
        transaction.transaction_status = 'paid'
    elif payment_status == 'canceled':
        transaction.transaction_status = 'failed'
        parking_spot = transaction.booking.parking_spot
        parking_spot.is_reserved = False
        parking_spot.is_empty = True
        parking_spot.save()
    else:
        print('Unexpected')

    transaction.save()