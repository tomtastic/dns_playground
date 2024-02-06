### Experiments with Python DNS
Iteratively building up from simple TCP echo responder, through adding threading support and UDP handlers, and finally to parsing specific RR elements from DNS queries.

#### echo_tcp_simple.py
Echo back messages over TCP
```shell
$ sudo -E python3 echo_tcp_simple.py
Connect by ('127.0.0.1', 54321)
```

```shell
$ echo -n "hello" | nc 127.0.0.10 53
HELLO%
```

#### echo_tcp_threaded.py
Echo back messages over TCP using a separate thread
```shell
$ sudo -E python3 echo_tcp_threaded.py
Server bind on : ('127.0.0.10', 53)
connect from ('127.0.0.1', 44638)
```

```shell
$ echo -n "hello" | nc 127.0.0.10 53
HELLO%
```

#### echo_threaded.py
Echo back messages over UDP or TCP using separate threads
```shell
$ sudo -E python3 echo_threaded.py
Thread 4813 listening on TCP : ('127.0.0.10', 53)
Thread 4814 listening on UDP : ('127.0.0.10', 53)
connection(TCP) from 127.0.0.1:57304
connection(UDP) from 127.0.0.1:34502
```

```shell
$ echo "hello" | socat - TCP4:127.0.0.10:53
TCP:HELLO
$ echo "hello" | socat - UDP4:127.0.0.10:53
UDP:HELLO
```

#### dns_threaded.py
Answer DNS messages over UDP or TCP using separate threads,
where the DNS answer is always fixed
```shell
$ sudo -E python dns_threaded.py
Thread 19594 listening TCP : ('127.0.0.10', 53)
Thread 19595 listening UDP : ('127.0.0.10', 53)
127.0.0.1:46417 [TCP] example.com. IN TXT
127.0.0.1:33792 [UDP] example.com. IN TXT
```
```shell
$ dig +tcp +retry=0 +noall +answer @127.0.0.10 example.com TXT
example.com.            300     IN      TXT     "fake=123txt"
$ dig +notcp +retry=0 +noall +answer @127.0.0.10 example.com TXT
example.com.            300     IN      TXT     "fake=123txt"
```
