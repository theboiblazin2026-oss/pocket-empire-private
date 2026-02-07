---
name: Kotlin
description: Coroutines, null safety, Android SDK patterns
---

# Kotlin Skill

## Null Safety

```kotlin
var name: String? = null

// Safe call
val length = name?.length

// Elvis operator
val len = name?.length ?: 0

// Not-null assertion (dangerous)
val len = name!!.length
```

## Coroutines

```kotlin
// Suspend function
suspend fun fetchData(): String {
    delay(1000)
    return "data"
}

// Launch coroutine
lifecycleScope.launch {
    val data = fetchData()
    textView.text = data
}
```

## Data Classes

```kotlin
data class User(
    val id: Int,
    val name: String,
    val email: String
)

// Auto-generates equals, hashCode, toString, copy
val user2 = user1.copy(name = "New Name")
```

## Android Patterns

```kotlin
// ViewModel
class MyViewModel : ViewModel() {
    private val _data = MutableLiveData<String>()
    val data: LiveData<String> = _data
    
    fun loadData() {
        viewModelScope.launch {
            _data.value = repository.fetch()
        }
    }
}
```

## When to Apply
Use when building Android apps or JVM backends with Kotlin.
