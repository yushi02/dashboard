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
def generate_plot():
    plt.figure(figsize=(4, 4))
    sns.countplot(x='Payment_Status', data=orders_df)
    plt.xticks(rotation=45)
    plt.xlabel("Payment Method")
    plt.ylabel("Count")
    plt.title("Payment Method Distribution")

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png',bbox_inches='tight')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url
@app.route('/', methods=['GET', 'POST'])
def dashboard():
    order_data=None
    error=None
    plot_url = generate_plot()
    feedback = None
    is_paid = False
    if request.method == 'POST':
        order_id = request.form.get('order_id')
    
    
        order = orders_df[orders_df['Order'] == order_id]

        if not order.empty:
            order_data = order.iloc[0].to_dict()  
        else:
            error = f"Order ID {order_id} not found."
        if 'feedback' in request.form:
            feedback = request.form.get('feedback')
            # Process the feedback as needed
            print(f"Received feedback: {feedback}")
            return redirect(url_for('dashboard'))
    
    return render_template('dashboard.html',order=order_data, error=error, plot_url=plot_url,feedback=feedback, is_paid=is_paid)
if __name__ == '__main__':
    app.run(debug=True)