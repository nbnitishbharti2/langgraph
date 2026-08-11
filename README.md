# LangGraph Learning Notes

This repository contains practical implementations, experiments, and learnings on **LangGraph**.

---

## 1. LangGraph Basics ([simple-graph.ipynb](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb))

The [simple-graph.ipynb](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb) notebook demonstrates how to construct, visualize, and execute a simple state-driven workflow graph using **LangGraph**.

### Key Learnings & Concepts

#### 1. Defining Graph State ([State](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb#L35-L39))
- The **State** schema serves as the input and output interface for all nodes and edges in the graph.
- Defined using `TypedDict` from Python's `typing_extensions` or `typing` module to provide type hints for state keys.
```python
from typing_extensions import TypedDict


class State(TypedDict):
  graph_info: str
```

#### 2. Defining Node Functions ([start_play](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb#L48-L51), [cricket](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb#L53-L55), [badminton](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb#L57-L59))
- **Nodes** are standard Python functions that receive the current state dictionary as an argument.
- Each node performs operations and returns a dictionary with key-value updates to be merged back into the graph state.
```python
def start_play(state: State):
  print("Start Play node has been called.")
  return {"graph_info": state["graph_info"] + ", I am planning to play"}


def cricket(state: State):
  print("Cricket node has been called.")
  return {"graph_info": state["graph_info"] + " Cricket"}


def badminton(state: State):
  print("Badminton node has been called.")
  return {"graph_info": state["graph_info"] + " Badminton"}
```

#### 3. Dynamic Conditional Routing ([random_play](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb#L72-L76))
- Routing functions analyze the current state (or external logic) and return a `Literal` matching the name of the next node to navigate to.
```python
import random
from typing import Literal


def random_play(state: State) -> Literal["cricket", "badminton"]:
  if random.random() > 0.5:
    return "cricket"
  else:
    return "badminton"
```

#### 4. Building, Scheduling, and Compiling the Graph ([StateGraph](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb#L101-L115))
- Instantiate `StateGraph(State)` passing the state schema.
- Use `add_node(name, func)` to register nodes.
- Use `add_edge(source, destination)` for static transitions (including special constants `START` and `END`).
- Use `add_conditional_edges(source, routing_func)` to establish dynamic branching based on router output.
- Call `.compile()` to produce an executable `CompiledGraph`.
```python
from langgraph.graph import END, START, StateGraph

# Initialize graph with state schema
graph = StateGraph(State)

# Add nodes
graph.add_node("start_play", start_play)
graph.add_node("cricket", cricket)
graph.add_node("badminton", badminton)

# Schedule edges and conditional flow
graph.add_edge(START, "start_play")
graph.add_conditional_edges("start_play", random_play)
graph.add_edge("cricket", END)
graph.add_edge("badminton", END)

# Compile graph
graph_builder = graph.compile()
```

#### 5. Visualizing the Graph Structure ([draw_mermaid_png](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb#L118))
- LangGraph graphs can be visualized using Mermaid PNG rendering via `graph_builder.get_graph().draw_mermaid_png()`.

#### 6. Executing / Invoking the Graph ([invoke](file:///d:/PHP8.2/htdocs/learning/python-learning/langgraph/langgraph-basics/simple-graph.ipynb#L147))
- Call `graph_builder.invoke(initial_state)` passing the initial dictionary.
- Returns the final state after the graph execution reaches `END`.
```python
result = graph_builder.invoke({"graph_info": "My name is Nitish"})
# Output: {'graph_info': 'My name is Nitish, I am planning to play Badminton'} (or Cricket)
```