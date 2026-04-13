# 🐍 Week 2 — Loops, Functions & Git
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [Git & GitHub Workflow](#1-git--github-workflow)
2. [ATM Banking System Assignment](#2-atm-banking-system-assignment)
3. [While Loops — Deep Dive](#3-while-loops--deep-dive)
4. [For Loops](#4-for-loops)
5. [Nested Loops & Patterns](#5-nested-loops--patterns)
6. [Functions](#6-functions)
7. [Lambda Functions](#7-lambda-functions)
8. [Recursion](#8-recursion)
9. [String Splitting & Map](#9-string-splitting--map)
10. [Notes & Tasks](#10-notes--tasks)

---

## 1. Git & GitHub Workflow

### 🔧 Push Your Code (First Time)
```bash
# 1. Create repo on GitHub and copy link
# 2. Initialize local repo
git init

# 3. Configure locally
git config --global user.name "Your Name"
git config --global user.email "you@email.com"

# 4. Connect to remote
git remote add origin <link>

# 5. Stage, commit, push
git add .
git commit -m "message"
git push origin main
```

> 💡 Check if connected: `git remote -v`

---

### 🤝 Working on Someone Else's Repository
```bash
# 1. Accept their invite
# 2. Clone their repo into a new folder
git clone <their-repo-link>
cd <folder>

# 3. Create your own branch
git checkout -b ahad

# 4. Make changes, then push
git add .
git commit -m "created new branch"
git push -u origin ahad
```

---

## 2. ATM Banking System Assignment

> **Assignment:** Build a simple ATM system. Ask for username and password, then let the user choose: check balance, deposit, or withdraw.

### Version 1 — Basic ATM (single session)
```python
user = input("please enter your username: ").lower()
passw = input("please enter your password: ")
balance = 745

if user == "ahad":
    if passw == "1234Aa":
        print("please choose the number of service from list below:")
        print("    1. check balance")
        print("    2. deposit money")
        print("    3. withdraw money")
        service = input("enter number here: ")

        if service == "1":
            print("your balance is", balance, "OMR")

        elif service == "2":
            deposit = float(input("enter your deposit amount: "))
            if deposit >= 0:
                balance = balance + deposit
                print(deposit, "OMR, Successfully deposited. Your current balance is", balance, "OMR")
            else:
                print("invalid number")

        elif service == "3":
            withd = float(input("enter your withdraw amount: "))
            if withd <= balance and withd >= 0:
                balance = balance - withd
                print(withd, "OMR, Successfully withdrawn. Your current balance is", balance, "OMR")
            elif withd > balance:
                print("you cannot withdraw more than your balance")
            else:
                print("invalid number")
        else:
            print("invalid")
    else:
        print("either password or username is incorrect")
else:
    print("either password or username is incorrect")
```

---

### Version 2 — ATM with Loop (multi-session)
```python
# Improved: allows multiple login attempts, press Enter to cancel
service = " "
user = " "

while user != "":
    user = input("please enter your username or press Enter to cancel: ").lower()
    passw = input("please enter your password: ")
    balance = 745

    if user == "ahad" and passw == "1234Aa":
        print("    1. check balance")
        print("    2. deposit money")
        print("    3. withdraw money")
        service = input("please choose the number of service from list below: ")

        if service == "1":
            print("your balance is", balance, "OMR")

        elif service == "2":
            deposit = float(input("enter your deposit amount: "))
            if deposit >= 0:
                balance = balance + deposit
                print(deposit, "OMR, Successfully deposited. Your current balance is", balance, "OMR")
            else:
                print("invalid number")

        elif service == "3":
            withd = float(input("enter your withdraw amount: "))
            if withd <= balance and withd >= 0:
                balance = balance - withd
                print(withd, "OMR, Successfully withdrawn. Your current balance is", balance, "OMR")
            elif withd > balance:
                print("you cannot withdraw more than your balance")
            else:
                print("invalid number")
    else:
        print("Access Denied")
```

---

## 3. While Loops — Deep Dive

### Count 1 to 10
```python
counter = 1
while counter <= 10:
    print(counter)
    counter = counter + 1
```

### Running Sum (1 to 10)
```python
counter = 1
summ = 0
while counter <= 10:
    summ = counter + summ
    print("in counter", counter, "the sum is", summ)
    counter = counter + 1
```

### Savings Doubling (5% Interest)
```python
balance = 10000
double = 20000
rate = 0.05
y = 0
while balance <= double:
    y = y + 1
    interest = balance * rate
    balance = balance + interest
print(balance)
print(y)  # → 15 years
```

### Countdown
```python
counter = 10
while counter >= 0:
    print(counter)
    counter -= 1  # ← prefer to update counter last
```

### Print Even Numbers (Two Ways)
```python
# Way 1 — step by 2
number = 0
while number <= 20:
    print(number)
    number += 2

# Way 2 — check with modulo
number = 0
while number <= 20:
    if number % 2 == 0:
        print(number)
    number = number + 1
```

### Prime Number Checker
```python
n = 2
while n <= 200:
    c = 2
    flag = True
    while c < n:
        if n % c == 0:
            flag = False
        c += 1
    if flag:
        print(n, flag)
    n += 1
```

### Running Average of Grades
```python
c = 0
total = 0
ave = 0
while c >= 0:
    grades = int(input("enter 4 grades: "))
    total = total + grades
    c += 1
    print("counter", c)
    ave = total / c
    print("average is ", ave)
```

### Find Maximum Grade
```python
m = 0
grade = 0
while grade >= 0:
    grade = int(input("enter a grade: "))
    if grade >= m:
        m = grade
    print(m, "is max")
```

### Find Minimum Grade
```python
grade = 0
m = 100
while grade >= 0:
    grade = int(input("enter a grade: "))
    if grade <= m and grade >= 0:
        m = grade
print(m, "is min")
```

### Max Until Empty Input
```python
mx = 0
number = 0
num = 0
while number != '':
    number = input("enter a number or press Enter to exit: ")
    if number.isnumeric():
        num = int(number)
        if num >= mx:
            mx = num
    print("max is ", mx)

print("max is ", mx)
```

### Print Negative Numbers
```python
number = 0
num = 0
while number != '':
    number = input("enter a number or press Enter to exit: ")
    if number.isnumeric():
        num = int(number)
        if num < 0:
            print("negative is ", num)
```

### Detect Consecutive Duplicates
```python
# Approach 1 — check if current == previous
cur = 0
pre = 0
while cur != "":
    cur = input("input current number: ")
    if cur.isdigit():
        cur = int(cur)
        if cur == pre:
            print("current same as previous")
        pre = cur

# Approach 2 — cleaner version
v = int(input("enter a value: "))
s = input("enter a value: ")
while s != "":
    pre = v
    v = int(s)
    if v == pre:
        print("duplicates")
    s = input("enter a value: ")
```

### Sum of Digits in a Number
```python
# Method: using string indexing
count = 0
total = 0
num = input("enter a number: ")
while count < len(num):
    total = total + int(num[count])
    count += 1
print(total)
```

---

## 4. For Loops

### Basic For Loop with `range()`
```python
for i in range(1, 10):
    print(i, end="")
```

### Iterate Over a String
```python
name = 'Ahad'
for i in range(len(name)):
    print(name[i], end=" ")
```

### Reverse Loop
```python
for i in range(10, 1, -1):
    print(i)
```

### Interest Table
```python
rate = 5
inbalance = 10000
nyears = int(input("enter number of years: "))
balance = inbalance

for year in range(1, nyears + 1):
    interest = balance * rate / 100
    balance = balance + interest
    print("%4d %10.2f" % (year, balance))
```

### Power Table
```python
n = 0
for i in range(1, 5):
    print("for the number: ", i)
    for s in range(1, 7):
        n = i ** s
        print(i, "**", s, " = ", n, end=" | ")
    print("")
```

### Sum of Digits in a Number (using for loop)
```python
total = 0
name = 'Ahad'
number = input("enter a number: ")

for n in number:
    print(int(n), end=" ")
    total = total + int(n)

print("\nsum is", total)

for na in name:
    print(na)
```

### Count Vowels in a Word
```python
v = 0
word = input("enter a word: ")
for i in word:
    if i.lower() in "aeiou":
        v += 1
        print(i, end=" | ")
```

### Reverse a Word
```python
w = "word"
for i in range(1, (len(w) + 1)):
    print(w[-i], end="")
```

### Fibonacci Sequence — Final Version
```python
def fib(m):
    a = 0
    b = 1
    for i in range(m):
        a, b = b, a + b
        if a > 8:
            break
        else:
            print(a, end=" ")

print(fib(30))
```

```python
# Simple Fibonacci up to N terms
a = 0
b = 1
for i in range(27):
    print(a, end=" ")
    a, b = b, a + b
```

---

## 5. Nested Loops & Patterns

### Rectangle of Stars
```python
n = "*"
for i in range(0, 2):
    for i in range(0, 6):
        print(n, end="")
    print("")
```

### Right Triangle (Growing)
```python
for i in range(6):
    for u in range(i):
        print("*", end="")
    print("")
```

### Right Triangle (Shrinking)
```python
for i in range(6, 0, -1):
    for u in range(i):
        print("*", end="")
    print("")
```

### Left-Aligned Triangle
```python
for i in range(6):
    print(" " * (6 - i), '*' * i, end="")
    print()
```

---

## 6. Functions

### Rectangle Area
```python
def areaRect(l, w):
    area = l * w
    return area

area = areaRect(2, 8)
print(area)  # → 16
```

### Volume of a Cube
```python
def volume(side):
    if side >= 0:
        return side ** 3
    else:
        return "can't be negative"

n = int(input())
volume(n)
```

### Volume of a Pyramid
```python
def parvolume(a, h):
    if a >= 0 and h >= 0:
        return (a ** 2) * (h / 3)
    else:
        return "can't be negative"

a = float(input("enter base length: "))
h = float(input("enter height: "))
print("area of pyramid is ", parvolume(a, h))
```

### Perfect Square Checker ✅ (Correct Version)
```python
from math import sqrt

def perfectsqr(n):
    sq = sqrt(int(n))
    if sq.is_integer():
        return "perfect square, square root is ", sq
    else:
        return "not a perfect square, square root is ", sq

n = input("enter a number: ")
perfectsqr(n)
```

### Box Around Text
```python
def boxstring(content):
    n = len(content)
    print("-" * (n + 2))
    print("|" + content + "|")
    print("-" * (n + 2))

boxstring('ahad')
```
Output:
```
------
|ahad|
------
```

### Multiplication Table
```python
def table(c):
    while c <= 12:
        for i in range(1, 13):
            r = i * c
            print(i, "*", c, "=", r, "|", end="")
        print("")
        print("")
        c += 1

table(1)
```

### Factorial
```python
def factorial(n):
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

factorial(5)  # → 120
```

### Function Inside Function
```python
def cal(a, b):
    def summ():
        r = a + b
        return r
    r1 = 5 + summ()
    return r1

cal(15, 10)  # → 30
# ⚠️ summ() cannot be called from outside cal() — it's not defined there
```

### Using `global` Variable
```python
balance = 1000

def withdraw(amount):
    global balance  # access the outer variable
    if balance > amount:
        balance -= amount
        return balance

amount = int(input())
print("balance", withdraw(56))
```

### Functions with Default Arguments
```python
def default1(score, n='ahad'):
    return "score: ", n, score

print(default1(100))          # → score: ahad 100
print(default1("layla", 76))  # → score: layla 76
```

### Variable Number of Arguments (`*args`)
```python
def func(*a):
    for i in a:
        print(i, end=" ")

func(2, 3, "ahad", 5, "rr", 43)
```

### Student Grade Average
```python
total = 0
ave = 0
totalAnother = 0


def ave1(g):
    ave = total / float(g)
    return ave


g = input("how many exam grades does each student have? ")

for i in range(int(g)):
    print("Exam ", i + 1, ": ", end="")
    e = float(input())
    total += e
print("the average is ", ave1(g))


def ave2(g):
    ave2 = totalAnother / float(g)
    return ave2


while True:
    another = input("enter exam grades for another student (Y/N)? ").lower()
    if another == 'y':
        for u in range(int(g)):
            print("Exam ", u + 1, ": ", end="")
            a = float(input())
            totalAnother += a
        print("the average is ", ave2(g))
    else:
        break
```

---

## 7. Lambda Functions

> **Lambda** = a small, anonymous (no-name) function written in one line.

```python
# Basic usage
word = "ahad"
upper = lambda x: x.upper()
print(upper(word))  # → AHAD

# Multiple arguments
v = lambda x, y, z: x * y * z
print(v(2, 3, 4))  # → 24

# Conditional logic
check = lambda x: "positive" if x > 0 else "negative" if x < 0 else "zero"
print(check(0))   # → zero
print(check(7))   # → positive
```

> 📖 **Read more:** [Lambda Functions — GeeksForGeeks](https://www.geeksforgeeks.org/python/python-lambda-anonymous-functions-filter-map-reduce/)

---

## 8. Recursion

> **Recursion** = a function that calls itself. Always needs a **base case** to stop.

### Factorial (Recursive)
```python
def factorial(n):
    if n == 0 or n == 1:  # base case
        return 1
    return n * factorial(n - 1)

factorial(5)  # → 120
```

### Sum 1 to N (Recursive)
```python
def summ(n):
    if n == 0:  # base case
        return 0
    return summ(n - 1) + n

summ(10)  # → 55
```

### Count Digits (Recursive)
```python
n = int(input("enter a digit: "))

def count1(n):
    if n == 0:
        return 0
    return 1 + count1(n // 10)

count1(n)
```

### Fibonacci (Recursive) — Work in Progress
```python
def fib(n):
    if n == 0:
        return 0
    return fib(n - 1) + 1  # ⚠️ still needs fixing for proper Fibonacci

fib(10)
```

---

## 9. String Splitting & Map

### `.split()` — Break a String
```python
name = "ahad salim"
fname = name.split()[0]
print(fname)   # → ahad

lname = name.split()[1]
print(lname)   # → salim

name = name.split()
print("full name", name)  # → full name ['ahad', 'salim']
```

### `map()` — Convert Multiple Inputs at Once
```python
# Read 3 integers separated by spaces
width, length, height = map(int, input("enter width length and height: ").split())

# Read time in HH:MM format
hour, minute = map(int, input("enter the time HH:MM ").split(":"))

# Read name and grade
name, grade = input("enter student name and grade ").split()
grade = int(grade)
```

### Regular Expressions (Intro)
```python
import re
text = "SplitStringByUpper"
result = re.split('(?=[A-Z])', text)
print(result)  # → ['Split', 'String', 'By', 'Upper']
```

> 📖 **Task:** Read more about Regular Expressions (`re` module)

---

## 10. Notes & Tasks

| # | Note |
|---|------|
| 📝 | **void** functions → always called "setters" (they do something, return nothing) |
| 📝 | **return** functions → called "getters" (they give back a value) |
| 📝 | **Recursion** has a base case, just like `factorial(0) = 1` |
| 🔧 | **Weekend exercise:** Write 3 functions — `display` (void), `deposit` (void), `withdraw` (void) for ATM |
| 🔧 | **Task:** Write numbers in words (e.g. 123 → "one hundred twenty three") |
| 🔧 | **Read:** `change func names`, `pass by reference`, `pass by name` |
| 🔧 | **Try:** Fibonacci recursive (fix the version above) |

---

*📅 Notes taken: April 5–9, 2026*
