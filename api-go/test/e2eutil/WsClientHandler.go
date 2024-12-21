package e2eutil

import "github.com/lxzan/gws"

type WsClientHandler struct {
	OnOpenHandler    func(socket *gws.Conn)
	OnCloseHandler   func(socket *gws.Conn, err error)
	OnPingHandler    func(socket *gws.Conn, payload []byte)
	OnPongHandler    func(socket *gws.Conn, payload []byte)
	OnMessageHandler func(socket *gws.Conn, message *gws.Message)
}

func NewWsClientHandler(
	onOpen func(socket *gws.Conn),
	onClose func(socket *gws.Conn, err error),
	onPing func(socket *gws.Conn, payload []byte),
	onPong func(socket *gws.Conn, payload []byte),
	onMessage func(socket *gws.Conn, message *gws.Message),
) *WsClientHandler {
	return &WsClientHandler{
		OnOpenHandler:    onOpen,
		OnCloseHandler:   onClose,
		OnPingHandler:    onPing,
		OnPongHandler:    onPong,
		OnMessageHandler: onMessage,
	}
}

func (h *WsClientHandler) OnOpen(socket *gws.Conn) {
	if h.OnOpenHandler != nil {
		h.OnOpenHandler(socket)
	}
}

func (h *WsClientHandler) OnClose(socket *gws.Conn, err error) {
	if h.OnCloseHandler != nil {
		h.OnCloseHandler(socket, err)
	}
}

func (h *WsClientHandler) OnPing(socket *gws.Conn, payload []byte) {
	if h.OnPingHandler != nil {
		h.OnPingHandler(socket, payload)
	}
}

func (h *WsClientHandler) OnPong(socket *gws.Conn, payload []byte) {
	if h.OnPongHandler != nil {
		h.OnPongHandler(socket, payload)
	}
}

func (h *WsClientHandler) OnMessage(socket *gws.Conn, message *gws.Message) {
	if h.OnMessageHandler != nil {
		h.OnMessageHandler(socket, message)
	}
}
