ages = [2,5,7,9,19,26,45,67]

def myFunc(x):
    if x < 18:
        return False
    else:
        return True
    
adults = filter(myFunc, ages)

for x in adults:
    print(x)
