from Chain import *
import datetime
import sqlite3
import socketserver
import socketio
import json
from aiohttp import web
from RSA import *

PORT = 3080
MINOR_DB = "Miner.sqlite"
MINOR_TABLE_OFF = "Miner"
VOTES_IN_A_BLOCK = 10

class MinerError(Exception):
    pass

class Miner:
    __chain = None
    __sio = None
    def __init__(self, chain, t):
        """
        :str chain: the name of the chain
        :int t: type of the chain. If the chain already exists, set t = 0,
                otherwise set t = 1
        """
        if type(chain) != str:
            raise MinerError("chain must be str, but not {}".format(type(chain)))
        if type(t) != int:
            raise MinerError("type must be int, but not {}".format(type(t)))
        self.__chain = Chain(chain)

        if t == 0:
            self.__load_chain()
        else:
            self.__chain.create()

        self.__sio = socketio.AsyncServer()
        app = web.Application()
        self.__sio.attach(app)


        @self.__sio.on('connect')
        def connect(sid, environ):
            print('connect', sid)

        @self.__sio.on("Vote")
        def vote(sid, data):
            d = json.loads(data)
            data = d["data"]

            sig = d["sign"]
            key_info = data['pubkey']
            target = data['target']
            prob_num = data['prob_num']
            selection = data['selection']


            key_info = key_info.encode("utf-8")

            vote = "{}:{}".format(data['prob_num'], data['selection'])
            # print(vote)

            # hash = hashlib.sha1()
            # hash.update(vote.encode('utf-8'))
            # print(hash.hexdigest())
            #
            # pubkey = load(key_info, PUB_KEY)
            # print(str(data))
            # sign(str(data).encode('utf-8'), )



            # print(verify(str(data).encode('utf-8'), pubkey, sig.encode("utf-8")))

            voteInfo = VoteInfo(get_timestamp(), target=target, pubkey=key_info, vote=(prob_num, selection), sign = sig)

            return "OK", 123

        web.run_app(app)

    def __load_chain(self):
        # todo load chain
        self.__chain.load()
        pass

    def add_block(self, block):
        if type(block) is not bytes:
            raise MinerError("block must be bytes, but not {}".format(type(block)))
        block = VoteBlock.load(block)
        if not block.check():
            raise MinerError("Block not valid")
        self.__chain.add_block(block)

    # this function should not belong here
    def add_vote(self, voteInfo):
        if type(voteInfo) is not bytes:
            raise MinerError("voteInfo must be bytes, but not {}".format(type(voteInfo)))
        voteInfo = VoteInfo.load(voteInfo)
        self.__chain.add_vote(voteInfo, -1)

    def check_vote(self, voteInfo):
        pass

    def check_block(self, blockInfo):
        pass

    def pack_block(self):
        lid, lhash, lprehash = self.__chain.get_last_block()
        voteBlock = VoteBlock(lid + 1, lhash.encode("utf-8"))

        votes = self.__chain.get_uncomfirmed_votes()
        pack = votes[:VOTES_IN_A_BLOCK]
        if(len(pack) == 0):
            return None

        for voteInfo in pack:
            voteBlock.add_info(voteInfo)
            self.__chain.remove_vote(voteInfo)

        voteBlock.close()
        self.__chain.add_block(voteBlock)
        return voteBlock

    def get_timestamp(self):
        #todo zhang
        pass



if __name__ == '__main__':
    miner = Miner("test", 0)
    # voteInfo = VoteInfo(datetime.datetime.now().timestamp(), b'target', b'pubkey', (2, [3]), b'sign')
    # miner.add_vote(bytes(voteInfo))
    # voteInfo = VoteInfo(datetime.datetime.now().timestamp(), b'target', b'pubkey', (3, [3]), b'sign')
    # miner.add_vote(bytes(voteInfo))
    # voteInfo = VoteInfo(datetime.datetime.now().timestamp(), b'target', b'pubkey', (4, [1]), b'sign')
    # miner.add_vote(bytes(voteInfo))
    # block = miner.pack_block()
    # bytes(block)
