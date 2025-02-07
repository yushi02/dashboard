import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from flask import Flask, redirect, request, render_template, url_for
import io
import base64

app = Flask(__name__)

# Load the Excel file as a DataFrame
orders_df = pd.read_excel("C://Users//lenovo//OneDrive//Desktop//dashboard//Product_Details.xlsx")
orders_df.columns = orders_df.columns.str.strip().str.replace(' ', '_')  # Clean column names
feedback_list=[]
def generate_plots(product_name):
    product_orders = orders_df[orders_df['Product_name'] == product_name]
    
    # Plot Order Quantity
    fig, ax = plt.subplots()
    product_orders['Order_Quantity'].plot(kind='bar', ax=ax)
    ax.set_title(f'Order Quantity of {product_name}')
    ax.set_xlabel('Order ID')
    ax.set_ylabel('Quantity')
    img1 = io.BytesIO()
    plt.savefig(img1, format='png')
    img1.seek(0)
    plot_url1 = base64.b64encode(img1.getvalue()).decode()
    # Plot Price
    fig, ax = plt.subplots()
    product_orders['Price'].plot(kind='bar', ax=ax)
    ax.set_title(f'Price of {product_name}')
    ax.set_xlabel('Order ID')
    ax.set_ylabel('Price')
    img2 = io.BytesIO()
    plt.savefig(img2, format='png')
    img2.seek(0)
    plot_url2 = base64.b64encode(img2.getvalue()).decode()

    # Plot Shipping Status
    fig, ax = plt.subplots()
    product_orders['Shipping_Status'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title(f'Shipping Status of {product_name}')
    ax.set_xlabel('Shipping Status')
    ax.set_ylabel('Count')
    img3 = io.BytesIO()
    plt.savefig(img3, format='png')
    img3.seek(0)
    plot_url3 = base64.b64encode(img3.getvalue()).decode()

    # Plot Payment Status
    fig, ax = plt.subplots()
    product_orders['Payment_Status'].value_counts().plot(kind='bar', ax=ax)
    ax.set_title(f'Payment Status of {product_name}')
    ax.set_xlabel('Payment Status')
    ax.set_ylabel('Count')
    img4 = io.BytesIO()
    plt.savefig(img4, format='png')
    img4.seek(0)
    plot_url4 = base64.b64encode(img4.getvalue()).decode()

    # Plot Stock Level
    fig, ax = plt.subplots()
    product_orders['Stock_Level'].plot(kind='bar', ax=ax)
    ax.set_title(f'Stock Level of {product_name}')
    ax.set_xlabel('Order ID')
    ax.set_ylabel('Stock Level')
    img5 = io.BytesIO()
    plt.savefig(img5, format='png')
    img5.seek(0)
    plot_url5 = base64.b64encode(img5.getvalue()).decode()

    # Plot Discount
    fig, ax = plt.subplots()
    product_orders['Discount_(%)'].plot(kind='bar', ax=ax)
    ax.set_title(f'Discount of {product_name}')
    ax.set_xlabel('Order ID')
    ax.set_ylabel('Discount')
    img6 = io.BytesIO()
    plt.savefig(img6, format='png')
    img6.seek(0)
    plot_url6 = base64.b64encode(img6.getvalue()).decode()

    # Pie Chart of Location
    fig, ax = plt.subplots()
    product_orders['Location'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
    ax.set_title(f'Location Distribution of {product_name}')
    img7 = io.BytesIO()
    plt.savefig(img7, format='png')
    img7.seek(0)
    plot_url7 = base64.b64encode(img7.getvalue()).decode()

    return {
        'plot_url1': plot_url1,
        'plot_url2': plot_url2,
        'plot_url3': plot_url3,
        'plot_url4': plot_url4,
        'plot_url5': plot_url5,
        'plot_url6': plot_url6,
        'plot_url7': plot_url7
    }
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    order_data=None
    error=None
    product_names = orders_df['Product_name'].unique()
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        order = orders_df[orders_df['Order'] == order_id]

        if not order.empty:
            order_data = order.iloc[0].to_dict()  
        else:
            error = f"Order ID {order_id} not found."
       
    return render_template('dashboard.html',order=order_data, error=error,product_names=product_names)
@app.route('/product/<product_name>')
def product_detail(product_name):
    product_orders = orders_df[orders_df['Product_name'] == product_name]
    if not product_orders.empty:
        product_data = product_orders.to_dict(orient='records')
        total_revenue = product_orders['Price'].sum()
        product_description = product_orders['Description'].iloc[0]
        product_category = product_orders['Category'].iloc[0]
        plots = generate_plots(product_name)
        return render_template('product_detail.html', product_name=product_name, product_data=product_data,total_revenue=total_revenue,product_description=product_description,product_category=product_category,plots=plots)
    else:
        return "Product not found", 404
@app.route('/order/<order_id>',methods=['GET','POST'])
def order_details(order_id):
    order = orders_df[orders_df['Order'] == order_id]
    feedback=None
    is_paid=False
    if request.method == 'POST':
            feedback = request.form.get('feedback')
        # Store the feedback
            feedback_list.append({'order_id': order_id, 'feedback': feedback})
            print(f"Received feedback for order {order_id}: {feedback}")
            return redirect(url_for('order_details', order_id=order_id))
    if not order.empty:
        order_data = order.iloc[0].to_dict()
        return render_template('order_details.html', order=order_data, feedback=feedback,is_paid=is_paid)
    else:
        return "Order not found", 404

    
if __name__ == '__main__':
    app.run(debug=True)