# Copyright (c) 2025, ETH Zurich. All rights reserved.
#
# Please, refer to the LICENSE file in the root directory.
# SPDX-License-Identifier: BSD-3-Clause

import httplib
from urlparse import urlparse
import json
import sys

keys = []

certs = json.loads(sys.argv[1])


for raw_url in certs:

    url = urlparse(raw_url)
    conn = None
    if url.scheme == "https":
        conn = httplib.HTTPSConnection(url.netloc)
    else:
        conn = httplib.HTTPConnection(url.netloc)
    conn.request(method="GET", url=url.path)
    resp = conn.getresponse()
    keys += json.loads(resp.read())["keys"]

f = open(sys.argv[2], "w")
f.write(json.dumps({"keys": keys}))
f.close()
