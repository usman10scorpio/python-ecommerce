# Python-Ecommerce

Learning project

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
- [Database Schema](#Database-Schema)

## Introduction

A small ecommerce based application

## Features

List some key features of your project.

- Post product
- Get sales between date range
- Get sales againt product id
- Get sales againt category id     
- Get sales againt date range, category id, product id     
- Get revenue against date range ( daily, monthly, annualy )
- Get revenue against category id
- Get revenue against date range ( daily, monthly, annualy ) and category id    
- Get all inventory
- Update an inventory
- Inventory low stock

## Getting Started

- Clone the repository by running below command
```
  git clone https://github.com/usman10scorpio/python-ecommerce.git
```
- After that we need to initialize virtual environment for that run below command
```
  python3 -m venv env
```
```
  source env/bin/activate
```
- Then we need to install required packages in order to operate for that we have to install few packages. Below command will do that
```
  pip install fastapi uvicorn sqlalchemy pymysql
```
- Lastly we need a web page where we can play with api endpoints that will be http://127.0.0.1:8000/docs#. Run below command and you will see a page with your exposed end points
```
  uvicorn main:app --reload
```

### Prerequisites

- Vscode
- python 3+
- pip
- fastapi
- uvicorn
- sqlalchemy
- pymysql
- mysql
- mysql workbench

## Database Schema

Relationship : Table product must be associated with category table

### Table 1: Products

| Column Name  | Data Type     | Description                   |
| ------------ | ------------- | ----------------------------- |
| id           | Integer       | Primary key                   |
| name         | String(100)   | Name of the product           |
| description  | String(500)   | Description of the product    |
| price        | Integer       | Price of the product          |
| created_at   | DateTime      | Timestamp of creation         |
| updated_at   | DateTime      | Timestamp of last update      |
| category_id  | Integer       | Foreign key to Categories     |

### Table 2: Categories

| Column Name  | Data Type     | Description                   |
| ------------ | ------------- | ----------------------------- |
| id           | Integer       | Primary key                   |
| name         | String(100)   | Name of the category          |
| description  | String(500)   | Description of the category   |
| created_at   | DateTime      | Timestamp of creation         |
| updated_at   | DateTime      | Timestamp of last update      |

Relationship : Table Inventory must be associated with category and product table

### Table 3: Inventory

| Column Name  | Data Type     | Description                   |
| ------------ | ------------- | ----------------------------- |
| id           | Integer       | Primary key                   |
| quantity     | Integer       | Quantity of the product       |
| created_at   | DateTime      | Timestamp of creation         |
| updated_at   | DateTime      | Timestamp of last update      |
| product_id   | Integer       | Foreign key to Products       |
| category_id  | Integer       | Foreign key to Categories     |

Relationship : Table Sale must be associated with category and product table

### Table 4: Sale

| Column Name  | Data Type     | Description                   |
| ------------ | ------------- | ----------------------------- |
| id           | Integer       | Primary key                   |
| total_price  | Integer       | Total price of the sale       |
| quantity     | Integer       | Quantity of items sold        |
| created_at   | DateTime      | Timestamp of sale creation    |
| updated_at   | DateTime      | Timestamp of last update      |
| product_id   | Integer       | Foreign key to Products       |
| category_id  | Integer       | Foreign key to Categories     |

Relationship : Table revenue must be associated with sale and category table

### Table 5: revenue

| Column Name           | Data Type     | Description                        |
| --------------------- | ------------- | ---------------------------------- |
| id                    | Integer       | Primary key                        |
| revenue_sales         | Integer       | revenue from product sales         |
| revenue_other         | Integer       | revenue from other sources         |
| revenue_total         | Integer       | Total revenue (sales + other)      |
| created_at            | DateTime      | Timestamp of revenue creation      |
| updated_at            | DateTime      | Timestamp of last update           |
| sale_id               | Integer       | Foreign key to Sales               |
| category_id           | Integer       | Foreign key to Categories          |

## Database usage

- Open mysql workbench. You will see a box saying `local instance 3306`. If you already have not made a connection, you can always go to `Database` > `Manage server connections`, and make one.

- Click on your new / already made connection. Click on Schemas tab. Right click over there and click `Create Schema` 

- A pop up window will appear, type your schema name, for this project I used, `ecommerce`. Click `Apply`. You will see the message `SQL script was successfully applied to the database.`

- Inside the schema there will be no tables, thats where our `database.py` and `models.py` come into play. Save your models info in `models.py` file. Hit save. Then go to `mysql workbench` and refresh your schema tables.

- In `File` > `New Query Tab` click on it and paste the query from `dump.sql`. This will populate all the data in respective tables
