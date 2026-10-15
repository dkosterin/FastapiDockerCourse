#pip install redis
import redis

#decode_responses=True
client = redis.Redis.from_url("redis://localhost:6379",
                              decode_responses=True
                            )

# Строки
client.set("user", "Ivan")
user = client.get("user")
print(user)
client.set("count", "100")
print(client.get("count"))
client.incrby("count", 20)
print(client.get("count"))
client.set("temp", "Something", 20)

# Списки
client.lpush("list", "First")
client.rpush("list", "Second")
client.rpush("list", "New")
l: list[str] = client.lrange("list", 0, -1)
print(l)
removed = client.lpop("list")
print(f"Удаленный элемент: {removed}")
print(client.lrange("list", 0, -1))

# Множества
client.sadd("set", "First")
client.sadd("set", "Second")
client.sadd("set", "Second")
s: set[str] = client.smembers("set")
print(s)

# Упорядоченное множество
client.zadd("users", {"Ivan": 100, "Viktor": 200, "Anton": 150})
users = client.zrange("users", 0, -1)
print(users)

# Хэш таблица
client.hset("user:123", "name", "Ivan")
client.hset("user:123", "role", "admin")
name = client.hget("user:123", "name")
print(name)
hashmap: dict[str, str] = client.hgetall("user:123")
print(hashmap)