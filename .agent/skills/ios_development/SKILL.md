---
name: iOS Development
description: SwiftUI, UIKit, App Store submission, Xcode debugging
---

# iOS Development Skill

## SwiftUI App Structure

```swift
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

## State Management

```swift
@State private var count = 0           // Local state
@Binding var value: String             // Parent-owned
@ObservedObject var viewModel: VM      // Observable class
@EnvironmentObject var store: Store    // Global state
```

## Navigation

```swift
NavigationStack {
    List(items) { item in
        NavigationLink(item.name, value: item)
    }
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
}
```

## App Store Checklist

- [ ] App icons (all sizes)
- [ ] Launch screen
- [ ] Screenshots for all devices
- [ ] Privacy policy URL
- [ ] App Store description
- [ ] Keywords
- [ ] Build uploaded via Xcode
- [ ] TestFlight testing done

## When to Apply
Use when building native iOS applications or submitting to App Store.
