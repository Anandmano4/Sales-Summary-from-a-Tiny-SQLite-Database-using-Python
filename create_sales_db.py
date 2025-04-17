import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def create_and_insert_data():
    conn = sqlite3.connect("sales_data.db")
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        product TEXT,
        quantity INTEGER,
        price REAL
    )""")
    
    # Sample data
    sample_data = [
        ('Product A', 10, 15.0),
        ('Product B', 5, 25.0),
        ('Product C', 8, 12.5),
        ('Product A', 7, 15.0),
        ('Product B', 3, 25.0),
        ('Product C', 6, 12.5)
    ]
    
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
    conn.commit()
    conn.close()
    print("Database created and data inserted successfully.")

def query_sales_data():
    conn = sqlite3.connect("sales_data.db")
    query = """
    SELECT 
        product, 
        SUM(quantity) AS total_quantity, 
        SUM(quantity * price) AS revenue 
    FROM sales 
    GROUP BY product
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def plot_sales_data(df):
    # Plot both revenue and quantity sold by product
    plt.figure(figsize=(10, 6))

    # Create two bar charts: one for quantity and one for revenue
    bar_width = 0.35
    index = range(len(df))

    fig, ax = plt.subplots()

    ax.bar(index, df['total_quantity'], bar_width, label='Quantity Sold', color='skyblue')
    ax.bar([i + bar_width for i in index], df['revenue'], bar_width, label='Revenue', color='orange')

    ax.set_xlabel('Product')
    ax.set_ylabel('Total Quantity / Revenue')
    ax.set_title('Quantity Sold and Revenue by Product')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(df['product'], rotation=45)
    ax.legend()

    plt.tight_layout()
    plt.show()

    # Save the chart if needed
    plt.savefig("sales_dual_chart.png")

# Run the functions
create_and_insert_data()
sales_data = query_sales_data()
print(sales_data)
plot_sales_data(sales_data)