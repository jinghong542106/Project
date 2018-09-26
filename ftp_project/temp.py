A = [1,2,[3,4,['434']]]
def fun(lst):
    L=[]
    for x in lst:
        if type(x) is list:
            L+=fun(x)
        else:
            L.append(x)
    return L
L=fun(A)
for i in L:
    print(i, end=" ")
print()
