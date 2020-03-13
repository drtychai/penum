# PSQL Schema
Table Outline:

|     Host    |     IP    |        FQDN         |  Open Port  |  Port Service  |  Last Modified  |
|:-----------:|:---------:|:-------------------:|:-----------:|:--------------:|:---------------:|
|   tst.com   |  0.0.0.0  |  ec2-asdf-test.com  |     80      |      http      |    YYYY-MM-DD   |
|   tst.com   |  0.0.0.0  |  ec2-asdf-test.com  |     443     |      https     |    YYYY-MM-DD   |
|   asdf.co   |    ::     |      asdf.co        |     22      |      ssh       |    YYYY-MM-DD   |
|  b.asdf.co  |    ::1    |     b.asdf.co       |    8080     |      http      |    YYYY-MM-DD   |


# Queries
All queries are structed for python3, e.g.,
```python
table = "penum"
q = "SELECT * FROM %s", table
cursor.execute(*q)
```

## Tool I/O
Update table with output
- `"INSERT INTO penum VALUES (%s, %s, %s)", <arg0>, <arg1>, <arg2>`
  => determine column length first

## Important Queries
Scanned Hosts => "Have we scanned this host before?"
- `SELECT host FROM penum;`

Results => "What are the results for <host>?"
- `SELECT * FROM penum WHERE host LIKE '*%s'", <host>`

Subdomains => "What are the subdomains of <host>?"
- `"SELECT host FROM penum WHERE host LIKE '*%s'", <host>`

