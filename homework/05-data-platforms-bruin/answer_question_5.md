# Question 5: Quality Checks

## Task Explanation

Data quality checks are important to ensure data integrity. This question asks which check to use for ensuring a column has no NULL values.

## Query Function

**Column Definition:**
```yaml
columns:
  - name: pickup_datetime
    type: timestamp
    primary_key: true
    checks:
      - name: not_null
```

**Breakdown:**
1. **`name: pickup_datetime`**: Column name
2. **`type: timestamp`**: Data type
3. **`checks`**: Array of quality checks
4. **`name: not_null`**: Check to ensure no NULL values

## Multiple Choice Options

- `name: unique`
- `name: not_null`
- `name: positive`
- `name: accepted_values, value: [not_null]`

## Answer

**`name: not_null`**

## Reason

- `not_null` is the built-in check to ensure column has no NULL values
- `unique` ensures all values are unique
- `positive` ensures values are > 0
- `accepted_values` ensures values are in a specific list

**Built-in Checks:**

| Check | Description | Example Use |
|-------|-------------|-------------|
| `not_null` | Cannot be NULL | Primary keys, required fields |
| `unique` | Must be unique | ID, email |
| `positive` | Must be > 0 | Amount, count |
| `non_negative` | Must be >= 0 | Quantity, duration |
| `accepted_values` | Must be in list | Status, category |
