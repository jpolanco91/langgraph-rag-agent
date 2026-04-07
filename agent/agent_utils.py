from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import (
	BaseMessage,
	ToolMessage,
	SystemMessage
)
from operator import add as add_messages
from langgraph.graph import StateGraph, END
from .tools import retriever_tool
from .config import SYSTEM_PROMPT

class AgentState(TypedDict):
	messages: Annotated[Sequence[BaseMessage], add_messages]

class AgentFlow:
	def __init__(self, llm):
		self.llm = llm
		self.llm.bind_tools([retriever_tool])
		self.tools_dict = {
			"retriever_tool": retriever_tool
		}

	def __should_continue(self, state: AgentState):
		"""
		Check if the last message contains tool calls.
		"""
		result = state['messages'][-1]
		return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0

	def __call_llm(self, state: AgentState) -> AgentState:
		"""
		LLM Agent. This calls the LLM with the current state.
		"""
		messages = list(state['messages'])
		messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
		message = self.llm.invoke(messages)

		return {'messages': [message]}

	def __take_action(self, state: AgentState) -> AgentState:
		"""
		Retriever Agent. Execute tool calls from the LLM's response.
		"""
		tool_calls = state['messages'][-1].tool_calls
		results = []

		for t in tool_calls:
			print(f"Calling tool: {t["name"]} with query: {t['args'].get('query', 'No query provided')}")

			if not t['name'] in self.tools_dict:
				print(f"\nTool: {t['name']} does not exist.")
				result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools"
			else:
				result = self.tools_dict[t['name']].invoke(t['args'].get('query', ''))
				print(f"Result length: {len(str(result))}")

			results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

		print("Tools execution complete. Back to the model!")

		return {'messages': results}

	def create_agent(self):
		"""
		This function creates the agent/agentic workflow.
		"""
		graph = StateGraph(AgentState)
		graph.add_node("llm", self.__call_llm)
		graph.add_node("retriever_agent", self.__take_action)

		graph.add_conditional_edges(
			"llm",
			self.__should_continue,
			{True: "retriever_agent", False: END}
		)

		graph.add_edge("retriever_agent", "llm")
		graph.set_entry_point("llm")

		return graph.compile()
