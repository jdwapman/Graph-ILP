import gurobipy as grb
import sys
import time

""" ========== SETUP ========== """

# Check that the program has been called appropriately
if len(sys.argv) != 2:
	print "Usage: gurobi graphILP.py filename.txt"
	exit()

""" ========== READ GRAPH FROM FILE ========== """

tProgStart = time.time()

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

# Create gurobi model
m = grb.Model()

# Limit run time
days = 1
m.setParam('TimeLimit', 86400)

# Create binary variables and add to the gurobi model
x = {}
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
m.setObjective(grb.quicksum(x[i] for i in range(1, n+1)), grb.GRB.MAXIMIZE)

# Perform the integer linear programming optimization
tOptStart = time.time()
m.optimize()
tOptEnd = time.time()

# Print the ILP result. Note: the cost function is the negative of
# the number of independent vertices
print x

tProgEnd = time.time()

print "Total program runtime: ", tProgEnd - tProgStart, " sec"
print "Optimization runtime: ", tOptEnd - tOptStart, " sec"
