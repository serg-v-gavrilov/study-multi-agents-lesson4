from agent import agent


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

        for chunk in agent.stream(
            {"messages": [("user", user_input)]},
            config={"configurable": {"thread_id": "main"}},
        ):
            chunkName = ""
            if "agent" in chunk:
                chunkName = "agent"
            elif "model" in chunk:
                chunkName = "model"

            if chunkName != "" and "messages" in chunk[chunkName]:
                for msg in chunk[chunkName]["messages"]:
                    if hasattr(msg, "content") and msg.content:
                        print(f"\nAgent: {msg.content}")


if __name__ == "__main__":
    main()
