import seaborn as sns
import pandas as pd
import numpy as np
from flask import Flask, redirect, request, render_template, url_for
from utils import generate_summaries 


app = Flask(__name__)

# Load the Excel file as a DataFrame
orders_df = pd.read_excel("C://Users//lenovo//OneDrive//Desktop//dashboard//Product_Details.xlsx")
orders_df.columns = orders_df.columns.str.strip().str.replace(' ', '_')  # Clean column names
customer_df = pd.read_excel("C://Users//lenovo//OneDrive//Desktop//dashboard//customer_offers.xlsx")
customer_df.columns = customer_df.columns.str.strip().str.replace(' ', '_')  # Clean column names

# Concatenate DataFrames column-wise
data = pd.concat([orders_df, customer_df], axis=1)



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
@app.route('/location_summary', methods=['GET'])
def location_summary():
    location = request.args.get('location')
    location_orders = data[data['Location'] == location]
    total_orders = location_orders.shape[0]
    total_revenue = location_orders['Price'].sum()
    summaries = generate_summaries(data, location=location)
    return render_template('location_summary.html', summaries=summaries, location=location, total_orders=total_orders, total_revenue=total_revenue, location_orders=location_orders.to_dict(orient='records'))
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
        summaries = generate_summaries(data,product_name, start_date, end_date)
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