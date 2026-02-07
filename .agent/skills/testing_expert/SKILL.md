---
name: Testing Expert
description: Unit, integration, and e2e testing patterns with mocking strategies
---

# Testing Expert Skill

## Testing Pyramid

```
    /\
   /E2E\      Few, slow, expensive
  /------\
 / Integ  \   Medium
/----------\
 Unit Tests   Many, fast, cheap
```

## Unit Testing Patterns

### AAA Pattern
```javascript
describe('Calculator', () => {
  test('adds two numbers', () => {
    // Arrange
    const calc = new Calculator();
    
    // Act
    const result = calc.add(2, 3);
    
    // Assert
    expect(result).toBe(5);
  });
});
```

### Good Test Characteristics
- **Fast**: < 100ms each
- **Isolated**: No external dependencies
- **Repeatable**: Same result every run
- **Self-validating**: Pass or fail, no interpretation

## Mocking

```javascript
// Mock function
const mockFn = jest.fn().mockReturnValue(42);

// Mock module
jest.mock('./api', () => ({
  fetchUser: jest.fn().mockResolvedValue({ id: 1, name: 'Test' })
}));

// Spy on existing method
const spy = jest.spyOn(console, 'log');
```

## Integration Testing

```javascript
describe('User API', () => {
  beforeAll(async () => {
    await db.connect();
    await db.seed();
  });

  afterAll(async () => {
    await db.cleanup();
    await db.disconnect();
  });

  test('creates user', async () => {
    const response = await request(app)
      .post('/users')
      .send({ name: 'Test', email: 'test@test.com' });
    
    expect(response.status).toBe(201);
    expect(response.body.id).toBeDefined();
  });
});
```

## E2E Testing (Playwright)

```javascript
test('user can login', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="email"]', 'user@test.com');
  await page.fill('[name="password"]', 'password');
  await page.click('button[type="submit"]');
  
  await expect(page).toHaveURL('/dashboard');
});
```

## Coverage Goals

| Metric | Target |
|--------|--------|
| Line coverage | 80% |
| Branch coverage | 75% |
| Critical paths | 100% |

## When to Apply
Use when writing tests, debugging test failures, or setting up test infrastructure.
