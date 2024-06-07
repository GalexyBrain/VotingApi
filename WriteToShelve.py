import shelve

with shelve.open("Test.db") as db:
    db[input("Enter Epic Id : ")] = input("Enter Solidity number : ")