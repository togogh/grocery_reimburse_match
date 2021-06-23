import re
import sqlite3
import csv
import pandas as pd

# Initialize SQLITE database
db_file = 'groceries.db'

try:
	conn = sqlite3.connect(db_file)
	cur = conn.cursor()
except:
	print("Couldn't connect to", db_file)
	quit()

# Create table for purchased items
cur.executescript('''
	DROP TABLE IF EXISTS Purchases;

	CREATE TABLE Purchases (
		id integer PRIMARY KEY NOT NULL,
		name text NOT NULL,
		quantity integer,
		price integer,
		subtotal integer
	);
''')

# Create table for checklist items
cur.executescript('''
	DROP TABLE IF EXISTS Checklist;

	CREATE TABLE Checklist (
		name text NOT NULL
	);
''')

conn.commit()

# Import OCR data from receipt
source_file = 'receipt.txt'
with open(source_file, 'r') as f:
	data = f.read()

# Clean OCR data
data = data.replace('\n', ' ')
data = data.replace(',', ' ')

# Separate individual items from receipt text and put them in list
items = re.findall(r'\d{13} [.\w\s/<%&@=\,\+]+? \d+\.*\d*[\s\.]X[\s\.]\d+\.\d+', data)

# Get the id, name, quantity, price, and subtotal of each item and add it to the Purchases table
for item in items:
	details = re.match(r'(\d{13}) ([.\w\s/<%&@=\,\+]+?) (\d+\.*\d*)[\s\.]X[\s\.](\d+\.\d+)', item)
	item_id = int(details.group(1))
	item_name = str(details.group(2))
	item_quant = float(details.group(3))
	item_price = float(details.group(4))
	item_subtotal = round(float(item_quant * item_price), 2)

	cur.execute('''INSERT INTO Purchases (id, name, quantity, price, subtotal)
		VALUES (?, ?, ?, ?, ?)''',
		(item_id, item_name, item_quant, item_price, item_subtotal))

conn.commit()

# Import OCR data from checklist
checklist_file = 'checklist.txt'
with open(checklist_file, 'r') as f:
	data = f.read()

# Clean OCR data & separate individual items
checklist_items = data.split('\n\n')

# Get the name of each item and insert it into Checklist table
for item in checklist_items:
	cur.execute('''INSERT INTO Checklist (name)
		VALUES (?)''', (item,))

conn.commit()

# Export id and name columns from Purchases and id column from Checklist
# to manually match items together
purchases_csv = 'purchases.csv'
db_df = pd.read_sql('SELECT id, name FROM Purchases', conn)
db_df.to_csv(purchases_csv, index=False, sep=';')

checklist_csv = 'checklist.csv'
db_df = pd.read_sql('SELECT oid, name FROM Checklist', conn)
db_df.to_csv(checklist_csv, index=False, sep=';')

conn.close()