from pyvisjs import Network, Options

trans = {
    "data": [
        {"id": 1, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
        {"id": 2, "from": "AM", "to": "JL", "amount": 100, "country": "LV", "class": "pers"},
        {"id": 3, "from": "AM", "to": "DM", "amount": 20, "country": "EE", "class": "pers"},
        {"id": 4, "from": "JL", "to": "Hypo", "amount": 150, "country": "GB", "class": "hypo"},
        {"id": 5, "from": "JL", "to": "AM", "amount": 50, "country": "LV", "class": "pers"},
        {"id": 6, "from": "AM", "to": "LMT", "amount": 33, "country": "LV", "class": "tele"},
        {"id": 7, "from": "DM", "to": "McDnlds", "amount": 5, "country": "US", "class": "food"},
    ],
}

opt = Options()
opt.pyvisjs.set_filtering()

net = Network.from_transactions(trans, options=opt)

net.show()