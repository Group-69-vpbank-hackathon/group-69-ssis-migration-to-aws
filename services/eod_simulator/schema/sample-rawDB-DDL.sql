USE [VPB_RAW_DATA]
GO

/****** Object:  Table [dbo].[TMP_EFZ_FT_HIS]    Script Date: 4/21/2025 2:27:59 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[TMP_EFZ_FT_HIS](
	[ID] [bigint] IDENTITY(1,1) NOT NULL,
	[REF_NO] [varchar](200) NOT NULL,
	[TRANSACTION_TYPE] [varchar](200) NULL,
	[DEBIT_ACCT_NO] [varchar](200) NULL,
	[DEBIT_CURRENCY] [varchar](50) NULL,
	[AMOUNT_DEBITED] [varchar](200) NULL,
	[DEBIT_VALUE_DATE] [varchar](50) NULL,
	[CREDIT_ACCT_NO] [varchar](200) NULL,
	[CREDIT_CURRENCY] [varchar](50) NULL,
	[AMOUNT_CREDITED] [varchar](200) NULL,
	[CREDIT_VALUE_DATE] [varchar](50) NULL,
	[DEBIT_COMP_CODE] [varchar](200) NULL,
	[CREDIT_COMP_CODE] [varchar](200) NULL,
	[BUSINESS_DATE] [varchar](20) NOT NULL,
	[RECORD_STATUS] [varchar](300) NULL,
	[SERVICE_CHANNEL] [varchar](50) NULL,
	[BEN_ACCT_NO] [varchar](50) NULL,
	[ATM_RE_NUM] [varchar](500) NULL,
	[CO_CODE] [varchar](500) NULL,
	[VPB_SERVICE] [nvarchar](250) NULL,
	[CONTACT_NUM] [nvarchar](250) NULL,
	[DEBIT_CUSTOMER] [nvarchar](250) NULL,
	[BOND_CODE] [varchar](500) NULL,
	[PR_CARD_NO] [varchar](500) NULL,
	[BEN_LEGAL_ID] [varchar](500) NULL,
	[BEN_ID_CUSTOMER] [varchar](500) NULL,
	[DEBIT_THEIR_REF] [nvarchar](500) NULL,
	[CREDIT_CARD] [varchar](200) NULL,
	[PROCESSING_DATE] [varchar](50) NULL,
	[CREDIT_AMOUNT] [varchar](50) NULL,
	[DEBIT_AMOUNT] [varchar](50) NULL,
	[CREDIT_THEIR_REF] [varchar](50) NULL,
	[AT_AUTH_CODE] [varchar](50) NULL,
	[TOTAL_CHARGE_AMT] [varchar](100) NULL,
	[ATM_TERM_ID] [varchar](100) NULL,
	[PROFIT_CENTRE_CUST] [varchar](30) NULL,
	[TREASURY_RATE] [varchar](50) NULL,
	[SOURCE_OF_FCY] [varchar](35) NULL,
	[VALUE_DT_LOCAL] [varchar](35) NULL,
	[VAT_NAME] [varchar](100) NULL,
	[R_CI_CODE] [varchar](35) NULL,
	[PURPOSE] [varchar](300) NULL,
	[B_ID_ISSUE_PLAC] [varchar](35) NULL,
	[CARD_NUMBER] [varchar](35) NULL,
	[TYPE_OF_DOC] [varchar](10) NULL,
	[VAT_CIF_NO] [varchar](100) NULL,
	[AUTHORISER] [varchar](500) NULL,
	[VPB_AUTHORISER] [varchar](500) NULL,
	[BAL_AFT_TXN] [varchar](100) NULL,
	[AT_MC_TRANS] [varchar](200) NULL,
	[TOTAL_TAX_AMOUNT] [varchar](35) NULL,
	[AUTH_DATE] [varchar](10) NULL,
	[SENDING_ACCT] [varchar](100) NULL,
	[DEPT_CODE] [varchar](10) NULL,
	[VPB_INPUTTER] [varchar](200) NULL,
 CONSTRAINT [PK_TMP_EFZ_FT_HIS] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO



CREATE TABLE [dbo].[TMP_EFZ_FT_HIS_DETAILS](
	[ID] [bigint] IDENTITY(1,1) NOT NULL,
	[REF_NO] [varchar](200) NOT NULL,
	[M] [int] NULL,
	[S] [int] NULL,
	[DATE_TIME] [varchar](300) NULL,
	[BUSINESS_DATE] [varchar](20) NULL,
	[PAYMENT_DETAILS] [varchar](500) NULL,
	[TXN_DETAIL_VPB] [varchar](500) NULL,
	[TXN_DETAIL] [varchar](500) NULL,
	[RECEIVING_NAME] [varchar](500) NULL,
	[REF_DATA_VALUE] [varchar](50) NULL,
	[REF_DATA_ITEM] [varchar](50) NULL,
	[INPUTTER] [varchar](200) NULL,
	[BEN_CUSTOMER] [varchar](300) NULL,
	[RECEIVING_ADDR] [varchar](300) NULL,
	[ORDERING_CUST] [varchar](300) NULL,
	[SENDING_ADDR] [varchar](300) NULL,
	[COMMISSION_AMT] [varchar](35) NULL,
 CONSTRAINT [PK_TMP_EFZ_FT_HIS_DETAILS] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO



CREATE TABLE [dbo].[TMP_EFZ_FT_AFTER_COB](
	[ID] [bigint] IDENTITY(1,1) NOT NULL,
	[REF_NO] [varchar](200) NOT NULL,
	[TRANSACTION_TYPE] [varchar](200) NULL,
	[DEBIT_ACCT_NO] [varchar](200) NULL,
	[DEBIT_CURRENCY] [varchar](50) NULL,
	[AMOUNT_DEBITED] [varchar](200) NULL,
	[DEBIT_VALUE_DATE] [varchar](50) NULL,
	[CREDIT_ACCT_NO] [varchar](200) NULL,
	[CREDIT_CURRENCY] [varchar](50) NULL,
	[AMOUNT_CREDITED] [varchar](200) NULL,
	[CREDIT_VALUE_DATE] [varchar](50) NULL,
	[DEBIT_COMP_CODE] [varchar](200) NULL,
	[CREDIT_COMP_CODE] [varchar](200) NULL,
	[BUSINESS_DATE] [varchar](20) NOT NULL,
	[RECORD_STATUS] [varchar](300) NULL,
	[SERVICE_CHANNEL] [varchar](50) NULL,
	[BEN_ACCT_NO] [varchar](50) NULL,
	[BOND_CODE] [varchar](500) NULL,
	[VPB_SERVICE] [nvarchar](250) NULL,
	[CONTACT_NUM] [nvarchar](250) NULL,
	[DEBIT_CUSTOMER] [nvarchar](250) NULL,
	[ATM_RE_NUM] [varchar](500) NULL,
	[CO_CODE] [varchar](500) NULL,
	[PR_CARD_NO] [varchar](500) NULL,
	[BEN_LEGAL_ID] [varchar](500) NULL,
	[BEN_ID_CUSTOMER] [varchar](500) NULL,
	[DEBIT_THEIR_REF] [nvarchar](500) NULL,
	[CREDIT_CARD] [varchar](200) NULL,
	[SECTOR] [varchar](50) NULL,
	[PURPOSE] [varchar](300) NULL,
	[VPB_BEN_COUNTRY] [varchar](50) NULL,
	[ORDER_COUNTRY] [varchar](50) NULL,
	[SOURCE_OF_FCY] [varchar](50) NULL,
	[PTTT] [varchar](50) NULL,
	[DAO] [varchar](50) NULL,
	[KBB_RATE] [varchar](50) NULL,
	[PRODUCT_LINE] [varchar](500) NULL,
	[LD_CONTRACT_NO] [varchar](100) NULL,
	[AUTHORISER] [varchar](100) NULL,
	[VAT_CIF_NO] [varchar](100) NULL,
	[BC_BANK_SORT_CODE] [varchar](100) NULL,
	[SENDING_ACCT] [varchar](100) NULL,
	[CLASSIFY_CODE] [varchar](100) NULL,
	[DEPT_CODE] [varchar](100) NULL,
	[BEN_OUR_CHARGES] [varchar](100) NULL,
	[TERM] [varchar](100) NULL,
	[TOTAL_CHARGE_AMT] [varchar](100) NULL,
	[VPB_INPUTTER] [varchar](500) NULL,
	[VPB_AUTHORISER] [varchar](500) NULL,
	[BOOKING_SERVICE] [varchar](100) NULL,
	[CHARGES_ACCT_NO] [varchar](100) NULL,
	[PROFIT_CENTRE_CUST] [varchar](100) NULL,
	[PROCESSING_DATE] [varchar](100) NULL,
	[RECEIVER_BANK] [varchar](100) NULL,
	[DELIVERY_INREF] [varchar](100) NULL,
	[ATM_TERM_ID] [varchar](100) NULL,
	[TREASURY_RATE] [varchar](50) NULL,
	[VALUE_DT_LOCAL] [varchar](35) NULL,
	[VAT_NAME] [varchar](100) NULL,
	[R_CI_CODE] [varchar](35) NULL,
	[B_ID_ISSUE_PLAC] [varchar](35) NULL,
	[CARD_NUMBER] [varchar](35) NULL,
	[AT_AUTH_CODE] [varchar](10) NULL,
	[AUTH_DATE] [varchar](10) NULL,
	[CREDIT_CUSTOMER] [varchar](35) NULL,
	[CREDIT_THEIR_REF] [varchar](35) NULL,
	[TYPE_OF_DOC] [varchar](10) NULL,
	[DEBIT_AMOUNT] [varchar](50) NULL,
	[BAL_AFT_TXN] [varchar](100) NULL,
	[AT_MC_TRANS] [varchar](200) NULL,
	[TOTAL_TAX_AMOUNT] [varchar](35) NULL,
 CONSTRAINT [PK_TMP_EFZ_FT_AFTER_COB] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO




CREATE TABLE [dbo].[TMP_EFZ_FT_AFTER_COB_DETAILS](
	[ID] [bigint] IDENTITY(1,1) NOT NULL,
	[REF_NO] [varchar](200) NOT NULL,
	[M] [int] NULL,
	[S] [int] NULL,
	[DATE_TIME] [varchar](300) NULL,
	[BUSINESS_DATE] [varchar](20) NULL,
	[PAYMENT_DETAILS] [varchar](500) NULL,
	[TXN_DETAIL_VPB] [varchar](500) NULL,
	[TXN_DETAIL] [varchar](500) NULL,
	[RECEIVING_NAME] [varchar](500) NULL,
	[NAME_OF_GOODS] [varchar](500) NULL,
	[ORDERING_BANK] [varchar](100) NULL,
	[ACCT_WITH_BANK] [varchar](100) NULL,
	[REF_DATA_VALUE] [varchar](100) NULL,
	[INPUTTER] [varchar](500) NULL,
	[ORDERING_CUST] [varchar](300) NULL,
	[AZ_LD_NRDATE] [varchar](100) NULL,
	[BEN_CUSTOMER] [varchar](300) NULL,
	[SUSPENSE_ID] [varchar](100) NULL,
	[REF_DATA_ITEM] [varchar](100) NULL,
	[RECEIVING_ADDR] [varchar](300) NULL,
	[SENDING_ADDR] [varchar](300) NULL,
	[COMMISSION_AMT] [varchar](35) NULL,
 CONSTRAINT [PK_TMP_EFZ_FT_AFTER_COB_DETAILS] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO




CREATE TABLE [dbo].[TMP_EFZ_FUNDS_TRANSFER](
	[ID] [bigint] IDENTITY(1,1) NOT NULL,
	[REF_NO] [varchar](200) NOT NULL,
	[TRANSACTION_TYPE] [varchar](200) NULL,
	[DEBIT_ACCT_NO] [varchar](200) NULL,
	[DEBIT_CURRENCY] [varchar](50) NULL,
	[AMOUNT_DEBITED] [varchar](200) NULL,
	[DEBIT_VALUE_DATE] [varchar](50) NULL,
	[CREDIT_ACCT_NO] [varchar](200) NULL,
	[CREDIT_CURRENCY] [varchar](50) NULL,
	[AMOUNT_CREDITED] [varchar](200) NULL,
	[CREDIT_VALUE_DATE] [varchar](50) NULL,
	[DEBIT_COMP_CODE] [varchar](200) NULL,
	[CREDIT_COMP_CODE] [varchar](200) NULL,
	[BUSINESS_DATE] [varchar](20) NOT NULL,
	[RECORD_STATUS] [varchar](300) NULL,
	[SERVICE_CHANNEL] [varchar](50) NULL,
	[BEN_ACCT_NO] [varchar](50) NULL,
	[BOND_CODE] [varchar](500) NULL,
	[VPB_SERVICE] [nvarchar](250) NULL,
	[CONTACT_NUM] [nvarchar](250) NULL,
	[DEBIT_CUSTOMER] [nvarchar](250) NULL,
	[ATM_RE_NUM] [varchar](500) NULL,
	[CO_CODE] [varchar](500) NULL,
	[PR_CARD_NO] [varchar](500) NULL,
	[BEN_LEGAL_ID] [varchar](500) NULL,
	[BEN_ID_CUSTOMER] [varchar](500) NULL,
	[DEBIT_THEIR_REF] [nvarchar](500) NULL,
	[CREDIT_CARD] [varchar](200) NULL,
	[PROCESSING_DATE] [varchar](50) NULL,
	[CREDIT_AMOUNT] [varchar](50) NULL,
	[DEBIT_AMOUNT] [varchar](50) NULL,
	[CREDIT_THEIR_REF] [varchar](50) NULL,
	[AT_AUTH_CODE] [varchar](50) NULL,
	[TOTAL_CHARGE_AMT] [varchar](100) NULL,
	[ATM_TERM_ID] [varchar](100) NULL,
	[PROFIT_CENTRE_CUST] [varchar](100) NULL,
	[VAT_CIF_NO] [varchar](100) NULL,
	[AUTHORISER] [varchar](200) NULL,
	[VPB_AUTHORISER] [varchar](50) NULL,
	[TREASURY_RATE] [varchar](50) NULL,
	[TYPE_OF_DOC] [varchar](10) NULL,
	[SOURCE_OF_FCY] [varchar](35) NULL,
	[VALUE_DT_LOCAL] [varchar](35) NULL,
	[VAT_NAME] [varchar](100) NULL,
	[R_CI_CODE] [varchar](35) NULL,
	[PURPOSE] [varchar](300) NULL,
	[B_ID_ISSUE_PLAC] [varchar](35) NULL,
	[BAL_AFT_TXN] [varchar](100) NULL,
	[AT_MC_TRANS] [varchar](200) NULL,
	[TOTAL_TAX_AMOUNT] [varchar](35) NULL,
	[AUTH_DATE] [varchar](10) NULL,
	[SENDING_ACCT] [varchar](100) NULL,
	[DEPT_CODE] [varchar](10) NULL,
	[VPB_INPUTTER] [varchar](200) NULL,
 CONSTRAINT [PK_TMP_EFZ_FUNDS_TRANSFER] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO



CREATE TABLE [dbo].[TMP_EFZ_FUNDS_TRANSFER_DETAILS](
	[ID] [bigint] IDENTITY(1,1) NOT NULL,
	[REF_NO] [varchar](200) NOT NULL,
	[M] [int] NULL,
	[S] [int] NULL,
	[DATE_TIME] [varchar](300) NULL,
	[BUSINESS_DATE] [varchar](20) NULL,
	[PAYMENT_DETAILS] [varchar](500) NULL,
	[TXN_DETAIL_VPB] [varchar](500) NULL,
	[TXN_DETAIL] [varchar](500) NULL,
	[RECEIVING_NAME] [varchar](500) NULL,
	[REF_DATA_VALUE] [varchar](50) NULL,
	[REF_DATA_ITEM] [varchar](50) NULL,
	[INPUTTER] [varchar](200) NULL,
	[BEN_CUSTOMER] [varchar](300) NULL,
	[RECEIVING_ADDR] [varchar](300) NULL,
	[ORDERING_CUST] [varchar](300) NULL,
	[SENDING_ADDR] [varchar](300) NULL,
	[COMMISSION_AMT] [varchar](35) NULL,
 CONSTRAINT [PK_TMP_EFZ_FUNDS_TRANSFER_DETAILS] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO



