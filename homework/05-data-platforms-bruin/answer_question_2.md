# Question 2: Materialization Strategies

## Task Explanation

NYC taxi data is organized by `pickup_datetime`. This question asks which materialization strategy is best for incremental processing with delete+insert per time period.

## Query Function

**Materialization Configuration:**
```yaml
materialization:
  type: table
  strategy: time_interval
  incremental_key: pickup_datetime
```

**Breakdown:**
1. **`type: table`**: Store result as a table (not a view)
2. **`strategy: time_interval`**: Incremental processing based on time range
3. **`incremental_key: pickup_datetime`**: Column used to determine time window

## Multiple Choice Options

- `append` - always add new rows
- `replace` - truncate and rebuild entirely
- `time_interval` - incremental based on a time column
- `view` - create a virtual table only

## Answer

**`time_interval` - incremental based on a time column**

## Reason

- `time_interval` is designed specifically for time-series data
- This strategy will delete data within the processed time range, then insert new data
- Perfect for NYC taxi data organized by `pickup_datetime`
- Avoids duplication for reruns on the same date

**Strategy Comparison:**

| Strategy | Behavior | Use Case |
|----------|----------|----------|
| `append` | Always add new rows | Log data, never delete |
| `replace` | Truncate + rebuild entire table | Full refresh |
| `time_interval` | Delete + insert per time window | Time-series data |
| `view` | Virtual table only | Aggregation layer |
