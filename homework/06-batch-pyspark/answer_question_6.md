# Question 6

## Task Explanation

Find the name of the **least frequent** pickup location zone. Need to join (combine) Yellow taxi data with Taxi Zone Lookup data.

### Query Function

**Query (SQL):**
```sql
SELECT z.Zone, COUNT(*) as trip_count
FROM yellow y
JOIN zones z ON y.PULocationID = z.LocationID
GROUP BY z.Zone
ORDER BY trip_count ASC
LIMIT 1;
```

**Query (Python):**
```python
# Load zones
df_zones = spark.read \
    .option("header", "true") \
    .csv("taxi_zone_lookup.csv")

df_zones.createOrReplaceTempView("zones")
df_yellow.createOrReplaceTempView("yellow")

result = spark.sql("""
    SELECT z.Zone, COUNT(*) as trip_count
    FROM yellow y
    JOIN zones z ON y.PULocationID = z.LocationID
    GROUP BY z.Zone
    ORDER BY trip_count ASC
    LIMIT 1
""")
```

**Breakdown:**
1.  **`JOIN`**: Combines two tables based on `LocationID`
2.  **`GROUP BY z.Zone`**: Groups by zone name
3.  **`COUNT(*)`**: Counts the number of trips per zone
4.  **`ORDER BY trip_count ASC`**: Sorts from smallest to largest
5.  **`LIMIT 1`**: Takes only the first row (least frequent)

**Multiple Choice Options:**
- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay

**Answer:** **Governor's Island/Ellis Island/Liberty Island**

**Reason:** This zone has only **1 trip** during November 2025, the least frequent of all zones.

**Top 5 Least Frequent Zones:**
| Zone | Trip Count |
|------|------------|
| Governor's Island/Ellis Island/Liberty Island | 1 |
| Eltingville/Annadale/Prince's Bay | 1 |
| Arden Heights | 1 |
| Port Richmond | 3 |
| Rikers Island | 4 |
