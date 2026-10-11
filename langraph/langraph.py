from typing import TypedDict

from langgraph.graph import StateGraph


class complainant_scomplaint_State(TypedDict):
    mesage:str
    confidance:int



def greeting_node(state: complainant_scomplaint_State) -> complainant_scomplaint_State:
    """This is to greet the user"""