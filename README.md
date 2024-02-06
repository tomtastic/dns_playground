### Experiments with Python DNS
Iteratively building up from simple TCP echo responder, through adding threading support and UDP handlers, and finally to parsing specific RR elements from DNS queries.

#### echo_tcp_simple.py
Echo back messages over TCP

#### echo_tcp_threaded.py
Echo back messages over TCP using a separate thread

#### echo_threaded.py
Echo back messages over UDP or TCP using separate threads

#### dns_threaded.py
Answer DNS messages over UDP or TCP using separate threads,
where the DNS answer is always fixed
