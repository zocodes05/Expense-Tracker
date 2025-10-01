import streamlit as st
import pandas as pd
from database import ExpenseDB
from datetime import datetime, date
from visualization import ExpenseVisualizer
import os

db = ExpenseDB()

st.title("Personal Expense Tracker")

page = st.sidebar.selectbox("Choose a page", ["Add Expense", "View Expenses", "Analytics"])

if page == "Add Expense":
    st.header("Add New Expense")

    col1, col2 = st.columns(2)

    with col1:
        expense_date = st.date_input("Date", date.today())
        amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")

    with col2:
        category = st.selectbox("Category", [
            "Food", "Shopping", "Entertainment", "Care", "Other"
        ])
        description = st.text_input("Description (optional)")

    if st.button("Add Expense"):
        db.add_expense(expense_date.strftime('%Y-%m-%d'), amount, category, description)
        st.success("Expense added successfully!")


elif page == "View Expenses":
    st.header("📋 Your Expenses")
    
    expenses = db.get_all_expenses()
    if expenses:
        df = pd.DataFrame(expenses, columns=['ID', 'Date', 'Amount', 'Category', 'Description', 'Created At'])
        
        df['ID'] = pd.to_numeric(df['ID'], errors='coerce')
        df['Amount'] = df['Amount'].astype(float)
        df['Date'] = pd.to_datetime(df['Date'])
        
        df = df.sort_values('ID')
        
        df = df.reset_index(drop=True)
        
        df_display = df.copy()
        df_display['Amount'] = df_display['Amount'].apply(lambda x: f"${x:,.2f}")
        df_display['Date'] = df_display['Date'].dt.strftime('%Y-%m-%d')
        
        st.dataframe(df_display, hide_index=True)
        
        st.subheader("📊 Expense Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_spent = df['Amount'].sum()
            st.metric("Total Spent", f"${total_spent:,.2f}")
        
        with col2:
            total_expenses = len(df)
            st.metric("Total Expenses", total_expenses)
        
        st.subheader("✏️Edit")
        
        edit_options = [f"ID: {row['ID']} - ${row['Amount']:.2f} - {row['Category']} - {row['Date'].strftime('%Y-%m-%d')}" 
                      for _, row in df.iterrows()]
        
        selected_edit_expense = st.selectbox("Select expense to edit:", edit_options, key="edit_select")
        
        if selected_edit_expense:
            expense_id = int(selected_edit_expense.split(" - ")[0].replace("ID: ", ""))
            selected_expense_data = df[df['ID'] == expense_id].iloc[0]
            
            col1, col2, col3, col4 = st.columns([1, 1, 2, 2])
            
            with col1:
                new_date = st.date_input("Date", value=selected_expense_data['Date'], key=f"date_{expense_id}")
            
            with col2:
                new_amount = st.number_input("Amount", value=float(selected_expense_data['Amount']), min_value=0.0, step=0.01, key=f"amount_{expense_id}")
            
            with col3:
                new_description = st.text_input("Description", value=selected_expense_data['Description'], key=f"desc_{expense_id}")
            
            with col4:
                categories = [
                    "🍔 Food", "🚗 Transportation", 
                    "🛒 Shopping", "🎬 Entertainment", "🧾 Other"
                ]
                new_category = st.selectbox("Category", categories, 
                                          index=categories.index(selected_expense_data['Category']) if selected_expense_data['Category'] in categories else categories.index("🧾 Other"),
                                          key=f"category_{expense_id}")
            
            if st.button("Update Expense", type="primary", key=f"update_btn_{expense_id}"):
                db.update_expense(expense_id, new_date, new_amount, new_category, new_description)
                st.success("Expense updated successfully!")
                st.rerun()
        
        st.subheader("🗑️ Delete Expenses")
        
        col1, col2 = st.columns(2)
        
        with col1:
            delete_options = [f"ID: {row['ID']} - ${row['Amount']:.2f} - {row['Category']} - {row['Date'].strftime('%Y-%m-%d')}" 
                            for _, row in df.iterrows()]
            
            selected_delete_expense = st.selectbox("Select expense to delete:", delete_options, key="delete_select")
            
            if st.button("Delete Selected Expense", type="secondary", key="delete_btn"):
                expense_id = int(selected_delete_expense.split(" - ")[0].replace("ID: ", ""))
                db.delete_expense(expense_id)
                st.success("Expense deleted successfully!")
                st.rerun()
        
        with col2:
            st.write("### 🚨 Danger Zone")
            confirm = st.checkbox("I understand this will permanently delete ALL expenses", key="confirm_all")
            if st.button("Clear ALL Expenses", type="primary", disabled=not confirm, key="clear_all_btn"):
                db.clear_all_expenses()
                st.error("All expenses have been deleted!")
                st.rerun()
    
    else:
        st.info("No expenses recorded yet. Add some expenses on the 'Add Expense' page!")

elif page == "Analytics":
    st.header("Spending Analytics")
    
    visualizer = ExpenseVisualizer(db)
    
    fig1 = visualizer.spending_by_category()
    if fig1:
        st.pyplot(fig1)
    else:
        st.info("No data available for category breakdown")
    
    fig2 = visualizer.spending_over_time()
    if fig2:
        st.pyplot(fig2)
    else:
        st.info("No data available for spending trend")