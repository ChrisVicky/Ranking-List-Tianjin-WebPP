from binascii import a2b_qp


a = {'abd':'fdf','b':33,'sfd':434}
for i,j in a.items():
    print(i,j)

X = [1,2,3]
w = [1,2, x for x in X]
print(w)