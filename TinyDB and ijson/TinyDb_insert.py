from tinydb import TinyDB, Query

# Step 1: Initialize a TinyDB instance
db = TinyDB('my_database.json')
# db.truncate()
# Step 2: Create a reference to a table (or create the table if it doesn't exist)
table = db.table('my_table')
table.truncate()
# Step 3: Add values to the table
data_to_insert = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]
print(type(data_to_insert))

# Insert the data into the table
table.insert_multiple(data_to_insert)

# Step 4: Read values from the table
# Query the data
query = Query()
result = table.search(query.id == 2)

# Step 5: Display the results
print("Data in the table:")
for item in table:
    print(item)

print("\nResult of the query (id = 2):")
print(result)

# Step 6: Close the database
db.close()


