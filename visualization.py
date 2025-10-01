import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta

class ExpenseVisualizer:
    def __init__(self, db):
        self.db = db
    
    def spending_by_category(self):
        """Create pie chart of spending by category"""
        expenses = self.db.get_all_expenses()
        if not expenses:
            return None
        
        df = pd.DataFrame(expenses, columns=['ID', 'Date', 'Amount', 'Category', 'Description', 'Created At'])
        category_totals = df.groupby('Category')['Amount'].sum()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%')
        ax.set_title('Spending by Category')
        
        return fig
    
    def spending_over_time(self):
        """Create line chart of spending over time"""
        expenses = self.db.get_all_expenses()
        if not expenses:
            return None
        
        df = pd.DataFrame(expenses, columns=['ID', 'Date', 'Amount', 'Category', 'Description', 'Created At'])
        df['Date'] = pd.to_datetime(df['Date'])
        daily_spending = df.groupby('Date')['Amount'].sum().resample('D').sum().fillna(0)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(daily_spending.index, daily_spending.values, marker='o')
        ax.set_title('Daily Spending Trend')
        ax.set_xlabel('Date')
        ax.set_ylabel('Amount Spent ($)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return fig