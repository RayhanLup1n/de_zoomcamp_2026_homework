# Question 1

## Task Explanation

Determine the version of Redpanda running in the container by executing `rpk version` command inside the Redpanda container.

### Command

**Command:**
```bash
docker exec -it workshop-redpanda-1 rpk version
```

**Breakdown:**
1.  **`docker exec`**: Execute command inside a running container
2.  **`-it`**: Interactive mode with pseudo-TTY allocation
3.  **`workshop-redpanda-1`**: Container name (assumes workshop directory)
4.  **`rpk`**: Redpanda CLI tool
5.  **`version`**: Command to show version information

**Answer:** v25.3.9

**Reason:**
Based on the `docker-compose.yml` file from the workshop, the Redpanda image used is `redpandadata/redpanda:v25.3.9`. When running `rpk version` command inside this container, it will return the version v25.3.9.
