package resourcequeue

import (
	"context"
	"errors"
	"fmt"
	"sync"
	"time"
)

// ResourceConfig stores resource requirements for different job types
type ResourceConfig struct {
	// Map of job types to their resource unit requirements
	JobTypeUnits map[string]float64
}

// NewResourceConfig creates a new resource configuration
func NewResourceConfig() ResourceConfig {
	return ResourceConfig{
		JobTypeUnits: make(map[string]float64),
	}
}

// SetJobTypeUnits sets the resource requirement for a specific job type
func (rc *ResourceConfig) SetJobTypeUnits(jobType string, units float64) {
	rc.JobTypeUnits[jobType] = units
}

// GetJobTypeUnits retrieves the resource requirement for a job type
func (rc *ResourceConfig) GetJobTypeUnits(jobType string) (float64, bool) {
	units, exists := rc.JobTypeUnits[jobType]
	return units, exists
}

// Job represents a task to be processed in the queue
type Job struct {
	ID        string
	Type      string
	Data      interface{}
	Units     float64
	CreatedAt time.Time
	ResultCh  chan<- JobResult
}

// JobResult represents the result of processing a job
type JobResult struct {
	ID        string
	Output    interface{}
	Error     error
	StartTime time.Time
	EndTime   time.Time
}

// JobProcessor defines the function signature for processing jobs
// It receives the job and a result channel where it should send results
type JobProcessor func(ctx context.Context, job *Job, resultCh chan<- JobResult)

// ResourceQueue manages jobs with resource constraints
type ResourceQueue struct {
	config          ResourceConfig
	maxUnits        float64
	availableUnits  float64
	queue           []*Job
	running         map[string]*Job
	processorFunc   JobProcessor
	mu              sync.Mutex
	itemAddedSignal chan struct{}
	ctx             context.Context
	cancel          context.CancelFunc
	wg              sync.WaitGroup
}

// NewResourceQueue creates a new queue with the specified maximum resource units
func NewResourceQueue(maxUnits float64, config ResourceConfig, processorFunc JobProcessor) *ResourceQueue {
	ctx, cancel := context.WithCancel(context.Background())

	return &ResourceQueue{
		config:          config,
		maxUnits:        maxUnits,
		availableUnits:  maxUnits,
		queue:           make([]*Job, 0),
		running:         make(map[string]*Job),
		processorFunc:   processorFunc,
		itemAddedSignal: make(chan struct{}, 1),
		ctx:             ctx,
		cancel:          cancel,
	}
}

// Start begins processing queue jobs
func (q *ResourceQueue) Start() {
	// log.Printf("Starting resource queue with %.2f maximum units", q.maxUnits)
	q.wg.Add(1)
	go q.processQueue()
}

// Stop gracefully shuts down the queue
func (q *ResourceQueue) Stop() {
	// log.Println("Stopping resource queue")
	q.cancel()
	q.wg.Wait()
	// log.Println("Resource queue stopped")
}

// Enqueue adds a new job to the queue
func (q *ResourceQueue) Enqueue(id, jobType string, data interface{}) (<-chan JobResult, error) {
	q.mu.Lock()
	defer q.mu.Unlock()

	// Get required units for the job type
	units, ok := q.config.JobTypeUnits[jobType]
	if !ok {
		return nil, fmt.Errorf("unknown job type: %s", jobType)
	}

	// Check if job requires more than max units
	if units > q.maxUnits {
		return nil, fmt.Errorf("job requires %.2f units, which exceeds maximum capacity of %.2f", units, q.maxUnits)
	}

	// Create result channel
	resultChan := make(chan JobResult, 1)

	// Create and add queue job
	job := &Job{
		ID:        id,
		Type:      jobType,
		Data:      data,
		Units:     units,
		CreatedAt: time.Now(),
		ResultCh:  resultChan,
	}

	q.queue = append(q.queue, job)
	// log.Printf("Enqueued job %s (Type: %s, Units: %.2f)", id, jobType, units)

	// Signal that a new job was added
	select {
	case q.itemAddedSignal <- struct{}{}:
	default:
		// Channel already has a signal, no need to send another
	}

	return resultChan, nil
}

// GetQueueStatus returns the current queue status
func (q *ResourceQueue) GetQueueStatus() QueueStatus {
	q.mu.Lock()
	defer q.mu.Unlock()

	running := make([]RunningJob, 0, len(q.running))
	for id, job := range q.running {
		running = append(running, RunningJob{
			ID:        id,
			Type:      job.Type,
			Units:     job.Units,
			StartTime: job.CreatedAt,
		})
	}

	pending := make([]PendingJob, 0, len(q.queue))
	for _, job := range q.queue {
		pending = append(pending, PendingJob{
			ID:        job.ID,
			Type:      job.Type,
			Units:     job.Units,
			CreatedAt: job.CreatedAt,
		})
	}

	return QueueStatus{
		MaxUnits:       q.maxUnits,
		AvailableUnits: q.availableUnits,
		RunningJobs:    running,
		PendingJobs:    pending,
		QueueLength:    len(q.queue),
	}
}

// QueueStatus represents the current state of the queue
type QueueStatus struct {
	MaxUnits       float64      `json:"maxUnits"`
	AvailableUnits float64      `json:"availableUnits"`
	RunningJobs    []RunningJob `json:"runningJobs"`
	PendingJobs    []PendingJob `json:"pendingJobs"`
	QueueLength    int          `json:"queueLength"`
}

// RunningJob represents a job currently being processed
type RunningJob struct {
	ID        string    `json:"id"`
	Type      string    `json:"type"`
	Units     float64   `json:"units"`
	StartTime time.Time `json:"startTime"`
}

// PendingJob represents a job waiting in the queue
type PendingJob struct {
	ID        string    `json:"id"`
	Type      string    `json:"type"`
	Units     float64   `json:"units"`
	CreatedAt time.Time `json:"createdAt"`
}

// processQueue handles the queue processing loop
func (q *ResourceQueue) processQueue() {
	defer q.wg.Done()

	for {
		select {
		case <-q.ctx.Done():
			return
		case <-q.itemAddedSignal:
			q.tryProcessNextJobs()
		}
	}
}

// tryProcessNextJobs attempts to process as many queued jobs as possible
func (q *ResourceQueue) tryProcessNextJobs() {
	q.mu.Lock()

	// Try to process jobs until we can't process any more
	processed := true
	for processed {
		processed = false

		// Look for a job that can be processed with available resources
		for i, job := range q.queue {
			if job.Units <= q.availableUnits {
				// Remove job from queue
				q.queue = append(q.queue[:i], q.queue[i+1:]...)

				// Add to running list and update available units
				q.running[job.ID] = job
				q.availableUnits -= job.Units

				// log.Printf("Starting to process job %s (Type: %s, Units: %.2f, Available: %.2f)",
				// 			job.ID, job.Type, job.Units, q.availableUnits)

				// Process this job (in a separate goroutine)
				q.wg.Add(1)
				go q.processJob(job)

				processed = true
				break
			}
		}
	}

	q.mu.Unlock()
}

// processJob handles the processing of a single queue job
func (q *ResourceQueue) processJob(job *Job) {
	defer q.wg.Done()

	// Create a context for this job that will be cancelled if the queue is stopped
	jobCtx, cancel := context.WithCancel(q.ctx)
	defer cancel()

	// Create a channel to receive job results
	resultCh := make(chan JobResult, 1)

	// Start processing with the processor function in its own goroutine
	startTime := time.Now()
	go q.processorFunc(jobCtx, job, resultCh)

	// Wait for either result, context cancellation, or timeout
	var result JobResult
	select {
	case result = <-resultCh:
		// Received result from processor function
	case <-jobCtx.Done():
		// Context was cancelled
		result = JobResult{
			ID:        job.ID,
			Error:     errors.New("job cancelled due to queue shutdown"),
			StartTime: startTime,
			EndTime:   time.Now(),
		}
	}

	// If no end time was set, set it now
	if result.EndTime.IsZero() {
		result.EndTime = time.Now()
	}

	// Forward the result to the original client
	select {
	case job.ResultCh <- result:
	default:
		// log.Printf("Warning: Could not send result for job %s (receiver may have timed out)", job.ID)
	}

	// Clean up and update available resources
	q.mu.Lock()
	delete(q.running, job.ID)
	q.availableUnits += job.Units
	// log.Printf("Finished processing job %s (Units released: %.2f, Available: %.2f)",
	// 		job.ID, job.Units, q.availableUnits)
	q.mu.Unlock()

	// Signal that resources are now available
	select {
	case q.itemAddedSignal <- struct{}{}:
	default:
		// Channel already has a signal, no need to send another
	}
}

// CancelJob removes a job from the queue if it hasn't started processing
func (q *ResourceQueue) CancelJob(id string) bool {
	q.mu.Lock()
	defer q.mu.Unlock()

	// Check if the job is in the queue
	for i, job := range q.queue {
		if job.ID == id {
			// Remove the job
			q.queue = append(q.queue[:i], q.queue[i+1:]...)

			// Send cancellation notification
			job.ResultCh <- JobResult{
				ID:        id,
				Error:     errors.New("job cancelled"),
				StartTime: time.Now(),
				EndTime:   time.Now(),
			}

			// log.Printf("Cancelled queued job %s", id)
			return true
		}
	}

	// Job not found in queue (might be running or already completed)
	return false
}
