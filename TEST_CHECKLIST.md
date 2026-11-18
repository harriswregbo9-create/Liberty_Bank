# Liberty Bank – Application Test Checklist

| No. | Test Description | Expected Result | Status |
|---|---|---|---|
| 1 | Start the application | Main menu displays successfully | PASS |
| 2 | Register a customer | Customer is saved with a unique ID | PASS |
| 3 | Create a bank account | Account is created with a unique account number | PASS |
| 4 | Check account balance | Correct balance is displayed | PASS |
| 5 | Deposit money | Account balance increases correctly | PASS |
| 6 | Withdraw money | Account balance decreases correctly | PASS |
| 7 | Withdraw more than available balance | Transaction is rejected | PASS |
| 8 | Enter zero or a negative amount | Invalid amount is rejected | PASS |
| 9 | View transaction history | Account transactions are displayed | PASS |
| 10 | Restart the application | Previously saved records remain available | PASS |
| 11 | Check customer records | At least 30 customer records exist | PASS |
| 12 | Check bank accounts | At least 30 accounts exist | PASS |
| 13 | Check transaction records | At least 30 transaction records exist | PASS |

## Testing Conclusion

All listed application tests were completed successfully. The application performed the required banking operations, validated transactions, and preserved records after restarting.

**Overall Result: PASS**