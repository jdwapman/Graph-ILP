import gurobipy as grb


# Initialize edge matrix to 0
n = 4 # Define number of vertices

e = []
for row in range(n):

	colList = []
	for col in range(n):
		colList.append(0)

	e.append(colList)

# Create graph (or read from file)
e[0][1] = 1
e[0][2] = 1
e[0][3] = 1

m = grb.Model()

# Add variables
x = {}

# Create binary variables
for i in range(n):
	x[i] = m.addVar(vtype=grb.GRB.BINARY, name="x%d" % i)


m.update()

# Add constraints
for i in range(n):
	for j in range(n):
		if e[i][j] == 1:
			m.addConstr(x[i]+x[j] <= 1)

# Create objective function
c = [1] * n
m.setObjective(grb.quicksum(-c[i]*x[i] for i in range(n)))

m.optimize()

print x
