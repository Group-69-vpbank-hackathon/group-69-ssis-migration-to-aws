import csv
from faker import Faker

fake = Faker()

# Mở file để ghi
with open("users.csv", mode="w", newline="", encoding="utf-8") as file:
    fieldnames = ["user_id", "username", "email"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()

    for user_id in range(1, 1001):
        username = fake.user_name()
        email = fake.email()
        writer.writerow({"user_id": user_id, "username": username, "email": email})

print("✅ Đã tạo file users.csv với 1000 users.")
