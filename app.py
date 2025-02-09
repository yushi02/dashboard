import seaborn as sns
import pandas as pd
import numpy as np
from flask import Flask, redirect, request, render_template, url_for



app = Flask(__name__)

# Load the Excel file as a DataFrame
orders_df = pd.read_excel("C://Users//lenovo//OneDrive//Desktop//dashboard//Product_Details.xlsx")
orders_df.columns = orders_df.columns.str.strip().str.replace(' ', '_')  # Clean column names
customer_df = pd.read_excel("C://Users//lenovo//OneDrive//Desktop//dashboard//customer_offers.xlsx")
customer_df.columns = customer_df.columns.str.strip().str.replace(' ', '_')  # Clean column names

# Concatenate DataFrames column-wise
data = pd.concat([orders_df, customer_df], axis=1)

def generate_summaries(product_name, start_date=None, end_date=None):
    product_orders = data[data['Product_name'] == product_name]
    
    if start_date and end_date:
        product_orders = product_orders[(product_orders['Order_Date'] >= start_date) & (product_orders['Order_Date'] <= end_date)]
    
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
    if 'Order_Date' in product_orders.columns and 'Price' in product_orders.columns:
        product_orders['Order_Date'] = pd.to_datetime(product_orders['Order_Date'])
        datewise_revenue = product_orders.groupby(product_orders['Order_Date'].dt.date)['Price'].sum()
        summaries['datewise_revenue'] = datewise_revenue.to_dict()

        # Additional time series analysis
        monthly_revenue = product_orders.groupby(product_orders['Order_Date'].dt.to_period('M'))['Price'].sum()
        summaries['monthly_revenue'] = monthly_revenue.to_dict()

        yearly_revenue = product_orders.groupby(product_orders['Order_Date'].dt.to_period('Y'))['Price'].sum()
        summaries['yearly_revenue'] = yearly_revenue.to_dict()

    return summaries

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    order_data = None
    error = None
    product_names = data['Product_name'].unique()
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        order = data[data['Order'] == order_id]

        if not order.empty:
            order_data = order.iloc[0].to_dict()
        else:
            error = f"Order ID {order_id} not found."
       
    return render_template('dashboard.html', order=order_data, error=error, product_names=product_names)

@app.route('/product/<product_name>', methods=['GET', 'POST'])
def product_detail(product_name):
    product_orders = data[data['Product_name'] == product_name]
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if not product_orders.empty:
        product_data = product_orders.to_dict(orient='records')
        total_revenue = product_orders['Price'].sum()
        product_description = product_orders['Description'].iloc[0]
        product_category = product_orders['Category'].iloc[0]
        summaries = generate_summaries(product_name, start_date, end_date)
        return render_template('product_detail.html', product_name=product_name, product_data=product_data, total_revenue=total_revenue, product_description=product_description, product_category=product_category, summaries=summaries, start_date=start_date, end_date=end_date)
    else:
        return "Product not found", 404

@app.route('/order/<order_id>', methods=['GET', 'POST'])
def order_details(order_id):
    order = data[data['Order'] == order_id]
    feedback = None
    is_paid = False
    tag = None

    if request.method == 'POST':
        tag = request.form.get('customer_tag', 'Unknown')  # Default to 'Unknown'
        feedback = request.form.get('feedback','None')

        # Update DataFrame and persist changes
        data.loc[data['Order'] == order_id, 'Customer_Tag'] = tag
        data.loc[data['Order'] == order_id, 'Feedback'] = feedback
        data.to_excel("C://Users//lenovo//OneDrive//Desktop//dashboard//Product_Details.xlsx", index=False)
        print(f"Received feedback for order {order_id}: {feedback}")
        return redirect(url_for('order_details', order_id=order_id))

    if not order.empty:
        order_data = order.iloc[0].to_dict()
        customer_name = order_data['Customer_Name']
        customer_email = order_data['Supplier_Contact']
        customer_orders = data[data['Supplier_Contact'] == customer_email].to_dict(orient='records')
        product_name = order_data['Product_name']
        related_orders = data[data['Product_name'] == product_name][['Order']].to_dict(orient='records')
        related_order_id = request.args.get('related_order_id')
        if related_order_id:
            return redirect(url_for('order_details', order_id=related_order_id))
        return render_template('order_details.html', order=order_data, feedback=feedback, is_paid=is_paid, tag=tag, related_orders=related_orders, customer_name=customer_name, customer_email=customer_email, customer_orders=customer_orders)
        
    else:
        return "Order not found", 404

if __name__ == '__main__':
    app.run(debug=True)