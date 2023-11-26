API Documentation

Endpoint: /api/parkings

    Method: GET
    Description: Get a list of all parking lots.
    Response:
    Status Code: 200 OK
    Content:
    [
       {
        "id": 27,
        "blocked": false,
        "aggregating": false,
        "category": {
            "zone_purpose": "all"
        },
        "location": {
            "type": "LineString",
            "coordinates": [
                [
                    60.5900073,
                    56.8312082
                ],
                [
                    60.5904472,
                    56.8300812
                ]
            ]
        },
        "center": [
            60.5902273,
            56.8306447
        ],
        "prices": [
            {
                "vehicle_type": "car",
                "min_price": 3000,
                "max_price": 3000
            }
        ],
        "total_spots": 28,
        "empty_spots": 28,
        "handicapped_spots": 2
    },
    ]

Endpoint: /api/parkings/<parking_id>/

    Method: GET
    Description: Get details of a parking lot by its ID.
    Parameters:
        parking_id (int): Parking lot ID
    Response:

    Status Code: 200 OK
    Content:
    {
        "id": 27,
        "blocked": false,
        "aggregating": false,
        "category": {
            "zone_purpose": "all"
        },
        "location": {
            "type": "LineString",
            "coordinates": [
                [
                    60.5900073,
                    56.8312082
                ],
                [
                    60.5904472,
                    56.8300812
                ]
            ]
        },
        "center": [
            60.5902273,
            56.8306447
        ],
        "prices": [
            {
                "vehicle_type": "car",
                "min_price": 3000,
                "max_price": 3000
            }
        ],
        "total_spots": 28,
        "empty_spots": 28,
        "handicapped_spots": 2
    },

Endpoint: /api/parkings/<parking_id>/comments

    Method: GET
    Description: Get comments for a parking lot by its ID.
    Parameters:
        parking_id (int): Parking lot ID
    Response:

    txt

    Status Code: 200 OK
    Content:
    [
        {
            "text": "Good parking space!",
            "rating": 5,
            "fio": "John Doe"
        },
        {
            "text": "Needs improvement.",
            "rating": 3,
            "fio": "Jane Doe"
        }
    ]

Endpoint: /api/parkings/<parking_id>/comments/add

    Method: PUT
    Description: Add a comment to a parking lot.
    Parameters:
        parking_id (int): Parking lot ID
    Request Body:


    {
        "text": "Great parking!",
        "rating": 5,
        "fio": "Alice Wonderland"
    }

    Response:


        Status Code: 200 OK
        Content: {"success": "Data uploaded successfully"}
    
Endpoint: /api/parkings/<parking_id>/reserve
    
    Method: POST
    Description: Reserve a parking spot and get a payment link.
    Parameters:
        parking_id (int): Parking lot ID
    Request Body:
 
    {
        "credentials": "User123",
        "duration": 2
    }
    
    Response:

    Status Code: 200 OK
    Content:
    {
        "payment_link": "https://payment.example.com/link",
        "payment_id": "12345"
    }

Endpoint: /api/payment/status

    Method: GET
    Description: Get the payment status by its ID.
    Parameters:
        payment_id (string): Payment ID
    Response:


    Status Code: 200 OK
    Content:
    {
        "status": "success"
    }
