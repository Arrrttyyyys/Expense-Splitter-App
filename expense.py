import tkinter as tk
from tkinter import messagebox

class ExpenseSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Splitter")
        self.expenses = []
        self.participants = []

        # GUI Elements
        self.setup_gui()

    def setup_gui(self):
        # Labels
        tk.Label(self.root, text="Expense Name").grid(row=0, column=0)
        tk.Label(self.root, text="Amount").grid(row=1, column=0)
        tk.Label(self.root, text="Paid By").grid(row=2, column=0)
        tk.Label(self.root, text="Participants (comma separated)").grid(row=3, column=0)

        # Entries
        self.expense_name_entry = tk.Entry(self.root)
        self.expense_name_entry.grid(row=0, column=1)

        self.amount_entry = tk.Entry(self.root)
        self.amount_entry.grid(row=1, column=1)

        self.paid_by_entry = tk.Entry(self.root)
        self.paid_by_entry.grid(row=2, column=1)

        self.participants_entry = tk.Entry(self.root)
        self.participants_entry.grid(row=3, column=1)

        # Buttons
        tk.Button(self.root, text="Add Expense", command=self.add_expense).grid(row=4, column=0)
        tk.Button(self.root, text="Calculate Split", command=self.calculate_split).grid(row=4, column=1)

        # Expense List
        self.expense_listbox = tk.Listbox(self.root, width=50)
        self.expense_listbox.grid(row=5, column=0, columnspan=2)

    def add_expense(self):
        name = self.expense_name_entry.get()
        amount = float(self.amount_entry.get())
        paid_by = self.paid_by_entry.get()
        participants = self.participants_entry.get().split(',')

        self.expenses.append({
            'name': name,
            'amount': amount,
            'paid_by': paid_by,
            'participants': participants
        })

        self.expense_listbox.insert(tk.END, f"{name} - ${amount:.2f} - Paid by {paid_by}")

        # Clear Entries
        self.expense_name_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.paid_by_entry.delete(0, tk.END)
        self.participants_entry.delete(0, tk.END)

    def calculate_split(self):
        balances = {}

        for expense in self.expenses:
            amount_per_person = expense['amount'] / len(expense['participants'])
            if expense['paid_by'] not in balances:
                balances[expense['paid_by']] = 0

            balances[expense['paid_by']] += expense['amount']

            for participant in expense['participants']:
                if participant not in balances:
                    balances[participant] = 0
                balances[participant] -= amount_per_person

        result = "Balances:\n"
        for participant, balance in balances.items():
            result += f"{participant}: {'owes' if balance < 0 else 'is owed'} ${abs(balance):.2f}\n"

        detailed_result = "Detailed Owes:\n"
        for expense in self.expenses:
            amount_per_person = expense['amount'] / len(expense['participants'])
            for participant in expense['participants']:
                if participant != expense['paid_by']:
                    detailed_result += f"{participant} owes {expense['paid_by']} ${amount_per_person:.2f} for {expense['name']}\n"

        messagebox.showinfo("Calculation Result", result + "\n" + detailed_result)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseSplitterApp(root)
    root.mainloop()