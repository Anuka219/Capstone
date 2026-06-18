import { useEffect, useMemo, useState } from 'react'

interface PointerPosition {
  x: number
  y: number
}

interface AnimatedAvatarProps {
  pointer: PointerPosition
  clickPulse: number
}

export default function AnimatedAvatar({ pointer, clickPulse }: AnimatedAvatarProps) {
  const [position, setPosition] = useState<PointerPosition>(pointer)
  const [mood, setMood] = useState<'idle' | 'cheer'>('idle')

  useEffect(() => {
    let frame = 0

    const followPointer = () => {
      setPosition((current) => ({
        x: current.x + (pointer.x + 34 - current.x) * 0.16,
        y: current.y + (pointer.y - 58 - current.y) * 0.16,
      }))
      frame = window.requestAnimationFrame(followPointer)
    }

    frame = window.requestAnimationFrame(followPointer)
    return () => window.cancelAnimationFrame(frame)
  }, [pointer.x, pointer.y])

  useEffect(() => {
    if (clickPulse === 0) return

    setMood('cheer')
    const timeout = window.setTimeout(() => setMood('idle'), 620)
    return () => window.clearTimeout(timeout)
  }, [clickPulse])

  const eyeShift = useMemo(() => {
    const dx = pointer.x - position.x
    const dy = pointer.y - position.y
    const distance = Math.max(Math.hypot(dx, dy), 1)

    return {
      x: (dx / distance) * 4,
      y: (dy / distance) * 3,
    }
  }, [pointer.x, pointer.y, position.x, position.y])

  return (
    <div
      aria-hidden="true"
      className="pointer-events-none fixed left-0 top-0 z-30 h-20 w-20 transition-transform duration-75"
      style={{ transform: `translate3d(${position.x}px, ${position.y}px, 0)` }}
    >
      <div className={`relative h-full w-full ${mood === 'cheer' ? 'animate-avatar-pop' : 'animate-avatar-run'}`}>
        <div className="absolute -bottom-1 left-3 h-3 w-14 rounded-full bg-slate-900/20 blur-sm" />

        <div className="absolute left-4 top-1 h-5 w-3 rotate-[-22deg] rounded-full bg-[#1f6f78]" />
        <div className="absolute right-4 top-1 h-5 w-3 rotate-[22deg] rounded-full bg-[#1f6f78]" />

        <div className="absolute inset-x-2 top-4 h-14 rounded-[1.35rem] border-2 border-slate-950 bg-[#ffd166] shadow-[0_8px_0_#1f6f78]">
          <div className="absolute left-3 top-4 h-5 w-5 rounded-full border-2 border-slate-950 bg-white">
            <span
              className="absolute left-1.5 top-1.5 h-2.5 w-2.5 rounded-full bg-slate-950"
              style={{ transform: `translate(${eyeShift.x}px, ${eyeShift.y}px)` }}
            />
          </div>
          <div className="absolute right-3 top-4 h-5 w-5 rounded-full border-2 border-slate-950 bg-white">
            <span
              className="absolute left-1.5 top-1.5 h-2.5 w-2.5 rounded-full bg-slate-950"
              style={{ transform: `translate(${eyeShift.x}px, ${eyeShift.y}px)` }}
            />
          </div>

          <div
            className={`absolute left-1/2 top-10 -translate-x-1/2 border-2 border-slate-950 ${
              mood === 'cheer'
                ? 'h-4 w-6 rounded-b-full bg-[#ef476f]'
                : 'h-2 w-7 rounded-b-full border-t-0'
            }`}
          />
        </div>

        <div className="absolute bottom-0 left-5 h-4 w-3 rounded-full bg-slate-950 animate-foot-left" />
        <div className="absolute bottom-0 right-5 h-4 w-3 rounded-full bg-slate-950 animate-foot-right" />

        {mood === 'cheer' && (
          <>
            <span className="absolute -left-1 top-0 h-2 w-2 rounded-full bg-[#ef476f] animate-spark-one" />
            <span className="absolute left-9 -top-3 h-2 w-2 rounded-full bg-[#1f6f78] animate-spark-two" />
            <span className="absolute right-0 top-3 h-2 w-2 rounded-full bg-[#06d6a0] animate-spark-three" />
          </>
        )}
      </div>
    </div>
  )
}
