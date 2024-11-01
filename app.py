from flask import Flask, render_template
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)

# Sample data generation function
def generate_sample_data():
    np.random.seed(0)
    dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
    amounts = np.random.randint(1, 100, size=len(dates))  # Random amounts
    data = pd.DataFrame({'PurchaseDate': dates, 'Amount': amounts})
    return data

@app.route('/')
def index():
    # Generate sample data
    data = generate_sample_data()

    # Ensure 'Amount' is numeric
    data['Amount'] = pd.to_numeric(data['Amount'], errors='coerce')

    # Use resampling to sum monthly sales
    monthly_sales = data.set_index('PurchaseDate').resample('M').sum()['Amount']

    # Plot monthly sales trend and save as PNG
    monthly_sales_fig = monthly_sales.plot(kind='line', title='Monthly Sales Trend', marker='o').get_figure()
    monthly_sales_fig.savefig("static/monthly_sales.png")
    
    # Close the figure after saving to avoid display issues
    plt.close(monthly_sales_fig)

    return render_template("index.html", image="static/monthly_sales.png")

if __name__ == '__main__':
    app.run(debug=True)
