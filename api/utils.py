from .models import Coordinate, Location, Category, Price, Parking, Transaction
from yookassa import Payment
import uuid

def create_payment(booking):
    value = booking.total_price/100
    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
            "confirmation": {
            "type": "redirect",
            "return_url": f"https://google.com"
        },
            "capture": True,
            "description": booking.credentials
    }, uuid.uuid4())
    
    transaction = Transaction(
        booking=booking,
        payment_id=payment.id
    )
    transaction.save()
    
    return payment

def get_payment_link(payment):    
    confirmation_url = payment.confirmation.confirmation_url
    return confirmation_url

def get_payment_id(payment):
    return payment.id


def get_payment_status(payment_id):

    # возвращает статус который отдает юмани
    return "succeed"


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
