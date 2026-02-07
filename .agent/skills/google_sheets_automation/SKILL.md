---
name: Google Sheets Automation
description: Advanced formulas, Apps Script, and integrations
---

# Google Sheets Automation Skill

## Power Formulas

### QUERY (SQL for Sheets)
```
=QUERY(A1:D100, "SELECT A, B WHERE C > 100 ORDER BY D DESC", 1)
```

### IMPORTRANGE (Pull from other sheets)
```
=IMPORTRANGE("spreadsheet_url", "Sheet1!A1:C100")
```

### ARRAYFORMULA (Apply to all rows)
```
=ARRAYFORMULA(IF(A2:A<>"", A2:A*B2:B, ""))
```

### INDEX/MATCH (Better than VLOOKUP)
```
=INDEX(B:B, MATCH(lookup_value, A:A, 0))
```

### REGEXEXTRACT
```
=REGEXEXTRACT(A1, "\d{3}-\d{3}-\d{4}")  -- Phone number
=REGEXEXTRACT(A1, "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")  -- Email
```

## Apps Script Basics

```javascript
function sendEmails() {
  const sheet = SpreadsheetApp.getActiveSheet();
  const data = sheet.getDataRange().getValues();
  
  for (let i = 1; i < data.length; i++) {
    const email = data[i][0];
    const name = data[i][1];
    
    MailApp.sendEmail({
      to: email,
      subject: 'Hello!',
      body: `Hi ${name}, ...`
    });
  }
}
```

## Triggers

```javascript
// Time-based trigger (daily)
function createTrigger() {
  ScriptApp.newTrigger('myFunction')
    .timeBased()
    .everyDays(1)
    .atHour(9)
    .create();
}

// On edit trigger
function onEdit(e) {
  const range = e.range;
  // Do something when cell edited
}
```

## API Integration

```javascript
function fetchData() {
  const response = UrlFetchApp.fetch('https://api.example.com/data');
  const json = JSON.parse(response.getContentText());
  
  const sheet = SpreadsheetApp.getActiveSheet();
  json.forEach((item, i) => {
    sheet.getRange(i + 1, 1).setValue(item.name);
  });
}
```

## When to Apply
Use when automating spreadsheets, building dashboards, or integrating with APIs.
