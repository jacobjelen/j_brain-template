import { expect, mock, test } from 'claude-code/testing'
import { classify } from './register'

const DRIVE = '/Users/john/Library/CloudStorage/GoogleDrive-john@example.com/My Drive/j_brain'

test('classify spots every way a session touches the brain', async () => {
  expect(classify('Read', { file_path: `${DRIVE}/memory/long/taste/films.md` })).toEqual({ kind: 'read', rel: 'memory/long/taste/films.md' })
  expect(classify('Read', { file_path: '/Users/john/j_brain/INDEX.md' })).toEqual({ kind: 'read', rel: 'INDEX.md' })
  expect(classify('Grep', { pattern: 'Maya', path: '~/j_brain/memory' })).toEqual({ kind: 'read', rel: 'memory' })
  expect(classify('Grep', { pattern: 'x', path: DRIVE })).toEqual({ kind: 'read', rel: '.' })
  expect(classify('Write', { file_path: '/Users/john/j_brain/inbox/2026-10-26-1412-claude-code-film.md' }))
    .toEqual({ kind: 'inbox', rel: 'inbox/2026-10-26-1412-claude-code-film.md' })
  expect(classify('Edit', { file_path: `${DRIVE}/system/rules/lessons.md` })).toEqual({ kind: 'edit', rel: 'system/rules/lessons.md' })
  expect(classify('Bash', { command: 'cat > ~/j_brain/inbox/x.md <<EOF' })).toEqual({ kind: 'inbox', rel: 'inbox/x.md' })
  expect(classify('Bash', { command: 'grep -ril maya ~/j_brain/memory/' })).toEqual({ kind: 'read', rel: 'memory' })
  expect(classify('Read', { file_path: '/Users/john/not_j_brain/x.md' })).toBeUndefined()
  expect(classify('Read', { file_path: '/Users/john/code/app.ts' })).toBeUndefined()
})

test('reads in a burst make one toast; an inbox save toasts at once', async ($, on) => {
  const clock = mock.clock(on)
  const toasts: string[] = []
  on('ui.toast', (_, e) => (toasts.push(e.text), { value: undefined }))
  on('tool.call', () => ({ result: {} }))

  await $.tool.call({ tool: 'Read', file_path: `${DRIVE}/INDEX.md` })
  await $.tool.call({ tool: 'Read', file_path: `${DRIVE}/memory/long/people/sam.md` })
  await $.tool.call({ tool: 'Read', file_path: '/tmp/unrelated.txt' })
  expect(toasts).toEqual([])
  await clock.advance(1500)
  expect(toasts).toEqual(['🧠 Read j_brain: INDEX.md, sam.md'])

  await $.tool.call({ tool: 'Write', file_path: `${DRIVE}/inbox/2026-10-26-1412-claude-code-film.md`, content: 'x' })
  expect(toasts[1]).toBe('📥 Saved to j_brain inbox: 2026-10-26-1412-claude-code-film.md')
})

test('a failed call toasts nothing', async ($, on) => {
  const clock = mock.clock(on)
  const toasts: string[] = []
  on('ui.toast', (_, e) => (toasts.push(e.text), { value: undefined }))
  on('tool.call', () => ({ result: 'no such file', isError: true }) as never)

  await $.tool.call({ tool: 'Read', file_path: `${DRIVE}/memory/nope.md` })
  await clock.advance(2000)
  expect(toasts).toEqual([])
})
