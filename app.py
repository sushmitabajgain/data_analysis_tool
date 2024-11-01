from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

app = Flask(__name__)

# Generate sample data
def generate_sample_data():
    # Create a date range for the past 12 months
    date_range = pd.date_range(start='2023-01-01', periods=12, freq='M')
    
    # Generate random sales data
    np.random.seed(0)  # For reproducibility
    sales_data = np.random.randint(1000, 5000, size=12)  # Random sales amounts
    
    # Create a DataFrame
    data = pd.DataFrame({'PurchaseDate': date_range, 'Amount': sales_data})
    return data

@app.route('/')
def index():
    # Generate sample data
    data = generate_sample_data()

    # Group by month and sum the Amount
    monthly_sales = data.groupby(data['PurchaseDate'].dt.to_period('M')).sum(numeric_only=True)

    # Plot monthly sales trend and save as PNG
    monthly_sales_fig = monthly_sales.plot(kind='line', title='Monthly Sales Trend', marker='o').get_figure()
    monthly_sales_fig.savefig("static/monthly_sales.png")
    
    # Close the figure after saving to avoid display issues
    plt.close(monthly_sales_fig)

    return render_template("index.html", image="static/monthly_sales.png")

if __name__ == "__main__":
    app.run(debug=True)
