import csv
import pandas as pd
import sqlite3

# Import matched csv of Purchases and Checklist items into dataframe
match_csv = 'matcher.csv'
df_grocery = pd.read_csv(match_csv)
df_grocery.dropna(subset = ["checklist_id"], inplace=True)
convert_dict = {
	'name': str,
	'checklist_id': int
}
df_grocery = df_grocery.astype(convert_dict)

# Connect to groceries database
db_file = 'groceries.db'
try:
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
except:
	print("Couldn't open", db_file)

# Create new Grocery table from dataframe
df_grocery.to_sql('Grocery', conn, if_exists='replace', index=False)
conn.commit()

# Select data from database needed to fill out checklist form
sql_string = '''
	SELECT Grocery.checklist_id AS No,
		Checklist.name AS Description,
		AVG(Purchases.price) AS Unit_Cost,
		SUM(Purchases.quantity) AS Quantity,
		SUM(Purchases.subtotal) AS Total_Amount
	FROM Grocery
	JOIN Purchases ON Purchases.id = Grocery.purchase_id
	JOIN Checklist ON Checklist.oid = Grocery.checklist_id
	GROUP BY No
	ORDER BY No
'''
df = pd.read_sql(sql_string, conn)

# Export selected data to csv for viewing in Google Sheets/Excel
output_file = 'output.csv'
df.to_csv(output_file, index=False, sep=';')

conn.close()