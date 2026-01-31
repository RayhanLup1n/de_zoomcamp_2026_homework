# Question 6: Schedule Trigger Timezone

### Question
How would you configure the timezone to New York in a Schedule trigger?
- Add a `timezone` property set to `EST` in the `Schedule` trigger configuration
- **Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration**
- Add a `timezone` property set to `UTC-5` in the `Schedule` trigger configuration
- Add a `location` property set to `New_York` in the `Schedule` trigger configuration

### Methodology
Based on Kestra's documentation for the `io.kestra.plugin.core.trigger.Schedule` plugin, the `timezone` property accepts a valid IANA timezone identifier. Adding `timezone: America/New_York` ensures that the schedule follows the local time in New York, including adjustments for Daylight Saving Time (DST).

### Answer
The correct configuration is to add a **`timezone` property set to `America/New_York`**.
