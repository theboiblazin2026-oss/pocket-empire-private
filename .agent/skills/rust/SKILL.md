---
name: Rust
description: Memory safety, ownership model, concurrency, and Cargo ecosystem
---

# Rust Skill

## Ownership Rules

1. Each value has one owner
2. Only one owner at a time
3. Value dropped when owner goes out of scope

```rust
let s1 = String::from("hello");
let s2 = s1;  // s1 is MOVED, no longer valid
// println!("{}", s1);  // ERROR!
```

## Borrowing

```rust
fn main() {
    let s = String::from("hello");
    
    // Immutable borrow
    let len = calculate_length(&s);
    
    // Mutable borrow
    let mut s2 = String::from("hello");
    change(&mut s2);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn change(s: &mut String) {
    s.push_str(", world");
}
```

## Common Patterns

```rust
// Option handling
match some_value {
    Some(x) => println!("{}", x),
    None => println!("Nothing"),
}

// Result handling
let file = File::open("file.txt")?;

// Iterators
let sum: i32 = vec![1, 2, 3].iter().map(|x| x * 2).sum();
```

## Cargo Commands

```bash
cargo new my_project
cargo build
cargo run
cargo test
cargo build --release
```

## When to Apply
Use when writing Rust code, debugging ownership issues, or optimizing performance.
