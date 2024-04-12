export const getLocalData = <Data>(key: string) => {
  const data = localStorage.getItem(key)
  return data ? (JSON.parse(data) as Data) : null
}
export const setLocalData = <Data>(key: string, data: Data) => {
  localStorage.setItem(key, JSON.stringify(data))
}
