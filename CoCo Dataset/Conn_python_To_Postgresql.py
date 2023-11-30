import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="whole_body_keypoints_val",
    user="postgres",
    password="1234")

# Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Executing an MYSQL function using the execute() method
cursor.execute("select version()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Connection established to: ",data)

#Creating table as per requirement
sql ='''CREATE TABLE EMPLOYEE(
   FIRST_NAME CHAR(20) NOT NULL,
   LAST_NAME CHAR(20),
   AGE INT,
   SEX CHAR(1),
   INCOME FLOAT
)'''
cursor.execute(sql)
print("Table created successfully........")
conn.commit()

#Closing the connection
conn.close()

print("dsfs")