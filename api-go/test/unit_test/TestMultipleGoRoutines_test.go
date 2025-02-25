package unittest_test

import (
	"api-go/pkg/broadcastchan"
	"api-go/pkg/utilerror"
	"api-go/pkg/utillog"
	"sync"
	"testing"
	"time"
)

func TestMultipleGoRoutines(t *testing.T) {
	receivers := []*broadcastchan.Receiver[int16]{}
	receiverCount := 3
	for range receiverCount {
		receivers = append(receivers, &broadcastchan.Receiver[int16]{
			DataChan: make(chan int16),
			QuitChan: make(chan struct{}),
		})
	}
	var expectedData [][]int16 = make([][]int16, receiverCount)
	broadcastGroup := broadcastchan.NewBroadcastGroup(make(chan int16), receivers)
	waitGroup := sync.WaitGroup{}
	for i, receiver := range broadcastGroup.Receivers {
		waitGroup.Add(3)
		go func() {
			for {
				select {
				case <-receiver.QuitChan:
					return
				case data, ok := <-receiver.DataChan:
					if !ok {
						break
					}
					utillog.PrintfTiming("Receiver %d received data: %d\n", i, data)
					expectedData[i] = append(expectedData[i], data)
					waitGroup.Done()
				}
			}
		}()
	}

	go func() {
		err := broadcastGroup.RunOnce(func() {
			broadcastGroup.GroupInChan <- 1
			broadcastGroup.GroupInChan <- 2
			broadcastGroup.GroupInChan <- 3
		}, 100*time.Millisecond)
		utilerror.FatalError("broascastGroup.RunOnce\n", err)
	}()

	waitGroup.Wait()

	if len(expectedData) != receiverCount {
		t.Errorf("Expected %d receivers, got %d\n", receiverCount, len(expectedData))
	}
	for i, expectedItem := range expectedData {
		if len(expectedItem) != 3 {
			t.Errorf("Expected 3 data items for receiver %d, got %d\n", i, len(expectedItem))
			t.Errorf("expectedData: %v\n", expectedData)
		}
	}

	// go func() {
	// 	broadcastGroup.GroupInChan <- 1
	// 	broadcastGroup.GroupInChan <- 2
	// 	broadcastGroup.GroupInChan <- 3
	// 	defer close(broadcastGroup.GroupQuitChan)
	// }()

	// select {
	// case <-time.After(3 * time.Second):
	// 	utillog.PrintfTiming("Timeout\n")
	// 	return
	// case <-broadcastGroup.GroupQuitChan:
	// 	t.Logf("Broadcast group quit\n")
	// }

}
