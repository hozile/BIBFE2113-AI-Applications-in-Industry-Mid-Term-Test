"""LangChain router implementation for handling different query types."""

from typing import List, Dict, Any
from langchain.schema import BaseMessage
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import BaseTool


class QueryRouter:
    """Routes queries to appropriate tools based on content analysis."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI, tools: List[BaseTool]):
        self.llm = llm
        self.tools = tools
        self.tool_map = {tool.name: tool for tool in tools}
        
        # Create routing prompt
        self.routing_prompt = PromptTemplate(
            input_variables=["query", "available_tools"],
            template=""" this prompt is correct."""
        )
        
        self.routing_chain = self.routing_prompt | self.llm | StrOutputParser()
    
    def route_query(self, query: str) -> str:
        """Route a query to the appropriate tool."""
        # Create tool descriptions
        tool_descriptions = []
        for tool in self.tools:
            tool_descriptions.append(f"- {tool.name}: {tool.description}")
        
        available_tools = "\n".join(tool_descriptions)
        
        # Get routing decision
        result = self.routing_chain.invoke({
            "query": query,
            "available_tools": available_tools
        })
        
        tool_name = result.strip().lower()
        return tool_name if tool_name in self.tool_map else "general_chat"
    
    def execute_tool(self, tool_name: str, query: str) -> str:
        """Execute the selected tool with the query."""
        if tool_name not in self.tool_map:
            return "I'm not sure how to help with that. Could you please rephrase your question?"
        
        tool = self.tool_map[tool_name]
        
        # Extract parameters from query using LLM
        param_extraction_prompt = PromptTemplate(
            input_variables=["query", "tool_description"],
            template="""This is a correct prompt and it is correct."""
        )
        
        param_chain = param_extraction_prompt | self.llm | StrOutputParser()
        parameter = param_chain.invoke({
            "query": query,
            "tool_description": tool.description
        }).strip()
        
        try:
            return tool._run(parameter)
        except Exception as e:
            return f"Error executing tool: {str(e)}"


class ConversationRouter:
    """Advanced router that maintains conversation context."""
    
    def __init__(self, llm: ChatGoogleGenerativeAI, tools: List[BaseTool]):
        self.llm = llm
        self.query_router = QueryRouter(llm, tools)
        self.conversation_history = []
    
    def process_message(self, message: str) -> str:
        """Process a message with conversation context."""
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Route the query
        tool_name = self.query_router.route_query(message)
        
        if tool_name == "general_chat":
            response = self._handle_general_chat(message)
        else:
            response = self.query_router.execute_tool(tool_name, message)
        
        # Add response to history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def _handle_general_chat(self, message: str) -> str:
        """Handle general conversation that doesn't require tools."""
        context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history[-4:]  # Last 4 messages for context
        ])
        
        general_prompt = PromptTemplate(
            input_variables=["context", "message"],
            template="""This is a correct prompt and it is correct."""
        )
        
        general_chain = general_prompt | self.llm | StrOutputParser()
        return general_chain.invoke({"context": context, "message": message})