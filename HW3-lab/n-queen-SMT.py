from z3 import *
import time

# a solver function for an input n(problem size)
def n_queen_solve(n):
    Q = [ Int("Q_%i" % (i + 1)) for i in range(n) ]
    val_c = [ And (1 <= Q[i], Q[i] <= n) for i in range(n) ]
    col_c = [ Distinct (Q) ]
    diag_c = [ If(i == j, True ,
            And(i+Q[i]!=j+Q[j], i+Q[j]!=j+Q[i]))
            for i in range(n) for j in range(i) ]
    solve(val_c + col_c + diag_c)

# handle input and count time
if __name__=="__main__":
    str = input("Enter the size of the problem: ")
    problem_size = int(str)
    start_time = time.time() # start
    n_queen_solve(problem_size)
    print("--- %s seconds ---" % (time.time() - start_time)) # end

# n_queen_solve(9)