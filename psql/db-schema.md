# PSQL Schema
Table Outline:

|   Domain  |      FQDN      |   IPv4    |   IPv6   | Open Port |  Port Service  |  Last Modified  |
|:---------:|:--------------:|:---------:|:--------:|:---------:|:--------------:|:---------------:|
|  tst.com  |  www.tst.com   |  0.0.0.0  |          |   80      |      http      |    YYYY-MM-DD   |
|  tst.com  |  www.tst.com   |  0.0.0.0  |          |   443     |      https     |    YYYY-MM-DD   |
|  tst.com  |  asdf.tst.com  |  0.0.0.1  |          |   443     |      https     |    YYYY-MM-DD   |
|  asdf.co  |  asdf.co       |           |    ::    |   22      |      ssh       |    YYYY-MM-DD   |
|  asdf.co  |  b.asdf.co     |           |    ::1   |   8080    |      http      |    YYYY-MM-DD   |


# Queries
All queries are structed for python3, e.g.,
```python
table = "output"
q = "SELECT * FROM %s", table
cursor.execute(*q)
```

## Tool I/O
Update table with output
- `"INSERT INTO output VALUES (%s, %s, %s)", <arg0>, <arg1>, <arg2>`
  => determine column length first

## Important Queries
Scanned Hosts => "Have we scanned this host before?"
- `SELECT domain FROM output;`

Results => "What are the results for <host>?"
- `SELECT * FROM output WHERE domain LIKE '*%s'", <host>`

Subdomains => "What are the subdomains of <host>?"
- `"SELECT domain FROM output WHERE domain LIKE '*%s'", <host>`

Webservers => "What are all the webservers for *.as.df?"
- `SELECT domain from output WHERE port-service LIKE 'http' OR port-service LIKE 'https'`
