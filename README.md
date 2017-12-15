# PubDNS
pubdns is a library for python to have public dns servers around the world at your python script. it works based on the public-dns.info collected data and there is a wrapper based on the dnspython to resolve all type of dns records through these public dns server smoothly.

```
pd = pubdns.pubdns()
servers = pd.servers('US', 'los angeles')
```
```
[{'city': 'Los Angeles', 'server': '12.127.16.67', 'name': 'rmtu.mt.rs.els-gms.att.net.', 'reliability': '1.00'}, 
 {'city': 'Los Angeles', 'server': '216.240.32.77', 'name': 'dns2.worldpassage.net.', 'reliability':'1.00'}, ....]
```
