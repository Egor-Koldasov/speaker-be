package e2etest_test

import (
	"api-go/pkg/utilerror"
	"api-go/pkg/utillog"
	"api-go/test/e2eutil"
	"testing"

	"github.com/lxzan/gws"
)

func TestWsHealth(t *testing.T) {
	wsConnected := false
	messageChannel := make(chan struct{})
	messageReceived := false
	var runner = e2eutil.WsClientRunner{
		Run: func(conn *gws.Conn) {
			utillog.PrintfTiming("Runner connected to WebSocket server\n")
			wsConnected = true
			conn.WriteMessage(gws.OpcodeText, []byte("Hello, WebSocket server!"))

			<-messageChannel
			messageReceived = true
			conn.WriteClose(1000, nil)
		},
		// OnMessage: func(message *gws.Message) {
		// 	utillog.PrintfTiming("Runner received message\n")
		// 	close(messageChannel)
		// },
	}
	utillog.PrintfTiming("Test output 1\n")
	err := e2eutil.NewWsClient(t, &runner)
	utillog.PrintfTiming("Test output 2\n")
	utilerror.FatalError("Failed to create WebSocket client: %v\n", err)

	if !wsConnected {
		t.Errorf("WebSocket client failed to connect to server\n")
	}
	if !messageReceived {
		t.Errorf("WebSocket client failed to receive message from server\n")
	}
}
