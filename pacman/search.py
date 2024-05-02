# coding=utf-8
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).
"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from game import Directions

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    # from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    pilha = util.Stack()
    # Apenas para armazenar os nós já visitados
    visitados = util.Stack()

    inicio = problem.startState
    fim = problem.goal

    pilha.push((inicio[0], inicio[1], ''))


    while not pilha.isEmpty():

        no = pilha.pop()

        if no[0] == fim[0] and no[1] == fim[1]: # Verifica se chegou ao ponto final
            break

        if not contem(pilha, no) and not contem( visitados, no):

            visitados.push((no[0], no[1], no[2]))
            nos_livres = no_adjacentes(problem, no)# Expande nó
            for no in nos_livres:
                if not contem(pilha, no) and not contem(visitados, no):
                    pilha.push(no)
    problem._expanded = len(visitados.list)#Exibe quantidade de no expandido no console
    return string_to_movimentos(no[2])

def contem(pilha, no):

    for no_temp in pilha.list:
        if no_temp[0] == no[0] and no_temp[1] == no[1]:
            return True
    return False

#o parametro no se refere ao no que se deseja consultar os arredores.
#Exemplo do parametro nó, uma tupla contendo ( x, y, '') onde a string contida
#na posição tupla[2] seria o caminho percorrido do no origem até o nó atual.
def no_adjacentes(problem, no):
    labirinto = problem.walls.data

    nos_adjacentes = []

    X = no[0]
    Y = no[1]
    C = no[2] #Caminho até no atual

    norte = labirinto[X][Y + 1]

    if not norte:
        nos_adjacentes.append(( X, Y+1, C+'n'))

    sul = labirinto[X][Y - 1]

    if not sul:
        nos_adjacentes.append((X, Y-1, C+'s'))

    leste = labirinto[X + 1][Y]

    if not leste:
        nos_adjacentes.append((X+1, Y, C+'e'))

    oeste = labirinto[X - 1][Y]

    if not oeste:
        nos_adjacentes.append((X-1, Y, C+'w'))

    return nos_adjacentes

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    DICA: Utilizar util.PriorityQueue
    *** YOUR CODE HERE ***
    """

    #unica diferença do codigo de busca em profundidade.
    pilha = util.Queue()
    # Apenas para armazenar os nós já visitados
    visitados = util.Stack()

    inicio = problem.startState
    fim = problem.goal

    pilha.push((inicio[0], inicio[1], ''))


    while not pilha.isEmpty():

        no = pilha.pop()

        if no[0] == fim[0] and no[1] == fim[1]: # Verifica se chegou ao ponto final
            break

        if not contem(pilha, no) and not contem( visitados, no):

            visitados.push((no[0], no[1], no[2]))
            nos_livres = no_adjacentes(problem, no)# Expande nó
            for no in nos_livres:
                if not contem(pilha, no) and not contem(visitados, no):
                    pilha.push(no)

    problem._expanded = len(visitados.list)#Exibe quantidade de no expandido no console
    return string_to_movimentos(no[2])

def string_to_movimentos( string_movimentos):

    s = Directions.SOUTH
    w = Directions.WEST
    e = Directions.EAST
    n = Directions.NORTH

    movimentos = []
    for i in range(0, len(string_movimentos)):
        if string_movimentos[i] == 'n':
            movimentos.append(n)
        if string_movimentos[i] == 's':
            movimentos.append(s)
        if string_movimentos[i] == 'w':
            movimentos.append(w)
        if string_movimentos[i] == 'e':
            movimentos.append(e)


    return movimentos

def uniformCostSearch(problem):
    """Search the node of least total cost first.
    *** YOUR CODE HERE ***
    """
    fila_prioridade = util.PriorityQueue()
    # Apenas para armazenar os nós já visitados
    processados = util.Stack()

    inicio = problem.startState
    fim = problem.goal

    #O item tupla[3] representa o custo até chegar ao nó.
    fila_prioridade.push((inicio[0], inicio[1], '', 0), 0)


    while not fila_prioridade.isEmpty():

        no = fila_prioridade.pop()

        if no[0] == fim[0] and no[1] ==  fim[1]: # Verifica se chegou ao ponto final
            break

        if not contem( processados, no):

            processados.push((no[0], no[1], no[2], no[3]))
            nos_livres = no_adjacentes(problem, no)# Expande nó
            for no_tmp in nos_livres:
                if not contem(processados, no_tmp):
                    custo_no = no[3]+1
                    no_tmp = ( no_tmp[0], no_tmp[1], no_tmp[2], custo_no)
                    fila_prioridade.push(no_tmp, custo_no)

    problem._expanded = len(processados.list)#Exibe quantidade de no expandido no console
    return string_to_movimentos(no[2])

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fila_prioridade = util.PriorityQueue()
    # Apenas para armazenar os nós já visitados
    processados = util.Stack()

    inicio = problem.startState
    fim = problem.goal

    #O item tupla[3] representa o custo até chegar ao nó.
    fila_prioridade.push((inicio[0], inicio[1], '', 0), 0)


    while not fila_prioridade.isEmpty():

        no = fila_prioridade.pop()

        if no[0] == fim[0] and no[1] ==  fim[1]: # Verifica se chegou ao ponto final
            break

        if not contem( processados, no):

            processados.push((no[0], no[1], no[2], no[3]))
            nos_livres = no_adjacentes(problem, no)# Expande nó
            for no_tmp in nos_livres:
                if not contem(processados, no_tmp):

                    custo_no = no[3]+1
                    x_no_tmp = no_tmp[0]
                    y_no_tmp = no_tmp[1]
                    string_caminho_no_tmp = no_tmp[2]
                    #adição da heuristica, diferenciando assim da busca uniforme
                    heuristica = heuristic((x_no_tmp, y_no_tmp), problem)

                    f = custo_no + heuristica

                    no_tmp = (x_no_tmp, y_no_tmp, string_caminho_no_tmp, custo_no)
                    fila_prioridade.push(no_tmp, f)#Adiciona nó na fila de prioridade de acordo com a função f

    problem._expanded = len(processados.list)#Exibe quantidade de no expandido no console
    return string_to_movimentos(no[2])


# Abbreviation
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
