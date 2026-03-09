# **Setup**
## requirements
* docker - for pipeline sources testing

## steps
* run Kafka container
```
docker run -d --name kafka -p 9092:9092 -e KAFKA_PROCESS_ROLES=broker,controller -e KAFKA_NODE_ID=1 -e KAFKA_CONTROLLER_QUORUM_VOTERS=1@localhost:9093 -e KAFKA_LISTENERS=PLAINTEXT://0.0.0.0:9092,CONTROLLER://0.0.0.0:9093 -e KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://localhost:9092 -e KAFKA_CONTROLLER_LISTENER_NAMES=CONTROLLER -e KAFKA_INTER_BROKER_LISTENER_NAME=PLAINTEXT -e KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR=1 confluentinc/cp-kafka:latest
```

* run RabbitMQ container
```
docker run -d --hostname rabbitmq --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

* run postgresDB container
```
docker run -d --name postgres-test -e POSTGRES_USER=testuser -e POSTGRES_PASSWORD=testpass -e POSTGRES_DB=testdb -p 5432:5432 postgres:16
```
create a test table
```sql
-- example
CREATE TABLE "Course" (
    academic_term TEXT,
    code TEXT,
    course_id TEXT PRIMARY KEY,
    credits INTEGER,
    level TEXT,
    name TEXT,
    org_id TEXT
);
```
insert items
```sql
-- example
INSERT INTO "Course" (academic_term, code, course_id, credits, level, name, org_id) VALUES
('2025A', 'CS101', 'C-1001', 4, 'Undergraduate', 'Introduction to Computer Science', 'ORG-01'),
('2025A', 'CS102', 'C-1002', 3, 'Undergraduate', 'Data Structures', 'ORG-01'),
('2025B', 'CS201', 'C-2001', 4, 'Undergraduate', 'Algorithms', 'ORG-01'),
('2025B', 'CS301', 'C-3001', 3, 'Graduate', 'Distributed Systems', 'ORG-02'),
('2026A', 'CS401', 'C-4001', 3, 'Graduate', 'Machine Learning', 'ORG-02');
```