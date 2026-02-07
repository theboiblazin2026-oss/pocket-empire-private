---
name: Flutter
description: Dart language, widgets, state management, hot reload
---

# Flutter Skill

## Widgets

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text('My App')),
        body: Center(
          child: Text('Hello, Flutter!'),
        ),
      ),
    );
  }
}
```

## StatefulWidget

```dart
class Counter extends StatefulWidget {
  @override
  _CounterState createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;

  void _increment() {
    setState(() {
      _count++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $_count'),
        ElevatedButton(onPressed: _increment, child: Text('+')),
      ],
    );
  }
}
```

## Common Widgets

| Widget | Purpose |
|--------|---------|
| Container | Box with padding, margin, decoration |
| Row/Column | Horizontal/vertical layout |
| ListView | Scrollable list |
| Stack | Overlapping widgets |
| Expanded | Fill available space |

## Commands

```bash
flutter create myapp
flutter run
flutter build apk
flutter build ios
```

## When to Apply
Use when building beautiful cross-platform apps with Flutter.
