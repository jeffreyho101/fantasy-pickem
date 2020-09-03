# SQLITE Shortcuts
*(for reference; non-exhaustive; will add to this as I see fit)*

Access the table names in a table:
```
.tables
```

Get column names from a table:
```
PRAGMA table_info(table_name);
```

Update games table (or any table, for that manner) by manual entry during a give week:

```
update games set winner = 'SEA' where week = 1 and (road_team = 'SEA' or home_team='SEA');
```