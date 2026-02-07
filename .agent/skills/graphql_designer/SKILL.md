---
name: GraphQL Designer
description: Schema design, resolvers, subscriptions, and best practices
---

# GraphQL Designer Skill

## Schema Design

```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  createdAt: DateTime!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  published: Boolean!
}

type Query {
  user(id: ID!): User
  users(limit: Int, offset: Int): [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

input CreateUserInput {
  name: String!
  email: String!
}
```

## Resolver Pattern

```javascript
const resolvers = {
  Query: {
    user: (_, { id }, context) => context.db.users.findById(id),
    users: (_, { limit, offset }, context) => 
      context.db.users.findAll({ limit, offset }),
  },
  Mutation: {
    createUser: (_, { input }, context) => 
      context.db.users.create(input),
  },
  User: {
    posts: (user, _, context) => 
      context.db.posts.findByAuthor(user.id),
  },
};
```

## N+1 Problem Solution

```javascript
// Use DataLoader
const userLoader = new DataLoader(async (ids) => {
  const users = await db.users.findByIds(ids);
  return ids.map(id => users.find(u => u.id === id));
});

// In resolver
author: (post, _, { loaders }) => loaders.user.load(post.authorId)
```

## Best Practices

| Practice | Why |
|----------|-----|
| Use `ID!` for identifiers | Explicit typing |
| Input types for mutations | Clean arguments |
| Pagination with cursors | Scalable |
| Error in response, not throw | Partial data possible |

## When to Apply
Use when designing GraphQL APIs, writing resolvers, or optimizing queries.
