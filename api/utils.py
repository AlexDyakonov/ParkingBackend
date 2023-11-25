import json
from .models import Coordinate, Location, Category, Price, Parking


def create_payment(secret_key, return_link):
    # должно возвращать id оплаты от юмани
    return "todo-youmoney-payment-link"


def get_payment_link(payment_id):
    # должно возвращать ссылку на оплату
    return "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


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
            # spaces_data = parking_data['spaces']
            # if spaces_data.get('handicapped') is not None:
            #     space = Space.objects.create(handicapped=spaces_data['handicapped'], total=spaces_data['total'])

            # Создание цен
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
                # space=space
            )

            parking.prices.set(prices)

            parking.save()
        except Exception:
            print("ad")
    # Готово! Данные загружены в базу данных Django.
