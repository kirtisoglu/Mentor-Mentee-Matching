from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD



def matching(mentee_choice, mentor_choice, uni_students, scores, max_student, uni_capacity, time):


    #Initialize a minimization problem
    problem = LpProblem("Mentor_Mentee_Matching", LpMaximize)


    # Create decision variable x_ij for every mentee i and mentor j
    decision = {(i, j): LpVariable(f"x_{i}_{j}", cat="Binary") for i in mentee_choice.keys() for j in mentor_choice.keys()}


    # Constraint (2): each mentor receives at least one mentees, at most 'max_student' mentees. 
    for j in mentor_choice.keys():
        problem += lpSum(decision[i, j] for i in mentee_choice.keys()) >= 1
        problem += lpSum(decision[i, j] for i in mentee_choice.keys()) <= max_student


    # Constraint (3): each mentee is assigned to at most one mentor.
    for i in mentee_choice.keys():
        problem += lpSum(decision[i, j] for j in mentor_choice.keys()) <= 1


    # Constraint (4): at most 'uni_capacity' mentees are assigned from every uni.
    for uni in uni_students.keys():
        problem += lpSum(decision[i, j] for i in uni_students[uni] for j in mentor_choice.keys()) <= uni_capacity


    # Constraint (5): mentee i is assigned to mentor j only if their interests overlap.
    for i in mentee_choice.keys():
        for j in mentor_choice.keys():
            problem += decision[i, j] <= decision[i, j]*scores[(i,j)]


    # Objective function: the total assignment score is maximized.
    problem += lpSum(decision[i, j]*scores[(i,j)] for i in mentee_choice.keys() for j in mentor_choice.keys())

    # Solve the problem
    problem.solve(PULP_CBC_CMD(msg=0, timeLimit=time))


    # Solution
    solution = {}
    for i in mentee_choice.keys():
        for j in mentor_choice.keys():
            if decision[i, j].varValue == 1:
                solution[(i, j)] = scores[(i,j)]


    return problem.objective.value(), solution