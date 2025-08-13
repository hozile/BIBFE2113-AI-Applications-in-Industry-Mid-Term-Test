## Bug #1: [Unable to load out the Google Gemini API Key]

**Error/Issue Observed:** Unable to load out the Google Gemini API Key

**LLM Assistance Used:** I'm asking why the Google Gemini API is not working even though I have added it into the .env file

**Root Cause:** load_dotenv is being imported but not being used

**Fix Applied:** 

```python
    load_dotenv()
    # Check if API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  No Google API key found. Using mock responses for demo.")
        run_mock_demo()
        return
```

**Verification:** The messages **⚠️ No Google API key found. Using mock responses for demo.** is not coming out anymore, and the codes is continue working without interrupt

## Bug #2: ["run_mock_demo" is not defined]

**Error/Issue Observed:** The code is being stopped since there is a function 'run_mock_demo' missing

**LLM Assistance Used:** I'm asking the ChatGPT to write me a 'run_mock_demo' function based on my codes

**Root Cause:** "run_mock_demo" function is not defined

**Fix Applied:** 

```python
def run_mock_demo():
    """Run the demo using mock responses (no API key)."""
    print("⚠️  Running mock demo mode...")

    mock_responses = {
        "What's the weather like in Tokyo?": "☀️ Sunny, 28°C",
        "Calculate 5 * 3": "15",
        "Find me news about machine learning": "Machine learning adoption is growing in 2025.",
        "Hello! How are you doing today?": "I'm just a mock AI, but doing great!"
    }

    for i, (query, response) in enumerate(mock_responses.items(), 1):
        print(f"\n--- Mock Demo {i} ---")
        print(f"Query: {query}")
        print(f"Response: {response}")


def run_api_demo():
    # Initialize LLM
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    # Initialize tools
    tools = [ FakeNewsSearchTool()]

    # Initialize router
    router = ConversationRouter(llm)

    # Demo queries
    demo_queries = [
        "What's the weather like in Tokyo?",
        "Calculate 5 * 3",
        "Find me news about machine learning",
        "Hello! How are you doing today?"
    ]


    print("\n🎯 Running demo queries...")

    for i, query in enumerate(demo_queries, 1):
        print(f"\n--- Demo {i} ---")
        print(f"Query: {query}")
        try:
            response = router.process_message(query)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {str(e)}")


def run_demo():
    """Run a demonstration of the application features."""
    print("🚀 LangChain Application Demo")
    print("=" * 40)

    # Load environment variables
    # os.environ[]

    load_dotenv()
    # Check if API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️  No Google API key found. Using mock responses for demo.")
        run_mock_demo()
        return
    else:
        run_api_demo()

if __name__ == "__main__":
    run_demo()
```

**Verification:** I have defined a run_mock_demo which running a mock demo without api being used and rewrite the demo with api into the function named run_api_demo

## Bug #3: [TypeError: ConversationRouter.__init__() missing 1 required positional argument: 'tools']

**Error/Issue Observed:**  The class 'ConverationRouter' is required one more arguments named 'tools', but only llm is given

```python
class ConversationRouter:
    """Advanced router that maintains conversation context."""

    def __init__(self, llm: ChatGoogleGenerativeAI, tools: List[BaseTool]):
        self.llm = llm
        self.query_router = QueryRouter(llm, tools)
        self.conversation_history = []
```

**LLM Assistance Used:** I'm confirming that i'm passing the correct 'tools' argument into the 'ConversationRouter'

**Root Cause:** There is one more argument named 'tools' need to be passing into the 'ConversationRouter'

**Fix Applied:** 

```python
    # Initialize tools
    tools = [ FakeNewsSearchTool()]

    # Initialize router
    router = ConversationRouter(llm,tools=tools)
```

**Verification:** I have observed that the code is continue running with demo query as i provied in the code and pass in to the process_message function.

## Bug #4: [The response from the LLM is not correct]

**Error/Issue Observed:** The LLM is answering the query with a totally non-related answer

**LLM Assistance Used:** I'm asking the LLM to generate me suitable prompts for each of the condition

**Root Cause:** The prompts and the tools is not passing correctly to the router

**Fix Applied:** 

passing all the tools into the router in demo.py:

```python
    # Initialize tools
    tools = [ FakeNewsSearchTool(),FakeWeatherSearchTool(),FakeCalculatorTool()]

    # Initialize router
    router = ConversationRouter(llm,tools=tools)
```

rewrite all the templates in the router.py:

```python
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
            template="""
            You are a query router. Based on the user query below, select the best tool
            from the list of available tools. Only return the exact tool name, nothing else.

            Query:
            {query}

            Available tools:
            {available_tools}
            """
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

        param_extraction_prompt = PromptTemplate(
            input_variables=["query", "tool_description"],
            template="""
            Extract the minimal parameter needed to execute the tool described below.
            Tool description:
            {tool_description}

            User query:
            {query}

            Only return the extracted parameter. No extra words.
            """
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
            template="""
            You are a helpful, friendly AI assistant. Continue the conversation naturally 
            based on the provided context and the latest user message.

            Conversation so far:
            {context}

            Latest user message:
            {message}

            Guidelines:
            - Keep responses clear and concise.
            - Stay consistent with the conversation's tone and topic.
            - If the user asks something unclear, politely ask for clarification.
            - Do not invent facts.

            Your response:
            """
        )


        general_chain = general_prompt | self.llm | StrOutputParser()
        return general_chain.invoke({"context": context, "message": message})
```

**Verification:** The LLM is now answering correct answer after the changes made

```cmd
--- Demo 1 ---
Query: What's the weather like in Tokyo?
Response: Weather in Tokyo:
- Condition: stormy
- Temperature: 12°C
- Humidity: 70%
- Wind Speed: 6 km/h

--- Demo 2 ---
Query: Calculate 5 * 3
Response: The result of 5 * 3 is 16

--- Demo 3 ---
Query: Find me news about machine learning
Response: Recent news about machine learning:
• New research reveals insights about machine learning
• Experts discuss the future of machine learning
• Local community responds to machine learning changes
• Global impact of machine learning continues to grow
• Breaking: Major developments in machine learning industry

--- Demo 4 ---
Query: Hello! How are you doing today?
Response: Hello! As an AI, I don't experience days or have feelings, but I'm ready and functioning well. How can I assist you today?
```

## Bug #5: [The answer for the calculation is always being added in 1 ]

**Error/Issue Observed:** The result of the calculation is always being added in 1

**LLM Assistance Used:** Debug on why the resulf of calculation is always added in 1

**Root Cause:**  The result output is written in result + 1, so the result of calculation is always incorrect

**Fix Applied:** 

Deleted + 1 from the result in mock_tools.py:

```python
class FakeCalculatorTool(BaseTool):
    """A mock calculator tool for basic math operations."""

    name: str = "calculator"
    description: str = "Perform basic mathematical calculations"
    args_schema: type = CalculatorInput

    def _run(self, expression: str) -> str:
        """Run the calculator tool."""
        try:
            result = eval(expression)
            return f"The result of {expression} is {result}"
        except Exception as e:
            return f"Error calculating {expression}: {str(e)}"
```

**Verification:** The result of calculation is now correct.
