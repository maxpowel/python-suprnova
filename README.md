# Python Suprnova
With this library you can manage your [suprnova](https://www.suprnova.cc/) account. This library is focused on worker
monitorization.

# Installation
pip install suprnova

# Example

```python
from suprnova import Suprnova, Currency
from scrapium.scrapium import InvalidCredentialsException

username = "myUsername"
password = "myPassword"

with Suprnova(username=username, password=password, currency=Currency.MagiCoin) as client:
    print("Fetching worker list...")
    try:
        workers = client.get_workers()
        print(workers)
    except InvalidCredentialsException:
        print("Invalid password or username")
```

The first time you run the example, it may take some time (because the library has to log in) but the cookies are stored
so next time you run it the response will be faster. By default the cookies are stored into a file but you can store
it into redis or mongo (or anywhere else you want, just write the connector) if you need a multiple instance access.
This library is based on [scrapium](https://github.com/maxpowel/scrapium) so check it for more details