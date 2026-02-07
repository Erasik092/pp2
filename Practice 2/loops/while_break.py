# Break statement exits the loop immediately

num = 1
while True:
    if num == 7:
        print("Found it!")
        break
    print(num)
    num += 1
