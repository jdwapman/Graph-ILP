import gurobipy as grb
import sys

""" ========== SETUP ========== """

# Check that the program has been called appropriately
if len(sys.argv) != 2:
	print "Usage: gurobi graphILP.py filename.txt"
	exit()

""" ========== READ GRAPH FROM FILE ========== """

# Open the file
graphFile = open(sys.argv[1], "r")

# Read the first line of the file as the number of vertices
n = int(graphFile.readline())

# Iterate over the file to read in the graph.
# Note: first line is ignored since it was already read
graph = {} # Create empty dict to store graph
for line in graphFile:
	nums = line.split()
	source = int(nums[0])
	dest = int(nums[1])

	# Add to dictionary
	if source in graph:
		graph[source].append(dest)
	else:
		graph[source] = [dest]

""" ========== GUROBI ILP ========== """

m = grb.Model()

# Add variables
x = {}

# Create binary variables
for i in range(1, n+1):
	x[i] = m.addVar(vtype=grb.GRB.BINARY, name="x%d" % i)

# Apply variables to gurobi model
m.update()

# Add constraints
for source, dests in graph.iteritems():
	for dest in dests:
		m.addConstr(x[source] + x[dest] <= 1)

# Create objective function. Note: Start from 1 to match file convention.
# Ignore entry at 0
c = [1] * (n+1)
m.setObjective(grb.quicksum(-c[i]*x[i] for i in range(1, n+1)))

m.optimize()

print x
