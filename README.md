# TradeX

**TradeX** is a dummy stock trading platform built with Django that simulates stock trading activities such as buying and selling stocks, portfolio management, and stock price fluctuations. This platform is designed as a REST API using Django REST Framework (DRF), allowing interaction via HTTP requests.

## Features

- **User Management**: 
  - User registration and authentication.
  - Users can view their accounts.
  
- **Stock Management**:
  - Admin can add, update, or delete stocks.
  - Users can view stock details.
  
- **Price Fluctuation**:
  - Stock prices fluctuate using management command.

- **Portfolio and Transactions**:
  - Users can track transactions, and view price history.
  - Users can manage their portfolios, including buying and selling stocks.
  - Admin can approve the selling of the stocks using a management command or API. 
  
- **Watchlist**:
  - Users can add stocks to their watchlist and receive alerts when a stock hits their target price.
  - Alerts are emailed using Celery tasks with Redis as the message broker.

## Technologies Used

- **Django**: Backend framework.
- **Django REST Framework**: For building the REST API.
- **Celery**: For handling asynchronous tasks like stock price fluctuations.
- **Redis**: As a message broker for Celery.
- **PostgreSQL**: Database used for the application.

## Prerequisites

- **Python 3.8+**
- **PostgreSQL**
- **Redis**

## Installation

### 1. Clone the Repository

```console
git clone https://github.com/MARIA-AZRAR/TradeX.git
cd tradex
```

### 2. Install Dependencies

```console
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root and add your PostgreSQL and Redis credentials:

```console
DB_NAME=<your_database_name>
DB_USER=<your_database_user>
DB_PASSWORD=<your_database_password>
DB_HOST=localhost
DB_PORT=5432
```

### 4. Set Up Database

Make sure PostgreSQL is running, then create the database:

```console
psql -U postgres
CREATE DATABASE tradex;
CREATE USER <your_database_user> WITH PASSWORD '<your_database_password>';
GRANT ALL PRIVILEGES ON DATABASE tradex TO <your_database_user>;
```

Apply the migrations:

```console
python manage.py migrate
```

### 5. Create a Superuser (Admin)

```console
python manage.py createsuperuser
```

### 6. Set Up Celery and Redis

Make sure Redis is running. Then, to start the Celery worker:

```console
python -m celery -A TraderX worker -l info --pool=solo
```

### 8. Run the Development Server

```console
python manage.py runserver
```

You can now access the API at `http://127.0.0.1:8000/`.

### Stocks API Endpoints

#### Get Stocks List
- **Endpoint**: `{{base_url}}/stocks/`
- **Method**: GET
- **Description**: Retrieve the list of all stocks.

#### Get Stock Detail
- **Endpoint**: `{{base_url}}/stocks/6`
- **Method**: GET
- **Description**: Retrieve detailed information about a specific stock with ID 6.

#### Delete Stock
- **Endpoint**: `{{base_url}}/stocks/6/`
- **Method**: DELETE
- **Description**: Delete the stock with ID 6.

#### Create Stock
- **Endpoint**: `{{base_url}}/stocks/`
- **Method**: POST
- **Description**: Create a new stock.

#### Update Stock
- **Endpoint**: `{{base_url}}/stocks/5/`
- **Method**: PUT/PATCH
- **Description**: Update the stock with ID 5.

#### Get Price History
- **Endpoint**: `{{base_url}}/stocks/history/?symbol=TECH`
- **Method**: GET
- **Description**: Retrieve the price history for the stock with the symbol `TECH`.

### User Authentication Endpoints

#### User Registration
- **Endpoint**: `{{base_url}}/auth/registration`
- **Method**: POST
- **Description**: Register a new user account.

#### User Login
- **Endpoint**: `{{base_url}}/auth/login`
- **Method**: POST
- **Description**: Authenticate a user and return a token for session management.

#### User Logout
- **Endpoint**: `{{base_url}}/auth/logout`
- **Method**: POST
- **Description**: Logout the authenticated user.

#### User Account
- **Endpoint**: `{{base_url}}/user/account`
- **Method**: GET
- **Description**: Retrieve details of the logged-in user's account.

### Trading (Portfolios & Transactions) Endpoints

#### Get Portfolio
- **Endpoint**: `{{base_url}}/portfolios/`
- **Method**: GET
- **Description**: Retrieve the current user's portfolio details.

#### Get Transactions
- **Endpoint**: `{{base_url}}/transaction/`
- **Method**: GET
- **Description**: Retrieve a list of all transactions made by the user.

#### Get Transaction Details
- **Endpoint**: `{{base_url}}/transaction/2/`
- **Method**: GET
- **Description**: Retrieve details of a specific transaction with ID 2.

#### Get Admin Portfolios
- **Endpoint**: `{{base_url}}/api/admin/portfolios/`
- **Method**: GET
- **Description**: Retrieve the list of portfolios for all users (Admin only).

#### Create Transaction
- **Endpoint**: `{{base_url}}/make-transaction/`
- **Method**: POST
- **Description**: Create a new stock transaction (buy/sell).

#### Update Transaction Status
- **Endpoint**: `{{base_url}}/transaction/`
- **Method**: PUT/PATCH
- **Description**: Update the status of an existing transaction.


### Watchlist API Endpoints

#### Get Watchlist
- **Endpoint**: `{{base_url}}/watchlist/`
- **Method**: GET
- **Description**: Retrieve the current user's watchlist.

#### Add to Watchlist
- **Endpoint**: `{{base_url}}/watchlist/`
- **Method**: POST
- **Description**: Add a new stock to the user's watchlist.

#### Update Watchlist
- **Endpoint**: `{{base_url}}/watchlist/1/`
- **Method**: PUT
- **Description**: Update the alert price for a stock in the watchlist.
  
#### Delete from Watchlist
- **Endpoint**: `{{base_url}}/watchlist/{{id}}/`
- **Method**: DELETE
- **Description**: Remove a stock from the user's watchlist.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Feel free to fork this repository and create pull requests. All contributions are welcome.
