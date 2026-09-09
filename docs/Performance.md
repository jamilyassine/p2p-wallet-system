# Performance

This document describes the performance considerations and optimization decisions for the P2P Wallet System.

---

## Pagination

Transaction history uses pagination to avoid retrieving an unbounded number of records.

The API supports:

```text
?page=1&limit=20
```

For example:

```text
/transactions?page=2&limit=20
```

Pagination limits the amount of data returned per request and reduces unnecessary database and network work.

---

## Database-Level Filtering

Transaction filtering is performed directly in PostgreSQL rather than retrieving all transactions and filtering them in application memory.

Supported operations include:

- Status filtering
- Sorting
- Search
- Pagination

Example:

```text
/transactions?status=SUCCESS
```

This approach reduces:

- Data transferred from the database
- Application memory usage
- Application-side processing

---

## Database-Level Sorting

Sorting is performed by the database.

Example:

```text
/transactions?sort=date
```

PostgreSQL can perform the ordering before returning the requested result set, avoiding unnecessary application-side sorting.

---

## Search

Transaction searches are performed at the database level.

Example:

```text
/transactions?search=...
```

This prevents the application from loading the entire transaction history before searching.

---

## Indexes

Indexes are used on frequently queried fields to improve transaction query performance.

Indexes allow PostgreSQL to locate relevant records more efficiently, particularly for filtering, sorting, and frequently accessed query paths.

Indexes are added selectively rather than indiscriminately.

---

## Unbounded Queries

Unbounded queries can become increasingly expensive as transaction history grows.

A query that retrieves every transaction can result in:

```text
Large Database Result
        ↓
Large Network Transfer
        ↓
High Application Memory Usage
        ↓
Increased Processing Time
```

Pagination and database-level filtering prevent this pattern for transaction history requests.

---

## Read vs Write Trade-Off

Indexes improve read performance but introduce write overhead.

When a record is inserted or updated, PostgreSQL may also need to update the relevant indexes.

Therefore, indexes are added only where their read-performance benefits justify their storage and write-maintenance costs.

---

## Current Optimization Strategy

The current system focuses on database-level optimizations that provide meaningful benefits without introducing unnecessary infrastructure.

The main strategies are:

- Pagination
- Database-level filtering
- Database-level sorting
- Database-level search
- Selective indexing
- Avoiding unbounded transaction queries

These optimizations are appropriate for the current scale of the application.

---

## Why Redis Is Not Used

Redis is not currently required.

The application's primary performance bottlenecks can be addressed through PostgreSQL queries, indexes, and pagination.

Introducing Redis would add:

- Additional infrastructure
- Cache invalidation complexity
- Another data store to operate
- Additional consistency considerations

Redis may become useful if future workloads require high-volume caching or very frequent repeated reads.

---

## Why Elasticsearch Is Not Used

Elasticsearch is not currently required.

The current transaction search requirements can be handled by PostgreSQL without introducing a separate search infrastructure.

Elasticsearch may become appropriate if future requirements involve:

- Large-scale full-text search
- Complex search relevance
- Very large transaction datasets
- Specialized search workloads

---

## Why Application-Level Caching Is Not Used

Application-level caching is not currently used for transaction history.

Transaction data can change, and caching introduces invalidation and consistency concerns.

For the current application, direct indexed database queries provide sufficient performance while keeping the data flow simple and predictable.

---

## Future Optimizations

If the application's workload grows significantly, potential future optimizations include:

- Query-plan analysis with `EXPLAIN ANALYZE`
- Additional targeted indexes
- Connection-pool tuning
- Read replicas
- Redis caching for suitable read-heavy workloads
- Elasticsearch for specialized large-scale search
- Background processing for non-critical workloads
- Database partitioning for very large transaction tables

These optimizations should be introduced based on measured bottlenecks rather than prematurely.