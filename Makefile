BINARY_NAME=goose
OUTPUT_DIR=./bin

build-goose:
	@mkdir -p $(OUTPUT_DIR)
	go build -o $(OUTPUT_DIR)/$(BINARY_NAME) cmd/goose/main.go
goose:
	@go run cmd/goose/main.go $(cmd)
