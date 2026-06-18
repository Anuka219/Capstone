import re


class SimpleChatbot:
    """Rule-based MEM capstone chatbot used by the FastAPI backend."""

    def __init__(self, name="MEM Guide Bot"):
        self.name = name

    def reply(self, message: str) -> str:
        msg = message.strip().lower()

        if not msg:
            return "Please ask a question about the MEM chatbot project."
        if re.search(r"\b(hi|hello|hey|start)\b", msg):
            return (
                "Welcome. I am the MEM capstone guide. Ask me about the chatbot "
                "task, deadline, presentation content, tools, or methodology."
            )
        if any(word in msg for word in ("deadline", "upload", "date", "moodle")):
            return (
                "Upload the result to Moodle by 24 June 2026 at 15:00. "
                "The final presentations are also scheduled for 24 June 2026."
            )
        if any(word in msg for word in ("presentation", "present", "slides")):
            return (
                "Each group has 15 minutes. Show the chatbot, then explain the "
                "implementation, tools used, methodology, group members, and references."
            )
        if any(word in msg for word in ("project", "task", "chatbot", "mem")):
            return (
                "Project 2 is to create a chatbot that answers questions about MEM. "
                "The brief suggests using the voice or style of Raphael Volz or Moritz Peter."
            )
        if any(word in msg for word in ("group", "member", "team")):
            return (
                "Groups should have about 5 to 6 members. Name all participating group "
                "members in the PDF upload and at the beginning of the presentation."
            )
        if any(word in msg for word in ("tool", "technology", "stack")):
            return (
                "This prototype uses React, TypeScript, Vite, Tailwind CSS, and a Python "
                "FastAPI backend. A real LLM API can be added later if the group wants it."
            )
        if any(word in msg for word in ("method", "implementation", "how")):
            return (
                "A good methodology is: analyze the brief, collect MEM FAQs, design the "
                "conversation flow, implement the UI and backend, test common questions, "
                "and document limitations."
            )
        if any(word in msg for word in ("bye", "thanks", "thank")):
            return "Happy to help. Good luck with the capstone presentation."

        return (
            "I can help with MEM chatbot project details, deadline, group rules, "
            "presentation structure, tools, and methodology."
        )


def main():
    bot = SimpleChatbot()
    print(f"{bot.name} started. Type a message, or type 'bye' to exit.")

    try:
        while True:
            user = input("You: ")
            response = bot.reply(user)
            print(f"Bot: {response}")
            if user.strip().lower() in {"bye", "exit", "quit"}:
                break
    except (KeyboardInterrupt, EOFError):
        print("\nBot: Goodbye.")


if __name__ == "__main__":
    main()
