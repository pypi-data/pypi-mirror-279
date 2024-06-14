from class_node import *
from langchain_core.prompts import BasePromptTemplate

node_factory = ClassNodeFactory()
bpt_node = node_factory.init(BasePromptTemplate)

graph = bpt_node.visualize_from_self()

graph.render('class_nodes', format='png', cleanup=True, view=True)
