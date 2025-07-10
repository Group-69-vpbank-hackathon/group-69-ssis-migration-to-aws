
import psycopg2
import random
from faker import Faker
from datetime import datetime
from tqdm import tqdm
import os
import argparse
from dotenv import load_dotenv
load_dotenv()
fake = Faker("vi_VN")

def connect_postgres():
    return psycopg2.connect(
        dbname=os.getenv("PG_DB"),
        user=os.getenv("PG_USER"),
        password=os.getenv("PG_PASSWORD"),
        host=os.getenv("PG_HOST"),
        port=os.getenv("PG_PORT")
    )

def fake_string(length=10):
    return fake.lexify(text="?" * length)

# --------------------- Fake
def fake_common_fields_header():
    return {
        "REF_NO": fake.uuid4(),
        "BUSINESS_DATE": datetime.today().strftime("%Y-%m-%d"),
    }

def fake_common_fields_detail():
    return {
        "REF_NO": fake.uuid4(),
        "M": random.randint(0, 59),
        "S": random.randint(0, 59),
        "DATE_TIME": fake.date_time().strftime("%Y-%m-%d %H:%M:%S"),
        "BUSINESS_DATE": datetime.today().strftime("%Y-%m-%d"),
    }

def fake_tmp_efz_ft_his():
    return {
        **fake_common_fields_header(),
        "TRANSACTION_TYPE": random.choice(["TRANSFER", "WITHDRAWAL", "DEPOSIT"]),
        "DEBIT_ACCT_NO": fake.bban(),
        "DEBIT_CURRENCY": random.choice(["VND", "USD", "EUR"]),
        "AMOUNT_DEBITED": str(round(random.uniform(1e6, 5e7), 2)),
        "DEBIT_VALUE_DATE": fake.date(pattern="%Y-%m-%d"),
        "CREDIT_ACCT_NO": fake.bban(),
        "CREDIT_CURRENCY": random.choice(["VND", "USD", "EUR"]),
        "AMOUNT_CREDITED": str(round(random.uniform(1e6, 5e7), 2)),
        "CREDIT_VALUE_DATE": fake.date(pattern="%Y-%m-%d"),
        "DEBIT_COMP_CODE": fake_string(3),
        "CREDIT_COMP_CODE": fake_string(3),
        "RECORD_STATUS": random.choice(["PENDING", "SUCCESS", "FAILED"]),
        "SERVICE_CHANNEL": random.choice(["ATM", "IB", "MOBILE"]),
        "BEN_ACCT_NO": fake.bban(),
        "ATM_RE_NUM": fake.bothify(text="ATM#######"),
        "CO_CODE": fake_string(4),
        "VPB_SERVICE": fake.word(),
        "CONTACT_NUM": fake.phone_number(),
        "DEBIT_CUSTOMER": fake.name(),
        "BOND_CODE": fake_string(8),
        "PR_CARD_NO": fake.credit_card_number(),
        "BEN_LEGAL_ID": fake.ssn(),
        "BEN_ID_CUSTOMER": fake.uuid4(),
        "DEBIT_THEIR_REF": fake.bothify(text="REF######"),
        "CREDIT_CARD": fake.credit_card_number(),
        "PROCESSING_DATE": fake.date(pattern="%Y-%m-%d"),
        "CREDIT_AMOUNT": str(round(random.uniform(1e6, 5e7), 2)),
        "DEBIT_AMOUNT": str(round(random.uniform(1e6, 5e7), 2)),
        "CREDIT_THEIR_REF": fake.bothify(text="REF######"),
        "AT_AUTH_CODE": fake.lexify(text="AUTH##"),
        "TOTAL_CHARGE_AMT": str(round(random.uniform(1000, 100000), 2)),
        "ATM_TERM_ID": fake.bothify(text="TERM###"),
        "PROFIT_CENTRE_CUST": fake_string(3),
        "TREASURY_RATE": str(round(random.uniform(1.5, 3.5), 2)),
        "SOURCE_OF_FCY": random.choice(["EXPORT", "LOAN", "SALE"]),
        "VALUE_DT_LOCAL": fake.date(pattern="%Y-%m-%d"),
        "VAT_NAME": fake.company(),
        "R_CI_CODE": fake_string(3),
        "PURPOSE": fake.sentence(nb_words=6),
        "B_ID_ISSUE_PLAC": fake_string(3),
        "CARD_NUMBER": fake.credit_card_number(),
        "TYPE_OF_DOC": random.choice(["01", "02", "03"]),
        "VAT_CIF_NO": fake.ean(length=13),
        "AUTHORISER": fake.name(),
        "VPB_AUTHORISER": fake.name(),
        "BAL_AFT_TXN": str(round(random.uniform(0, 1e9), 2)),
        "AT_MC_TRANS": fake.lexify(text="TRN####"),
        "TOTAL_TAX_AMOUNT": str(round(random.uniform(1000, 10000), 2)),
        "AUTH_DATE": fake.date(pattern="%Y-%m-%d"),
        "SENDING_ACCT": fake.bban(),
        "DEPT_CODE": fake.bothify(text="DPT##"),
        "VPB_INPUTTER": fake.name()
    }

def fake_tmp_efz_ft_his_details():
    return {
        **fake_common_fields_detail(),
        "PAYMENT_DETAILS": fake.text(100),
        "TXN_DETAIL_VPB": fake.text(100),
        "TXN_DETAIL": fake.text(100),
        "RECEIVING_NAME": fake.name(),
        "REF_DATA_VALUE": fake.lexify(text="VAL##"),
        "REF_DATA_ITEM": fake.lexify(text="ITEM##"),
        "INPUTTER": fake.name(),
        "BEN_CUSTOMER": fake.name(),
        "RECEIVING_ADDR": fake.address(),
        "ORDERING_CUST": fake.name(),
        "SENDING_ADDR": fake.address(),
        "COMMISSION_AMT": str(random.randint(1000, 5000))
    }

def fake_tmp_efz_ft_after_cob():
    return {
        **fake_common_fields_header(),
        "TRANSACTION_TYPE": fake.word(),
        "DEBIT_ACCT_NO": fake.bban(),
        "DEBIT_CURRENCY": "VND",
        "AMOUNT_DEBITED": str(random.randint(1_000_000, 10_000_000)),
        "DEBIT_VALUE_DATE": fake.date(pattern="%Y-%m-%d"),
        "CREDIT_ACCT_NO": fake.bban(),
        "CREDIT_CURRENCY": "VND",
        "AMOUNT_CREDITED": str(random.randint(1_000_000, 10_000_000)),
        "CREDIT_VALUE_DATE": fake.date(pattern="%Y-%m-%d"),
        "DEBIT_COMP_CODE": fake_string(3),
        "CREDIT_COMP_CODE": fake_string(3),
        "RECORD_STATUS": "NEW",
        "SERVICE_CHANNEL": "MOBILE",
        "BEN_ACCT_NO": fake.bban(),
        "BOND_CODE": fake_string(8),
        "VPB_SERVICE": fake.word(),
        "CONTACT_NUM": fake.phone_number(),
        "DEBIT_CUSTOMER": fake.name(),
        "ATM_RE_NUM": fake.bothify(text="ATM#######"),
        "CO_CODE": fake_string(4),
        "PR_CARD_NO": fake.credit_card_number(),
        "BEN_LEGAL_ID": fake.ssn(),
        "BEN_ID_CUSTOMER": fake.uuid4(),
        "DEBIT_THEIR_REF": fake.bothify(text="REF######"),
        "CREDIT_CARD": fake.credit_card_number(),
        "SECTOR": fake.word(),
        "PURPOSE": fake.sentence(),
        "VPB_BEN_COUNTRY": fake.country_code(),
        "ORDER_COUNTRY": fake.country_code(),
        "SOURCE_OF_FCY": "EXPORT",
        "PTTT": fake.word(),
        "DAO": fake.word(),
        "KBB_RATE": str(round(random.uniform(1, 5), 2)),
        "PRODUCT_LINE": fake.word(),
        "LD_CONTRACT_NO": fake.bothify(text="LD########"),
        "AUTHORISER": fake.name(),
        "VAT_CIF_NO": fake.ean(length=13),
        "BC_BANK_SORT_CODE": fake.bothify(text="SC###"),
        "SENDING_ACCT": fake.bban(),
        "CLASSIFY_CODE": fake.lexify(text="CL??"),
        "DEPT_CODE": fake.bothify(text="DPT##"),
        "BEN_OUR_CHARGES": fake.word(),
        "TERM": fake.word(),
        "TOTAL_CHARGE_AMT": str(random.randint(1000, 100000)),
        "VPB_INPUTTER": fake.name(),
        "VPB_AUTHORISER": fake.name(),
        "BOOKING_SERVICE": fake.word(),
        "CHARGES_ACCT_NO": fake.bban(),
        "PROFIT_CENTRE_CUST": fake_string(3),
        "PROCESSING_DATE": fake.date(pattern="%Y-%m-%d"),
        "RECEIVER_BANK": fake.company(),
        "DELIVERY_INREF": fake.lexify(text="INREF###"),
        "ATM_TERM_ID": fake.bothify(text="TERM###"),
        "TREASURY_RATE": str(round(random.uniform(1.5, 3.5), 2)),
        "VALUE_DT_LOCAL": fake.date(pattern="%Y-%m-%d"),
        "VAT_NAME": fake.company(),
        "R_CI_CODE": fake_string(3),
        "B_ID_ISSUE_PLAC": fake_string(3),
        "CARD_NUMBER": fake.credit_card_number(),
        "AT_AUTH_CODE": fake.lexify(text="AUTH##"),
        "AUTH_DATE": fake.date(pattern="%Y-%m-%d"),
        "CREDIT_CUSTOMER": fake.name(),
        "CREDIT_THEIR_REF": fake.bothify(text="REF######"),
        "TYPE_OF_DOC": random.choice(["01", "02"]),
        "DEBIT_AMOUNT": str(random.randint(1_000_000, 10_000_000)),
        "BAL_AFT_TXN": str(random.randint(1_000_000, 10_000_000)),
        "AT_MC_TRANS": fake.lexify(text="TRN####"),
        "TOTAL_TAX_AMOUNT": str(random.randint(1000, 10000))
    }

def fake_tmp_efz_ft_after_cob_details():
    return {
        **fake_common_fields_detail(),
        "PAYMENT_DETAILS": fake.text(100),
        "TXN_DETAIL_VPB": fake.text(100),
        "TXN_DETAIL": fake.text(100),
        "RECEIVING_NAME": fake.name(),
        "NAME_OF_GOODS": fake.word(),
        "ORDERING_BANK": fake.company(),
        "ACCT_WITH_BANK": fake.bban(),
        "REF_DATA_VALUE": fake.lexify(text="VAL##"),
        "INPUTTER": fake.name(),
        "ORDERING_CUST": fake.name(),
        "AZ_LD_NRDATE": fake.date(pattern="%Y-%m-%d"),
        "BEN_CUSTOMER": fake.name(),
        "SUSPENSE_ID": fake.uuid4(),
        "REF_DATA_ITEM": fake.lexify(text="ITEM##"),
        "RECEIVING_ADDR": fake.address(),
        "SENDING_ADDR": fake.address(),
        "COMMISSION_AMT": str(random.randint(1000, 5000))
    }

def fake_tmp_efz_funds_transfer():
    return {
        **fake_common_fields_header(),
        "TRANSACTION_TYPE": fake.word(),
        "DEBIT_ACCT_NO": fake.bban(),
        "DEBIT_CURRENCY": "VND",
        "AMOUNT_DEBITED": str(random.randint(1_000_000, 10_000_000)),
        "DEBIT_VALUE_DATE": fake.date(pattern="%Y-%m-%d"),
        "CREDIT_ACCT_NO": fake.bban(),
        "CREDIT_CURRENCY": "VND",
        "AMOUNT_CREDITED": str(random.randint(1_000_000, 10_000_000)),
        "CREDIT_VALUE_DATE": fake.date(pattern="%Y-%m-%d"),
        "DEBIT_COMP_CODE": fake_string(3),
        "CREDIT_COMP_CODE": fake_string(3),
        "RECORD_STATUS": "NEW",
        "SERVICE_CHANNEL": "MOBILE",
        "BEN_ACCT_NO": fake.bban(),
        "BOND_CODE": fake_string(8),
        "VPB_SERVICE": fake.word(),
        "CONTACT_NUM": fake.phone_number(),
        "DEBIT_CUSTOMER": fake.name(),
        "ATM_RE_NUM": fake.bothify(text="ATM#######"),
        "CO_CODE": fake_string(4),
        "PR_CARD_NO": fake.credit_card_number(),
        "BEN_LEGAL_ID": fake.ssn(),
        "BEN_ID_CUSTOMER": fake.uuid4(),
        "DEBIT_THEIR_REF": fake.bothify(text="REF######"),
        "CREDIT_CARD": fake.credit_card_number(),
        "PROCESSING_DATE": fake.date(pattern="%Y-%m-%d"),
        "CREDIT_AMOUNT": str(random.randint(1_000_000, 10_000_000)),
        "DEBIT_AMOUNT": str(random.randint(1_000_000, 10_000_000)),
        "CREDIT_THEIR_REF": fake.bothify(text="REF######"),
        "AT_AUTH_CODE": fake.lexify(text="AUTH##"),
        "TOTAL_CHARGE_AMT": str(random.randint(1000, 100000)),
        "ATM_TERM_ID": fake.bothify(text="TERM###"),
        "PROFIT_CENTRE_CUST": fake_string(3),
        "VAT_CIF_NO": fake.ean(length=13),
        "AUTHORISER": fake.name(),
        "VPB_AUTHORISER": fake.name(),
        "TREASURY_RATE": str(round(random.uniform(1.5, 3.5), 2)),
        "TYPE_OF_DOC": random.choice(["01", "02"]),
        "SOURCE_OF_FCY": "EXPORT",
        "VALUE_DT_LOCAL": fake.date(pattern="%Y-%m-%d"),
        "VAT_NAME": fake.company(),
        "R_CI_CODE": fake_string(3),
        "PURPOSE": fake.sentence(),
        "B_ID_ISSUE_PLAC": fake_string(3),
        "BAL_AFT_TXN": str(random.randint(1_000_000, 50_000_000)),
        "AT_MC_TRANS": fake.lexify(text="TRN####"),
        "TOTAL_TAX_AMOUNT": str(random.randint(1000, 10000)),
        "AUTH_DATE": fake.date(pattern="%Y-%m-%d"),
        "SENDING_ACCT": fake.bban(),
        "DEPT_CODE": fake.bothify(text="DPT##"),
        "VPB_INPUTTER": fake.name()
    }

def fake_tmp_efz_funds_transfer_details():
    return {
        **fake_common_fields_detail(),
        "PAYMENT_DETAILS": fake.text(100),
        "TXN_DETAIL_VPB": fake.text(100),
        "TXN_DETAIL": fake.text(100),
        "RECEIVING_NAME": fake.name(),
        "REF_DATA_VALUE": fake.lexify(text="VAL##"),
        "REF_DATA_ITEM": fake.lexify(text="ITEM##"),
        "INPUTTER": fake.name(),
        "BEN_CUSTOMER": fake.name(),
        "RECEIVING_ADDR": fake.address(),
        "ORDERING_CUST": fake.name(),
        "SENDING_ADDR": fake.address(),
        "COMMISSION_AMT": str(random.randint(1000, 5000))
    }

# --------------------- insert
def insert_fake_rows(table, row_generator, n=5):
    conn = connect_postgres()
    cur = conn.cursor()
    for _ in tqdm(range(n), ncols=100, colour="green", desc=table):
        row = row_generator()
        columns = ', '.join(f'"{k}"' for k in row.keys())
        values = ', '.join(['%s'] * len(row))
        sql = f'INSERT INTO "{table}" ({columns}) VALUES ({values})'
        cur.execute(sql, list(row.values()))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    n_sample = 10
    parser = argparse.ArgumentParser()
    parser.add_argument("--n_sample", required=False, default=10)
    args = parser.parse_args()
    n_sample = int(args.n_sample)
    print(f'🚀 Generate with {n_sample} sample data')
    insert_fake_rows("TMP_EFZ_FT_HIS", fake_tmp_efz_ft_his, n=n_sample)
    insert_fake_rows("TMP_EFZ_FT_HIS_DETAILS", fake_tmp_efz_ft_his_details, n=n_sample)
    insert_fake_rows("TMP_EFZ_FT_AFTER_COB", fake_tmp_efz_ft_after_cob, n=n_sample)
    insert_fake_rows("TMP_EFZ_FT_AFTER_COB_DETAILS", fake_tmp_efz_ft_after_cob_details, n=n_sample)
    insert_fake_rows("TMP_EFZ_FUNDS_TRANSFER", fake_tmp_efz_funds_transfer, n=n_sample)
    insert_fake_rows("TMP_EFZ_FUNDS_TRANSFER_DETAILS", fake_tmp_efz_funds_transfer_details, n=n_sample)