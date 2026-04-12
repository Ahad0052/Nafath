# 🐍 Week 1 — Python Fundamentals
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [Math & Operators](#1-math--operators)
2. [Variables & Data Types](#2-variables--data-types)
3. [String Methods](#3-string-methods)
4. [User Input & Formatting](#4-user-input--formatting)
5. [Conditionals (if / elif / else)](#5-conditionals-if--elif--else)
6. [Boolean Logic](#6-boolean-logic)
7. [While Loops](#7-while-loops)
8. [Practice Programs](#8-practice-programs)
9. [Notes & Tasks](#9-notes--tasks)

---

## 1. Math & Operators

### Compound Interest Formula
```python
b = int(input("enter b"))
r = int(input())
n = int(input())

n = b * (1 + (r / 100)) ** n
print(n)
```

### Rials & Bisa Converter
```python
a = 1500
bisa = (a % 1000)
rial = (a // 1000)
print("i have ", rial, " rial and ", bisa, " bisa")

b = 10500
bisa1 = (b % 1000)
rial1 = (b // 1000)
print("i have ", rial1, " rial and ", bisa1, " bisa")
```
> 💡 `%` = modulo (remainder), `//` = floor division

### `abs()` — Absolute Value
```python
abs(-678)  # → 678
```

### Math Library
```python
from math import *
y = sqrt(5)
print(y)       # → 2.2360679...
print(int(y))  # → 2
```

---

## 2. Variables & Data Types

### Augmented Assignment
```python
t = 10
t += 5
print(t)  # → 15
```

### String Concatenation
```python
fn = "Ahad"
ln = "Aljabri"
n = fn + " " + ln
print(n)           # → Ahad Aljabri
print(fn, " ", ln) # → Ahad   Aljabri
```

### String Repetition
```python
b = "x" * 100
print(b)  # prints x 100 times
```

### String Indexing & Length
```python
name = "ahad salim"
print(len(name))        # → 10
print(name[9], name[-1]) # → m m  (last character, 2 ways)
```

### Escape Characters
```python
print("\\")  # → \
```

### Boolean
```python
b = True
print(b)  # → True

if False:
    print("a")  # this never runs
```

---

## 3. String Methods

### Common Methods
```python
"hi".upper()  # → "HI"
```

```python
title = "python for everyone"
title = title.replace("for everyone", "")
title = title.upper()
title = title + "program"
print(title)  # → PYTHON program
```

```python
sth = "a,a,a,a"
r = sth.replace("a", "b", 3)  # replace only first 3 occurrences
print(r)  # → b,b,b,a
```

```python
ex = "asd das sda"
r = ex.rfind("a", 1)  # find 'a' searching from right, starting at index 1
print(r)
```

```python
ex = "a00 0a0 00a"
r = ex.count("a", 0)  # count occurrences of 'a' starting at index 0
print(r)  # → 3
```

> 📖 **Reference:** [All Python String Methods — W3Schools](https://www.w3schools.com/python/python_ref_string.asp)

---

## 4. User Input & Formatting

### Basic Input
```python
n = input("name: ")
age = int(input("age: "))
```

### `%` Formatting (Old Style)
```python
ppl = 11111
print("price is %4d" % (ppl))  # → price is 11111
```

```python
cpp = 6
pp = float(input())
cv = float(input())
pv = pp * cpp
ppo = pp / pv
print("%f" % ppo)
```

> 💡 **Print formatting options:**
> - `%d` → integer
> - `%f` → float
> - `%4d` → integer with width 4
> - `%.2f` → float with 2 decimal places

---

## 5. Conditionals (if / elif / else)

### Floor Number (Superstitious Building)
```python
floor = int(input("floor number: "))
if floor > 13:
    af = floor - 1
elif floor == 13:
    af = floor
    print("danger")
else:
    af = floor
print(af)
```

### Even or Odd
```python
n = int(input("enter a number: "))
a = n % 2
print("mod is ", a)
if a == 0:
    print("number is even")
else:
    print("number is odd")
```

### Grade Discount
```python
n = int(input("enter the grade: "))
if n >= 85:
    print("discount")
else:
    print("nothing")
```

### Price After Discount
```python
price = int(input("enter price: "))
if price >= 128:
    discount = 0.92
else:
    discount = 0.84

after = price * (1 - discount)
print("price after discount is ", after)
```

### Tile Gap Calculator
```python
numberTiles = int(input("enter number of tiles: "))
totalW = 100
tileW = 5
maxTiles = totalW // tileW
usedW = numberTiles * tileW
remain = totalW - usedW
gap = remain / 2
print("number of tiles: ", numberTiles)
print("gap: ", gap)
```

### Earthquake Damage Level
```python
n = float(input("enter degree: "))
if n >= 8:
    print("very very big damage")
elif n >= 7 and n <= 7.99:
    print("very big damage")
elif n >= 6 and n <= 6.99:
    print("damage")
elif n >= 5 and n <= 5.99:
    print("damage")
else:
    print("light damage")
```

### Water State
```python
temp = float(input("enter temp: "))
if temp > 0 and temp < 100:
    print("water is liquid")
elif temp >= 100:
    print("its gas")
else:
    print("solid")
```

### Grade Letter
```python
from sys import exit

g = float(input("enter your grade: "))
if g > 100 or g < 0:
    exit("wrong value")

if g >= 90 and g <= 100:
    print("a")
elif g >= 80 and g < 90:
    print("b")
elif g >= 70 and g < 80:
    print("c")
elif g >= 60 and g < 70:
    print("c")
elif g >= 50 and g < 60:
    print("p")
else:
    print("fail")
```

### Login System
```python
un = input("enter your username: ")
if un == "admin":
    p = int(input("input password: "))
    if p == 1234:
        print("Access granted")
elif un == "guest":
    print("Access granted")
else:
    print("wrong username")
```

### Nested Conditionals — Engineering & Gender Check
```python
major = input("type your major: ").lower()
gender = input("what is your gender: ").lower()

# Using .find()
r = major.find("eng", 0)
rg = gender.find("f", 0)
if r != -1:
    if rg != -1:
        print("u r a wonderful eng.")
    else:
        print("not female")
else:
    print("not eng.")
```

---

## 6. Boolean Logic

### `and`, `or`, `not` Operators
```python
attending = True
grade = 70

if not attending or grade < 70:
    print("drop")

if attending and not grade < 70:
    print("stay")

if attending and grade >= 70:
    print("stay without not")
```

> 💡 `not` flips True → False and vice versa

---

## 7. While Loops

### Savings Doubling Problem
```python
# Task: How many years to double savings at 5% interest?
s = 10000
d = 20000
intr = 0.05
y = 0
while s < d:
    s *= (1 + intr)
    y = y + 1

print(s)  # final amount
print(y)  # years taken
```

---

## 8. Practice Programs

### Time Comparison (HH:MM)
```python
# Task: Compare two times and find which comes first
t1 = input("enter time1 HH:MM : ")
t2 = input("enter time2 HH:MM : ")

time11 = []
time1 = t1.split(":")
for a in time1:
    a = int(a)
    time11.append(a)

time22 = []
time2 = t2.split(":")
for b in time2:
    b = int(b)
    time22.append(b)

if time11[0] > time22[0]:
    print("time 2 comes first")
elif time11[0] < time22[0]:
    print("time 1 comes first")
elif time11[0] == time22[0] and time11[1] > time22[1]:
    print("time 2 comes first")
elif time11[0] == time22[0] and time11[1] < time22[1]:
    print("time 1 comes first")
else:
    print("times both the same")
```

---

## 9. Notes & Tasks

| # | Note |
|---|------|
| 📝 | **Implicit** → you need to think and extract info from the problem |
| 📝 | **Explicit** → info is directly given |
| 📝 | `void` return value in OOP means the function returns nothing |
| 📝 | Django can be used for web development in Python |
| 🔧 | **Task:** What is the difference between methods and functions? |
| 🔧 | **HW:** Write an article on LinkedIn about using `print()` formatting: `,` vs `%` vs `f-strings` |
| 🔧 | **Task:** What is an API? |

---

*📅 Notes taken: April 1–4, 2026*
