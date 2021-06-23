# grocery_reimburse_match
Tool to make filling out reimbursement form for groceries less tedious

## Why this was made
For a while, our family received a monthly grocery reimbursement subsidy from my father's company. Which was nice, but the process for filling out the reimbursement form was manual and very tedious, sometimes taking hours. I developed this script to cut down that time to just a few minutes, and making sure family members who can't code are still able to make use of it.

## How to use
0. Claim forms from dad's company and buy groceries
1. Scan receipt and convert to text through OCR (I used Google Lens, because I found that to be the most accurate OCR scanner, and developing my own OCR receipt scanner is outside of my abilities right now)
2. Clean OCR text file to only have ID, name, quantity, and unit cost of each item (see **receipt.txt** for example)
3. Replace **receipt.txt** with cleaned OCR text
4. Run **parser.py**
5. Open **purchases.csv** and **checklist.csv** through Google Sheets/Excel
6. Match the 2 lists by creating a new column in **purchases.csv** and adding the corresponding id from **checklist.csv** to that column
7. Download the updated **purchases.csv** and rename it to **matcher.csv**
8. Run **output.py**
9. Open **output.csv** through Google Sheets/Excel, and use the data to fill out the reimbursement form
