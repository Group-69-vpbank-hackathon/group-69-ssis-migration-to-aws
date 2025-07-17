import csv
import uuid
import random
from datetime import datetime, timedelta


def random_date(start, end):
    """
    Trả về ngày ngẫu nhiên giữa start và end
    """
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)


def generate_transactions(num_rows=100, output_file="transactions.csv"):
    headers = ["transaction_id", "user_id", "amount", "date"]
    today = datetime.today()
    six_months_ago = today - timedelta(days=180)

    with open(output_file, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for _ in range(num_rows):
            transaction = {
                "transaction_id": str(uuid.uuid4()),
                "user_id": random.randint(1, 20),
                "amount": round(random.uniform(10, 5000), 2),
                "date": random_date(six_months_ago, today).strftime("%Y-%m-%d"),
            }
            writer.writerow(transaction)

    print(f"✅ Generated {num_rows} transactions to {output_file}")


if __name__ == "__main__":
    generate_transactions()
