user = input("please enter your username: ").lower()
passw = input("please enter your password: ")
balance = 745
if user == "ahad" :
    if passw == "1234Aa" :
        print("please choose the number of servise from list bellow:")
        print("    1. check balance")
        print("    2. deposit money")
        print("    3. withdraw money")
        servise = int(input("enter number here: "))
        if servise == 1 :
            print("your balance is", balance,"OMR")
        elif servise == 2:
            deposit = float(input("enter your deposit amount: "))
            if deposit >= 0:
                balance =balance + deposit
                print(deposit, "OMR, Successfully deposited your current balance is",balance, "OMR")
            else :
                print("invalid number")
        elif servise == 3:
            withd = float(input("enter your withd amount: "))
            if withd <= balance :
                balance = balance - withd
                print(withd, "OMR, Successfully withdrawed your current balance is",balance, "OMR")
            else :
                print("you can not withdrow more than your balance")
        else:
            print("invalid number")
    else :
        print("either password or username is incorrect")
else:
    print("either password or username is incorrect")
        