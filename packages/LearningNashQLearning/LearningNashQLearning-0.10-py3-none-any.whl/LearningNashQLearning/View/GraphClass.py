import networkx as nx
from netgraph import Graph
import matplotlib.pyplot as plt

from ..Model.Environment import Environment


class GraphClass:
    def __init__(self):
        self.graph = None
        self.edge_labels = {}
        self.node_colors = {}
        self.edge_colors = {}
        self.actionLabels = {}

    def create_graph(self, env: Environment):
        self.node_colors.clear()
        self.edge_colors.clear()
        self.graph = nx.DiGraph()
        self.env = env
        for i in range(env.getGames().shape[0]):
            self.graph.add_node(i)
            game = env.getGame(i)

            # find all non empty indexes
            actionProfiles = game.getAllActionProfiles()

            for action in actionProfiles:
                games, probs = game.getTransition(
                    tuple(action)).getTransitions()

                for g, p in zip(games, probs):
                    p = round(p, 3)
                    if p > 0:
                        self.setActionLabel(i, g, tuple(action), '')
                        self.graph.add_edge(i, g)

        for node in list(self.graph.nodes):
            self.node_colors.update({node: 'blue'})

        for edge in list(self.graph.edges):
            self.edge_colors.update({edge: 'black'})

        return self

    def plotGraph(self, ax: plt.Axes, fig: plt.Figure):
        ax.clear()
        self.updateLabelsFromActionLabels()
        plotInstance = Graph(self.graph, node_labels=True, node_layout='circular', edge_labels=self.edge_labels, edge_label_fontdict=dict(size=8), edge_layout='arc', node_size=10,
                             edge_width=0.5, arrows=True, ax=ax, node_edge_color=self.node_colors, node_label_fontdict=dict(size=10), edge_label_position=0.3, edge_color=self.edge_colors)
        fig.canvas.draw()
        fig.canvas.flush_events()

    def current_state_set(self, state):
        for node in list(self.graph.nodes):
            if node == state:
                self.node_colors.update({node: 'red'})
            else:
                self.node_colors.update({node: 'blue'})

    def setCurrentActionProfile(self, currentState, nextState):
        for edge in list(self.graph.edges):
            if edge[0] == currentState and edge[1] == nextState:
                self.edge_colors.update({edge: 'red'})
            else:
                self.edge_colors.update({edge: 'black'})

    def setActionLabel(self, fromGame, toGame, action, label):
        self.actionLabels.update({(fromGame, toGame, tuple([action])): label})

    def clearActionLabels(self):
        self.actionLabels.clear()

    def updateLabelsFromActionLabels(self):
        for (fgame, tgame, action), label in self.actionLabels.items():
            self.edge_labels.update({(fgame, tgame): ""})

        for (fgame, tgame, action), label in self.actionLabels.items():
            edge = (fgame, tgame)
            self.edge_labels[edge] += f'{action[0]}: ' + label + '\n'

        for (fgame, tgame, action), label in self.actionLabels.items():
            edge = (fgame, tgame)
            self.edge_labels[edge] = self.edge_labels[edge].strip()

    '''
    Set the labels of the edges of the graph
    @param labelFunction: function that takes an edge as input and returns a string
    '''

    def setLabels(self, labelFunction):
        for edge in list(self.graph.edges):
            self.edge_labels.update({edge: labelFunction(edge)})
