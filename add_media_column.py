import sqlite3

# Replace with the path to your SQLite database file
db_path = 'instance/cv_builder.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add the 'media' column to the 'post' table
try:
    cursor.execute("ALTER TABLE post ADD COLUMN media TEXT;")
    conn.commit()
    print("Successfully added 'media' column to the 'post' table.")
except sqlite3.OperationalError as e:
    print(f"An error occurred: {e}")

# Verify the columns in the 'post' table
cursor.execute("PRAGMA table_info(post);")
columns = cursor.fetchall()

print("\nColumns in the 'post' table after modification:")
for column in columns:
    print(column)

# Close the connection
conn.close()
