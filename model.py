

# Summary Example
""" MAIN FUNCTION: Bipartition of Tree
    This function finds a balanced 2 partition of a graph by drawing a
    spanning tree and finding an edge to cut that leaves at most an epsilon
    imbalance between the populations of the parts. If a root fails, new roots
    are tried until node_repeats in which case a new tree is drawn.

    Builds up a connected subgraph with a connected complement whose population
    is ``epsilon * pop_target`` away from ``pop_target``."""


"""Key functionalities include:

- Predecessor and successor functions for graph traversal using breadth-first search.
- Implementation of random and uniform spanning trees for graph partitioning.

Dependencies:

- networkx: Used for graph data structure and algorithms.
- random: Provides random number generation for probabilistic approaches.
- typing: Used for type hints.

Last Updated: March 22, 2024
"""


from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpBinary, PULP_CBC_CMD
import pandas as pd


# Use 'functools' (import partial) and 'typing' libraries to define the following function
def matching_one(mentee_choice, mentor_choice, uni_students, scores, max_student, uni_capacity, time):

    # intro Example
    """
    Builds a spanning tree chosen by Kruskal's method using random weights.

    :param graph: The input graph to build the spanning tree from. Should be a Networkx Graph.
    :type graph: nx.Graph
    :param weight_dict: Dictionary of weights to add to the random weights used in region-aware
    variants.
    :type weight_dict: Optional[Dict], optional

    :returns: The maximal spanning tree represented as a Networkx Graph.
    :rtype: nx.Graph
    """

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
            problem += decision[i, j] <= scores[(i,j)]

    # Objective function: the total assignment score is maximized.
    problem += lpSum(decision[i, j]*scores[(i,j)] for i in mentee_choice.keys() for j in mentor_choice.keys())

    # Solve the problem
    problem.solve(PULP_CBC_CMD(msg=0, timeLimit=time))

    # Solution
    solution = {'Mentor' : [], 'Student' : [], 'Score' : []}
    for j in mentor_choice.keys():
        for i in mentee_choice.keys():
            if decision[i, j].varValue == 1:
                solution['Mentor'].append(j)
                solution['Student'].append(i)
                solution['Score'].append(scores[(i,j)])
                                 
    df = pd.DataFrame(data = solution)

    return problem.objective.value(), solution, df



def matching_two(mentee_choice, mentor_choice, uni_students, mentee_high, mentor_high, scores, gender, ref_score, max_student, 
                 uni_capacity, time, epsilon, min_ref, weight_subject, weight_class, weight_ref):

    """
    Model 2: Constraints (6) and (7) are added. Objective function is changed. The rest is the same as Model 1.
        
        will be completed later on
    """

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
            problem += decision[i, j] <= scores[(i,j)]


    # Constraint (6): gender equality.
    problem += lpSum(decision[i, j]*gender[i] for i in mentee_choice.keys() for j in mentor_choice.keys()) >= (1 - epsilon) * lpSum(decision[i, j] for i in mentee_choice.keys() for j in mentor_choice.keys())
        
    
    # Constraint (7): eliminates mentees with ref score below r.
    for i in mentee_choice.keys():
        for j in mentor_choice.keys():
            problem += min_ref * decision[i, j] <= ref_score[i]
    

    # Objective function: sum od assignment scores is maximized.
    problem += weight_subject *lpSum(decision[i, j]*score[(i,j)] for i in mentee_choice.keys() for j in mentor_choice.keys()) + weight_class * lpSum(decision[i, j] for i in mentee_high for j in mentor_high) + weight_ref * lpSum(decision[i, j]*ref_score[i] for i in mentee_choice.keys() for j in mentor_choice.keys())

    # Solve the problem
    problem.solve(PULP_CBC_CMD(msg=0, timeLimit=time))


    # Solution
    solution = {'Mentor' : [], 'Student' : [], 'Score' : []}
    for j in mentor_choice.keys():
        for i in mentee_choice.keys():
            if decision[i, j].varValue == 1:
                solution['Mentor'].append(j)
                solution['Student'].append(i)
                solution['Score'].append(score[(i,j)])
                                 
    df = pd.DataFrame(data = solution)


    return problem.objective.value(), solution, df
