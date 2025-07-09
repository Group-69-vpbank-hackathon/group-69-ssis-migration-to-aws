SELECT 
  u.user_id, 
  u.username,
  u.email,
  t.id as transaction_id,
  t.amount
FROM users u
RIGHT JOIN transactions t
  ON u.user_id = t.user_id