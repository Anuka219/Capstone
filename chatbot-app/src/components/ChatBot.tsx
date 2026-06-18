import { useEffect, useRef, useState } from 'react'

interface Message {
  id: string
  text: string
  sender: 'user' | 'bot'
  timestamp: Date
}

const suggestions = [
  'What is the chatbot project?',
  'When is the deadline?',
  'What should we present?',
  'Which tools did we use?',
]

function createId() {
  return typeof crypto !== 'undefined' && 'randomUUID' in crypto
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(16).slice(2)}`
}

function localReply(message: string) {
  const text = message.toLowerCase()

  if (/\b(hi|hello|hey|start)\b/.test(text)) {
    return 'Welcome. I am the MEM capstone guide. Ask me about the chatbot task, the deadline, presentation content, tools, or methodology.'
  }

  if (text.includes('deadline') || text.includes('upload') || text.includes('date')) {
    return 'The result should be uploaded to Moodle by 24 June 2026 at 15:00. The presentation day is also listed as 24 June 2026.'
  }

  if (text.includes('presentation') || text.includes('present')) {
    return 'Each group has 15 minutes. Besides showing the chatbot, explain the implementation, tools used, methodology, group members, and any third-party references.'
  }

  if (text.includes('project') || text.includes('task') || text.includes('chatbot')) {
    return 'Project 2 is to create a chatbot that answers questions about MEM. The slide also suggests using the voice or style of Raphael Volz or Moritz Peter.'
  }

  if (text.includes('group') || text.includes('member')) {
    return 'Groups should have about 5 to 6 members. Name all participating group members in the PDF upload and at the beginning of the presentation.'
  }

  if (text.includes('tool') || text.includes('technology') || text.includes('stack')) {
    return 'This prototype uses React, TypeScript, Vite, Tailwind CSS, and a Python FastAPI backend. The bot can be connected to a real LLM later, but it already works with a rule-based MEM knowledge base.'
  }

  if (text.includes('method') || text.includes('implementation') || text.includes('how')) {
    return 'A strong methodology slide can say: read the project brief, define MEM FAQ topics, design the conversation flow, implement the frontend and backend, test common questions, and document limitations.'
  }

  if (text.includes('bye') || text.includes('thanks') || text.includes('thank')) {
    return 'Happy to help. Good luck with the capstone presentation.'
  }

  return 'I can help with MEM chatbot project details, deadline, group rules, presentation structure, tools, and methodology. Try asking: "What should we present?"'
}

export default function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: createId(),
      text: 'Hello. I am your MEM capstone chatbot guide. Ask me about the AI chatbot project, deadlines, presentation content, or tools.',
      sender: 'bot',
      timestamp: new Date(),
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (messageText = input) => {
    const trimmed = messageText.trim()
    if (!trimmed || loading) return

    const userMessage: Message = {
      id: createId(),
      text: trimmed,
      sender: 'user',
      timestamp: new Date(),
    }

    setMessages((current) => [...current, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: trimmed }),
      })

      if (!response.ok) {
        throw new Error('Backend returned an error')
      }

      const data = (await response.json()) as { response?: string }
      setBackendOnline(true)
      setMessages((current) => [
        ...current,
        {
          id: createId(),
          text: data.response || localReply(trimmed),
          sender: 'bot',
          timestamp: new Date(),
        },
      ])
    } catch {
      setBackendOnline(false)
      window.setTimeout(() => {
        setMessages((current) => [
          ...current,
          {
            id: createId(),
            text: localReply(trimmed),
            sender: 'bot',
            timestamp: new Date(),
          },
        ])
      }, 280)
    } finally {
      window.setTimeout(() => setLoading(false), 300)
    }
  }

  return (
    <section className="flex h-[min(720px,calc(100vh-48px))] min-h-[560px] flex-col overflow-hidden rounded-lg border-2 border-slate-950 bg-white shadow-[10px_10px_0_#1f6f78]">
      <header className="border-b-2 border-slate-950 bg-[#ffd166] px-5 py-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs font-black uppercase tracking-[0.2em] text-[#1f6f78]">AI chatbot creation</p>
            <h2 className="text-2xl font-black text-slate-950">MEM Guide Bot</h2>
          </div>
          <span className="rounded-full border-2 border-slate-950 bg-white px-3 py-1 text-xs font-bold text-slate-800">
            {backendOnline === null ? 'Local + API ready' : backendOnline ? 'Backend connected' : 'Local fallback'}
          </span>
        </div>
      </header>

      <div className="border-b border-slate-200 bg-[#f7f3ea] px-5 py-3">
        <div className="flex gap-2 overflow-x-auto pb-1">
          {suggestions.map((suggestion) => (
            <button
              className="shrink-0 rounded-full border border-slate-300 bg-white px-3 py-2 text-sm font-semibold text-slate-700 transition hover:border-[#1f6f78] hover:text-[#1f6f78] disabled:opacity-50"
              disabled={loading}
              key={suggestion}
              onClick={() => void sendMessage(suggestion)}
              type="button"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>

      <div className="flex-1 space-y-4 overflow-y-auto bg-[#fffaf0] px-4 py-5 sm:px-5">
        {messages.map((message) => (
          <article className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`} key={message.id}>
            <div
              className={`max-w-[82%] rounded-lg border-2 border-slate-950 px-4 py-3 text-sm leading-6 shadow-[4px_4px_0_rgba(15,23,42,0.16)] sm:max-w-[70%] ${
                message.sender === 'user'
                  ? 'bg-[#1f6f78] text-white'
                  : 'bg-white text-slate-800'
              }`}
            >
              <p>{message.text}</p>
              <time className={`mt-2 block text-[10px] font-semibold ${message.sender === 'user' ? 'text-white/70' : 'text-slate-400'}`}>
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </time>
            </div>
          </article>
        ))}

        {loading && (
          <div className="flex justify-start">
            <div className="rounded-lg border-2 border-slate-950 bg-white px-4 py-3 shadow-[4px_4px_0_rgba(15,23,42,0.16)]">
              <div className="flex gap-2">
                <span className="h-2.5 w-2.5 animate-bounce rounded-full bg-[#1f6f78]" />
                <span className="h-2.5 w-2.5 animate-bounce rounded-full bg-[#e17e45] [animation-delay:120ms]" />
                <span className="h-2.5 w-2.5 animate-bounce rounded-full bg-[#ef476f] [animation-delay:240ms]" />
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form
        className="border-t-2 border-slate-950 bg-white p-4"
        onSubmit={(event) => {
          event.preventDefault()
          void sendMessage()
        }}
      >
        <div className="flex gap-3">
          <input
            className="min-w-0 flex-1 rounded-lg border-2 border-slate-300 px-4 py-3 text-base outline-none transition focus:border-[#1f6f78] focus:ring-4 focus:ring-[#1f6f78]/15"
            disabled={loading}
            onChange={(event) => setInput(event.target.value)}
            placeholder="Ask about MEM, deadline, tools, or methodology..."
            type="text"
            value={input}
          />
          <button
            aria-label="Send message"
            className="grid h-12 w-12 place-items-center rounded-lg border-2 border-slate-950 bg-[#ef476f] text-xl font-black text-white shadow-[4px_4px_0_#111827] transition hover:-translate-y-0.5 disabled:translate-y-0 disabled:cursor-not-allowed disabled:opacity-50"
            disabled={loading || !input.trim()}
            type="submit"
          >
            <span aria-hidden="true">-&gt;</span>
          </button>
        </div>
      </form>
    </section>
  )
}
