import { expect, test } from '@playwright/test'

test.setTimeout(5000)

test('LensQuery', async ({ page }) => {
  await page.goto('http://localhost:3001/user')
  await test.step('WebSocket connection open', async () => {
    await page.waitForEvent(
      'websocket',
      (ws) => ws.url() === 'ws://localhost:6969/ws',
    )
  })
  await test.step('IDB initialization', async () => {
    const { objectStoreNames } = await page.evaluate(async () => {
      const idb = await window.idbPromise
      return {
        objectStoreNames: [...idb.objectStoreNames],
      }
    })
    expect(objectStoreNames).toEqual(expect.arrayContaining(['User']))
    expect(objectStoreNames).toEqual(expect.arrayContaining(['UserSettings']))
  })
})
