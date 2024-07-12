import os
import json
import datetime

current_directory = os.getcwd()
filename = "atmdb.json"
full_path = os.path.join(current_directory, filename)


class Method:
    @staticmethod
    def update_user(user):
        temp = []
        try:
            with open(full_path, 'r') as f:
                db = json.load(f)
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return
        for userCred in db:
            if userCred["userName"] != user["userName"]:
                temp.append(userCred)
            else:
                temp.append(user)
        with open(full_path, 'w') as fW:
            json.dump(temp, fW, indent=4)


class UserLogin:
    def __init__(self, userName, pin):
        self.userName = userName
        self.pin = pin

    def checkCredentials(self):
        try:
            with open(full_path, 'r') as f:
                db = json.load(f)
        except FileNotFoundError:
            print(f"Error: {filename} not found.")
            return None
        for userCred in db:
            if userCred["userName"] == self.userName:
                if userCred["pin"] == self.pin:
                    print("Login Successful")
                    return userCred
                else:
                    print("Invalid Password")
                    return None
        print("Invalid Credentials")
        return None


class TransactionsHistory:
    @staticmethod
    def view(transactionHistory):
        print("TRANSID\tTYPE\tAMOUNT\tDATE\tBALANCE")
        for data in transactionHistory.get("transactions", []):
            print(f"{data['transID']}\t{data['type']}\t{data['amt']}\t{data['dateOfTrans']}\t{data['currentBal']}")


class Transaction:
    @staticmethod
    def generate_transID():
        return int(datetime.datetime.now().timestamp() * 1000)

    @staticmethod
    def save_transaction(user, amt, trans_type):
        newData = {}
        currAmt = user["Balance"] + amt if trans_type == "credit" else user["Balance"] - amt
        newData["transID"] = Transaction.generate_transID()
        newData["type"] = trans_type
        newData["amt"] = amt
        newData["dateOfTrans"] = f"{datetime.datetime.now()}"
        newData["currentBal"] = currAmt
        user["Balance"] = currAmt
        user["transactions"].append(newData)
        Method.update_user(user)
        print("Transaction Saved Successfully!")


class Withdraw:
    def __init__(self, amt, user):
        if amt > user["Balance"]:
            print("Insufficient balance!")
            return
        Transaction.save_transaction(user, amt, "debit")


class Deposit:
    def __init__(self, amt, user):
        Transaction.save_transaction(user, amt, "credit")


class Transfer:
    def __init__(self, user):
        self.user = user

    def sendMoney(self):
        try:
            amt = int(input("Enter the amount: "))
            upi = input("Enter UPI ID: ")
            if amt > self.user["Balance"]:
                print("Insufficient balance!")
                return
            newData = {
                "transID": Transaction.generate_transID(),
                "upiID": upi,
                "type": "debit",
                "amt": amt,
                "dateOfTrans": f"{datetime.datetime.now()}",
                "currentBal": self.user["Balance"] - amt
            }
            self.user["Balance"] -= amt
            self.user["transactions"].append(newData)
            Method.update_user(self.user)
            print("Transaction Saved Successfully!")
        except ValueError:
            print("Invalid amount entered!")


# Driver's code
print("\n********** Welcome to our ATM **********")
userName = input("Enter your user ID: ")
try:
    pin = int(input("Enter your PIN : "))
except ValueError:
    print("Invalid PIN entered!")
    exit()

userLogin = UserLogin(userName, pin)
user = userLogin.checkCredentials()
if not user:
    exit()

print("MENU List:- ")
print("\n[1]. View Transaction History\n[2]. Make a withdrawal \n[3]. Make deposit \n[4]. Transfer money \n[5]. Exit the program.\n")

while True:
    try:
        op = int(input("\nEnter your choice: "))
        match op:
            case 1:
                TransactionsHistory.view(user)
            case 2:
                amt = int(input("Enter the amount you want to withdraw: "))
                Withdraw(amt, user)
            case 3:
                amt = int(input("Enter the amount you want to deposit: "))
                Deposit(amt, user)
            case 4:
                Transfer(user).sendMoney()
            case 5:
                print("Thanks for using our ATM service.\n")
                break
            case _:
                print("Invalid choice! Please enter a valid option.")
    except ValueError:
        print("Invalid input! Please enter a number.")
