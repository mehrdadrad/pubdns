## PubDNS
pubdns is a library for python to have public dns servers around the world at your python script. it works based on the public-dns.info collected data and there is a wrapper based on the dnspython to resolve all type of dns records through these public dns server smoothly.

```
import pubdns
pd = pubdns.pubdns()
servers = pd.servers('US', 'los angeles')
```
```
[{
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
}]
```
## Feature Support

- Search by country and city
- Cache public-dns.info data and update with specific TTL
- Support HTTP proxy to get external data
- Query the public DNS with specific record type(s)

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
