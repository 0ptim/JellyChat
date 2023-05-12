from defichain import Ocean


class Network:
    MAINNET: str = "mainnet"
    TESTNET: str = "testnet"


oceanMainnet = Ocean(network="mainnet")
oceanTestnet = Ocean(network="testnet")


def getOcean(network: str = Network.MAINNET) -> Ocean:
    if network == Network.MAINNET:
        return oceanMainnet
    elif network == Network.TESTNET:
        return oceanTestnet
    else:
        raise Exception("The selected network does not exist!")


def filterJson(json: {}, keys: []):
    result = {}
    for key in keys:
        result.update({key: json[key]})
    return result
    