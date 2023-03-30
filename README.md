# Odoo Runner #

Small wrapper for running headless Odoo scripts.

# Install #

```
pip install odoo-runner
```

# Example #

test.py:

```python
#! /usr/bin/env python

import sys
from odoo_runner import OdooRunner


def start(env):
    return env['res.partner'].search_count([])


if __name__ == "__main__":
    args = sys.argv[1:]
    runner = OdooRunner(args, start)
    partner_count = runner.run()
    print("Number of partners:", partner_count)

    sys.exit(0)
```

running:

```shell
PYTHONPATH=/path/to/odoo/src/ ./test.py -c /path/to/odoo.conf --logfile=''
```
