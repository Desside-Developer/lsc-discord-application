import redis

R_CONFIG = {
    'host': 'bot-redis-stack-1',
    'port': 6379,
    'db': 0
}

class RedisConnect:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisConnect, cls).__new__(cls)
            cls._instance.config = R_CONFIG
            cls._instance.connectToRedis()
        return cls._instance
    def connectToRedis(self):
        self.StrictRedis = redis.StrictRedis(**self.config)
    def reconnectToRedis(self):
        if self.StrictRedis:
            self.StrictRedis.shutdown(save=True)
            self.connectToRedis()
    def disconnect(self):
        if self.StrictRedis:
            self.StrictRedis.close()

    def savePrefixesToHash(self, guild_id:int, prefix:str):
        return self.StrictRedis.hset('guild_prefixes', guild_id, prefix)

    def getPrefixes(self, guild_id:int):
        return self.StrictRedis.hget('guild_prefixes', guild_id)

rRedis = RedisConnect()