## Question 2. Understanding Docker Networking and Docker Compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that **pgadmin** should use to connect to the **postgres** database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

### Options:
- `postgres:5433`
- `localhost:5432`
- `db:5433`
- `postgres:5432`
- `db:5432`

---

## ANSWER

The correct answers are **db:5432** or **postgres:5432**.

## REASON

When containers are in the same network created by Docker Compose, they communicate using:
1.  **Hostname**: Either the **service name** (`db`) or the **container name** (`postgres`).
2.  **Port**: The **internal port** of the service (`5432`), not the port mapped to the host machine (`5433`).

Since `pgadmin` and `db` are in the same default network, `pgadmin` can reach the database using `db:5432`. `localhost` would refer to the pgadmin container itself, and `5433` is only for access from outside Docker (your host machine).

## COMMAND

To verify and test this configuration:

1.  **Start the services**:
    ```bash
    docker-compose up -d
    ```
2.  **Access pgAdmin**:
    Open your browser and go to `http://localhost:8080`.
3.  **Login to pgAdmin**:
    - **Email**: `pgadmin@pgadmin.com`
    - **Password**: `pgadmin`
4.  **Register the Server**:
    - **Host name/address**: `db` (or `postgres`)
    - **Port**: `5432`
    - **Username**: `postgres`
    - **Password**: `postgres`