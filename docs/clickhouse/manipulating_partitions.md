### DROP

```python
qb.drop_partitions('events', ['2026-01-01', '2026-01-02'], 'raw', on_cluster='{cluster}')
# ALTER TABLE raw.events ON CLUSTER {cluster} DROP PARTITION '2026-01-01', DROP PARTITION '2026-01-02'
```

### ATTACH

```python
qb.attach_partition('events', '2020-11-21', 'maintenance', 'dev_events', 'prod', '{cluster}')
# ALTER TABLE maintenance.events ON CLUSTER {cluster} ATTACH PARTITION '2020-11-21' FROM prod.dev_events
```

### DETACH

```python
qb.detach_partition('events', '2020-11-21', 'maintenance', '{cluster}')
# ALTER TABLE maintenance.events ON CLUSTER {cluster} DETACH PARTITION '2020-11-21'
```

### FREEZE

```python
qb.freeze_partition('events', '2020-11-21', 'backup_name', 'prod', '{cluster}')
# ALTER TABLE prod.events ON CLUSTER {cluster} FREEZE PARTITION '2020-11-21' WITH NAME 'backup_name'
```

### UNFREEZE

```python
qb.unfreeze_partition('events', '2020-11-21', 'backup_name', 'prod', '{cluster}')
# ALTER TABLE prod.events ON CLUSTER {cluster} UNFREEZE PARTITION '2020-11-21' WITH NAME 'backup_name'
```

### REPLACE

```python
qb.replace_partition('events', '2020-11-21', 'maintenance', 'dev_events', 'prod', '{cluster}')
# ALTER TABLE maintenance.events ON CLUSTER {cluster} REPLACE PARTITION '2020-11-21' FROM prod.dev_events
```

### FETCH

```python
qb.fetch_partition('events', '2020-11-21', 'path-in-zookeeper', 'prod', '{cluster}')
# ALTER TABLE prod.events ON CLUSTER {cluster} FETCH PARTITION '2020-11-21' FROM 'path-in-zookeeper'
```

### MOVE

```python
qb.move_partition_to_table('events', '2020-11-21', 'events_v2', 'maintenance', 'prod', '{cluster}')
# ALTER TABLE maintenance.events ON CLUSTER {cluster} MOVE PARTITION '2020-11-21' TO TABLE prod.events_v2

qb.move_partition_to_disk('events', '2020-11-21', 'fast_ssd', 'prod', '{cluster}')
# ALTER TABLE prod.events ON CLUSTER {cluster} MOVE PARTITION '2020-11-21' TO DISK 'fast_ssd'

qb.move_partition_to_volume('events', '2020-11-21', 'fast_ssd', 'prod', '{cluster}')
# ALTER TABLE prod.events ON CLUSTER {cluster} MOVE PARTITION '2020-11-21' TO VOLUME 'fast_ssd'
```

see [test_partitions.py](https://github.com/d-ganchar/david8_clickhouse/blob/main/tests/test_partitions.py)