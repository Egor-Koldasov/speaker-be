export const playAudioBase64 = (base64: string) => {
  const audio = new Audio()
  audio.src = 'data:audio/wav;base64,' + base64
  return audio.play()
}
