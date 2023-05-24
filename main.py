from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
# import redis
from ecommerce.user.routes import router as user_router
from ecommerce.products.routes import router as product_router
from ecommerce.cart.routes import router as cart_router
from ecommerce.orders.routes import router as order_router
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from dataframe import df
import os

# import debugpy
# debugpy.listen(('0.0.0.0', 5678))

app = FastAPI(
    title="Ecommerce API",
    version="0.0.1",
)

# r = redis.Redis(host='redis', port=6379, db=0)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)

@app.post("/generate_chart")
def generate_chart():
    # Generate the bar chart
    df.plot(kind="bar")
    plt.title("Bar Chart")
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")

    # Save the chart to a temporary file
    chart_file = "test.png"
    plt.savefig(chart_file)
    plt.close()

    # Read the saved chart file
    with open(chart_file, "rb") as file:
        chart_data = file.read()

    # Remove the temporary chart file
    os.remove(chart_file)

    # Return the chart data
    return chart_data


@app.get("/chart/")
async def get_chart():
    df = pd.DataFrame({
        'Fruit': ['Apples', 'Bananas', 'Grapes'],
        'Amount': [50, 15, 7]
    })

    fig = plt.figure()
    df.plot.bar(x='Fruit', y='Amount', rot=0)

    image_path = 'chart.png'
    plt.savefig(image_path)
    plt.close(fig)  # Close the figure

    if not Path(image_path).exists():
        raise HTTPException(status_code=404, detail="Image not found")

    response = FileResponse(image_path, media_type='image/png')
    # os.remove(image_path)  # Delete the image file after returning it

    return response