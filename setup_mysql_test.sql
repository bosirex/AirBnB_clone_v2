-- Creates a MySQL server with:
--   Database = hbnb_dev_db.
--   User = hbnb_dev in localhost with 
--   password = hbnb_dev_pwd.
--   all privileges granted to hbnb_dev on hbnb_dev_db.
--   SELECT privilege on performance granted to hbnb_dev.

-- Connect to the MySQL server as root.
db = MySQLdb.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='your_root_password'
)

-- cursor object to execute queries
cursor = db.cursor()

-- Create database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS hbnb_dev_db")

-- Create user if it doesn't exist and set the password
cursor.execute("CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd'")

-- Grant all privileges to hbnb_dev on the database
cursor.execute("GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost'")

-- Grant SELECT privilege to hbnb_dev
cursor.execute("GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost'")

-- Flush privileges to apply the changes
cursor.execute("FLUSH PRIVILEGES")

-- Close the cursor
cursor.close()

-- Close database connection
db.close()
