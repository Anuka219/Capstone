import { useEffect, useState } from 'react'
import ChatBot from './components/ChatBot'
import AnimatedAvatar from './components/AnimatedAvatar'

function App() {
  const [pointer, setPointer] = useState({
    x: typeof window === 'undefined' ? 0 : window.innerWidth / 2,
    y: typeof window === 'undefined' ? 0 : window.innerHeight / 2,
  })
  const [clickPulse, setClickPulse] = useState(0)

  useEffect(() => {
    const handlePointerMove = (event: PointerEvent) => {
      setPointer({ x: event.clientX, y: event.clientY })
    }

    const handlePointerDown = (event: PointerEvent) => {
      setPointer({ x: event.clientX, y: event.clientY })
      setClickPulse((pulse) => pulse + 1)
    }

    window.addEventListener('pointermove', handlePointerMove)
    window.addEventListener('pointerdown', handlePointerDown)

    return () => {
      window.removeEventListener('pointermove', handlePointerMove)
      window.removeEventListener('pointerdown', handlePointerDown)
    }
  }, [])

  return (
    <main className="min-h-screen overflow-hidden bg-[#f7f3ea] text-slate-950">
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_top_left,rgba(30,95,116,0.18),transparent_34%),radial-gradient(circle_at_bottom_right,rgba(225,126,69,0.2),transparent_32%)]" />
      <div className="absolute inset-0 pointer-events-none opacity-[0.16] [background-image:linear-gradient(#203040_1px,transparent_1px),linear-gradient(90deg,#203040_1px,transparent_1px)] [background-size:32px_32px]" />

      <section className="relative z-10 mx-auto flex min-h-screen w-full max-w-6xl items-center px-4 py-6 sm:px-6 lg:px-8">
        <div className="grid w-full gap-6 lg:grid-cols-[320px_minmax(0,1fr)] lg:items-center">
          <aside className="hidden lg:block">
            <p className="mb-3 text-sm font-semibold uppercase tracking-[0.22em] text-[#1f6f78]">MEM Capstone 2026</p>
            <h1 className="text-4xl font-black leading-tight text-slate-950">AI chatbot with a playful guide</h1>
            <p className="mt-4 text-base leading-7 text-slate-700">
              Ask about the MEM/MIM capstone assignment, deadlines, presentation expectations, tools, and project method. The little guide follows your pointer and reacts when you click.
            </p>
          </aside>

          <ChatBot />
        </div>
      </section>

      <AnimatedAvatar clickPulse={clickPulse} pointer={pointer} />
    </main>
  )
}

export default App
