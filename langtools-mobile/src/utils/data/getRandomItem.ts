export const getRandomItem = <Item>(items: Item[]): Item | null => {
  if (items.length === 0) {
    return null
  }

  const randomIndex = Math.floor(Math.random() * items.length)
  return items[randomIndex] ?? null
}
