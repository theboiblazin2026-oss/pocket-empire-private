---
name: Firebase Master
description: Authentication, Firestore, Cloud Functions, and Hosting
---

# Firebase Master Skill

## Authentication

```javascript
// Email/Password signup
import { createUserWithEmailAndPassword } from 'firebase/auth';
await createUserWithEmailAndPassword(auth, email, password);

// Google Sign-In
import { signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
const provider = new GoogleAuthProvider();
await signInWithPopup(auth, provider);

// Auth state listener
onAuthStateChanged(auth, (user) => {
  if (user) console.log('Logged in:', user.uid);
});
```

## Firestore

```javascript
// Add document
await addDoc(collection(db, 'users'), { name: 'John', age: 30 });

// Get document
const snap = await getDoc(doc(db, 'users', 'userId'));

// Query
const q = query(
  collection(db, 'posts'),
  where('author', '==', 'userId'),
  orderBy('createdAt', 'desc'),
  limit(10)
);
const docs = await getDocs(q);

// Real-time listener
onSnapshot(doc(db, 'users', 'userId'), (doc) => {
  console.log('Updated:', doc.data());
});
```

## Security Rules

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can only read/write their own data
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
    
    // Public read, authenticated write
    match /posts/{postId} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

## Cloud Functions

```javascript
const functions = require('firebase-functions');

exports.onUserCreate = functions.auth.user().onCreate((user) => {
  // New user signed up
  console.log('New user:', user.uid);
});

exports.api = functions.https.onRequest((req, res) => {
  res.json({ message: 'Hello!' });
});
```

## Hosting

```bash
firebase init hosting
firebase deploy --only hosting
```

## When to Apply
Use when building Firebase apps, writing security rules, or deploying functions.
