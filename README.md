## PubDNS (interact with 28K public DNS servers around the world)
pubdns is a library for python to have more than 28K public dns servers from 190+ countries at your python script. it works based on the public-dns.info collected data and there is a wrapper based on the dnspython to resolve all type of dns records through these public dns server smoothly.

### Quick start

```python
import pubdns
pd = pubdns.pubdns()
servers = pd.servers('US', 'los angeles')
```

### Sample data

```
[
  {
    'city': 'Los Angeles',
    'server': '12.127.16.67',
    'name': 'rmtu.mt.rs.els-gms.att.net.',
    'reliability': '1.00'
  },
  {
    'city': 'Los Angeles',
    'server': '216.240.32.77',
    'name': 'dns2.worldpassage.net.',
    'reliability':'1.00'
  },
...
]
```

### Sample DNS Query

```python
rs = pubdns.dns.resolver(servers, 'amazon.com', ['A'])
for r in rs:
    print(r)
```

### Sample Data

```
{
    'server':
        {
         'city': 'Los Angeles',
         'server': '12.127.16.67',
         'name': 'rmtu.mt.rs.els-gms.att.net.',
         'reliability': '1.00'
        },
    'resolve': [
        {'name': '176.32.98.166', 'type': 'A'},
        {'name': '176.32.103.205', 'type': 'A'},
        {'name': '205.251.242.103', 'type': 'A'}
    ]
}
```

## Feature Support

- Search by country and city
- Cache public-dns.info data and update with specific TTL
- Support HTTP proxy to get external data
- Query the public DNS with specific record type(s)

## Requirements

Python 2.6 or later.

## Installation

```
pip install pubdns
```

## License

This project is licensed under MIT license. Please read the LICENSE file.


## Contribute

Welcomes any kind of contribution, please follow the next steps:

- Fork the project on github.com.
- Create a new branch.
- Commit changes to the new branch.
- Send a pull request.
