import pyodbc
import random
from faker import Faker
from datetime import datetime

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=localhost,1433;DATABASE=VPB_RAW_DATA;UID=sa;PWD=Abc1234secure'
)
cursor = conn.cursor()
fake = Faker("vi_VN")

def fake_row_TMP_EFZ_FT_HIS():
    return {
        "REF_NO": fake.uuid4(),
        "TRANSACTION_TYPE": random.choice(["TRANSFER", "WITHDRAWAL", "DEPOSIT"]),
        "DEBIT_ACCT_NO": fake.bban(),
        "DEBIT_CURRENCY": random.choice(["VND", "USD", "EUR"]),
        "AMOUNT_DEBITED": str(round(random.uniform(1000000, 50000000), 2)),
        "DEBIT_VALUE_DATE": fake.date(pattern="%Y-%m-%d"),
        "CREDIT_ACCT_NO": fake.bban(),
        "CREDIT_CURRENCY": random.choice(["VND", "USD", "EUR"]),
        "AMOUNT_CREDITED": str(round(random.uniform(1000000, 50000000), 2)),
        "CREDIT_VALUE_DATE": fake.date(pattern="%Y-%m-%d"),
        "DEBIT_COMP_CODE": fake.lexify(text="???"),
        "CREDIT_COMP_CODE": fake.lexify(text="???"),
        "BUSINESS_DATE": datetime.today().strftime("%Y-%m-%d"),
        "RECORD_STATUS": random.choice(["PENDING", "SUCCESS", "FAILED"]),
        "SERVICE_CHANNEL": random.choice(["ATM", "IB", "MOBILE"]),
        "BEN_ACCT_NO": fake.bban(),
        "ATM_RE_NUM": fake.bothify(text="ATM#######"),
        "CO_CODE": fake.lexify(text="??"),
        "VPB_SERVICE": fake.word(),
        "CONTACT_NUM": fake.phone_number(),
        "DEBIT_CUSTOMER": fake.name(),
        "BOND_CODE": fake.lexify(text="BOND????"),
        "PR_CARD_NO": fake.credit_card_number(),
        "BEN_LEGAL_ID": fake.ssn(),
        "BEN_ID_CUSTOMER": fake.uuid4(),
        "DEBIT_THEIR_REF": fake.bothify(text="REF######"),
        "CREDIT_CARD": fake.credit_card_number(),
        "PROCESSING_DATE": fake.date(pattern="%Y-%m-%d"),
        "CREDIT_AMOUNT": str(round(random.uniform(1000000, 50000000), 2)),
        "DEBIT_AMOUNT": str(round(random.uniform(1000000, 50000000), 2)),
        "CREDIT_THEIR_REF": fake.bothify(text="REF######"),
        "AT_AUTH_CODE": fake.lexify(text="??????"),
        "TOTAL_CHARGE_AMT": str(round(random.uniform(10000, 500000), 2)),
        "ATM_TERM_ID": fake.bothify(text="TERM###"),
        "PROFIT_CENTRE_CUST": fake.lexify(text="???"),
        "TREASURY_RATE": str(round(random.uniform(10, 50), 2)),
        "SOURCE_OF_FCY": random.choice(["EXPORT", "LOAN", "SALE"]),
        "VALUE_DT_LOCAL": fake.date(pattern="%Y-%m-%d"),
        "VAT_NAME": fake.company(),
        "R_CI_CODE": fake.lexify(text="??"),
        "PURPOSE": fake.sentence(nb_words=4),
        "B_ID_ISSUE_PLAC": fake.lexify(text="VN??"),
        "CARD_NUMBER": fake.credit_card_number(),
        "TYPE_OF_DOC": random.choice(["01", "02", "03"]),
        "VAT_CIF_NO": fake.ean(length=13),
        "AUTHORISER": fake.name(),
        "VPB_AUTHORISER": fake.name(),
        "BAL_AFT_TXN": str(round(random.uniform(0, 999999999), 2)),
        "AT_MC_TRANS": fake.lexify(text="TRN####"),
        "TOTAL_TAX_AMOUNT": str(round(random.uniform(10000, 500000), 2)),
        "AUTH_DATE": fake.date(pattern="%Y-%m-%d"),
        "SENDING_ACCT": fake.bban(),
        "DEPT_CODE": fake.lexify(text="D??"),
        "VPB_INPUTTER": fake.name()
    }

def fake_row_TMP_EFZ_FT_HIS_DETAILS():
    return {
        "REF_NO": fake.uuid4(),
        "M": random.randint(1, 100),
        "S": random.randint(1, 100),
        "DATE_TIME": fake.date_time().strftime("%Y-%m-%d %H:%M:%S"),
        "BUSINESS_DATE": fake.date(pattern="%Y-%m-%d"),
        "PAYMENT_DETAILS": fake.sentence(),
        "TXN_DETAIL_VPB": fake.text(100),
        "TXN_DETAIL": fake.text(100),
        "RECEIVING_NAME": fake.name(),
        "REF_DATA_VALUE": fake.lexify(text="VAL###"),
        "REF_DATA_ITEM": fake.lexify(text="ITEM##"),
        "INPUTTER": fake.name(),
        "BEN_CUSTOMER": fake.name(),
        "RECEIVING_ADDR": fake.address(),
        "ORDERING_CUST": fake.company(),
        "SENDING_ADDR": fake.address(),
        "COMMISSION_AMT": str(round(random.uniform(10000, 1000000), 2))
    }

def fake_row_TMP_EFZ_FUNDS_TRANSFER():
    return {
        "REF_NO": fake.uuid4(),
        "TRANSACTION_TYPE": random.choice(["TRANSFER", "DEPOSIT", "WITHDRAW"]),
        "DEBIT_ACCT_NO": fake.bban(),
        "DEBIT_CURRENCY": random.choice(["VND", "USD"]),
        "AMOUNT_DEBITED": str(round(random.uniform(100000, 10000000), 2)),
        "DEBIT_VALUE_DATE": fake.date(),
        "CREDIT_ACCT_NO": fake.bban(),
        "CREDIT_CURRENCY": random.choice(["VND", "USD"]),
        "AMOUNT_CREDITED": str(round(random.uniform(100000, 10000000), 2)),
        "CREDIT_VALUE_DATE": fake.date(),
        "DEBIT_COMP_CODE": fake.lexify("???"),
        "CREDIT_COMP_CODE": fake.lexify("???"),
        "BUSINESS_DATE": fake.date(),
        "RECORD_STATUS": random.choice(["PENDING", "DONE"]),
        "SERVICE_CHANNEL": random.choice(["ATM", "IB"]),
        "BEN_ACCT_NO": fake.bban(),
        "BOND_CODE": fake.lexify("BOND####"),
        "VPB_SERVICE": fake.word(),
        "CONTACT_NUM": fake.phone_number(),
        "DEBIT_CUSTOMER": fake.name(),
        "ATM_RE_NUM": fake.bothify("ATM###"),
        "CO_CODE": fake.lexify("CC"),
        "PR_CARD_NO": fake.credit_card_number(),
        "BEN_LEGAL_ID": fake.ssn(),
        "BEN_ID_CUSTOMER": fake.uuid4(),
        "DEBIT_THEIR_REF": fake.lexify("REF####"),
        "CREDIT_CARD": fake.credit_card_number(),
        "PROCESSING_DATE": fake.date(),
        "CREDIT_AMOUNT": str(round(random.uniform(100000, 10000000), 2)),
        "DEBIT_AMOUNT": str(round(random.uniform(100000, 10000000), 2)),
        "CREDIT_THEIR_REF": fake.lexify("REF####"),
        "AT_AUTH_CODE": fake.lexify("AUTH##"),
        "TOTAL_CHARGE_AMT": str(round(random.uniform(1000, 100000), 2)),
        "ATM_TERM_ID": fake.lexify("ATM###"),
        "PROFIT_CENTRE_CUST": fake.lexify("PCC"),
        "VAT_CIF_NO": fake.ean(length=13),
        "AUTHORISER": fake.name(),
        "VPB_AUTHORISER": fake.name(),
        "TREASURY_RATE": str(round(random.uniform(10, 50), 2)),
        "TYPE_OF_DOC": random.choice(["01", "02", "03"]),
        "SOURCE_OF_FCY": random.choice(["SALE", "LOAN"]),
        "VALUE_DT_LOCAL": fake.date(),
        "VAT_NAME": fake.company(),
        "R_CI_CODE": fake.lexify("RCI"),
        "PURPOSE": fake.sentence(),
        "B_ID_ISSUE_PLAC": fake.lexify("VN##"),
        "BAL_AFT_TXN": str(round(random.uniform(0, 100000000), 2)),
        "AT_MC_TRANS": fake.lexify("TMC####"),
        "TOTAL_TAX_AMOUNT": str(round(random.uniform(1000, 50000), 2)),
        "AUTH_DATE": fake.date(),
        "SENDING_ACCT": fake.bban(),
        "DEPT_CODE": fake.lexify("D??"),
        "VPB_INPUTTER": fake.name()
    }

def fake_row_TMP_EFZ_FT_AFTER_COB():
    return {
        "REF_NO": fake.uuid4(),
        "TRANSACTION_TYPE": random.choice(["DEPOSIT", "TRANSFER"]),
        "DEBIT_ACCT_NO": fake.bban(),
        "DEBIT_CURRENCY": "VND",
        "AMOUNT_DEBITED": str(round(random.uniform(1_000_000, 10_000_000), 2)),
        "DEBIT_VALUE_DATE": fake.date(),
        "CREDIT_ACCT_NO": fake.bban(),
        "CREDIT_CURRENCY": "VND",
        "AMOUNT_CREDITED": str(round(random.uniform(1_000_000, 10_000_000), 2)),
        "CREDIT_VALUE_DATE": fake.date(),
        "DEBIT_COMP_CODE": fake.lexify("DCC###"),
        "CREDIT_COMP_CODE": fake.lexify("CCC###"),
        "BUSINESS_DATE": fake.date(),
        "RECORD_STATUS": "SUCCESS",
        "SERVICE_CHANNEL": random.choice(["IB", "ATM", "MOBILE"]),
        "BEN_ACCT_NO": fake.bban(),
        "BOND_CODE": fake.lexify("BOND####"),
        "VPB_SERVICE": fake.word(),
        "CONTACT_NUM": fake.phone_number(),
        "DEBIT_CUSTOMER": fake.name(),
        "ATM_RE_NUM": fake.bothify("ATM###"),
        "CO_CODE": fake.lexify("C###"),
        "PR_CARD_NO": fake.credit_card_number(),
        "BEN_LEGAL_ID": fake.ssn(),
        "BEN_ID_CUSTOMER": fake.uuid4(),
        "DEBIT_THEIR_REF": fake.lexify("REF####"),
        "CREDIT_CARD": fake.credit_card_number(),
        "SECTOR": "Banking",
        "PURPOSE": fake.sentence(),
        "VPB_BEN_COUNTRY": "VN",
        "ORDER_COUNTRY": "VN",
        "SOURCE_OF_FCY": "EXPORT",
        "PTTT": "TT",
        "DAO": "ABC",
        "KBB_RATE": str(round(random.uniform(1.0, 5.0), 2)),
        "PRODUCT_LINE": fake.bs(),
        "LD_CONTRACT_NO": fake.lexify("LD#####"),
        "AUTHORISER": fake.name(),
        "VAT_CIF_NO": fake.ean(length=13),
        "BC_BANK_SORT_CODE": fake.lexify("BC###"),
        "SENDING_ACCT": fake.bban(),
        "CLASSIFY_CODE": "A1",
        "DEPT_CODE": fake.lexify("D??"),
        "BEN_OUR_CHARGES": str(round(random.uniform(1000, 50000), 2)),
        "TERM": "Short",
        "TOTAL_CHARGE_AMT": str(round(random.uniform(1000, 100000), 2)),
        "VPB_INPUTTER": fake.name(),
        "VPB_AUTHORISER": fake.name(),
        "BOOKING_SERVICE": fake.word(),
        "CHARGES_ACCT_NO": fake.bban(),
        "PROFIT_CENTRE_CUST": fake.lexify("PCC"),
        "PROCESSING_DATE": fake.date(),
        "RECEIVER_BANK": fake.company(),
        "DELIVERY_INREF": fake.lexify("IN####"),
        "ATM_TERM_ID": fake.lexify("ATM###"),
        "TREASURY_RATE": str(round(random.uniform(10.0, 20.0), 2)),
        "VALUE_DT_LOCAL": fake.date(),
        "VAT_NAME": fake.company(),
        "R_CI_CODE": fake.lexify("RCI"),
        "B_ID_ISSUE_PLAC": fake.lexify("VN##"),
        "CARD_NUMBER": fake.credit_card_number(),
        "AT_AUTH_CODE": fake.lexify("AUTH##"),
        "AUTH_DATE": fake.date(),
        "CREDIT_CUSTOMER": fake.name(),
        "CREDIT_THEIR_REF": fake.lexify("REF####"),
        "TYPE_OF_DOC": random.choice(["01", "02"]),
        "DEBIT_AMOUNT": str(round(random.uniform(1_000_000, 10_000_000), 2)),
        "BAL_AFT_TXN": str(round(random.uniform(1_000_000, 100_000_000), 2)),
        "AT_MC_TRANS": fake.lexify("MC####"),
        "TOTAL_TAX_AMOUNT": str(round(random.uniform(5000, 100000), 2)),
    }

def insert_fake_data_TMP_EFZ_FT_AFTER_COB(n=300):
    sample = fake_row_TMP_EFZ_FT_AFTER_COB()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FT_AFTER_COB ({','.join(columns)}) VALUES ({placeholders})"
    for _ in range(n):
        row = fake_row_TMP_EFZ_FT_AFTER_COB()
        cursor.execute(sql, [row[c] for c in columns])
    conn.commit()
    print(f"✅ Inserted {n} rows into TMP_EFZ_FT_AFTER_COB.")

def fake_row_TMP_EFZ_FT_AFTER_COB_DETAILS():
    return {
        "REF_NO": fake.uuid4(),
        "M": random.randint(1, 100),
        "S": random.randint(1, 100),
        "DATE_TIME": fake.date_time().strftime("%Y-%m-%d %H:%M:%S"),
        "BUSINESS_DATE": fake.date(),
        "PAYMENT_DETAILS": fake.sentence(),
        "TXN_DETAIL_VPB": fake.text(50),
        "TXN_DETAIL": fake.text(50),
        "RECEIVING_NAME": fake.name(),
        "NAME_OF_GOODS": fake.word(),
        "ORDERING_BANK": fake.company(),
        "ACCT_WITH_BANK": fake.bban(),
        "REF_DATA_VALUE": fake.lexify("VAL###"),
        "INPUTTER": fake.name(),
        "ORDERING_CUST": fake.name(),
        "AZ_LD_NRDATE": fake.date(),
        "BEN_CUSTOMER": fake.name(),
        "SUSPENSE_ID": fake.lexify("SP###"),
        "REF_DATA_ITEM": fake.lexify("ITEM##"),
        "RECEIVING_ADDR": fake.address(),
        "SENDING_ADDR": fake.address(),
        "COMMISSION_AMT": str(round(random.uniform(1000, 100000), 2)),
    }

def insert_fake_data_TMP_EFZ_FT_AFTER_COB_DETAILS(n=500):
    sample = fake_row_TMP_EFZ_FT_AFTER_COB_DETAILS()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FT_AFTER_COB_DETAILS ({','.join(columns)}) VALUES ({placeholders})"
    for _ in range(n):
        row = fake_row_TMP_EFZ_FT_AFTER_COB_DETAILS()
        cursor.execute(sql, [row[c] for c in columns])
    conn.commit()
    print(f"✅ Inserted {n} rows into TMP_EFZ_FT_AFTER_COB_DETAILS.")

def insert_fake_data_TMP_EFZ_FUNDS_TRANSFER(n=300):
    sample = fake_row_TMP_EFZ_FUNDS_TRANSFER()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FUNDS_TRANSFER ({','.join(columns)}) VALUES ({placeholders})"
    for _ in range(n):
        row = fake_row_TMP_EFZ_FUNDS_TRANSFER()
        cursor.execute(sql, [row[c] for c in columns])
    conn.commit()
    print(f"✅ Inserted {n} rows into TMP_EFZ_FUNDS_TRANSFER.")

def insert_fake_data_TMP_EFZ_FT_HIS_DETAILS(n=500):
    sample = fake_row_TMP_EFZ_FT_HIS_DETAILS()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FT_HIS_DETAILS ({','.join(columns)}) VALUES ({placeholders})"
    for _ in range(n):
        row = fake_row_TMP_EFZ_FT_HIS_DETAILS()
        cursor.execute(sql, [row[c] for c in columns])
    conn.commit()
    print(f"✅ Inserted {n} rows into TMP_EFZ_FT_HIS_DETAILS.")

def insert_fake_data_TMP_EFZ_FT_HIS(n=100):
    sample = fake_row_TMP_EFZ_FT_HIS()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FT_HIS ({','.join(columns)}) VALUES ({placeholders})"

    for _ in range(n):
        row = fake_row_TMP_EFZ_FT_HIS()
        cursor.execute(sql, [row[col] for col in columns])

    conn.commit()
    print(f"✅ Inserted {n} fake rows into TMP_EFZ_FT_HIS.")

# ---
def insert_fake_data_TMP_EFZ_FT_HIS_with_ref(n=500):
    ref_list = []
    sample = fake_row_TMP_EFZ_FT_HIS()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FT_HIS ({','.join(columns)}) VALUES ({placeholders})"
    for _ in range(n):
        row = fake_row_TMP_EFZ_FT_HIS()
        ref_no = row["REF_NO"]
        ref_list.append(ref_no)
        cursor.execute(sql, [row[c] for c in columns])
    conn.commit()
    print(f"✅ Inserted {n} TMP_EFZ_FT_HIS rows.")
    return ref_list

def insert_fake_data_TMP_EFZ_FT_HIS_DETAILS_by_ref(ref_list):
    sample = fake_row_TMP_EFZ_FT_HIS_DETAILS()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FT_HIS_DETAILS ({','.join(columns)}) VALUES ({placeholders})"

    total = 0
    for ref in ref_list:
        for _ in range(random.randint(1, 5)):
            row = fake_row_TMP_EFZ_FT_HIS_DETAILS()
            row["REF_NO"] = ref
            cursor.execute(sql, [row[c] for c in columns])
            total += 1

    conn.commit()
    print(f"✅ Inserted {total} TMP_EFZ_FT_HIS_DETAILS rows.")

def insert_fake_data_TMP_EFZ_FUNDS_TRANSFER_with_ref(n=200):
    ref_list = []
    sample = fake_row_TMP_EFZ_FUNDS_TRANSFER()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FUNDS_TRANSFER ({','.join(columns)}) VALUES ({placeholders})"
    for _ in range(n):
        row = fake_row_TMP_EFZ_FUNDS_TRANSFER()
        ref_no = row["REF_NO"]
        ref_list.append(ref_no)
        cursor.execute(sql, [row[c] for c in columns])
    conn.commit()
    print(f"✅ Inserted {n} TMP_EFZ_FUNDS_TRANSFER rows.")
    return ref_list

def insert_fake_data_TMP_EFZ_FUNDS_TRANSFER_DETAILS_by_ref(ref_list):
    sample = fake_row_TMP_EFZ_FT_HIS_DETAILS()  # tái sử dụng nếu schema giống
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FUNDS_TRANSFER_DETAILS ({','.join(columns)}) VALUES ({placeholders})"
    total = 0
    for ref in ref_list:
        for _ in range(random.randint(1, 4)):
            row = fake_row_TMP_EFZ_FT_HIS_DETAILS()
            row["REF_NO"] = ref
            cursor.execute(sql, [row[c] for c in columns])
            total += 1
    conn.commit()
    print(f"✅ Inserted {total} TMP_EFZ_FUNDS_TRANSFER_DETAILS rows.")

def insert_fake_data_TMP_EFZ_FT_AFTER_COB_with_ref(n=200):
    ref_list = []
    sample = fake_row_TMP_EFZ_FT_AFTER_COB()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FT_AFTER_COB ({','.join(columns)}) VALUES ({placeholders})"
    for _ in range(n):
        row = fake_row_TMP_EFZ_FT_AFTER_COB()
        ref_no = row["REF_NO"]
        ref_list.append(ref_no)
        cursor.execute(sql, [row[c] for c in columns])
    conn.commit()
    print(f"✅ Inserted {n} TMP_EFZ_FT_AFTER_COB rows.")
    return ref_list

def insert_fake_data_TMP_EFZ_FT_AFTER_COB_DETAILS_by_ref(ref_list):
    sample = fake_row_TMP_EFZ_FT_AFTER_COB_DETAILS()
    columns = list(sample.keys())
    placeholders = ",".join("?" for _ in columns)
    sql = f"INSERT INTO TMP_EFZ_FT_AFTER_COB_DETAILS ({','.join(columns)}) VALUES ({placeholders})"
    total = 0
    for ref in ref_list:
        for _ in range(random.randint(1, 5)):
            row = fake_row_TMP_EFZ_FT_AFTER_COB_DETAILS()
            row["REF_NO"] = ref
            cursor.execute(sql, [row[c] for c in columns])
            total += 1
    conn.commit()
    print(f"✅ Inserted {total} TMP_EFZ_FT_AFTER_COB_DETAILS rows.")

if __name__ == "__main__":
    insert_fake_data_TMP_EFZ_FT_HIS(n=500)
    insert_fake_data_TMP_EFZ_FT_HIS_DETAILS(n=1000)
    insert_fake_data_TMP_EFZ_FUNDS_TRANSFER(n=300)
    insert_fake_data_TMP_EFZ_FT_AFTER_COB(n=300)
    insert_fake_data_TMP_EFZ_FT_AFTER_COB_DETAILS(n=500)

    ref_his = insert_fake_data_TMP_EFZ_FT_HIS_with_ref(n=300)
    insert_fake_data_TMP_EFZ_FT_HIS_DETAILS_by_ref(ref_his)

    ref_transfer = insert_fake_data_TMP_EFZ_FUNDS_TRANSFER_with_ref(n=200)
    insert_fake_data_TMP_EFZ_FUNDS_TRANSFER_DETAILS_by_ref(ref_transfer)

    ref_cob = insert_fake_data_TMP_EFZ_FT_AFTER_COB_with_ref(n=200)
    insert_fake_data_TMP_EFZ_FT_AFTER_COB_DETAILS_by_ref(ref_cob)