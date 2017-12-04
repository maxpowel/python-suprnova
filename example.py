from suprnova import Suprnova, Currency
from scrapium.scrapium import InvalidCredentialsException

username = "user"
password = "pass"

with Suprnova(username=username, password=password, currency=Currency.MagiCoin) as client:
    print("Fetching worker list...")
    try:
        workers = client.get_workers()
        print(workers)
    except InvalidCredentialsException:
        print("Invalid password or username")



