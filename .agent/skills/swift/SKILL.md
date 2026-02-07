---
name: Swift
description: SwiftUI, protocols, optionals, and iOS frameworks
---

# Swift Skill

## SwiftUI Basics

```swift
struct ContentView: View {
    @State private var count = 0
    
    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") {
                count += 1
            }
        }
    }
}
```

## Optionals

```swift
var name: String? = nil

// Safe unwrap
if let n = name {
    print(n)
}

// Guard
guard let n = name else { return }

// Nil coalescing
let displayName = name ?? "Anonymous"
```

## Protocols

```swift
protocol Drawable {
    func draw()
}

struct Circle: Drawable {
    func draw() {
        print("Drawing circle")
    }
}
```

## Common Patterns

```swift
// Async/await
func fetchData() async throws -> Data {
    let (data, _) = try await URLSession.shared.data(from: url)
    return data
}

// Codable
struct User: Codable {
    let name: String
    let email: String
}
```

## When to Apply
Use when building iOS/macOS apps with Swift and SwiftUI.
