def ispandigital(string):
    for i in range(1,len(string)+1):
        if string.find(str(i)) ==-1:
            return False
    if(len(string) > 9):
        return False
    return True


def pandigital(nums):
    try:
        lst = [item for item in nums if ispandigital(str(item))]
    except:
        if ispandigital(str(nums)):
            lst = [nums]
        else:
            lst = []
    return lst


if __name__ == "__main__":
    lst = pandigital(eval(input()))
    if lst == []:
        print('not found')
    else:
        for i in lst:
            print(i)

