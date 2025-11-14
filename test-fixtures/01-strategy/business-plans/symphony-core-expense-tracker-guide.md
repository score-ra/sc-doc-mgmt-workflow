---
title: Symphony Core Expense Tracker Guide
tags: [finance, tools]
status: active
---

# Symphony Core Expense Tracker Guide

## How to Track Expenses

Use the following format in your CSV file:

```csv
Date,Description,Amount,Category
2025-01-15,Office Supplies,$45.00,Operations
2025-01-16,AWS Hosting,$120.00,Infrastructure
```

## Data Import

Import your expense data using this command:

```bash
import-expenses --file expenses.csv --validate
```

## Report Generation

Generate monthly reports:

```bash
generate-report --month 2025-01 --format pdf
```

## Reconciliation Process

Match transactions with this SQL query:

```sql
SELECT * FROM expenses
WHERE category = 'Operations'
AND amount > 100
```
