from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Parking, Parkomat, Terminal, Comment, Booking, ParkingSpot
from .serializer import ParkingSerializer, TerminalSerializer, ParkomatSerializer, CommentSerializer
from rest_framework import status
from .utils import load_parkings_from_ek, create_payment, get_payment_link, get_payment_status, get_payment_id, payment_status_handler, update_parking_spots
from datetime import timedelta


# Create your views here.


# Происходит бронирование места на парковке и возвращает payment_link от юкассы
@api_view(['POST'])
def parking_reserve(request, parking_id):
    parking = get_object_or_404(Parking, id=parking_id)
    credentials = request.data.get('credentials')
    int_duration = request.data.get('duration') or 1
    duration = timedelta(hours=int_duration)

    if credentials is None:
        return Response({"error": "no credentials"})

    if parking.empty_spots == 0:
        return Response({"error": "no empty spots"})

    if parking.prices is None:
        return Response({"error": "no price"})

    update_parking_spots(parking)

    empty_parking_spot = ParkingSpot.objects.filter(parking=parking, is_empty=True, is_reserved=False).first()
    empty_parking_spot.is_reserved = True
    empty_parking_spot.is_empty = False
    empty_parking_spot.save()

    booking = Booking(
        parking_spot=empty_parking_spot,
        credentials=credentials,
        duration=duration,
        total_price=int_duration * parking.prices.first().max_price,
    )
    booking.save()

    payment = create_payment(booking)

    return Response({
        "payment_link": get_payment_link(payment),
        "payment_id": get_payment_id(payment),
    })


@api_view(['GET'])
def payment_status(request):
    payment_id = request.data.get('payment_id')
    if payment_id is None:
        return Response({"error": "no payment_id"})
    pay_status = get_payment_status(payment_id)

    payment_status_handler(payment_id, pay_status)

    return Response({
        "status": pay_status
    })


@api_view(['GET'])
def get_parkings(request):
    parkings = Parking.objects.all()
    serializer = ParkingSerializer(parkings, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_terminals(request):
    terminals = Terminal.objects.all()
    serializer = TerminalSerializer(terminals, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_parkomats(request):
    parkomats = Parkomat.objects.all()
    serializer = ParkomatSerializer(parkomats, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def put_comment(request, parking_id):
    parking = get_object_or_404(Parking, id=parking_id)
    text = request.data.get('text')
    if text is None:
        return Response({"error": "no text"})
    fio = request.data.get('fio')
    if fio is None:
        return Response({"error": "no fio"})
    rating = request.data.get('rating')
    if rating is None:
        return Response({"error": "no rating"})
    comment = Comment(
        parking=parking,
        text=text,
        rating=rating,
        fio=fio
    )
    comment.save()
    return Response({"success": "Data uploaded successfully"})


@api_view(['GET'])
def get_comments(request, parking_id):
    parking = get_object_or_404(Parking, id=parking_id)
    comments = parking.comment_set.all()
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_parking_by_id(request, parking_id):
    # Get the parking object based on the provided ID or return a 404 response
    parking = get_object_or_404(Parking, id=parking_id)

    # Serialize the parking object
    serializer = ParkingSerializer(parking)

    # Return the serialized data as JSON
    return Response(serializer.data)


@api_view(['PUT'])
def put_ek(request):
    json_data = request.data['parkings']
    if not json_data:
        return Response({'error': 'JSON data is required'}, status=status.HTTP_400_BAD_REQUEST)

    load_parkings_from_ek(json_data)
    return Response({'success': 'Data uploaded successfully'}, status=status.HTTP_201_CREATED)

# 
# @csrf_exempt
# @require_POST
# def yookassa_webhook(request):
#     try:
#         data = request.json()
#         payment_id = data.get("object", {}).get("id")
#         payment_status = data.get("object", {}).get("status")

#         if payment_status == 'pending':
            
#         elif payment_status == 'waiting_for_capture':
            
#         elif payment_status == 'succeeded':
            
#         elif payment_status == 'canceled':
            
#         else:
#             print('Unexpected')

#         return JsonResponse({"status": "success"})
#     except Exception as e:
#         return JsonResponse({"status": "error", "message": str(e)})
