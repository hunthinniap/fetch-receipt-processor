from datetime import datetime


def calculate_points(receipt: dict) -> int:
    points = 0

    # Rule 1: One point for every alphanumeric character in the retailer name
    retailer_name = receipt.get("retailer", "")
    points += sum(c.isalnum() for c in retailer_name)

    # Rule 2: 50 points if the total is a round dollar amount with no cents
    total = float(receipt.get("total", 0))
    if total.is_integer():
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25
    if total % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt
    items = receipt.get("items", [])
    points += (len(items) // 2) * 5

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer.
    # The result is the number of points earned.

    for item in items:
        description = item.get("shortDescription", "").strip()
        price = float(item.get("price", 0))
        if len(description) % 3 == 0:
            points += -(-price * 0.2)

    # Rule 6: 6 points if the day in the purchase date is odd
    purchase_date = receipt.get("purchaseDate", "")
    if purchase_date:
        day = datetime.strptime(purchase_date, "%Y-%m-%d").day
        if day % 2 == 1:
            points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00pm and before 4:00pm
    purchase_time = receipt.get("purchaseTime", "")
    if purchase_time:
        purchase_hour = datetime.strptime(purchase_time, "%H:%M").hour
        if 14 <= purchase_hour < 16:
            points += 10

    return points
