#!/usr/bin/env python

import asyncio
import logging

from dotenv import load_dotenv

# Websockets imports.
from websockets.asyncio.server import serve


# AI Agent support libraries.
from langchain_google_genai import ChatGoogleGenerativeAI
from agent.agent_utils import AgentFlow
from langchain_core.messages import HumanMessage

# Loading env variables.
load_dotenv()

logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.DEBUG,
)

async def handler(websocket):
    # Initializing Google LLM.

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    
    # Creating langGraph agent
    
    agent_workflow = AgentFlow(llm)
    agent = agent_workflow.create_agent()
    
    # Logic for receiving messages through the websocket.
    messages_stream = []

    async for message in websocket:
        # Converting message into LangChain HumanMessage to send it to the agent.
        messages_stream.append(HumanMessage(content=message))
        
        # Invoking the agents to get the results from the query.
        agent_query_result = None
        agent_query_result = agent.invoke({"messages": messages_stream})
        
        # Return the message contents back to the UI/Websocket client.
        if agent_query_result != None:
            response = agent_query_result['messages'][-1].content
            await websocket.send(response)

async def main():
    async with serve(handler, "", 8001) as server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
