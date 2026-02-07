---
name: PHP
description: Laravel, Composer, WordPress internals, legacy patterns
---

# PHP Skill

## Laravel Basics

```php
// Routes
Route::get('/users', [UserController::class, 'index']);
Route::post('/users', [UserController::class, 'store']);

// Controller
class UserController extends Controller
{
    public function index()
    {
        return User::all();
    }
    
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string',
            'email' => 'required|email|unique:users',
        ]);
        
        return User::create($validated);
    }
}
```

## Eloquent ORM

```php
// Find
$user = User::find(1);
$user = User::where('email', $email)->first();

// Create
User::create(['name' => 'John', 'email' => 'john@example.com']);

// Relationships
class User extends Model
{
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}
```

## Composer

```bash
composer require laravel/framework
composer install
composer update
composer dump-autoload
```

## When to Apply
Use when working with PHP, Laravel, or WordPress backends.
