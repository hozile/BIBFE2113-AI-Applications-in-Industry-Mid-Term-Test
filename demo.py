"""Demo script to showcase the LangChain application features."""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from mock_tools import FakeWeatherSearchTool, FakeCalculatorTool, FakeNewsSearchTool
from router import ConversationRouter

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
    tools = [ FakeNewsSearchTool(),FakeWeatherSearchTool(),FakeCalculatorTool()]
    
    # Initialize router
    router = ConversationRouter(llm,tools=tools)
    
    # # Demo queries
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