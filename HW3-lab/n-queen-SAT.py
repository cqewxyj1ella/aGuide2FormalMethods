from z3 import *
import time
# preparation
n = int(input("n is the size of the problem, n = "))
bool_p = []
for i in range(n):
    bool_p_j = [Bool('P_%s_%s' %(i+1, j+1)) for j in range(n)]
    bool_p.append(bool_p_j)

# define constraints
## constraints for rows
row_cons1 = True
for i in range(n):
    row_j = Or(bool_p[i])
    row_cons1 = And(row_cons1, row_j)
row_cons2 = True
for i in range(n):
    row_j = True
    for k in range(n):
        for j in range(k):
            row_j = And(row_j, Or(Not(bool_p[i][j]), Not(bool_p[i][k])))
    row_cons2 = And(row_cons2, row_j)
row_cons = And(row_cons1, row_cons2)
## constraints for columns
col_cons1 = True
for j in range(n):
    col_i = True
    for i in range(n):
        col_i = Or(col_i, bool_p[i][j])
    col_cons1 = And(col_cons1, col_i)
col_cons2 = True
for j in range(n):
    col_i = True
    for k in range(n):
        for i in range(k):
            col_i = And(col_i, Or(Not(bool_p[i][j]), Not(bool_p[k][j])))
    col_cons2 = And(col_cons2, col_i)
col_cons = And(col_cons1, col_cons2)
## constraints for diagonal
diag_cons = True
for i_0 in range(n):
    for i in range(i_0):
        for j_0 in range(n):
            for j in range(n):
                if (i+j == i_0+j_0) or (i-j == i_0-j_0):
                    diag_cons = And(diag_cons, Or(Not(bool_p[i][j]), Not(bool_p[i_0][j_0])))

# solve the problem
start_time = time.time() # start
s = Solver()
s.add(row_cons); s.add(col_cons); s.add(diag_cons)
if s.check() != sat:
    print("unsatisfiable")
else: # is sat
    print("sat!")
    for i in range(n):
        for j in range(n):
            if s.model()[bool_p[i][j]]: # a queen
                print("Q[{}]: {}".format(i+1, j+1))
                break
print("--- %s seconds ---" % (time.time() - start_time)) # end