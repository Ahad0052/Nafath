# 🐍 Week 3 — Data Structures, Files & Error Handling
> AI & Data Science Bootcamp | Ahad Aljabri

---

## 📚 Table of Contents
1. [ATM System — Final Version (with Functions)](#1-atm-system--final-version-with-functions)
2. [Lists](#2-lists)
3. [List Methods & Operations](#3-list-methods--operations)
4. [2D Lists (Nested Lists)](#4-2d-lists-nested-lists)
5. [Searching Algorithms](#5-searching-algorithms)
6. [Dictionaries](#6-dictionaries)
7. [Tuples](#7-tuples)
8. [Sets](#8-sets)
9. [Files](#9-files)
10. [Error Handling (try / except)](#10-error-handling-try--except)
11. [Notes & Tasks](#11-notes--tasks)

---

## 1. ATM System — Final Version (with Functions)

> Refactored version of the Week 2 ATM assignment — each action is now its own function.

```python
balance = 745

def check_balance():
    global balance
    print("your balance is", balance, "OMR")

def deposit():
    global balance
    amount = float(input("enter deposit amount: "))
    if amount > 0:
        balance += amount
        print(amount, "OMR deposited, new balance:", balance, "OMR")
    else:
        print("invalid amount")

def withdraw():
    global balance
    amount = float(input("Enter withdraw amount: "))
    if amount <= 0:
        print("invalid amount")
    elif amount > balance:
        print("Cannot withdraw more than your balance")
    else:
        balance -= amount
        print(amount, "OMR withdrawn, New balance:", balance, "OMR")

def login(user, passw):
    if user == "ahad" and passw == "1234Aa":
        return True
    else:
        return False

def main():
    while True:
        user = input("Enter username, or press Enter to quit: ")
        if user == "":
            break
        passw = input("Enter password: ")

        if login(user, passw):
            print("1. check Balance")
            print("2. deposit")
            print("3. withdraw")
            service = int(input("Choose a service: "))
            if service == 1:
                check_balance()
            elif service == 2:
                deposit()
            elif service == 3:
                withdraw()
            else:
                print("Invalid choice")
        else:
            print("Access Denied")

main()
```

---

## 2. Lists

> A list is an **ordered, mutable** collection. Can hold mixed types.

### Creating & Accessing
```python
values = ["ahad", "aljabri", 29, 45, 26, 33, 887, 43, 2, 3]

print(len(values))                              # → 10  (len works on lists too)
print(values[0][3])                             # → 'd'  (index into a string element)
print(values[1][len(values[1]) - 1])            # last character of "aljabri" → 'i'
print(values[1][len(values[1]) // 2])           # middle character → 'j'
```

> 💡 **String vs List:** Strings are **immutable** (can't change characters). Lists are **mutable** (can change elements).

### Building a List with a Loop
```python
grades = []
for i in range(5):
    grade = float(input("enter student grade: "))
    grades.append(grade)

print("final grades", grades)

# Iterate by element
for i in grades:
    print(i)

# Iterate by index
for i in range(len(grades)):
    print(i, grades[i])
```

### Common List Operations
```python
values = []
values.append(1)      # add to end → [1]
values.append(2)      # → [1, 2]
values.append(3)      # → [1, 2, 3]
values[2] = 2         # change element → [1, 2, 2]
```

---

## 3. List Methods & Operations

### Inserting at a Position (Manual vs `.insert()`)
```python
# Manual shift — insert 'b' at index 1
l1 = ['a', 'c', 'd', 'e']
l1.append("")                      # make room at the end
for i in range(len(l1) - 1, 1, -1):
    l1[i] = l1[i - 1]
l1[1] = 'b'
print(l1)  # → ['a', 'b', 'c', 'd', 'e']

# Easier way — use .insert()
l2 = ['a', 'c', 'd', 'e']
l2.insert(1, "b")
print(l2)  # → ['a', 'b', 'c', 'd', 'e']
```

### Searching, Deleting, Checking
```python
# Check if element exists
if 'b' in l2:
    print("yes b is here")

# Find index of an element
print("d at index", l2.index("d"))

# Delete by index
l2.pop(3)
print("after popping index 3", l2)

# Delete by value
l2.remove('a')
print("after removing a", l2)
```

### Concatenation, Repetition, Comparison, Copy
```python
l3 = [1, 2, 3]
l4 = [5, 7, 8]

l5 = l3 + l4          # concatenate → [1, 2, 3, 5, 7, 8]
l6 = [""] * 5         # repeat      → ['', '', '', '', '']
print(l3 == l4)       # compare     → False

# ⚠️ To properly copy a list use list()
l3 = list(l4)         # now l3 is a copy of l4, not a reference
```

### Slicing
```python
l7 = [10, 20, 30, 40, 50, 60, 70, 80]
print(l7[4:7])  # → [50, 60, 70]
print(l7[6:])   # → [70, 80]
```

### Reverse a List
```python
n = [1, 2, 3, 4, 5][::-1]
print(n)  # → [5, 4, 3, 2, 1]
```

### Multiply All Elements by a Factor
```python
def mul(li, factor):
    li = list(li)                  # copy so original stays the same
    for i in range(len(li)):
        li[i] *= factor
    return li

listt = [1, 2, 3]
print(mul(listt, 2))   # → [2, 4, 6]
print(listt)           # → [1, 2, 3]  (original unchanged)
```

### Sum of All Elements
```python
list1 = [1, 2, 34, 6, 8, 3, 5, 1]
total = 0
for i in range(len(list1)):
    total += list1[i]
print("final total is", total)
```

### Find Max & Min
```python
list1 = [1, 2, 34, 6, 8, 3, 5]

# Max — way 1 (index loop)
maxx = list1[0]
for i in range(len(list1)):
    if maxx < list1[i]:
        maxx = list1[i]

# Max — way 2 (for-in loop, cleaner)
maxx = list1[0]
for i in list1:
    if i > maxx:
        maxx = i

# Min
minn = list1[0]
for i in list1:
    if i < minn:
        minn = i
```

### Filter Odd Numbers
```python
list1 = [1, 2, 34, 6, 8, 3, 0, 5]
for i in list1:
    if i % 2 != 0:
        print(i, "is odd number")
```

### Replace Negatives with Zero
```python
list1 = [1, 45, 7, -3, -5, -2, 4, 6, 3, -8, 0]
for i in range(len(list1)):
    if list1[i] < 0:
        print("negative is", list1[i], end="  ...  ")
        list1[i] = 0
        print("now converted to", list1[i])
print("new list:", list1)
```

### Two Numbers That Sum to Target
```python
l = [3, 2, 7, 6, 8, 9, 1, 0, 4]
target = int(input("enter target: "))
for i in range(len(l)):
    for j in range(i + 1, len(l)):
        if l[j] + l[i] == target:
            print(l[j], "+", l[i], "=", target)
```

### Find Duplicates & Count Occurrences (Clean Version)
```python
l = [3, 2, 7, 5, 6, 8, 9, 1, 0, 4, 4, 3, 5, 5, 5, 5]
check = []
for i in l:
    if i not in check:
        c = l.count(i)
        if c > 1:
            print(i, "repeated", c, "times")
        check.append(i)
```

### Find Numbers Greater Than 100
```python
l8 = [1, 2, 3, 567, 3, 9, 0, 654, 101]
found = False
n = 0
for i in l8:
    if i > 100:
        n += 1
        print("a number greater than 100 found:", i, "|", n, "times")
        found = True

print("found" if found else "not found")
```

### List of Functions (Mini App)
```python
l = [1, 2, 4, 3, 4, 6, 0, -3, -6, -6, 7]

def findmax():
    global l
    mx = l[0]
    for i in range(len(l)):
        if l[i] > mx:
            mx = l[i]
    print("max is", mx)

def findmin():
    global l
    mn = l[0]
    for i in range(len(l)):
        if l[i] < mn:
            mn = l[i]
    print("min is", mn)

def findindex():
    global l
    num = int(input("enter number to find: "))
    for i in range(len(l)):
        if l[i] == num:
            print("found at index", i)

def nonegatives():
    global l
    for i in range(len(l)):
        if l[i] < 0:
            l[i] = 0
    print("list without negatives:", l)

def main():
    print(l)
    print("1 - find max\n2 - find min\n3 - find index\n4 - convert negatives to zeros")
    inn = int(input("enter a number: "))
    if inn == 1:   findmax()
    elif inn == 2: findmin()
    elif inn == 3: findindex()
    elif inn == 4: nonegatives()

main()
```

---

## 4. 2D Lists (Nested Lists)

```python
l9 = [
    [1, 2, 3],
    [4, 2, 1],
    [3, 6, 3]
]

# Print each row
for i in l9:
    print(i)

# Print each element
for i in range(len(l9)):
    for j in range(len(l9[i])):
        print(l9[i][j], " ", end="")
    print()
```

### Sum Each Row, Find Max Row Sum
```python
l10 = [[2, 4, 5, 1], [3, 2, 9, 6], [1, 0, 2, 10]]
sums = []
s = 0
for i in range(len(l10)):
    for j in range(len(l10[i])):
        s += l10[i][j]
    sums.append(s)

print("sums:", sums)
print("max row sum:", max(sums))
```

---

## 5. Searching Algorithms

### Linear Search
```python
values = [12, 34, 67, 987, 32, 5, 12]
inn = int(input("enter number to find: "))
flag = False

for i in range(len(values)):
    if values[i] == inn:
        print("found at index", i)
        flag = True
        break     # stops at first match

print(flag)
```

### Binary Search (list must be sorted)
```python
l2 = [1, 2, 3, 4, 5, 6, 7, 8, 11]
target = 11
low = 0
high = len(l2) - 1

while low <= high:
    mid = (low + high) // 2
    if l2[mid] == target:
        print("found at index", mid)
        break
    elif target > l2[mid]:
        low = mid + 1
    else:
        high = mid - 1
```

> 💡 **Complexity:**
> - Linear Search → **O(n)** — checks every element
> - Binary Search → **O(log n)** — halves the list each step (must be sorted)
> - Also exists: Bubble Sort, Merge Sort, etc.
>
> 📖 **Task:** Read more about algorithm complexity

---

## 6. Dictionaries

> A dictionary stores **key-value pairs**. Keys must be unique.

### Basics
```python
dict1 = {
    0: [1, 2, 4, 5],
    'b': 2,
    'c': 9,         # duplicate key — only last value kept ⚠️
    'd': [1, 2, 3, 4]
}

dict1['e'] = 23         # add new key
dict1.pop('c')          # delete by key
print(dict1.get('b', 411))   # → 2       (key exists)
print(dict1.get('bb', 411))  # → 411     (key missing, return default)
```

### Looping — Keys, Values, Items
```python
contacts = {
    "aaa": [9854345, 9345268],
    "bbb": 9654576,
    "ccc": 9678762,
    "ddd": [9267233, 9345697]
}

# .items() → (key, value) pairs
for i in contacts.items():
    print(i[0], i[1])
    if type(i[1]) is list:
        for j in i[1]:
            print("list element:", j)

# .values()
for i in contacts.values():
    print("value:", i)

# .keys()
for i in contacts.keys():
    print("key:", i)
```

### Count Occurrences Using a Dictionary
```python
l11 = [1, 2, 3, 4, 1, 1, 1, 8, 7]
dict2 = {}
for i in l11:
    if i not in dict2:
        dict2[i] = l11.count(i)
print(dict2)  # → {1: 4, 2: 1, 3: 1, 4: 1, 8: 1, 7: 1}
```

### Nested Dictionary — Students & Grades
```python
l12 = [
    ("Ali", "Math", 85),
    ("Sara", "Math", 90),
    ("Ali", "Science", 78),
    ("Sara", "Science", 88),
    ("Ali", "English", 92),
    ("Sara", "English", 85)
]

bigDic = {}
for i in range(len(l12)):
    name    = l12[i][0]
    subject = l12[i][1]
    grade   = l12[i][2]
    if name not in bigDic:
        bigDic[name] = {}
    bigDic[name][subject] = grade

# → {'Ali': {'Math': 85, 'Science': 78, 'English': 92},
#    'Sara': {'Math': 90, 'Science': 88, 'English': 85}}
```

### Average Grade Per Subject
```python
bigDic = {
    'Ali':  {'Math': 85, 'Science': 78, 'English': 92},
    'Sara': {'Math': 90, 'Science': 88, 'English': 85}
}
subjectsDic = {}

for stdName, innerDic in bigDic.items():
    for subject, grade in innerDic.items():
        if subject not in subjectsDic:
            subjectsDic[subject] = 0
        subjectsDic[subject] += grade

for sub, totalGrade in subjectsDic.items():
    print(sub, "average:", totalGrade / len(bigDic))
```

### Weekly Temperature Dictionary
```python
dict8 = {
    "Sunday": 30, "Monday": 29, "Tuesday": 31,
    "Wednesday": 33, "Thursday": 35, "Friday": 28, "Saturday": 25
}

# Sum, min, max
print("total:", sum(dict8.values()))
print("min:", min(dict8.values()))
print("max:", max(dict8.values()))

# Find which day had max temp
m = max(dict8.values())
for day, temp in dict8.items():
    if temp == m:
        print("hottest day:", day)
```

### Dictionary with List Values — Add Weekly Temps
```python
dict9 = {
    "Sunday": [30, 31], "Monday": [23, 25], "Tuesday": [27, 29],
    "Wednesday": [25, 28], "Thursday": [33, 27],
    "Friday": [31, 21], "Saturday": [35, 29]
}

# Average of second week temps
t = 0
for i, j in dict9.items():
    t += j[1]
print("average of second week:", t / len(dict9))

# Add a third week from a list
temps = [21, 34, 43, 22, 1, 2, 33]
index = 0
for k in dict9.keys():
    dict9[k].append(temps[index])
    index += 1
print(dict9)
```

---

## 7. Tuples

> A tuple is like a list but **immutable** — you can't change it after creation. Use `()`.

```python
tup = (1, 2, 3, [1, 4], 'n')    # can hold mixed types, even a list inside
print(tup)

# Nested tuple
tup2 = ((1, 2, 3), (4, 5, 6, 7, 8))
for i in tup2:
    for j in i:
        print(j, end=" ")

# Tuple methods
tup3 = (1, 2, 3, 4, 5, 6, 2, 1, 2, 3)
print("count of 3:", tup3.count(3))    # → 2
print("index of 4:", tup3.index(4))    # → 3
```

---

## 8. Sets

> A set is an **unordered** collection of **unique** elements — no duplicates.

```python
st = {1, 2, 3, 4, 4, 4, 4}
print(st)   # → {1, 2, 3, 4}  (duplicates removed automatically)

# ⚠️ Empty {} creates a dict, not a set!
st1 = {}            # → dict
st2 = set()         # → empty set (correct way)
st3 = set([1, 2, 3, 4, 5, 6, 7])   # → set from a list
```

---

## 9. Files

### Read Line by Line
```python
infile = open("data.txt", "r")

line = infile.readline()
while line != "":
    print(line)
    line = infile.readline()

infile.close()
```

### Read All Lines at Once
```python
infile = open("data.txt", "r")

lines = infile.readlines()           # returns a list of strings
for i in range(len(lines)):
    lines[i] = int(lines[i].strip()) # strip removes \n, then convert to int

print("average:", sum(lines) / len(lines))
print("maximum:", max(lines))
print("minimum:", min(lines))
infile.close()
```

### Read Entire File as One String
```python
infile = open("data.txt", "r")
nn = infile.read().split("\n")   # split into lines manually
print(nn)
infile.close()
```

### Write to a File
```python
infile = open("data.txt", "w")      # "w" overwrites existing content

infile.write("Hello World\nfrom Ahad\n>>>\n")
print("hello", "world", file=infile)  # print() can write to a file

infile.close()
```

> 💡 **File modes:**
> - `"r"` → read
> - `"w"` → write (overwrites)
> - `"a"` → append (adds to end)

### Count Word Frequency in a File
```python
f2 = open("thursday.txt", "r")
txt = f2.read()
words = txt.split()

# Normalize
for i in range(len(words)):
    words[i] = words[i].lower().strip()

# Count "the" — way 1
print("count of 'the':", words.count("the"))

# Count "the" — way 2
rep = 0
for i in words:
    if i == "the":
        rep += 1
print("count of 'the':", rep)

f2.close()
```

### Kaggle Dataset — Parse a Math File
```python
import kagglehub
from pathlib import Path

path = kagglehub.dataset_download("deepak711/4-subject-data-text-classification")

f100 = open(".../Maths/Math_100.txt", "r")
lines = f100.readlines()

title  = lines[0]
number = lines[1]
print("title:", title, "number:", number)

# Split into description and examples at the "Example" keyword
for i in range(len(lines)):
    if 'Example' in lines[i]:
        description = lines[2:i]
        examples    = lines[i:]

f100.close()
```

---

## 10. Error Handling (try / except)

### Raise Your Own Error
```python
amount = 700
balance = 200
if amount > balance:
    raise ValueError("amount exceeds balance")
```

### try / except — Catch Specific Errors
```python
try:
    m = 5 / 0                      # ZeroDivisionError
    line = infile.readline()

except IOError:
    print("Could not open input file.")

except Exception as exceptObj:
    print("Error:", str(exceptObj))
```

### try / finally — Always Close the File
```python
try:
    infile = open("thursday.txt", "r")
    line = infile.readline()
    print(line)
finally:
    infile.close()    # runs whether or not an error occurred
```

### Validate User Input with a Loop
```python
inputOk = False
while not inputOk:
    try:
        num = float(input("enter a number: "))
        inputOk = True
    except ValueError:
        print("that's not a number, try again")

print(num * 2)
```

---

## 11. Notes & Tasks

| # | Note |
|---|------|
| 📝 | `len()` works on lists, strings, dictionaries, and tuples |
| 📝 | Strings are **immutable**, lists are **mutable** |
| 📝 | A dictionary key can only have **one value** — duplicate keys overwrite |
| 📝 | `{}` creates a dict — use `set()` to create an empty set |
| 📝 | Linear Search = O(n) \| Binary Search = O(log n) (must be sorted) |
| 🔧 | **Task:** Read about algorithm **complexity** (Big O notation) |
| 🔧 | **Task:** Read about **shallow copy** vs deep copy and `.copy()` |
| 🔧 | **Assignment (GP):** Go through 4 Kaggle files — print name, number, description, examples for each |

---

*📅 Notes taken: April 12–16, 2026*
