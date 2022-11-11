

def getBestHeight(rpc_connection):
    return rpc_connection.getblockcount()

def getinfo(rpc_connection):
    return rpc_connection.getinfo()

# def getblockchaininfo(rpc_connection):
#     return rpc_connection.getblockchaininfo()

def getBlockHash(rpc_connection, height):
    return rpc_connection.getblockhash(height)

def getBlockBatch(fromBlock, toBlock):
    commands = [ [ "getblockhash", height] for height in range(fromBlock, toBlock) ]
    return sendRPCCommand(commands)

def getDecodedBlock(fromBlock, toBlock):
    commands = [ [ "getblock", height, bool("true")] for height in getBlockBatch(fromBlock, toBlock) ]
    return sendRPCCommand(commands)

def getRawTransaction(rpc_connection, txHash):
    return rpc_connection.getrawtransaction(txHash, True)

def sendRPCCommand(rpc_connection, command):
    return rpc_connection.batch_(command)

# def getRawTransaction():
#     return rpc_connection.getrawtransaction('365d2aa75d061370c9aefdabac3985716b1e3b4bb7c4af4ed54f25e5aaa42783', True)

# print(getRawTransaction())