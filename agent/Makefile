build:
	@go build -o ./bin/rtsa ./main.go
	@chmod +x ./bin/rtsa

clean:
	@rm -rf ./bin

run: build
	@./bin/rtsa

test:
	@go test -coverprofile=agent_test_coverage.out ./...

coverage: test
	@go tool cover -html=agent_test_coverage.out