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
    start_time = time.time() # start
    s = Solver()
    s.add(val_c); s.add(col_c); s.add(diag_c)
    if s.check() != sat:
        print("unsatisfiable")
    else: # is sat
        for i in range(n):
            print("Q[{}]: {}".format(i+1, s.model()[Q[i]]))
    print("--- %s seconds ---" % (time.time() - start_time)) # end


# handle input and count time
if __name__=="__main__":
    str = input("Enter the size of the problem: ")
    problem_size = int(str)
    n_queen_solve(problem_size)