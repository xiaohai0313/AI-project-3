import queue
import os
import re
import copy
from collections import OrderedDict
from collections import defaultdict
f1 = open("input.txt","r")
All_line = f1.readlines()
Task = []
for line in All_line:
    temp = line.strip('\n')
    temp = line.split('\t')
    temp = line.strip('\n')
    Task.append(temp)
Q_base = []
KB = []
N = int(Task[0])
for i in range(N):
    Q_base.append(Task[i+1])
K = int(Task[N+1])
for i in range(N+2,K+N+2,1):
    KB.append(Task[i])
hold = [False]
postfix = [1]
KB_list = []
Q_list = []
TrueKB_list = []
result = ['FALSE' for num in range(N)]

class Single_predicate:         #
    def __init__(self,pre,argument):
        self.pred = pre if pre[0] != '~' else pre[1:]
        self.arglen = 0
        self.arg = []
        self.is_true = True if pre[0] != '~' else False
        s = argument.split(',')
        for x in s:
            if x in variable_list:
                self.arg.append(x+str(postfix[0]))
            else:
                self.arg.append(x)

            self.arglen += 1
        if hold[0] == False:
            postfix[0] += 1


variable_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

class KB_class:
    def __init__(self, pre, con):
        self.pred_list = []
        self.conclusion = []
        if pre:
            for x in pre:
                self.pred_list.append(Single_predicate(x[0],x[1]))


        self.conclusion = Single_predicate(con[0],con[1])

class ALL_KB_class:
    def __init__(self, pre, con):
        hold[0] = True
        self.pred_list = []

        if pre:
            for x in pre:
                self.pred_list.append(Single_predicate(x[0],x[1]))
        for y in self.pred_list:
            y.is_true = True if y.is_true == False else False

        self.pred_list.append(Single_predicate(con[0],con[1]))
        postfix[0] += 1


def check_duplicate(target,list):
    for node in list:
        if check_same_signle_pred(target,node):
            return
    list.append(target)

def check_same_signle_pred(pre1,pre2):                                                              #如果两个pred 相同
    if pre1.pred == pre2.pred and pre1.arg == pre2.arg and pre1.is_true == pre2.is_true:
        return True
    return False

def check_same_list(l1,l2):
    #if type(l1) == Single_predicate and type(l2) != Single_predicate:
    if type(l1) != type(l2):
        return False
    if type(l1) == Single_predicate:
        return check_same_signle_pred(l1,l2)
    else:
        if len(l1) != len(l2):
            return False
        for i in range(len(l1)):
            if check_same_signle_pred(l1[i],l2[i]):
                continue
            else:
                return False
    return True

def check_list_in_TrueKB(list):
    for x in TrueKB_list:
        if check_same_list(x,list):
            return True
    return False


def cleanpro():                                                                                 #初始化
    for x in Q_base:
        hold[0] = False
        temp = [" ".join(y.split()) for y in re.split(r'[()]',x) if y.strip()]
        temp[1].split(',')
        myque = Single_predicate(temp[0],temp[1])
        Q_list.append(myque)                                    #Query dont need check duplicate


    for x in KB:

        temp = x.split('=>')
        premise , conclusion = None, None
        if len(temp) > 1:
            conclusion = temp[1]
            premise = temp[0].split('&')
        else:
            conclusion = temp[0]

        conclusion = [" ".join(y.split()) for y in re.split(r'[()]', conclusion) if y.strip()]

        temp1 = []
        if premise:
            for index, x in enumerate(premise):
                temp1 += [[" ".join(y.split()) for y in re.split(r'[()]', x) if y.strip()]]
            premise = temp1
            KB_list.append(ALL_KB_class(premise,conclusion))

        else:
            hold[0] = False
            temp = Single_predicate(conclusion[0],conclusion[1])            #check duplicate
            check_duplicate(temp,TrueKB_list)



def if_in_list(char,list):          #如果在当前list里 那么返回应该的值
    for x in list:
        if char == x[0]:
            return x[1]
    return

'''def check_contradiction_signle_pred(pre1,pre2):                                                     #如果两个pred 元素是相反的
    if pre1.pred == pre2.pred and pre1.arg == pre2.arg and pre1.is_true != pre2.is_true:
        return True
    return False
'''
def check_contradiction_signle_pred(sen1,sen2):                                                     #如果两个pred 元素是相反的
    #if sen1.pred == sen2.pred and sen1.arg == sen2.arg and sen1.is_true != sen2.is_true:
     #   return True
    if sen1.pred != sen2.pred or sen1.is_true == sen2.is_true or sen1.arglen != sen2.arglen:
        return False
    pair = []
    for i in range(sen1.arglen):
        if sen1.arg[i][0] not in variable_list and sen2.arg[i][0] not in variable_list:
            if sen1.arg[i] == sen2.arg[i]:
                continue
            else:
                return False
        if sen1.arg[i][0] in variable_list and sen1.arg[i][1].isdigit() and sen2.arg[i][0] in variable_list and sen2.arg[i][1].isdigit():
            for x1 , x2 in pair:
                if x1 == sen1.arg[i]:
                    if x2 == sen2.arg[i]:
                        continue
                    else:
                        return False
                if x2 == sen2.arg[i]:
                    if x1 == sen1.arg[i]:
                        continue
                    else:
                        return False
            continue
        else:
            for x3, x4 in pair:                     #y,y,x and x,y,y situation
                if x3 == sen1.arg[i] and x3[0] in variable_list:
                    if x4 == sen2.arg[i]: #or x4[0] not in variable_list:
                        continue
                    else:
                        return False
                if x4 == sen2.arg[i] and x4[0] in variable_list: #and sen2.arg[i][0] in variable_list:
                    if x3 == sen1.arg[i]:# or x3[0] not in variable_list:
                        continue
                    else:
                        return False
        pair.append([sen1.arg[i],sen2.arg[i]]) if [sen1.arg[i],sen2.arg[i]] not in pair else None
    return True


def check_contradiction_list(l1,l2):                                                            #看整个list 和另一个list是否有contradiction
    if len(l1) != len(l2):
        return False
    for i in range(len(l1)):                                                                        #如果整个list和另一个list是contradiction 那么每一个元素对应都是contradiction
        if check_contradiction_signle_pred(l1[i], l2[i]):                                     #####这块要改  相反元素的index不一样相同
            continue
        return False
    return True

def they_are_contradiction():                                                                   #看
    for i in range(len(TrueKB_list)):
        for j in range(i+1,len(TrueKB_list),1):
            if type(TrueKB_list[i]) == type(TrueKB_list[j]) == Single_predicate:
                if check_contradiction_signle_pred(TrueKB_list[i], TrueKB_list[j]):
                    return True
    return False

def replace_variable_to_constant(list,pair):
    for i in range(len(list)):
        for y in pair:
            if list[i] == y[1]:
                list[i] = y[0]


def is_valid_pair(sen1,sen2,pair,sen2duplicate,index):
    #ret = []
    for i in range(sen1.arglen):
        if sen1.arg[i][0] not in variable_list and sen2.arg[i][0] not in variable_list:
            if sen1.arg[i] == sen2.arg[i]:
                continue
            else:
                return []

        if sen1.arg[i][0] in variable_list and sen1.arg[i][1].isdigit() and sen2.arg[i][0] in variable_list and sen2.arg[i][1].isdigit():

            for x1 , x2 in pair:
                if x1 == sen1.arg[i]:
                    if x2 == sen2.arg[i]:
                        continue
                    else:
                        return []
                if x2 == sen2.arg[i]:
                    if x1 == sen1.arg[i]:
                        continue
                    else:
                        return []

            #continue

        else:
            for x3, x4 in pair:                     #y,y,x and x,y,y situation
                if x3 == sen1.arg[i] and x3[0] in variable_list:
                    if x4 == sen2.arg[i]:
                        continue
                    else:
                        return []

                if x4 == sen2.arg[i] and x4[0] in variable_list:
                    if x3 == sen1.arg[i]:
                        continue
                    else:
                        return []

        pair.append([sen1.arg[i],sen2.arg[i]]) if [sen1.arg[i],sen2.arg[i]] not in pair else None
    del sen2duplicate[index]

    for item in sen2duplicate:
        replace_variable_to_constant(item.arg,pair)

    if len(sen2duplicate) == 1:
        sen2duplicate = sen2duplicate[0]


    if not check_list_in_TrueKB(sen2duplicate):
        TrueKB_list.append(sen2duplicate)
    return pair


def delete_contradict_and_insert_new(sen1,sen2):      #sen1是单个的  sen2是list                                              #一个单个的  和一个list删取反的 把剩下的加进KB
    #if len(sen1) != 1 or len(sen2) == 1:

      #  return
    for index , x in enumerate(sen2):                   #sen2里面每一个元素 看是否能消掉
        if x.pred == sen1.pred and x.is_true != sen1.is_true and x.arglen == sen1.arglen:
            pair = []

            is_valid_pair(sen1,x,pair,copy.deepcopy(sen2),index)            #pair[0] is sen1   看有没有可以消的一对
    return


def backward_checking():
    i = 0
    while i < len(TrueKB_list):
        j = 0
        while j < len(TrueKB_list):
            if i != j and type(TrueKB_list[i]) == Single_predicate and type(TrueKB_list[j]) != Single_predicate:            #前面单个  后面List
                delete_contradict_and_insert_new(TrueKB_list[i], TrueKB_list[j])
            j += 1
        i += 1
    return

if __name__=="__main__":
    cleanpro()
    pre , cur = len(TrueKB_list), 0
    for x in KB_list:
        TrueKB_list.append(x.pred_list)
    backup_list = copy.deepcopy(TrueKB_list)                #TrueKB_list 是读完文件   拆分成or 左边取反后的结果

    for i in range(len(Q_list)):
        TrueKB_list = copy.deepcopy(backup_list)
        pre = len(TrueKB_list)
        que = copy.deepcopy(Q_list[i])
        que.is_true = False if que.is_true == True else True            #每次取1个query element去测试
        TrueKB_list.append(que)
        while pre != cur :
            pre = len(TrueKB_list)
            backward_checking()                                         #1.找有没有可以删的   2.删掉单个有反的  3.把新的加回TrueKB_list
            cur = len(TrueKB_list)
            if they_are_contradiction():
                result[i] = 'TRUE'
                break
        TrueKB_list.remove(que)


    print_out, rlength = '', 0
    for x in result:
        print_out += x
        if rlength < len(result) - 1:
            print_out += '\n'
            rlength += 1
    #print(print_out)
    f = open("output.txt", "w")
    for x in print_out:
        f.write(x)
    #print(print_out)
    f.close()

