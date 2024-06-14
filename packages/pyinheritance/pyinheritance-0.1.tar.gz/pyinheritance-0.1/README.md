## Introduce

This package use tree structure to model inheritance hierarchy of Python project.
The core class is `_ClassNode` which represents a Python class, it maintains two lists to store all of its base classes
and subclasses

On top of that, `_ClassNode` provides hierarchy visualization

## Usage

``` Python
## Initiaze ClassNodeFactory which manages all _ClassNode
node_factory = ClassNodeFactory()

## Initiaze a class node of BasePromptTemplate which is a class from langchain
bpt_node = node_factory.init(BasePromptTemplate)

## Visuralize the class node by calling _ClassNode.visualize_from_self(). It returns a Digraph from graphviz
graph = bpt_node.visualize_from_self()
graph.render('class_nodes', format='png', cleanup=True, view=True)
```