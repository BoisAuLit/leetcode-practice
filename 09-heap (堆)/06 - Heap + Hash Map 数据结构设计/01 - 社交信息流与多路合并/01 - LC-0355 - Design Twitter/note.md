# Design Twitter 笔记

### 📝 2026-09-28 - retry 1

```python
class Twitter:
    def __init__(self):
        self.time = 0
        self.tweets = defaultdict(list)  # userId -> list of (time, tweetId)
        self.following = defaultdict(set)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweets[userId].append((self.time, tweetId))
        self.time += 1

    def getNewsFeed(self, userId: int) -> list[int]:
        users = self.following[userId] | {userId}
        candidates = [t for u in users for t in self.tweets[u][-10:]]
        return [tid for _, tid in heapq.nlargest(10, candidates)]

    def follow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.following[followerId].discard(followeeId)
```

### 📝 2026-10-02 - retry 2

```python
class Twitter:
    def __init__(self):
        self.followMap = defaultdict(set)
        self.tweets = defaultdict(list)
        self.time = 0

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.time += 1
        self.tweets[userId].append((self.time, tweetId))

    def getNewsFeed(self, userId: int) -> list[int]:
        all_tweets = self.tweets[userId][-10:].copy()
        for followee in self.followMap[userId]:
            # ! 注意, 这里不能写 all_tweets = all_tweets.extend()
            # ! 因为 extend() 的结果是 None, extend 是 in-place 的!
            all_tweets.extend(self.tweets[followee][-10:])
        return [x[1] for x in heapq.nlargest(10, all_tweets, key=lambda x: x[0])]

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followMap[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        self.followMap[followerId].discard(followeeId)
```
