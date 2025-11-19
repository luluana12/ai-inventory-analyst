import json
from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
from agent.tools import tool_get_unhealthy_items

client = OpenAI()

SYSTEM_PROMPT = """
You are an AI inventory analyst for a cruise line

Your job:
- Minimize unhealthy inventory (overstock risk)
- Use the tools to pull real numbers before answering
- Always return clear explanations + metrics
- When showing results, be concise but helpful
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "tool_get_unhealthy_items",
            "description": "Find unhealthy inventory items for a specific ship.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "ship_name" : { "type" : "string"},
                    "as_of_date" : {"type" : "string"},
                    "top_k" : {"type" : "integer", "default" : 10}
                },
                "required" : ["ship_name", "as_of_date"]
                }
            }
    }
]

def run_agent(user_message, chat_history):
    """
    The main function that routes user messages through the LLM and handles tool calls.
    """

    messages = (
        [{"role" : "system" , "content" : SYSTEM_PROMPT}]
        + chat_history
        + [{"role" : "user", "content" : user_message}]
    )

    response = client.chat.completions.create(
        model = "gpt-4.1-mini",
        messages = messages,
        tools = TOOLS,
        tool_choice = "auto"
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        tc = msg.tool_calls[0]
        args = json.loads(tc.function.arguments)

        result = tool_get_unhealthy_items(**args)

        tool_msg = {
            "role" : "tool",
            "tool_call_id" : tc.id,
            "name" : tc.function.name,
            "content" : json.dumps(result)
        }

        final_resp = client.chat.completions.create(
            model = "gpt-4.1-mini",
            messages = messages + [msg,tool_msg]
        )

        return final_resp.choices[0].message.content
    
    #if no tool was used
    return msg.content
