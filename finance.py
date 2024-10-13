import json
import pandas as pd
from datetime import datetime

class User:
    def __init__(self, username, password):  
        self.username = username
        self.password = password

    @staticmethod
    def register():
        print("\n--- User Registration ---")
        username = input("Enter a new username: ")
        password = input("Enter a new password: ")

        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            users = {}

        if username in users:
            print("\n[!] Username already exists. Please try again.\n")
            return None
        
        users[username] = password
        with open('users.json', 'w') as file:
            json.dump(users, file)
        
        print(f"\n[✓] User '{username}' registered successfully!\n")
        return User(username, password)

    @staticmethod
    def login():
        print("\n--- User Login ---")
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
        except FileNotFoundError:
            print("\n[!] No users found. Please register first.\n")
            return None

        if username in users and users[username] == password:
            print(f"\n[✓] Login successful! Welcome, {username}.\n")
            return User(username, password)
        else:
            print("\n[!] Invalid username or password. Please try again.\n")
            return None

    def logout(self):
        print(f"\n[✓] User '{self.username}' logged out successfully!\n")
        return None

class FinanceRecord:
    def __init__(self, description, amount, category, date):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date

    def to_dict(self):
        return {
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

class FinanceManager:
    def __init__(self, user):
        self.user = user
        self.records = []

    def load_data(self):
        try:
            with open('finances.json', 'r') as file:
                data = json.load(file)
                self.records = [FinanceRecord(**record) for record in data.get(self.user.username, [])]
        except FileNotFoundError:
            self.records = []

    def save_data(self):
        try:
            with open('finances.json', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}

        data[self.user.username] = [record.to_dict() for record in self.records]

        with open('finances.json', 'w') as file:
            json.dump(data, file)

    def add_record(self, record):
        self.records.append(record)
        self.save_data()

    def delete_record(self, index):
        if 0 <= index < len(self.records):
            del self.records[index]
            self.save_data()
            print("\n[✓] Record deleted successfully!\n")
        else:
            print("\n[!] Invalid record number.\n")

    def update_record(self, index, new_record):
        if 0 <= index < len(self.records):
            self.records[index] = new_record
            self.save_data()
            print("\n[✓] Record updated successfully!\n")
        else:
            print("\n[!] Invalid record number.\n")

    def generate_report(self):
        df = pd.DataFrame([record.to_dict() for record in self.records])
        if not df.empty:
            print("\n--- Finance Report ---")
            print(df.describe())
            print("\n----------------------")
        else:
            print("\n[!] No records available to generate a report.\n")

    def input_finance_record(self):
        print("\n--- Add New Finance Record ---")
        description = input("Enter the description: ")
        amount = float(input("Enter the amount: "))
        
        # Asking user to choose between Income and Expense
        print("Select the category:")
        print("1. Income")
        print("2. Expense")
        choice = input("Enter your choice (1/2): ")
        
        if choice == '1':
            category = 'Income'
            amount = abs(amount)  # Ensure the amount is positive for income
        elif choice == '2':
            category = 'Expense'
            amount = -abs(amount)  # Ensure the amount is negative for expense
        else:
            category = 'Unknown'
            print("\n[!] Invalid category selected. Record will not be added.")

        # Automatically set the current date
        date = datetime.now().strftime('%Y-%m-%d')

        return FinanceRecord(description, amount, category, date)

    def display_records(self):
        if not self.records:
            print("\n[!] No records available.\n")
            return
        print("\n--- Existing Records ---")
        for idx, record in enumerate(self.records):
            print(f"{idx + 1}. {record.description} | {record.amount} | {record.category} | {record.date}")
        print("------------------------")

    def total_income_expenses(self):
        df = pd.DataFrame([record.to_dict() for record in self.records])
        if not df.empty:
            total_income = df[df['category'].str.lower() == 'income']['amount'].sum()
            total_expenses = df[df['category'].str.lower() == 'expense']['amount'].sum()
            remaining_salary =total_income + total_expenses  # Add total_expenses since it's negative
            
            print(f"\n--- Financial Overview ---")
            print(f"Total Income: {total_income}")
            print(f"Total Expenses: {total_expenses}")
            print(f"Remaining Balance: {remaining_salary}\n")
        else:
            print("\n[!] No records available to calculate totals.\n")

    def spending_distribution(self):
        df = pd.DataFrame([record.to_dict() for record in self.records])
        if not df.empty:
            distribution = df.groupby('category')['amount'].sum().reset_index()
            print("\n--- Spending Distribution by Category ---")
            print(distribution)
            print("------------------------")
        else:
            print("\n[!] No records available to display distribution.\n")

    def monthly_trends(self):
        df = pd.DataFrame([record.to_dict() for record in self.records])
        if not df.empty:
            df['date'] = pd.to_datetime(df['date'])
            df['month'] = df['date'].dt.to_period('M')
            trends = df.groupby(['month', 'category'])['amount'].sum().unstack(fill_value=0)
            print("\n--- Monthly Spending Trends ---")
            print(trends)
            print("------------------------")
        else:
            print("\n[!] No records available to display trends.\n")

def main():
    current_user = None

    while True:
        if not current_user:
            print("\n--- Welcome! Please Choose an Option ---")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("\nEnter your choice: ")

            if choice == '1':
                current_user = User.register()
            elif choice == '2':
                current_user = User.login()
            elif choice == '3':
                print("\n[✓] Goodbye! See you next time.\n")
                break
            else:
                print("\n[!] Invalid choice. Please try again.\n")

        else:
            print(f"\n--- Welcome, {current_user.username}! ---")
            print("1. Add Finance Record")
            print("2. View Report")
            print("3. Delete Record")
            print("4. Update Record")
            print("5. Total Income and Expenses")
            print("6. Spending Distribution by Category")
            print("7. Monthly Spending Trends")
            print("8. Logout")
            choice = input("\nEnter your choice: ")

            finance_manager = FinanceManager(current_user)
            finance_manager.load_data()

            if choice == '1':
                record = finance_manager.input_finance_record()
                if record.category != 'Unknown':  # Only add the record if it's valid
                    finance_manager.add_record(record)
                    print("\n[✓] Finance record added successfully!\n")
            elif choice == '2':
                finance_manager.generate_report()
            elif choice == '3':
                finance_manager.display_records()
                index = int(input("Enter the record number to delete: ")) - 1
                finance_manager.delete_record(index)
            elif choice == '4':
                finance_manager.display_records()
                index = int(input("Enter the record number to update: ")) - 1
                new_record = finance_manager.input_finance_record()
                finance_manager.update_record(index, new_record)
            elif choice == '5':
                finance_manager.total_income_expenses()
            elif choice == '6':
                finance_manager.spending_distribution()
            elif choice == '7':
                finance_manager.monthly_trends()
            elif choice == '8':
                current_user.logout()
                current_user = None  # Log the user out
            else:
                print("\n[!] Invalid choice. Please try again.\n")

if __name__ == "__main__":
    main()

