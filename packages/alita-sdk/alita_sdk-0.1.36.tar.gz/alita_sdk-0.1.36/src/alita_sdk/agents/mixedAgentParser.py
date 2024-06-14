import json
from typing import Union

from langchain_core.agents import AgentAction, AgentFinish, AgentStep
from langchain_core.exceptions import OutputParserException

from langchain.agents.agent import AgentOutputParser

from .utils import unpack_json

FORMAT_INSTRUCTIONS = """Respond only with JSON format as described below
{
    "thoughts": {
        "text": "message to a user in crisp and clear business language",
        "plan": "short bulleted, list that conveys long-term plan",
        "criticism": "constructive self-criticism",
    },
    "tool": {
        "name": "tool name",
        "args": { "arg name": "value" }
    }
}

You must answer with only JSON and it could be parsed by Python json.loads
"""


class UnexpectedResponseError(Exception):
    pass


class MixedAgentOutputParser(AgentOutputParser):
    """ Parser for JSON Style Communication Agent """

    def get_format_instructions(self) -> str:
        return FORMAT_INSTRUCTIONS

    def parse(self, text: str) -> Union[AgentAction, AgentFinish]:
        try:
            response = unpack_json(text)
        except json.decoder.JSONDecodeError:
            text.replace("\n", "\\n")
            response = unpack_json(text)
        if not isinstance(response, dict):
            return AgentFinish({"output": f'{response}\n\n*Note:* reposonse was not in expected format'}, log=response)
        tool: dict | str | None = response.get("tool", None)
        action = None
        tool_input = {}
        if tool:
            if isinstance(tool, dict):
                action: str | None = tool.get("name")
                tool_input: dict = tool.get("args", {})
            elif isinstance(tool, str):
                action: str | None = tool
                tool_input: dict = response.get("args", {})
            else:
                raise UnexpectedResponseError(f'Unexpected response {response}')
        thoughts = response.get("thoughts", {})
        if not isinstance(thoughts, dict):
            return AgentFinish({"output": f'Unexpected Format: {response}'}, log=response)
        plan: list | str = thoughts.get("plan", [])
        if isinstance(plan, list):
            plan: str = "\n".join(plan)
        txt: str = thoughts.get("text", '')
        criticism: str = thoughts.get("criticism", '')
        log: str = f"""Step Details:
{txt}
Long Term Plan:
{plan}
Criticism:
{criticism}

Running Tool:
{action} with param {tool_input}
"""
        if action in ['complete_task', 'respond', 'ask_user']:
            try:
                output: str = tool_input[list(tool_input.keys())[0]]
            except AttributeError:
                output: str = tool_input
            if output.strip() == "final_answer":
                output = txt
            return AgentFinish({"output": output}, log=log)
        elif action:
            return AgentAction(action, tool_input, log)
        elif txt:
            return AgentFinish({"output": txt}, log=log)
        else:
            return AgentFinish({"output": f"{response}. \n\n *NOTE: Response format wasn't followed*"}, log=log)
    @property
    def _type(self) -> str:
        return "mixed-agent-parser"
