interface Window {
  pttcat: Record<string, unknown> & {
    actions: Record<string, unknown>
  }
}

namespace NodeJS {
  interface Process {
    server: boolean
    client: boolean
  }
}
