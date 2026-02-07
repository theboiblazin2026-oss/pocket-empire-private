---
name: Go
description: Goroutines, channels, interfaces, and simple error handling
---

# Go Skill

## Goroutines & Channels

```go
// Start goroutine
go myFunction()

// Channels
ch := make(chan string)

go func() {
    ch <- "message"
}()

msg := <-ch  // Receive
```

## Error Handling

```go
func readFile(name string) (string, error) {
    data, err := os.ReadFile(name)
    if err != nil {
        return "", fmt.Errorf("reading %s: %w", name, err)
    }
    return string(data), nil
}

// Usage
content, err := readFile("test.txt")
if err != nil {
    log.Fatal(err)
}
```

## Interfaces

```go
type Writer interface {
    Write([]byte) (int, error)
}

// Any type implementing Write() satisfies Writer
type MyWriter struct{}

func (w MyWriter) Write(data []byte) (int, error) {
    return len(data), nil
}
```

## Common Patterns

```go
// HTTP Server
http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
    fmt.Fprintf(w, "Hello!")
})
http.ListenAndServe(":8080", nil)

// JSON
json.Marshal(data)
json.Unmarshal(bytes, &data)
```

## Commands

```bash
go mod init myproject
go run main.go
go build
go test ./...
```

## When to Apply
Use when writing Go backends, CLIs, or concurrent applications.
