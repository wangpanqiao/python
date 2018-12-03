def find_person(dict_users, strU):
    if str(strU)  in  dict_users:
        return dict_users[strU]
    else:
        return 'Not Found'


if __name__ == "__main__":
    dict = {"xiaoyun":88888, "xiaohong":5555555,
            "xiaoteng":11111,"xiaoyi":12341234,"xiaoyang":1212121}
    strU = input()
    print(find_person(dict, strU))