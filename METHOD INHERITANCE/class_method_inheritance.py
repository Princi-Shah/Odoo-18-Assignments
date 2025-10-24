class BankAccount:
    """
    define: BankAccount
    description: calculates and shows deposited amount, withdrawals and displays the
                 upto date data
    returns: None
    """
    def __init__(self, account_number, holder, balance):
        self.account_number = account_number
        self.holder = holder
        self.balance = balance

    def deposit(self, amount):
        """
        define: Deposit
        description: Deposits the given amount into the account by adding it into the
                     current balance
        returns: None
        """
        self.balance += amount
        print("Deposit Successful")
        print("Deposit Amount:", amount)

    def withdrawal(self, amount):
        """
        define: withdrawal
        description: Calculates withdrawal amount by deducting it from the main balance.
        returns: None
        """
        if amount <= self.balance:
            self.balance -= amount
            print("Withdrawal Successful")
            print("Withdrawal Amount:", amount)
        else:
            print("Withdrawal Failed due to insufficient balance")
            print("Withdrawal Amount:", amount)

    def displaying_balance(self):
        """
        define: displaying balance
        description: displays user information with number, name and balance
        """
        print("Account Number:", self.account_number)
        print("Holder:", self.holder)
        print("Balance Amount:", self.balance)


class SavingsAccount(BankAccount):
    """
    define: SavingsAccount
    description: Calculates the interest based on the values fetched from the main
                 parent class (BankAccount)
    returns: None
    """
    def __init__(self, account_number, holder, balance, interest_rate):
        super().__init__(account_number, holder, balance)
        self.interest_rate = interest_rate

    def interest(self):
        """
        define: Interest
        description: Calculates the interest based on the values fetched from the main
        returns: None
        """
        interest_amount = (self.interest_rate * self.balance) / 100
        print("Interest Amount:", interest_amount)
        print(f"Total Balance after Interest: {self.balance + interest_amount}")


class CurrentAccount(BankAccount):
    """
    define: CurrentAccount
    description: Calculates the withdrawal amount and shows the total balance based on
                 the data fetched from the main parent class (BankAccount).
    returns: None
    """
    def __init__(self, account_number, holder, balance, overdraft_limit):
        super().__init__(account_number, holder, balance)
        self.overdraft_limit = overdraft_limit

    def withdrawal(self, amount):
        """
        define: Withdrawal
        description: Calculates the balance after withdrawal and shows the withdrawal
                    amount
        returns: None
        """
        if amount <= (self.balance + self.overdraft_limit):
            self.balance -= amount
            print("Withdrawal Successful")
            print("Withdrawal Amount:", amount)
            print(f"Balance after withdrawal: {self.balance}")
        else:
            print("Withdrawal Failed due to exceeding overdraft limit")


def main_choice_menu():
    """
    define: Main Choice Menu
    description: Main Choice Menu
    returns: None
    """
    print("\nMain Menu")
    print("1. Savings Account")
    print("2. Current Account")
    print("3. Exit")

def sub_menu():
    """
    define: Sub Menu
    description: Sub Menu choices
    returns: None
    """
    print("\nSub Menu")
    print("1. Deposit")
    print("2. Withdraw")
    print("3. Display Balance")
    print("4. Calculate Interest")
    print("5. Exit to Main Menu")

def info_details():
    """
    define: Info Details
    description: displays details for user to enter a value in it.
    returns: acc_number, holder_nm, total_balance
    """
    acc_number = input("Enter Account Number: ")
    holder_nm = input("Enter Holder Name: ")
    while True:
        try:
            total_balance = float(input("Enter Initial Balance: "))
            break
        except ValueError:
            print("Invalid input! Please enter a valid  number for balance.")
    return acc_number, holder_nm, total_balance

def main_menu():
    """
    define: Main Menu
    description: Main Menu calling all the functionalities
    returns: None
    """
    while True:
        main_choice_menu()
        try:
            choice = int(input("Enter Choice: "))
        except ValueError:
            print("Invalid input! Please enter a valid  number for choice.")
            continue

        if choice == 1:
            account_number, holder, balance = info_details()
            while True:
                try:
                    interest_rate = float(input("Enter interest rate in (%): "))
                    break
                except ValueError:
                    print("Invalid input! Please enter a valid  number for interest rate.")
            account = SavingsAccount(account_number, holder, balance, interest_rate)

        elif choice == 2:
            account_number, holder, balance = info_details()
            while True:
                try:
                    overdraft_limit = float(input("Enter overdraft limit: "))
                    break
                except ValueError:
                    print("Invalid input! Please enter a valid number.")
            account = CurrentAccount(account_number, holder, balance, overdraft_limit)

        elif choice == 3:
            print("Bye!")
            break
        else:
            print("Invalid choice! Try again.")
            continue

        while True:
            sub_menu()
            try:
                sub_choice = int(input("Enter your choice: "))
            except ValueError:
                print("Invalid input! Please enter a number.")
                continue

            if sub_choice == 1:
                try:
                    deposit_amount = float(input("Enter deposit amount: "))
                    account.deposit(deposit_amount)
                except ValueError:
                    print("Invalid input! Please enter a valid number.")

            elif sub_choice == 2:
                try:
                    withdrawal_amount = float(input("Enter withdrawal amount: "))
                    account.withdrawal(withdrawal_amount)
                except ValueError:
                    print("Invalid input! Please enter a valid number.")

            elif sub_choice == 3:
                account.displaying_balance()

            elif sub_choice == 4:
                if isinstance(account, SavingsAccount):
                    account.interest()
                else:
                    print("Interest calculation is only for Savings Account!")

            elif sub_choice == 5:
                print("Back to Main Menu...")
                break
            else:
                print("Invalid choice. Please try again!")

main_menu()