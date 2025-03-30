import requests

url = "http://127.0.0.1:5000/api/update"
new_data = {
    "Order": "008",
    "Product_name": "Product H",
    "Price": 300.0,
    "Order_date": "2025-03-30",
    "Delivery_Date": "2025-04-05",
    "Location": "New York",
    "Shipping_Status": "Pending",
    "Payment_Status": "Unpaid"
}

response = requests.post(url, json=new_data)

print(response.json())