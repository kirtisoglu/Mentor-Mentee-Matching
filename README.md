# Directed Reading Program (DRP) Matching Model

### Description
The Directed Reading Program Matching Model is a Python-based solution designed to automate the matching process between mentees and mentors for the [DRP Türkiye](https://sites.google.com/view/drp-turkey/) in Türkiye.

Using the PuLP library, a linear programming model is constructed that provides matching according to certain criteria. This model aims to maximize the overall match quality based on interests, ensuring each mentee is paired with a suitable mentor while adhering to capacity constraints.

### About the Linear Programming 
An optimum solution of a minimization model is a vector x that satisfies all the constraints, and has the minimum objective value f(x). ( x does not have to be unique.) Luckily, we do not need to find the best solution: who cares if we have a perfect matching of mentors & mentees, it is enough for us to find a “good” matching. For this reason, we might use a metaheuristic algorithm to solve our model: 

### DRP Türkiye
DRP Türkiye is an online program that pairs undergraduate students studying mathematics at universities in and around Türkiye with graduate students and young researchers at institutions around the world to work together on selected books or articles in mathematics during the summer.
To check out more details, please see the [Previous Programs](https://sites.google.com/view/drp-turkey/previous-programs?authuser=0) and [DRP Türkiye YouTube Channel](https://www.youtube.com/@drpturkey2583)
## Prerequisites

Before you use the DRP Matching Model, ensure you have Python installed on your system. This project is tested on Python 3.8+. You will also need to install the required libraries:

```bash
pip install pulp pandas
```
* The model is returned as output as a dictionary and pandas DataFrame containing scores with each mentor and matched mentee(s).

## Schema of the CSV File
To create an input file conforming to the schema used by the program,
you should use the following format:

### Columns for Students and Mentors
*Name*<br>
The full name of the applicant

*Gender*<br>
Gender of the applicant

*University*<br>
The university of the student

*Department*<br>
The department of the applicant

*Class for Mentees & Position for Mentors*<br>
What grade the student is in or what position the Mentor holds.

*Which of the following topic(s) would you be most interested in reading about?*<br>
The columns 5 to 35 in the test data are dedicated to this question is the same in both the student and mentor datasets and identifies the areas of interest of both students and mentors. While students chose 3 areas of interest, mentors chose 4.

### Areas of Interests
*Analysis*<br>
Real Analysis/Functional Analysis, Complex Analysis, Harmonic Analysis, Numerical Analysis, Probability Theory, Statistics

*Foundations of mathematics*<br>
Mathematical logic (Set/Model Theory etc..), Category theory

*Algebra*<br>
Rings and Algebra, Group theory, Representation theory

*Number theory*<br>
Analytic number theory, Algebraic number theory

*Combinatorics and Graph theory*<br>
Combinatorics, Graph theory

*Geometry and Topology*<br>
General topology, Geometric topology, Algebraic topology, Algebraic geometry, Differential geometry

*Applied Mathematics*<br>
Probability theory, Statistics, Computer algebra, Data science, Cryptography/Coding theory, Mathematical modeling, Classical mechanics, Complex/Dynamical systems, Quantum theory, Relativity and Quantum relativistic theories, Statistical mechanics






