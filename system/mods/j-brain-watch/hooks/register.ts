import type { EngineInterface, Register } from 'claude-code'

export type Touch = { kind: 'read' | 'edit' | 'inbox'; rel: string }

// Any spelling of the brain: ~/j_brain, the symlink, or the full Google Drive path.
const BRAIN = /(?:^|[\s'"=/~])j_brain(?:\/([^\s'"]*))?/
const WRITES = new Set(['Write', 'Edit', 'NotebookEdit'])
const SHELL_WRITE = /(>|\btee\b|\bcp\b|\bmv\b)/
const READ_BATCH_MS = 1500

/** What a tool call did to the brain, if anything. Pure, so the test can hold it. */
export function classify(tool: string, args: Record<string, unknown>): Touch | undefined {
  const text = [args.file_path, args.path, args.notebook_path, args.pattern, args.command]
    .filter((v): v is string => typeof v === 'string')
    .join(' ')
  const m = BRAIN.exec(text)
  if (!m) return undefined
  const rel = (m[1] ?? '').replace(/\/$/, '') || '.'
  const isInbox = rel.startsWith('inbox/') && rel !== 'inbox/.gitkeep'
  if (tool === 'Bash') return { kind: isInbox && SHELL_WRITE.test(text) ? 'inbox' : 'read', rel }
  if (WRITES.has(tool)) return { kind: isInbox ? 'inbox' : 'edit', rel }
  return { kind: 'read', rel }
}

const short = (rel: string) => rel.split('/').pop() || rel

// Reads come in bursts (INDEX, then a few notes): one toast per burst.
let reads: string[] = []
let flush: { cancel: () => void } | undefined

function notify($: EngineInterface, touch: Touch | undefined) {
  if (!touch) return
  if (touch.kind === 'inbox') {
    $.ui.toast(`📥 Saved to j_brain inbox: ${short(touch.rel)}`, { timeoutMs: 6000 })
  } else if (touch.kind === 'edit') {
    $.ui.toast(`✏️ Edited j_brain: ${touch.rel}`, { timeoutMs: 6000 })
  } else {
    if (!reads.includes(touch.rel)) reads.push(touch.rel)
    flush?.cancel()
    flush = $.clock.after(READ_BATCH_MS, () => {
      const names = reads.map(short)
      const shown = names.slice(0, 4).join(', ') + (names.length > 4 ? ` +${names.length - 4}` : '')
      $.ui.toast(`🧠 Read j_brain: ${shown}`)
      reads = []
      flush = undefined
    })
  }
}

export const register: Register = on => {
  on('tool.call', async ($, e, next) => {
    const ran = await next(e)
    if (ran.deny !== undefined || ran.isError) return ran
    try {
      notify($, classify(e.tool, e as unknown as Record<string, unknown>))
    } catch {
      // A watcher must never break the tool call it watches.
    }
    return ran
  })
}
