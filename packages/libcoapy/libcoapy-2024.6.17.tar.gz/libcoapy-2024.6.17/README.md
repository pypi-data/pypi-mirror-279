libcoapy
========

libcoapy project enables communication over the CoAP protocol (RFC 7252). The
`llapi` module provides ctypes-based wrappers for the [libcoap](https://libcoap.net/)
C library. The `libcoapy` module uses `llapi` to provide a high-level class interface
to the libcoap functions.

Dependencies:
-------------

 - libcoap

Status
------

This project is still in early development. Several functions of the libcoap
library are not yet available and existing high-level libcoapy APIs might change
in the future.

Example
-------

```python
from libcoapy import *

if len(sys.argv) < 2:
	uri_str = "coaps://localhost/.well-known/core"
else:
	uri_str = sys.argv[1]

ctx = CoapContext()

session = ctx.newSession(uri_str, hint="user", key="password")

def rx_cb(session, tx_msg, rx_msg, mid):
	print(rx_msg.bytes)
	if not tx_msg.observe:
		session.ctx.stop_loop()

session.sendMessage(payload="example data", observe=False, response_callback=rx_cb)

ctx.loop()
```

For an example with the low-level API, see `examples/ll-client.py`.
