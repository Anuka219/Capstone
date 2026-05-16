```python
import sys


class SimpleChatbot:
	"""A minimal rule-based chatbot."""

	def __init__(self, name="Chatbot"):
		self.name = name

	def reply(self, message: str) -> str:
		msg = message.strip().lower()
		if not msg:
			return "Please say something."
		if any(g in msg for g in ("hi", "hello", "hey")):
			return "Hello. How can I help you?"
		if "help" in msg:
			return "I can answer simple questions or chat. Try asking about the weather or say 'bye' to exit."
		if "weather" in msg:
			return "I can't fetch live weather, but it might be a good idea to check your local forecast."
		if "bye" in msg or "exit" in msg or "quit" in msg:
			return "bye"
		return "Sorry, I don't have an answer for that."


def main():
	bot = SimpleChatbot(name="AI Chatbot")
	print(f"{bot.name} started. Type a message (type 'bye' to exit).")
	try:
		while True:
			user = input("You: ")
			resp = bot.reply(user)
			if resp == "bye":
				print("Bot: Goodbye.")
				break
			print(f"Bot: {resp}")
	except (KeyboardInterrupt, EOFError):
		print("\nBot: Goodbye.")


if __name__ == "__main__":
	main()
```
