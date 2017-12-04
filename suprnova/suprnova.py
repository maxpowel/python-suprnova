from scrapium.scrapium import AuthenticatedWeb, AuthMethod, InvalidCredentialsException, FileCookieStorage
import re


class WorkerError(Exception):
    pass


class Currency(object):
    BitcoinCash = "bcc"
    BitcoinGold = "btg"
    Polytimos = "poly"
    Electroneum = "etn"
    Straks = "stak"
    SmartCash = "smart"
    Minexcoin = "mnx"
    ZCLASSIC = "zcl"
    ZENCash = "zen"
    ZCASH = "zec"
    BitcoinZ = "btcz"
    ZCoin = "xzc"
    BitSend = "bsd"
    BitCore = "btx"
    MachineCoin = "mac"
    Einsteinium = "emc2"
    Komodo = "kmd"
    ZDASH = "zdash"
    Monero = "xmr"
    DashCoin = "dash"
    ZeroCoin = "zero"
    LbryioCredits = "lbry"
    Ethereum = "eth"
    UBIQ = "ubq"
    Expanse = "exp"
    Decred = "dcr"
    Chaincoin = "chc"
    eMark = "dem"
    SiberianChervonets = "sib"
    EuropeCoinV3 = "erc"
    HOdlcoinV3 = "hodl"
    MonaCoin = "mona"
    GroestlCoin = "grs"
    Myriad = "myrgrs"
    DigibyteGroestl = "dgbg"
    DigibyteQubit = "dgbq"
    DigibyteSkein = "dgbs"
    GameCredits = "gmc"
    SpreadCoin = "spr"
    StartCoin = "start"
    FlorinCoin = "flo"
    GeoCoin = "geo"
    Litecoin = "ltc"
    MagiCoin = "xmg"

class SuprnovaWeb(AuthenticatedWeb):
    def __init__(self, username, password, currency, cookie_storage):
        super().__init__(AuthMethod(username, password, "suprnova"), cookie_storage=cookie_storage)
        self.currency = currency

    def is_logged(self, request):
        # Login or raise bad credentials
        return request.url != "https://{currency}.suprnova.cc/index.php?page=login".format(currency=self.currency)

    def login(self):
        # Login or raise bad credentials
        data = {
            "ctoken": "",
            "password": self.auth_method.password,
            "username": self.auth_method.username,
        }
        header = {
            "Referer": "https://{currency}.suprnova.cc/index.php?page=login".format(currency=self.currency)
        }
        r = self.browser.post("https://{currency}.suprnova.cc/index.php?page=login".format(currency=self.currency), data, headers=header, verify=False)

        if "Invalid username or password" in r.text:
            raise InvalidCredentialsException("Invalid credentials")
        return True


class Suprnova(object):
    def __init__(self, username, password, currency, cookie_storage=FileCookieStorage()):
        self.web = SuprnovaWeb(username, password, currency, cookie_storage)
        self.base = "https://{currency}.suprnova.cc/index.php?page=".format(currency=currency)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()

    def flush(self):
        self.web.flush()

    def get_workers(self):
        html = self.web.get_html(self.base + "account&action=workers")
        worker_table = html.find("tbody")
        workers = []
        for worker_row in worker_table.findAll("tr"):
            worker = {}
            columns = worker_row.findAll("td")
            # Worker name
            first_part = columns[0].find("span").getText()
            second_part = columns[0].find("input")["value"]
            id_part = columns[0].find("input")["name"]
            m = re.search('data\[([0-9]+)\]\[username\]', id_part)
            worker.update({"id": m.group(1), "name": first_part + second_part})
            # Worker password
            worker["password"] = columns[1].find("input")["value"]
            # Active
            worker["active"] = columns[2].find("i", {"class": "fa fa-check fa-fw"}) is not None

            worker["monitor"] = columns[3].find("input")["value"]
            worker["khash"] = columns[4].getText()
            worker["difficulty"] = columns[5].getText()

            workers.append(worker)

        return workers

    def add_worker(self, username, password):
        data = {
            "page": "account",
            "action": "workers",
            "do": "add",
            "ctoken": "",
            "username": username,
            "password": password
        }
        r = self.web.post(self.base + "account&action=workers", data)

        if "Worker added" not in r.text:
            html = self.web.html(r.text)
            danger = html.find("div", {"id": "static"})

            raise WorkerError(danger.getText().strip())

    def remove_worker(self, worker_id):
        r = self.web.get(self.base + "account&action=workers&do=delete&id={worker_id}&ctoken=".format(worker_id=worker_id))
        if "Worker removed" not in r.text:
            html = self.web.html(r.text)
            danger = html.find("div", {"id": "static"})

            raise WorkerError(danger.getText().strip())

    def remove_worker_by_name(self, worker_name):
        for worker in self.get_workers():
            if worker["name"] == worker_name:
                return self.remove_worker(worker["id"])

        raise WorkerError("Worker with name \"{worker_name}\" does not exist".format(worker_name=worker_name))


