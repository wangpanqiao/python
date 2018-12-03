def countfeq(s):
    #a_s_list = s.split('.')
    #b_s_list = a_s_list[0].split(',')
    #print(b_s_list)
    #s_list = []
    s_list = [i for i in list(s) if i != '.' and i !=',']
    str_s= ''.join(s_list)
    s_list= str_s.split(' ')
    #print(a_s_list)
    #s_list = [str(i.split(' ')) for i in a_s_list]
    k_list = list(set(s_list))
    v_list = [s_list.count(k_list[i]) for i in range(k_list.__len__())]
    Dict = dict(zip(k_list,v_list))
    return Dict


if __name__ == "__main__":
    s = "Not clumsy person in this world, only lazy people, only people can not hold out until the last."
    s_dict = countfeq(s.lower())
    #print(s_dict)
    word = input()
    if word in s_dict:
        print(s_dict[word])
    else:
        print(0)
    #help(list)