# Module 4 Homework - Question 2

## Question: dbt Tests

You've configured a generic test like this in your `schema.yml`:

```yaml
columns:
  - name: payment_type
    data_tests:
      - accepted_values:
          arguments:
            values: [1, 2, 3, 4, 5]
```

Your model `fct_trips` has been running successfully for months. A new value `6` now appears in the source data.

### What happens when you run `dbt test --select fct_trips`?

**Options:**
- A) dbt will skip the test because the model didn't change
- B) dbt will fail the test, returning a non-zero exit code
- C) dbt will pass the test with a warning about the new value
- D) dbt will update the configuration to include the new value

---

### Answer: B

**Reasoning:**
- The `accepted_values` generic test ensures only specified values are allowed in the column
- When value `6` appears (not in `[1, 2, 3, 4, 5]`), the test will **FAIL**
- dbt returns a **non-zero exit code** on test failure (important for CI/CD pipelines)
- dbt will report which rows contain the invalid value(s)
- This is the intended behavior - data quality tests should alert you when unexpected data appears

