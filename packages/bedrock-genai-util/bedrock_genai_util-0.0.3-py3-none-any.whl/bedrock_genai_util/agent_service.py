# Copyright (c) 2024 Biprajeet Kar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import json
import inspect

from bedrock_util import yaml
from bedrock_util.bedrock_genai_util.model_map import allowed_model_for_tool


def __read_agent_config(file_path):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except Exception as e:
        raise Exception(f"Error decoding YAML in file {file_path}: {e}")
    return None


def __read_tools_spec_config(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    except Exception as e:
        raise Exception(f"Error decoding tool specs in file {file_path}: {e}")
    return None


def __validate_model(model):
    return model in allowed_model_for_tool


def __filter_function_list(service_id, function_list):
    tool_set = set(agent_service_map["AgentServices"][service_id]["allowedTools"])

    func_list = [
        func
        for func in function_list
        if func.__name__ in tools_config["agentFunctions"]
    ]

    func_list = [func for func in func_list if func.__name__ in tool_set]

    return func_list


def __create_tool_spec(service_id, function_list):
    # Create tool specs

    function_list = __filter_function_list(service_id, function_list)

    if function_list is None or len(function_list) == 0:
        return None

    result = {
        "tools": [
            {
                "toolSpec": {
                    "name": func.__name__,
                    "description": tools_config["agentFunctions"][func.__name__].get(
                        "description", ""
                    ),
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            **({
                                   "properties": {
                                       prop: prop_data
                                       for prop, prop_data in tools_config["agentFunctions"][
                                           func.__name__
                                       ]["functionProperties"].items()
                                   },
                                   "required": tools_config["agentFunctions"][func.__name__][
                                       "requiredProperties"
                                   ],
                               } if "functionProperties" in tools_config["agentFunctions"][func.__name__] else {})
                        }
                    },
                }
            }
            for func in function_list
            if func.__name__ in tools_config["agentFunctions"]
        ]
    }

    return result


def __init_system_message(service_id, function_list):
    system_message = agent_service_map["AgentServices"][service_id].get(
        "agentInstruction"
    )

    function_list = __filter_function_list(service_id, function_list)
    if function_list is None or len(function_list) == 0:
        raise Exception("No valid function found")
    function_ops = __function_details_for_agent(function_list)

    extra_sys_msg = f"""Perform Below tool operations efficiently:\n{function_ops}.\nIf you are asked anything which cannot be achieved with above tools, politely decline."""

    if system_message is None or len(system_message) == 0:
        system_message = extra_sys_msg

    else:
        system_message = system_message + "\n" + extra_sys_msg

    return system_message


def __tool_call(
        bedrock_client, messages, model_id, system_message, inferenceConfig, tool_spec
):
    tool_call = bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=[{
            "text": system_message}],
        inferenceConfig=inferenceConfig,
        toolConfig=tool_spec,
    )

    return tool_call


def __invoke_function(func, input_data):
    return func(**input_data)


def __extract_tool_results(messages):
    tool_results = []
    for msg in messages:
        if msg.get("role") == "user":
            content = msg.get("content", [{}])[0]
            tool_result = content.get("toolResult", {})
            json_data = tool_result.get("content", [{}])[0].get("json", {})
            outcome = json_data.get("Outcome")
            if outcome:
                tool_results.append(str(outcome))

    return "\n".join(tool_results)


def __function_details_for_agent(function_list):
    func_details = [
        "- "
        + func.__name__
        + " - "
        + tools_config["agentFunctions"][func.__name__]["description"]
        for func in function_list
    ]
    return "\n".join(func_details)


def __agent_response(
        service_id,
        bedrock_client,
        model_id,
        system_message,
        inference_config,
        prompt,
        tool_result,
        function_tools,
):
    function_ops = __function_details_for_agent(
        __filter_function_list(service_id, function_tools)
    )

    if not function_ops:
        raise Exception("No valid function found")

    final_prompt = __create_final_prompt(prompt, tool_result)

    messages = [{
        "role": "user",
        "content": [{
            "text": final_prompt}]}]

    agent_resp = __call_converse_api(
        bedrock_client,
        model_id,
        messages,
        system_message,
        inference_config,
    )

    return __extract_agent_response(agent_resp)


def __call_converse_api(
        bedrock_client, model_id, messages, system_message, inference_config
):
    return bedrock_client.converse(
        modelId=model_id,
        messages=messages,
        system=[{
            "text": system_message}],
        inferenceConfig=inference_config,
    )


def __extract_agent_response(agent_resp):
    return agent_resp["output"]["message"]["content"][0]["text"]


def __invoke_tool(func, input_data, tool_use_id):
    return {
        "toolUseId": tool_use_id,
        "content": {
            "Outcome": f"""Output for {func.__name__} operation - {__invoke_function(func, input_data)}"""
        },
    }


def __create_tool_result_message(func_resp):
    return {
        "role": "user",
        "content": [
            {
                "toolResult": {
                    "toolUseId": func_resp["toolUseId"],
                    "content": [{
                        "json": func_resp["content"]}],
                }
            }
        ],
    }


def __create_final_prompt(prompt, tool_result):
    return f"""You are an AI assistant that generates responses to user queries based on the provided tool 
    results. Your task is to generate a response that is relevant to the user's query, incorporating the tool results in 
    a natural way. The response should be written in first-person point of view.

    If there are no tool results, Only reply "Sorry i was not able to find answers to your query."
    If tools provided is not matching with user query, Reply "Sorry i wont be able to process this request."

    #EXAMPLE:

    Query: 
    Hi Good morning.
    I would like you to perform the following:
    1. Introduce yourself.
    2. Add the numbers 1 and 1. 
    3. Subtract 3 from 2.

    Tool Result:
    Output for get_welcome operation - Hi. I am an AI assistant.
    Output for sum operation - 2
    Output for diff operation - -1

    Output:
    Hi. I am an AI assistant. 
    As per your queries please find details below- 
    - Addition of numbers 1 and 1 is 2.
    - Subtraction of 3 from 2 is -1.

    #ACTUAL:

    Query:
    {prompt}

    Tool Result:
    {tool_result}

    Output:

    #NOTE- Follow output format strictly.
    """


def run_agent(
        bedrock_client,
        model_id,
        agent_service_id,
        function_list,
        prompt,
        inference_config=None,
):
    if not prompt or not __validate_model(model_id):
        return None

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "text": f"""
                    {prompt}
                    """
                }
            ],
        }
    ]

    tool_specs = __create_tool_spec(agent_service_id, function_list)

    if not tool_specs:
        raise Exception("No valid tool found")

    system_message = __init_system_message(agent_service_id, function_list)

    if inference_config is None:
        inference_config = {
            "maxTokens": 4000,
            "temperature": 0}

    func_dict = {
        func.__name__: (func, set(inspect.signature(func).parameters.keys()))
        for func in function_list
    }

    tool_resp = __tool_call(
        bedrock_client,
        messages,
        model_id,
        system_message,
        inference_config,
        tool_specs,
    )
    messages.append(tool_resp["output"]["message"])

    while tool_resp["stopReason"] == "tool_use":
        for content in tool_resp["output"]["message"]["content"]:
            if "toolUse" in content:
                func_name = content["toolUse"]["name"]
                input_data = content["toolUse"]["input"]

                if func_name in func_dict:
                    func, param_names = func_dict[func_name]

                    if param_names == set(input_data.keys()):
                        func_resp = __invoke_tool(
                            func, input_data, content["toolUse"]["toolUseId"]
                        )
                        messages.append(__create_tool_result_message(func_resp))

                        tool_resp = __tool_call(
                            bedrock_client,
                            messages,
                            model_id,
                            system_message,
                            inference_config,
                            tool_specs,
                        )
                        messages.append(tool_resp["output"]["message"])
                    else:
                        print(f"Input keys do not match the parameters of {func_name}")
                else:
                    print(f"No function found with the name {func_name}")

    tool_result = __extract_tool_results(messages)

    return __agent_response(
        agent_service_id,
        bedrock_client,
        model_id,
        system_message,
        inference_config,
        prompt,
        tool_result,
        function_list,
    )


agent_service_map = __read_agent_config("agent_store.yaml")
tools_config = __read_tools_spec_config("tool_spec.json")
