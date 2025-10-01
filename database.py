import sqlite3
import os

class ExpenseDB:
    def __init__(self, db_name="expenses.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """Create the expenses table if it doesn't exist"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_expense(self, expense_date, amount, category, description=""):
        """Add a new expense to the database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (expense_date, amount, category, description)
            VALUES (?, ?, ?, ?)
        ''', (expense_date, amount, category, description))
        
        conn.commit()
        conn.close()
    
    def get_all_expenses(self):
        """Retrieve all expenses from database"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM expenses ORDER BY expense_date DESC')
        expenses = cursor.fetchall()
        
        conn.close()
        return expenses
    
    def delete_expense(self, expense_id):
        """Delete a specific expense by ID"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
    
        cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    
        conn.commit()
        conn.close()

    def clear_all_expenses(self):
        """Delete all expenses and reset the ID counter"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
    
        cursor.execute('DELETE FROM expenses')
        cursor.execute('DELETE FROM sqlite_sequence WHERE name="expenses"')
    
        conn.commit()
        conn.close()
        print("All expenses cleared and ID counter reset")

    def update_expense(self, expense_id, date, amount, category, description):
        """Update an existing expense"""
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE expenses 
                SET expense_date = ?, amount = ?, category = ?, description = ?
                WHERE id = ?
            ''', (date, amount, category, description, expense_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error updating expense: {e}")
            return False