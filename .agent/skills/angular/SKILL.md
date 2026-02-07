---
name: Angular
description: TypeScript-first, RxJS, modules, dependency injection
---

# Angular Skill

## Component

```typescript
@Component({
  selector: 'app-user',
  template: `
    <h1>{{ user.name }}</h1>
    <button (click)="onClick()">Click</button>
  `,
})
export class UserComponent {
  @Input() user!: User;
  @Output() selected = new EventEmitter<User>();

  onClick() {
    this.selected.emit(this.user);
  }
}
```

## Services & DI

```typescript
@Injectable({ providedIn: 'root' })
export class UserService {
  constructor(private http: HttpClient) {}

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>('/api/users');
  }
}

// In component
constructor(private userService: UserService) {}
```

## RxJS Basics

```typescript
this.userService.getUsers().pipe(
  map(users => users.filter(u => u.active)),
  catchError(err => {
    console.error(err);
    return of([]);
  })
).subscribe(users => this.users = users);
```

## Routing

```typescript
const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'users', component: UsersComponent },
  { path: 'users/:id', component: UserDetailComponent },
];
```

## When to Apply
Use when building Angular applications or working with enterprise TypeScript projects.
