---
name: Android Development
description: Jetpack Compose, Activities, Firebase integration
---

# Android Development Skill

## Jetpack Compose

```kotlin
@Composable
fun Greeting(name: String) {
    Column(modifier = Modifier.padding(16.dp)) {
        Text(text = "Hello, $name!", style = MaterialTheme.typography.h4)
        Button(onClick = { /* action */ }) {
            Text("Click me")
        }
    }
}
```

## State in Compose

```kotlin
@Composable
fun Counter() {
    var count by remember { mutableStateOf(0) }
    
    Button(onClick = { count++ }) {
        Text("Count: $count")
    }
}
```

## Navigation

```kotlin
val navController = rememberNavController()

NavHost(navController = navController, startDestination = "home") {
    composable("home") { HomeScreen(navController) }
    composable("details/{id}") { backStackEntry ->
        DetailsScreen(backStackEntry.arguments?.getString("id"))
    }
}

// Navigate
navController.navigate("details/123")
```

## Firebase Setup

```kotlin
// Authentication
Firebase.auth.signInWithEmailAndPassword(email, password)
    .addOnSuccessListener { user -> }
    .addOnFailureListener { e -> }

// Firestore
Firebase.firestore.collection("users")
    .document(userId)
    .get()
    .addOnSuccessListener { doc -> }
```

## When to Apply
Use when building native Android applications with Kotlin.
