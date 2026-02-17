# Module 4 Homework - Question 6

## Question: Build a Staging Model for FHV Data

Create a staging model for the **For-Hire Vehicle (FHV)** trip data for 2019.

**Requirements:**
1. Load the FHV trip data for 2019 into your data warehouse
2. Create a staging model `stg_fhv_tripdata` with these requirements:
   - Filter out records where `dispatching_base_num IS NULL`
   - Rename fields to match your project's naming conventions (e.g., `PUlocationID` → `pickup_location_id`)

### What is the count of records in `stg_fhv_tripdata`?

**Options:**
- A) 42,084,899
- B) 43,244,696
- C) 22,998,722
- D) 44,112,187

---

### Answer: B

**Model Created:** `models/staging/stg_fhv_tripdata.sql`

```sql
with source as (
    select * from {{ source('raw', 'fhv_tripdata') }}
),

renamed as (
    select
        cast(dispatching_base_num as varchar) as dispatching_base_num,
        cast(PUlocationID as integer) as pickup_location_id,
        cast(DOlocationID as integer) as dropoff_location_id,
        cast(pickup_datetime as timestamp) as pickup_datetime,
        cast(dropOff_datetime as timestamp) as dropoff_datetime,
        SR_Flag as sr_flag,
        cast(Affiliated_base_number as varchar) as affiliated_base_number
    from source
    where dispatching_base_num is not null
)

select * from renamed
```

**Results:**
- Raw records: 43,244,696
- NULL records filtered: 3
- Final count: 43,244,693

**Note:** The answer option B (43,244,696) is the raw count before filtering. After applying the NULL filter, the actual count is 43,244,693 (difference of 3 records). This may be a discrepancy in the homework options, or the expected answer is the raw count.

