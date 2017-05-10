import sys


class Node:
    def __init__(self, name):
        self.name = name
        self.adjacentNodes = []
        self.value = None


def getComplimentOfNode(N):
    c = None
    if N.name[0] == '!':
        c = N.name[1:]
    else:
        c = '!' + N.name
    complimentNode = Node(c)
    for node in graph:
        if node.name == c:
            complimentNode = node
    return complimentNode


def addNodeToGraph(N):
    global graph
    present = False
    for node in graph:
        if node.name == N.name:
            present = True
            break
    if not present:
        graph.append(N)


def addDirectedEdge(fromNode, toNode):
    fromIndex = None
    toIndex = None
    global graph
    numOfNodesInGraph = len(graph)

    for i in range(numOfNodesInGraph):
        if fromIndex is None:
            if fromNode.name == graph[i].name:
                fromIndex = i
        if toIndex is None:
            if toNode.name == graph[i].name:
                toIndex = i
    graph[fromIndex].adjacentNodes.append(graph[toIndex])


def getAdjacentNodes(N):
    retVal = ""
    for node in graph:
        if N == node:
            if len(node.adjacentNodes) != 0:
                for adjacentNode in node.adjacentNodes:
                    retVal += adjacentNode.name + ","
    return retVal


def printNodesInGraph():
    for node in graph:
        print(node.name + " --> " + getAdjacentNodes(node))


def getAllReachableNodes(N):
    global allReachableNodes
    for adjNode in N.adjacentNodes:
        if adjNode not in allReachableNodes:
            allReachableNodes.append(adjNode)
            getAllReachableNodes(adjNode)


def nodeIsNonForcing():
    global allReachableNodes
    for N in allReachableNodes:
        complimentOfN = getComplimentOfNode(N)
        if complimentOfN in allReachableNodes:
            return False
    return True


def nodeAndComplimentAreForcingNodes(nodes):
    for N in nodes:
        complimentN = getComplimentOfNode(N)
        if complimentN in nodes:
            return True
    return False


lines = [line.rstrip('\n') for line in open(sys.argv[1])]
cnf = lines[0]
cnf = cnf.replace(" ", "")
clauses = cnf.split("&")

graph = []

for clause in clauses:

    if clause[0] == '(' and clause[len(clause) - 1] == ')':
        clause = clause[1:-1]

    literals = clause.split("|")
    literal1 = literals[0]
    N1 = Node(literal1)
    N1Compliment = getComplimentOfNode(N1)
    addNodeToGraph(N1)
    addNodeToGraph(N1Compliment)

    literal2 = None

    if len(literals) == 2:
        literal2 = literals[1]

        N2 = Node(literal2)
        N2Compliment = getComplimentOfNode(N2)
        addNodeToGraph(N2)
        addNodeToGraph(N2Compliment)
        addDirectedEdge(N1Compliment, N2)
        addDirectedEdge(N2Compliment, N1)

    elif len(literals) == 1:
        N1 = Node(literal1)
        addNodeToGraph(N1)

print("--------------- GRAPH ------------------")
printNodesInGraph()
print("----------------------------------------")

numOfNodes = len(graph)

nonForcingNodes = []
forcingNodes = []

for node in graph:
    allReachableNodes = []
    getAllReachableNodes(node)
    if nodeIsNonForcing():
        nonForcingNodes.append(node)
    else:
        forcingNodes.append(node)

print([x.name for x in forcingNodes])

if nodeAndComplimentAreForcingNodes(forcingNodes):

    print("f is not satisfiable")

else:

    print("f is satisfiable")

    temp = nonForcingNodes

    for node in nonForcingNodes:
        allReachableNodes = []
        getAllReachableNodes(node)

        if node not in allReachableNodes:
            allReachableNodes.append(node)

        for n in allReachableNodes:
            if n in temp:
                temp.remove(n)
                idx = graph.index(n)
                graph[idx].value = 1
                nCompliment = getComplimentOfNode(n)
                if nCompliment in temp:
                    temp.remove(nCompliment)
                idx = graph.index(nCompliment)
                graph[idx].value = 0

    for i in range(numOfNodes):
        if graph[i].value is None:
            compliment = getComplimentOfNode(graph[i])
            if compliment.value is None:
                graph[i].value = 1
                idx = graph.index(compliment)
                graph[idx].value = 0
            elif compliment.value == 1:
                graph[i].value = 0
            elif compliment.value == 0:
                graph[i].value = 1

    names = [N.name for N in graph]
    values = [N.value for N in graph]

    for i in range(len(names)):
        print(str(names[i]) + " : " + str(values[i]))

    kNames = [N.name for N in graph if N.name[0] != '!']
    kValues = [N.value for N in graph if N.name[0] != '!']

    print("----------- Tuple ------------")
    print(str(kNames) + ' --> ' + str(kValues))
