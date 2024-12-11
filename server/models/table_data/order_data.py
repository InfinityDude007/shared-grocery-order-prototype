from datetime import datetime

# hardcoded data for the Orders table for prototyping purposes
hardcoded_orders = [
    {"order_id": "O001", "accommodation_id": "G101", "creation_date": datetime(2024, 11, 30, 9, 30, 42), "order_status": "Pending", "delivery_fee": 15.0},
    {"order_id": "O002", "accommodation_id": "G102", "creation_date": datetime(2024, 12, 1, 10, 45, 30),"order_status": "Completed", "delivery_fee": 10.0},
    {"order_id": "O003", "accommodation_id": "G103", "creation_date": datetime(2024, 12, 2, 14, 20, 15),"order_status": "Cancelled", "delivery_fee": 8.5},
    {"order_id": "O004", "accommodation_id": "G104", "creation_date": datetime(2024, 12, 3, 8, 0, 0),"order_status": "Pending", "delivery_fee": 12.0},
    {"order_id": "O005", "accommodation_id": "G105", "creation_date": datetime(2024, 12, 4, 12, 15, 45), "order_status": "Completed", "delivery_fee": 9.75},
    {"order_id": "O006", "accommodation_id": "G106", "creation_date": datetime(2024, 12, 5, 16, 50, 25), "order_status": "Cancelled", "delivery_fee": 14.0},
    {"order_id": "O007", "accommodation_id": "G107", "creation_date": datetime(2024, 12, 6, 18, 30, 10), "order_status": "Pending", "delivery_fee": 7.5},
    {"order_id": "O008", "accommodation_id": "G108", "creation_date": datetime(2024, 12, 7, 20, 0, 5), "order_status": "Completed", "delivery_fee": 6.0},
    {"order_id": "O009", "accommodation_id": "G109", "creation_date": datetime(2024, 12, 8, 6, 45, 30), "order_status": "Cancelled", "delivery_fee": 11.25},
    {"order_id": "O010", "accommodation_id": "G110", "creation_date": datetime(2024, 12, 9, 11, 10, 10), "order_status": "Pending", "delivery_fee": 13.0},
    {"order_id": "O011", "accommodation_id": "G111", "creation_date": datetime(2024, 12, 10, 13, 35, 50), "order_status": "Completed", "delivery_fee": 10.5},
    {"order_id": "O012", "accommodation_id": "G112", "creation_date": datetime(2024, 12, 11, 15, 40, 20), "order_status": "Pending", "delivery_fee": 9.0},
    {"order_id": "O013", "accommodation_id": "G113", "creation_date": datetime(2024, 12, 12, 19, 25, 35), "order_status": "Cancelled", "delivery_fee": 7.25},
    {"order_id": "O014", "accommodation_id": "G114", "creation_date": datetime(2024, 12, 13, 21, 15, 0), "order_status": "Completed", "delivery_fee": 8.0},
    {"order_id": "O015", "accommodation_id": "G115", "creation_date": datetime(2024, 12, 14, 5, 55, 55), "order_status": "Pending", "delivery_fee": 14.5},
]