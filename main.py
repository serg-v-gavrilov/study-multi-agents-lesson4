from agent import agent
from config import Settings
from langgraph.errors import GraphRecursionError

def print_chunk(chunk):
    chunkName = ""
    if "agent" in chunk:
        chunkName = "agent"
    elif "model" in chunk:
        chunkName = "model"

    if chunkName != "" and "messages" in chunk[chunkName]:
        for msg in chunk[chunkName]["messages"]:
            if hasattr(msg, "content") and msg.content:
                print(f"\nAgent: {msg.content}")


def main():
    print("Research Agent (type 'exit' to quit)")
    print("-" * 40)

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        try:
            for chunk in agent.stream(
                {"messages": [("user", user_input)]},
                config={
                    "configurable": {"thread_id": "main"},
                    "recursion_limit": Settings.max_iterations
                },
            ):
                print_chunk(chunk)
        except GraphRecursionError:
            for chunk in agent.stream(
                {"messages": [("user", "Підсумуй результати досліджень та запиши звіт на основі вже зібраної інформації.")]},
                config={
                    "configurable": {"thread_id": "main"},
                    "recursion_limit": Settings.max_iterations
                },
            ):
                print_chunk(chunk)


if __name__ == "__main__":
    main()
