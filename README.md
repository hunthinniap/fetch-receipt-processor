
# **Receipt Processing API Documentation**

## **API Overview**

This API allows you to process receipts and calculate points based on the contents of the receipts. You can process a receipt to generate an ID, and then retrieve the points associated with that receipt ID.

---

## **API Endpoints**

### **1. Process Receipts**

- **Endpoint**: `/receipts/process`
- **Method**: `POST`
- **Description**: 
  - This endpoint accepts a JSON receipt and returns a JSON object containing a unique ID for the receipt.
  - The points associated with the receipt are calculated based on several rules.

---

### **2. Get Points**

- **Endpoint**: `/receipts/{id}/points`
- **Method**: `GET`
- **Description**:
  - This endpoint retrieves the points awarded for the receipt specified by the `id`.
- **Request URL Parameters**:
  - `id`: The unique ID of the receipt, returned by the `/receipts/process` endpoint.
  

## **Points Calculation Rules**

The points are calculated based on the following rules:

1. **Retailer Name**: One point for every alphanumeric character in the retailer name.
2. **Total Amount**:
   - 50 points if the total is a round dollar amount (no cents).
   - 25 points if the total is a multiple of 0.25.
3. **Items**: 5 points for every two items on the receipt.
4. **Item Descriptions**: If the length of an item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. This value is added to the points.
5. **Purchase Date**: 6 points if the day in the purchase date is odd.
6. **Purchase Time**: 10 points if the time of purchase is between 2:00 PM and 4:00 PM.

---

## **Running the Application Locally**

### **Prerequisites**
- Python 3.x
- Redis (installed locally or running via Docker)
- Flask and Redis Python libraries

### **Steps to Run Locally**

1. **Install dependencies**:
   - Create a virtual environment (optional but recommended):
     ```bash
     python -m venv venv
     ```
   - Activate the virtual environment:
     - **Linux/macOS**: 
       ```bash
       source venv/bin/activate
       ```
     - **Windows**:
       ```bash
       .env\Scriptsctivate
       ```
   - Install required packages:
     ```bash
     pip install -r requirements.txt
     ```


2. **Run the Flask App**:
   - Set the `REDIS_HOST` to `localhost` (or leave it as default in the `.env` file).
   - Run the Flask app:
     ```bash
     python app.py
     ```

3. **Access the API**:
   - The API will be available at `http://127.0.0.1:5000`.

4. **Run the tests**: 
    You can run the tests using the following command:

    ```bash
    pytest
---

## **Running the Application with Docker**

### **Prerequisites**
- Docker
- Docker Compose

### **Steps to Run with Docker**

1. **Build and Start Docker Containers**:
   Run the following command to start the app and Redis in Docker containers:
   ```bash
   docker-compose up --build
   ```

2. **Access the API**:
   The API will be available at `http://127.0.0.1:5001`.

3. **Run the tests**:

    You can run the tests using the following command:

    ```bash
    docker-compose up -d
    docker-compose run --rm test
    ```

---

## **Testing the Application**

### **1. Test the API using `curl`**

You can test the API using `curl` commands. Here’s an example of how to use `curl` to call the API:

#### **1.1 Process Receipt**

To process a receipt and get an ID:
5000 for running locally; 5001 for running on docker
```bash
curl -X POST -H "Content-Type: application/json" \
-d @test_receipts/simple-receipt.json \
http://127.0.0.1:5001/receipts/process
```

This will return a response with a receipt ID:
```json
{
  "id": "0c92e533-e25b-4a82-b5e8-5420d793cf31"
}
```

#### **1.2 Get Points for Receipt**

To get the points for a receipt, replace `{id}` with the ID from the previous response:

```bash
curl -X GET http://localhost:5001/receipts/0c92e533-e25b-4a82-b5e8-5420d793cf31/points
```

This will return the points:
```json
{
  "points": 31
}
```

---

