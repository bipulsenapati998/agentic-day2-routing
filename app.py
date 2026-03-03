from langchain_core.tools import tool
from typing import TypedDict, Annotated
from langchain_core.messages import AIMessage, BaseMessage
import operator
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage


class SupportState(TypedDict):
    messages: Annotated[list[BaseMessage], operator.add]
    should_escalate: bool
    issue_type: str
    user_tier: str  # "vip" or "standard"


# ===== TOOLS =====


# ==== Nodes =====
def check_user_tier_node(state: SupportState):
    """Decide if user is VIP or standard (mock implementation)."""
    first_message = state["messages"][0].content.lower()
    if "vip" in first_message or "premium" in first_message:
        return {"user_tier": "vip"}
    return {"user_tier": "standard"}


def vip_agent_node(state: SupportState):
    """VIP path: fast lane, no escalation."""
    # You can call an LLM here if you want.
    # For the assignment it is fine to just set a friendly VIP response.
    response = AIMessage(content=f"Hello VIP user! Your request is being fast-tracked.")
    return {"should_escalate": False, "messages": [response]}


def standard_agent_node(state: SupportState):
    """Standard path: may escalate."""
    # For now, just mark should_escalate = True to simulate escalation.
    response = AIMessage(
        content="Hello! Let me check your request. I may need to escalate this."
    )
    return {"should_escalate": True, "messages": [response]}


# ===== ROUTING =====
def route_by_tier(state: SupportState) -> str:
    """Route based on user tier."""
    if state.get("user_tier") == "vip":
        return "vip_path"
    return "standard_path"


# ===== BUILD GRAPH =====
def build_graph():
    workflow = StateGraph(SupportState)
    # Add nodes
    workflow.add_node("check_tier", check_user_tier_node)
    workflow.add_node("vip_agent", vip_agent_node)
    workflow.add_node("standard_agent", standard_agent_node)

    # Set entry points
    workflow.set_entry_point("check_tier")

    # Add conditional edges from the router
    workflow.add_conditional_edges(
        "check_tier",
        route_by_tier,
        {
            "vip_path": "vip_agent",
            "standard_path": "standard_agent",
        },
    )

    workflow.add_edge("vip_agent", END)
    workflow.add_edge("standard_agent", END)

    return workflow.compile()


def main() -> None:
    graph = build_graph()

    vip_result = graph.invoke(
        {
            "messages": [
                HumanMessage(content="I'm a VIP customer, please check my order")
            ],
            "should_escalate": False,
            "issue_type": "order_status",
            "user_tier": "",
        }
    )
    print("VIP result:", vip_result.get("user_tier"),"\n Should Escalate: ", vip_result.get("should_escalate"))

    standard_result = graph.invoke(
        {
            "messages": [HumanMessage(content="Check my order status")],
            "should_escalate": False,
            "issue_type": "order_status",
            "user_tier": "",
        }
    )
    print(
        "Standard result:",
        standard_result.get("user_tier"), "\n Should Escalate: ",
        standard_result.get("should_escalate"),
    )


if __name__ == "__main__":
    main()
