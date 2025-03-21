import pandas as pd
from textblob import TextBlob
import json
import plotly.express as px


def analyze_sentiment(feedback):
    if isinstance(feedback, str):
        analysis = TextBlob(feedback)
        polarity = 'Positive' if analysis.sentiment.polarity >= 0 else 'Negative'
        subjectivity = analysis.sentiment.subjectivity
        return polarity, subjectivity
    else:
        return None, None

def generate_summaries(data,product_name=None, start_date=None, end_date=None,location=None):
    if product_name:
        product_orders = data[data['Product_name'] == product_name]
    else:
        product_orders = data
    
    if start_date and end_date:
        product_orders = product_orders[(product_orders['Order_date'] >= start_date) & (product_orders['Order_date'] <= end_date)]
    
    if location:
        product_orders = product_orders[product_orders['Location'] == location]
    
    summaries = {}

    # Summary of Order Quantity
    if 'Order_Quantity' in product_orders.columns:
        summaries['total_order_quantity'] = product_orders['Order_Quantity'].sum()
        summaries['average_order_quantity'] = product_orders['Order_Quantity'].mean()

    # Summary of Price
    if 'Price' in product_orders.columns:
        summaries['total_revenue'] = product_orders['Price'].sum()
        summaries['average_price'] = product_orders['Price'].mean()

    # Summary of Shipping Status
    if 'Shipping_Status' in product_orders.columns:
        summaries['shipping_status_counts'] = product_orders['Shipping_Status'].value_counts().to_dict()

    # Summary of Payment Status
    if 'Payment_Status' in product_orders.columns:
        summaries['payment_status_counts'] = product_orders['Payment_Status'].value_counts().to_dict()

    # Summary of Stock Level
    if 'Stock_Level' in product_orders.columns:
        summaries['total_stock_level'] = product_orders['Stock_Level'].sum()
        summaries['average_stock_level'] = product_orders['Stock_Level'].mean()

    # Summary of Discount
    if 'Discount' in product_orders.columns:
        summaries['total_discount'] = product_orders['Discount'].sum()
        summaries['average_discount'] = product_orders['Discount'].mean()

    # Summary of Location
    if 'Location' in product_orders.columns:
        summaries['location_distribution'] = product_orders['Location'].value_counts().to_dict()

    # Time Series Analysis
    if 'Order_date' in product_orders.columns and 'Price' in product_orders.columns:
        product_orders['Order_date'] = pd.to_datetime(product_orders['Order_date'])
        if start_date and end_date:
            product_orders = product_orders[(product_orders['Order_date'] >= start_date) & (product_orders['Order_date'] <= end_date)]
            datewise_revenue = product_orders.groupby(product_orders['Order_date'].dt.date)['Price'].sum()
            summaries['datewise_revenue'] = datewise_revenue.to_dict()
        # Additional time series analysis
        monthly_revenue = product_orders.groupby(product_orders['Order_date'].dt.to_period('M'))['Price'].sum()
        summaries['monthly_revenue'] = monthly_revenue.to_dict()

        yearly_revenue = product_orders.groupby(product_orders['Order_date'].dt.to_period('Y'))['Price'].sum()
        summaries['yearly_revenue'] = yearly_revenue.to_dict()

    return summaries

def plot_graph(data, product_name):
    # Plot number of orders from each location for the product
    location_orders = data[data['Product_name'] == product_name]
    location_order_counts = location_orders['Location'].value_counts().reset_index()
    location_order_counts.columns = ['Location', 'Count']
    location_fig = px.bar(location_order_counts, x='Location', y='Count', title=f'Number of Orders from Each Location for {product_name}')

    # Plot total revenue over time for the product
    product_orders = data[data['Product_name'] == product_name]
    product_orders['Order_date'] = pd.to_datetime(product_orders['Order_date'])
    product_orders = product_orders.sort_values(by='Order_date')
    product_fig = px.line(product_orders, x='Order_date', y='Price', title=f'Total Revenue Over Time for {product_name}', labels={'Order_date': 'Order Date', 'Price': 'Total Revenue'})

    return location_fig.to_json(), product_fig.to_json()