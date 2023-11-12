from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel

import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Use Depends directly, without Annotated
db_dependency = Depends(get_db)

# Post product
@app.post("/post/product", status_code=status.HTTP_201_CREATED)
async def create_product(
    name: str | None = None,
    description: str | None = None,
    price: int | None = None, db: Session = db_dependency):
    db_post = models.Product(name=name, description=description, price=price)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# Get sales between date range ( 2023-01-01  -  2023-01-01)
@app.get("/sales/{start_date}/{end_date}", status_code=status.HTTP_200_OK)
async def get_sales_range(
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = db_dependency
):
    """
    Example:
    ```json
    {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
    ```
    """
    try:
        sales_data = db.query(models.Sale).filter(
            models.Sale.created_at >= start_date,
            models.Sale.created_at <= end_date
        ).all()

        return sales_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get sales againt product id
@app.get("/sales/{type_product}", status_code=status.HTTP_200_OK)
async def get_sales_product(
    type_product: int,
    db: Session = db_dependency
):
    """
    Example:
    ```json
    {
        "type_product": 1
    }
    ```
    """    
    try:
        query = db.query(models.Sale)

        query = query.filter(models.Sale.product_id == type_product)

        sales_data = query.all()

        return sales_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get sales againt category id     
@app.get("/sales/{type_category}", status_code=status.HTTP_200_OK)
async def get_sales_product(
    type_category: int,
    db: Session = db_dependency
): 
    """
    Example:
    ```json
    {
        "type_category": 1
    }
    ```
    """  
    try:
        query = db.query(models.Sale)

        query = query.filter(models.Sale.category_id == type_category)

        sales_data = query.all()

        return sales_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))   

# Get sales againt date range, category id, product id     
@app.get("/sales/{start_date}/{end_date}/{type_product}/{type_category}", status_code=status.HTTP_200_OK)
async def get_sales(
    start_date: str | None = None,
    end_date: str | None = None,
    type_product: int = None,
    type_category: int = None,
    db: Session = db_dependency
):
    """
    Example:
    ```json
    {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "type_product": 1,
        "type_category": 1,
    }
    ```
    """  
    try:
        sales_data = db.query(models.Sale).filter(
            models.Sale.created_at >= start_date,
            models.Sale.created_at <= end_date,
            models.Sale.product_id == type_product,
            models.Sale.category_id == type_category
        ).all()

        return sales_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Revenue against date range ( daily, monthly, annualy )
@app.get("/revenue/{start_date}/{end_date}", status_code=status.HTTP_200_OK)
async def get_revenue_period(
    start_date: str | None = None,
    end_date: str | None = None,
    db: Session = db_dependency
):
    """
    Example:
    ```json
    {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31"
    }
    ```
    """  
    try:
        revenue_data = db.query(models.Revenue).filter(
            models.Revenue.created_at >= start_date,
            models.Revenue.created_at <= end_date,
        ).all()

        return revenue_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Revenue against category id
@app.get("/revenue/{type_category}", status_code=status.HTTP_200_OK)
async def get_revenue_category(
    type_category: int = None,
    db: Session = db_dependency
):
    """
    Example:
    ```json
    {
        "type_category": 1
    }
    ```
    """  
    try:
        revenue_data = db.query(models.Revenue).filter(
            models.Revenue.category_id == type_category
        ).all()

        return revenue_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get Revenue against date range ( daily, monthly, annualy ) and category id    
@app.get("/revenue/{start_date}/{end_date}/{type_category}", status_code=status.HTTP_200_OK)
async def get_revenue(
    start_date: str | None = None,
    end_date: str | None = None,
    type_category: int = None,
    db: Session = db_dependency
):
    """
    Example:
    ```json
    {
        "start_date": "2023-01-01",
        "end_date": "2023-12-31",
        "type_category": 1,
    }
    ```
    """ 
    try:
        revenue_data = db.query(models.Revenue).filter(
            models.Revenue.created_at >= start_date,
            models.Revenue.created_at <= end_date,
            models.Revenue.category_id == type_category
        ).all()

        return revenue_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    

# Get all inventory
@app.get("/inventory", status_code=status.HTTP_201_CREATED)
async def get_inventory(db: Session = db_dependency):
    inventory = db.query(models.Inventory).all()
    return inventory

# Update an inventory
@app.put("/inventory/{inventory_id}", status_code=status.HTTP_201_CREATED)
async def update_inventory(
    id:  int = None,
    quantity: int = None,
    product_id: int = None,
    category_id: int = None,
    db: Session = db_dependency):
    
    """
    Example:
    ```json
    {
        "id": 1,
        "quantity": 1,
        "product_id": 1,
        "category_id": 1,
    }
    ```
    """ 
    # Check if the product exists
    db_inventory = db.query(models.Inventory).filter(models.Inventory.id == id).first()
    if not db_inventory:
        raise HTTPException(status_code=404, detail="Inventory not found")

    # Update the product properties
    if quantity:
        db_inventory.quantity = quantity
    if product_id:
        db_inventory.product_id = product_id
    if category_id:
        db_inventory.category_id = category_id

    # Commit the changes to the database
    db.commit()
    db.refresh(db_inventory)

    return db_inventory

# Inventory low stock
@app.get("/inventory/low/stocks", status_code=status.HTTP_201_CREATED)
async def low_stock_inventory(db: Session = db_dependency):
    """
   Stock alerts for items less than 5 in quantity
    """     
    try:
        low_inventory = db.query(models.Inventory).filter(
            models.Inventory.quantity < 5
        ).all()

        return low_inventory
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))    