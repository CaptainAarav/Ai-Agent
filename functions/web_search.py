import os
import requests
from dotenv import load_dotenv
from config import WEB_SEARCH_MAX_RESULTS

# defines functions schema 
schema_web_search = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Lets you search web with a given query and returns top 5 results.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "the search query you must provide for search engine for results",
                },
            },
            "required": ["query"]
        },
    },
}

def web_search(working_directory: str, query: str) -> str:
    # setup a try except block to catch any exceptions from external library
    try:
        # loads and sets our tavily api key required for searching web
        load_dotenv()
        tavily_api_key = os.environ.get("TAVILY_API_KEY")
        # checks if it loaded anything if not returns the error
        if not tavily_api_key:
            return f"Error: could not load tavily api key"
        
        # creates a HTTP post request to tavily api with our query and a max results to what our config set it to and a timeout of 10 seconds
        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": tavily_api_key,
                "query": query,
                "max_results": WEB_SEARCH_MAX_RESULTS,
            },
            timeout=10
        )
        
        # checks if our response returned any HTTP error code, if so raises an exception for us
        response.raise_for_status()
        
        # parses the response json into a python dict
        data: dict = response.json()
        
        output_string: str = ""
        output_string += f"search query: {data['query']}\n"
        # a generator expression that loops through our results and builds a result section for each one
        output_string += "\n".join(
            f"Result:\nTitle: {result['title']}\nurl: {result['url']}\ncontent: {result['content']}\nscore: {result['score']}"
            for result in data["results"]
        )

        return output_string
    except Exception as e:
        # handles any exception thrown by external librarys gracefully and returns them for agent
        return f"Error: {e}"