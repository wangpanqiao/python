def fuc(n):
    c = 0
    for i in range(1,n):
        if(n % i == 0):
            c +=i
    return c

n = int(input("please input a number:"))
for i in range(n):
    if(fuc(i) > n):
        continue
    elif(i == fuc(fuc(i)) and i < fuc(i)):
        print("{0}-{1}".format(i,fuc(i)))


