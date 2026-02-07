---
name: Rails
description: ActiveRecord, generators, conventions over configuration
---

# Rails Skill

## Generators

```bash
rails new myapp
rails generate model User name:string email:string
rails generate controller Users index show
rails generate scaffold Post title:string body:text
rails db:migrate
```

## ActiveRecord

```ruby
# Create
User.create(name: 'John', email: 'john@example.com')

# Read
User.all
User.find(1)
User.where(active: true)
User.find_by(email: 'test@test.com')

# Update
user.update(name: 'Jane')

# Delete
user.destroy
```

## Associations

```ruby
class User < ApplicationRecord
  has_many :posts
  has_one :profile
  belongs_to :company
  has_many :comments, through: :posts
end
```

## Validations

```ruby
class User < ApplicationRecord
  validates :name, presence: true
  validates :email, presence: true, uniqueness: true
  validates :age, numericality: { greater_than: 0 }
end
```

## Conventions

| Convention | Example |
|------------|---------|
| Model | Singular, CamelCase (User) |
| Table | Plural, snake_case (users) |
| Controller | Plural (UsersController) |
| View folder | Plural (app/views/users/) |

## When to Apply
Use when building Ruby on Rails applications or following Rails conventions.
</Parameter>
<parameter name="Complexity">2
