---
name: Ruby
description: Rails conventions, gems, metaprogramming, testing
---

# Ruby Skill

## Rails Basics

```ruby
# Routes
Rails.application.routes.draw do
  resources :users
  get '/about', to: 'pages#about'
end

# Controller
class UsersController < ApplicationController
  def index
    @users = User.all
  end
  
  def create
    @user = User.new(user_params)
    if @user.save
      redirect_to @user
    else
      render :new
    end
  end
  
  private
  
  def user_params
    params.require(:user).permit(:name, :email)
  end
end
```

## ActiveRecord

```ruby
# Find
User.find(1)
User.where(status: 'active')
User.find_by(email: 'test@test.com')

# Scopes
class User < ApplicationRecord
  scope :active, -> { where(active: true) }
  scope :recent, -> { order(created_at: :desc).limit(10) }
end
```

## Ruby Idioms

```ruby
# Blocks
[1, 2, 3].map { |n| n * 2 }

# Symbols
:symbol_name

# Hash rocket vs symbol keys
{ :name => 'John' }  # old
{ name: 'John' }     # new
```

## When to Apply
Use when working with Ruby or Rails applications.
