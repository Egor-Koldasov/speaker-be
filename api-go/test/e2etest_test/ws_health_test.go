package e2etest_test

import (
	"api-go/pkg/utilerror"
	"api-go/test/e2eutil"
	"testing"
	"time"

	"github.com/lxzan/gws"
)

func TestWsHealth(t *testing.T) {
	wsConnected := false
	messageReceived := false
	var handler gws.Event = &e2eutil.WsClientHandler{
		OnOpenHandler: func(socket *gws.Conn) {
			wsConnected = true
		},
		OnMessageHandler: func(socket *gws.Conn, message *gws.Message) {
			t.Logf("WebSocket client received message: %s\n", string(message.Bytes()))
			messageReceived = true
		},
	}
	wsClient, err := e2eutil.WsClient(&handler)
	utilerror.FatalError("Failed to create WebSocket client: %v\n", err)
	done := make(chan struct{})
	go func() {
		wsClient.ReadLoop()
		close(done)
	}()

	wsClient.WriteMessage(gws.OpcodeText, []byte("Hello, WebSocket server!"))

	select {
	case <-done:
		t.Logf("WebSocket client read loop completed\n")
	case <-time.After(1 * time.Second):
		wsClient.NetConn().Close()
	}
	if !wsConnected {
		t.Errorf("WebSocket client failed to connect to server\n")
	}
	if !messageReceived {
		t.Errorf("WebSocket client failed to receive message from server\n")
	}
}
