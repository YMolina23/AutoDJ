from langgraph.graph import END, StateGraph

from .agents import bpm_agent, ingest_agent, mix_agent, plan_agent
from .models import AutoDJState, Config


def build_graph():
    graph = StateGraph(AutoDJState)

    graph.add_node("ingest", ingest_agent)
    graph.add_node("analyze", bpm_agent)
    graph.add_node("plan", plan_agent)
    graph.add_node("mix", mix_agent)

    graph.set_entry_point("ingest")
    graph.add_edge("ingest", "analyze")
    graph.add_edge("analyze", "plan")
    graph.add_edge("plan", "mix")
    graph.add_edge("mix", END)
    return graph.compile()


def run_pipeline(config: Config) -> AutoDJState:
    graph = build_graph()
    initial_state: AutoDJState = {
        "config": config,
        "track_paths": [],
        "tracks": [],
        "ordered_tracks": [],
        "mix_path": "",
        "report_path": "",
    }

    return graph.invoke(initial_state)
