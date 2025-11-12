import mysql.connector
from mysql.connector import Error
import json

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                port=3306,
                database='flask_image_sharing',
                user='root',
                password='kien3766'
            )
            print("Connected to MySQL database")
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
    
    def create_tables(self):
        cursor = self.connection.cursor()
        
        # Users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(50) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                full_name VARCHAR(100),
                bio TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Images table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS images (
                id VARCHAR(50) PRIMARY KEY,
                filename VARCHAR(255) NOT NULL,
                image_name VARCHAR(255),
                image_category VARCHAR(100),
                uploader VARCHAR(50),
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uploader) REFERENCES users(username)
            )
        """)
        
        self.connection.commit()
        cursor.close()
        print("Tables created successfully")

db = Database()