import os
import csv
from datetime import datetime, timedelta

OUTPUT_DIR = "output_partitioned_csv"
START_DATE = "2025-07-01"
END_DATE = "2025-07-10"


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def generate_sample_data(date_str, num_records=10):
    """
    Generate a list of sample rows with the given date.
    """
    rows = []
    for i in range(1, num_records + 1):
        rows.append(
            {
                "id": i,
                "transaction_date": date_str,
                "amount": round(1000 * i * 1.1, 2),
                "description": f"Sample transaction {i}",
            }
        )
    return rows


def write_partition_csv(date_str):
    partition_path = os.path.join(OUTPUT_DIR, f"date={date_str}")
    ensure_dir(partition_path)
    file_path = os.path.join(partition_path, "part-0000.csv")

    rows = generate_sample_data(date_str)

    with open(file_path, mode="w", newline="") as csvfile:
        fieldnames = ["id", "transaction_date", "amount", "description"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print(f"Wrote {len(rows)} records to {file_path}")


def main():
    start_dt = datetime.strptime(START_DATE, "%Y-%m-%d").date()
    end_dt = datetime.strptime(END_DATE, "%Y-%m-%d").date()

    current_date = start_dt
    while current_date <= end_dt:
        date_str = current_date.strftime("%Y-%m-%d")
        write_partition_csv(date_str)
        current_date += timedelta(days=1)


if __name__ == "__main__":
    main()
