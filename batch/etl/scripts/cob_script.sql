SELECT 
  after_cob.ID, 
  after_cob.BUSINESS_DATE,
  after_cob_detail.RECEIVING_ADDR
FROM after_cob
JOIN after_cob_detail
  ON after_cob.REF_NO = after_cob_detail.REF_NO