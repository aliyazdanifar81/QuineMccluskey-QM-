from math import log


class minterm:
    def __init__(self, _number: list, _binform: str, _value, _dif='0'):
        self.number = _number
        self.binform = _binform
        self.value = _value
        self.coverd = 0
        self.dif = _dif
        self.one_count = self.one_counter()

    def one_counter(self):
        return self.binform.count('1')


def haming_def(obj1, obj2):
    counter = 0
    dif = 0
    for ch in obj1:
        if ch != obj2[counter]:
            dif += 1
        counter += 1
    return dif


def full_bin(binary, n):
    return (n * "0") + binary


def check_minterms(m1, m2):
    m1: minterm
    m2: minterm
    if len(m1.number) == 1:
        if int(m1.number[0]) < int(m2.number[0]):
            _log = log(int(m2.number[0]) - int(m1.number[0]), 2)
            if int(_log) == _log:
                if haming_def(m1.binform, m2.binform) == 1:
                    return True
    else:
        if m1.dif == m2.dif:
            if haming_def(m1.binform, m2.binform) == 1:
                return True
    return False


def make_binform(m1, m2):
    str_1 = ""
    counter = 0
    for ch in m1.binform:
        if ch == m2.binform[counter]:
            str_1 += ch
        else:
            str_1 += '-'
        counter += 1
    return str_1


def dif_maker(_list):
    res = ""
    counter = 0
    while counter < len(_list) - 1:
        num = int(_list[counter + 1]) - int(_list[counter])
        res += str(num)
        counter += 1
    return res


def change_coverd(_min):
    _min.coverd = 1


def contain_list(list_1, list_2):
    counter = 0
    for j in list_2:
        if j in list_1:
            counter += 1
        if counter == len(list_2):
            return True
    return False


def pi_sel(i):
    flag = 1
    if i.coverd == 0:
        if pi_list == []:
            pi_list.append(i)
        else:
            for min in pi_list:
                l1 = min.number
                l2 = i.number
                check = contain_list(l1, l2)
                if check:
                    flag = 0
                    break
            if flag:
                pi_list.append(i)
    else:
        if selected_list == []:
            selected_list.append(i)
        else:
            for min in selected_list:
                l1 = min.number
                l2 = i.number
                check = contain_list(l1, l2)
                if check:
                    flag = 0
                    break
            if flag:
                selected_list.append(i)


epi = list()
min_num = list()
sorted_by_one = list()
grouped_list = list()
pi_list = list()
temp_list = list()
selected_list = list()
number_var = int(input("insert number of variable : "))
print("insert minterms number (insert e or E for end) : ")
for i in input().split():
    if i == 'e' or i == 'E':
        break
    binform = format(int(i), "b")
    min_num.append(minterm([i], full_bin(binform, number_var - len(binform)), '1'))
print("insert dont cares number (insert e or E for end) : ")
for i in input().split():
    if i == 'e' or i == 'E':
        break
    binform = format(int(i), "b")
    min_num.append(minterm([i], full_bin(binform, number_var - len(binform)), 'd'))
min_num.sort(key=lambda m: int(m.number[0]))
for i in range(number_var + 1):
    sorted_by_one.append([])
for min in min_num:
    sorted_by_one[min.one_count].append(min)
counter = 0
while len(sorted_by_one) > 0:
    if len(sorted_by_one[counter]) != 0:
        for i in sorted_by_one[counter]:
            for j in sorted_by_one[counter + 1]:
                if check_minterms(i, j):
                    number_list = list()
                    number_list.extend([*i.number, *j.number])
                    temp_list.append(minterm(number_list, make_binform(i, j), '1', dif_maker(number_list)))
                    change_coverd(i)
                    change_coverd(j)
            pi_sel(i)
        if temp_list != []:
            grouped_list.append(temp_list.copy())
            temp_list.clear()
        else:
            if grouped_list != [[]]:
                grouped_list.append([])
                temp_list.clear()
    counter += 1
    if counter == len(sorted_by_one) - 1:
        counter = 0
        if grouped_list != [[]]:
            for last_i in sorted_by_one[-1]:
                pi_sel(last_i)
            sorted_by_one.clear()
            sorted_by_one.extend(grouped_list.copy())
        else:
            if sorted_by_one[-1] != []:
                for last_i in sorted_by_one[-1]:
                    pi_sel(last_i)
            sorted_by_one.clear()
        grouped_list.clear()
        temp_list.clear()
for min in min_num:
    if min.value == '1':
        num = min.number[0]
        counter = 0
        last_pi: minterm
        for min_2 in pi_list:
            if num in min_2.number:
                counter += 1
                last_pi = min_2
        if counter == 1:
            if last_pi not in epi:
                epi.append(last_pi)
print(f"epi number = {len(epi)} and pi number = {len(pi_list)}")
print('PI:')
for min in pi_list:
    print(min.number)
print('\n')
print('EPI:')
for min in epi:
    print(min.number)
print('\n')
print('sl:')
for min in selected_list:
    print(min.number)
