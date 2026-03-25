import json
from typing import List
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageToolCall
from tools import TOOLS_SCHEMA, TOOLS_MAP
from config import Settings, SYSTEM_PROMPT

client = OpenAI(api_key=Settings.api_key.get_secret_value())

history: list[dict] = []

def call_tools(tool_calls: List[ChatCompletionMessageToolCall]):
    for tool_call in tool_calls:
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        print(f"\n[Tool] {name}({args})")

        func = TOOLS_MAP.get(name)
        if func is None:
            result = f"error: unknown tool '{name}'"
        else:
            try:
                result = func(**args)
            except (EOFError, KeyboardInterrupt):
                result = f"call_tools error: {type(e).__name__}: {e}"


        history.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result, ensure_ascii=False),
        })


def run_agent(user_input: str) -> str:
    history.append({"role": "user", "content": user_input})

    for _ in range(Settings.max_iterations):
        response = client.chat.completions.create(
            model=Settings.model_name,
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            tools=TOOLS_SCHEMA,
        )

        message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        if finish_reason == "tool_calls":
            history.append(message.model_dump(exclude_unset=False))
            call_tools(message.tool_calls)

        elif finish_reason == "stop":
            final = message.content or ""
            history.append({"role": "assistant", "content": final})
            return final

        else:
            break

    summary_prompt = "Підсумуй результати досліджень та запиши звіт на основі вже зібраної інформації."
    history.append({"role": "user", "content": summary_prompt})

    response = client.chat.completions.create(
        model=Settings.model_name,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
        tools=TOOLS_SCHEMA,
    )
    final = response.choices[0].message.content or ""
    history.append({"role": "assistant", "content": final})
    call_tools(final.tool_calls)

    return final
