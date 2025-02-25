package broadcastchan

import (
	"api-go/pkg/utilerror"
	"api-go/pkg/utillog"
	"errors"
	"time"
)

type Receiver[Data any] struct {
	QuitChan chan struct{}
	DataChan chan Data
}

type BroadcastGroup[Data any] struct {
	GroupInChan   chan Data
	GroupQuitChan chan struct{}
	Receivers     []*Receiver[Data]
}

func (broadcastGroup *BroadcastGroup[Data]) RunOnce(runFn func(), timeout time.Duration) error {
	go func() {
		runFn()
	}()

	select {
	case <-time.After(timeout):
		err := errors.New("broadcast group timeout")
		utilerror.LogError("BroadcastGroup.RunOnce\n", err)
		return err
	case <-broadcastGroup.GroupQuitChan:
		return nil
	}
}

func NewBroadcastGroup[Data any](inputDataChan chan Data, receivers []*Receiver[Data]) *BroadcastGroup[Data] {
	broadcastGroup :=
		BroadcastGroup[Data]{GroupInChan: inputDataChan, Receivers: receivers, GroupQuitChan: make(chan struct{})}
	for _, receiver := range receivers {
		receiver.QuitChan = broadcastGroup.GroupQuitChan
	}
	go func() {
		for {
			data, ok := <-inputDataChan
			if !ok {
				utillog.PrintfTiming("inputDataChan closed unexpectedly\n")
				break
			}
			utillog.PrintfTiming("inputDataChan received data %d\n", data)
			for _, receiver := range receivers {
				receiver.DataChan <- data
			}
		}
	}()

	return &broadcastGroup
}
