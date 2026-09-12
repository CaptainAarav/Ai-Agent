import json
from config import AGENT_LOOP_LIMIT, MODEL
from available_functions import available_functions
from functions.call_function import call_function
from display import console, show_thinking, show_calling_function, show_tool_result, show_response, show_loop_exceeded


# runs agent loop
def run_agent(client, messages, user_prompt, verbose=False):
    # loops until agent is done or until agent loop limit is exceeded
    for _ in range(AGENT_LOOP_LIMIT):
        # displays a spinning circle in terminal using rich
        with show_thinking():
            # creates the chat completion request
            response = client.chat.completions.create(
                model=MODEL, messages=messages, tools=available_functions, temperature=0,
            )

        # adds the new response to the messages list
        messages.append(response.choices[0].message)

        # checks whether response had any tool calls
        if response.choices[0].message.tool_calls:
            # goes through each tool call and calls the corresponding function
            for tool_call in response.choices[0].message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                show_calling_function(tool_call.function.name, function_args, verbose)

                tool_call_result = call_function(tool_call)

                # checks whether tool call result content is nothing; if so, raises an exception
                if not tool_call_result["content"]:
                    raise Exception("tool call returned no content")

                # if the user passed the --verbose arg they will get this extra info
                show_tool_result(tool_call_result["content"], verbose)

                # adds the tool call result to the messages list
                messages.append(tool_call_result)
        # if no tool calls are in response, simply displays the content
        else:
            show_response(response, user_prompt, verbose)
            break
    else:
        # if agent loop limit is exceeded we exit with code 1
        show_loop_exceeded()