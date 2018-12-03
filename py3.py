def countchar(string):
    a = [chr(i) for i in range(97,123)]
    Lstring = list(string.lower())
    Lstring.sort()
    b = [Lstring.count(a[i]) for i in range(0,26)]
    return b

if __name__ == "__main__":
    string = 'aaaa'
    print(countchar(string))
