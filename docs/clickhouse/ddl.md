### CREATE TABLE

```python
query = (qb
    .create_table_as(
       qb.select('name', 'created_at').from_table('events'),
       'events_copy',
       'maintenance'
    )
    .order_by('created_at', 'name')
    .partition_by(to_date('created_at'), 'name')
    .on_cluster('{cluster}')
    .engine('MergeTree')
)
# CREATE TABLE maintenance.events_copy ON CLUSTER {cluster}
# ENGINE = MergeTree 
# PARTITION BY (toDate(created_at), name) 
# ORDER BY (created_at, name)
# AS SELECT name, created_at FROM events
```