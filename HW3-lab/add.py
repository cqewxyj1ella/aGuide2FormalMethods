from z3 import * 
# preparation
## read input
a = int(input("a = "))
b = int(input("b = "))
## convert to binary
def convert_bin(n):
    # convert an integer n from decimal to binary
    arr = []
    while n > 0:
        arr.append(n%2)
        n = n >> 1
    return arr
arr_a = convert_bin(a); arr_b = convert_bin(b)
## get max length
len_a = len(arr_a); len_b = len(arr_b)
len_max = len_a + 1 if len_a > len_b else len_b + 1
for i in range(len_a, len_max, 1):
    arr_a.append(0)
for i in range(len_b, len_max, 1):
    arr_b.append(0)
print("bin_a: ", arr_a[::-1])
print("bin_b: ", arr_b[::-1])
## declare bool array
bool_a = [Bool('A_%i' % (i+1)) for i in range(len_max)]
bool_b = [Bool('B_%i' % (i+1)) for i in range(len_max)]
bool_c = [Bool('C_%i' % (i+1)) for i in range(len_max+1)]
bool_d = [Bool('D_%i' % (i+1)) for i in range(len_max)]

# define constraints
## constraints for a_i
cond1 = True
for i in range(len_max):
    if(arr_a[i]>0):
        cond1 = And(cond1,bool_a[i])
    else:
        cond1 = And(cond1,Not(bool_a[i]))
## constraints for b_i
cond2 = True
for i in range(len_max):
    if(arr_b[i]>0):
        cond2 = And(cond2,bool_b[i])
    else:
        cond2 = And(cond2,Not(bool_b[i]))
## constraints for d_i and c_i
cond3 = True
for i in range(len_max):
    cond3_i = bool_d[i] == (bool_a[i] == (bool_b[i] == bool_c[i]))
    cond3 = And(cond3, cond3_i)
## constraints for c and a b
cond4 = True
for i in range(len_max):
    cond4_i = Or( And(bool_a[i], bool_b[i]), 
                  And(bool_a[i], bool_c[i]), 
                  And(bool_b[i], bool_c[i]) )
    cond4_i = bool_c[i+1] == cond4_i
    cond4 = And(cond4, cond4_i)

# solve the problem
print("a + b = d")
s = Solver()
s.add(cond1); s.add(cond2); s.add(cond3); s.add(cond4);
if s.check() != sat:
    print("unsatisfiable!")
else: # is sat
    print("The result of the solver is:")
    for i in range(len_max-1, -1, -1):
        print("d[{}]: ".format(i), s.model()[bool_d[i]])
    ## convert bool to binary
    arr_d = []
    for i in range(len_max):
        if s.model()[bool_d[i]]: # True
            arr_d.append(1)
        else:
            arr_d.append(0)
    print("The binary format of d is: ", arr_d[::-1])
    ## convert binary to decimal
    d = 0; factor = 1
    for i in range(len_max):
        d += factor * arr_d[i]
        factor *= 2
    print("The decimal format of d is: ", d)