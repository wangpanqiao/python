from math import sqrt
def prime(num):
    if num == 1:
        return False
    k = int(sqrt(num))
    for j in range(2,k+1):
        if num%j==0:
            return False
    return True


def monisen(no):
    i = 2
    count = 0
    while count<no:
        if prime(i) and prime(2**i-1):
            n = 2**i-1
            count+=1
        i+=1
    return n
n = int(input())
print(monisen(n))