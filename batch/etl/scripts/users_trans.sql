SELECT 
  u.user_id, 
  u.username,
  u.email,
  t.transaction_id as transaction_id,
  t.amount
FROM users u
JOIN transactions t
  ON u.user_id = t.user_id