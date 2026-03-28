fruits = ["apple", "banana", "cherry"]
for i, fruit in enumerate(fruits):
    print(i, fruit)
#0 apple
#1 banana
#2 cherry
for i, fruit in enumerate(fruits, start=1):
    print(i, fruit)
#1 apple
#2 banana
#3 cherry

names = ["Alice", "Bob", "Charlie"]
scores = [85, 90, 78]
result = list(zip(names, scores))
print(result)
#[('Alice', 85), ('Bob', 90), ('Charlie', 78)]
for name, score in zip(names, scores):
    print(name, score)

nums = [5, 2, 9, 1]
print(sorted(nums))
#[1, 2, 5, 9]