# LangChain Application with Router and Mock Tools

A comprehensive LangChain application demonstrating routing capabilities and mock tool integration.

## Features

- **Smart Query Routing**: Automatically routes user queries to appropriate tools
- **Mock Tools**: Includes fake weather, calculator, and news search tools
- **Conversation Context**: Maintains conversation history for better responses
- **Interactive CLI**: Easy-to-use command-line interface

## Project Structure

```
├── main.py           # Main application entry point
├── router.py         # Query routing logic
├── mock_tools.py     # Mock tool implementations
├── demo.py          # Demonstration script
├── requirements.txt  # Python dependencies
├── .env.example     # Environment variables template
└── README.md        # This file
```

## Setup

1. **Create virtual environment** (if not already done):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your Google API key for Gemini
   # Get your API key from: https://makersuite.google.com/app/apikey
   ```

## Usage

### Run the main application:
```bash
python main.py
```

### Run the demo:
```bash
python demo.py
```

## Available Tools

### 1. Weather Search Tool
- **Purpose**: Get weather information for any location
- **Example**: "What's the weather in Paris?"
- **Returns**: Mock weather data including temperature, conditions, humidity, and wind speed

### 2. Calculator Tool
- **Purpose**: Perform basic mathematical calculations
- **Example**: "Calculate 15 * 23"
- **Returns**: Mathematical results

### 3. News Search Tool
- **Purpose**: Search for news articles on specific topics
- **Example**: "Find news about artificial intelligence"
- **Returns**: Mock news headlines related to the topic

## Router Components

### QueryRouter
- Analyzes user queries using LLM
- Routes queries to appropriate tools
- Handles parameter extraction

### ConversationRouter
- Extends QueryRouter with conversation context
- Maintains chat history
- Handles general conversation

## Example Interactions

```
💬 You: What's the weather in Tokyo?
🤖 Assistant: Weather in Tokyo:
- Condition: partly cloudy
- Temperature: 22°C
- Humidity: 65%
- Wind Speed: 12 km/h

💬 You: Calculate 42 * 17
🤖 Assistant: The result of 42 * 17 is 714

💬 You: Find news about machine learning
🤖 Assistant: Recent news about machine learning:
• Breaking: Major developments in machine learning industry
• Experts discuss the future of machine learning
• New research reveals insights about machine learning
```

## Customization

### Adding New Tools
1. Create a new tool class in `mock_tools.py`
2. Inherit from `BaseTool`
3. Define input schema with Pydantic
4. Implement the `_run` method
5. Add to the tools list in `main.py`

### Modifying Router Logic
- Edit `router.py` to change routing behavior
- Customize prompts for better tool selection
- Add new routing strategies

## Dependencies

- `langchain`: Core LangChain framework
- `langchain-google-genai`: Google Gemini integration
- `langchain-community`: Community tools and utilities
- `python-dotenv`: Environment variable management

## Notes

- Mock tools generate random/fake data for demonstration
- In production, replace mock tools with real API integrations
- The router uses LLM for intelligent query analysis
- Conversation history is maintained in memory (not persistent)