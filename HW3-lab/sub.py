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
## convert to complement format
def convert_complement(arr):
    len_arr = len(arr)
    ### negate by bit
    if (arr[len_arr-1] == 0): # positive
        return arr
    # else, negative
    for i in range(len_arr-1):
        arr[i] = 0 if arr[i] == 1 else 1
    ### then plus 1
    for i in range(len_arr):
        if arr[i] == 1:
            arr[i] = 0
        else: # arr[i] is 0
            arr[i] = 1
            break
    return arr
arr_a = convert_bin(a); arr_a.append(0)
arr_b = convert_bin(b); arr_b.append(0); arr_b.append(1) # minus
print("bin_a: ", arr_a[::-1])
print("bin_b: ", arr_b[::-1])
arr_a = convert_complement(arr_a); arr_b = convert_complement(arr_b)
print("complement_a1: ", arr_a[::-1])
print("complement_b1: ", arr_b[::-1])
## get max length
len_a = len(arr_a); len_b = len(arr_b)
len_max = len_a + 1 if len_a > len_b else len_b + 1
append_a = arr_a[len_a-1]
for i in range(len_a, len_max, 1):
    arr_a.append(append_a)
append_b = arr_b[len_b-1]
for i in range(len_b, len_max, 1):
    arr_b.append(append_b)
print("complement_a2: ", arr_a[::-1])
print("complement_b2: ", arr_b[::-1])

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
    print("The result of the solver is(complement format):")
    for i in range(len_max-1, -1, -1):
        print("d[{}]: ".format(i), s.model()[bool_d[i]])
    ## convert bool to complement
    arr_d = []
    for i in range(len_max):
        if s.model()[bool_d[i]]: # True
            arr_d.append(1)
        else:
            arr_d.append(0)
    ## convert complement to binary
    arr_d = convert_complement(arr_d)
    '''
    meet_1_flag = False
    for i in range(len_max):
        if (meet_1_flag is False) and (arr_d[i] == 1):
            meet_1_flag = True
        if meet_1_flag:
            arr_d[i] = 0 if arr_d[i] == 1 else 1
    '''
    ## print binary d
    print("The binary format of d is: ", arr_d[::-1])
    ## convert binary to decimal
    d = 0; factor = 1
    for i in range(len_max-1):
        d += factor * arr_d[i]
        factor *= 2
    if arr_d[len_max-1] == 1: # negative
        d = -d
    print("The decimal format of d is: ", d)