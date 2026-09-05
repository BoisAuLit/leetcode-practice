from collections import defaultdict
import heapq


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


twitter = Twitter()
twitter.postTweet(1, 10)  # User 1 posts a new tweet with id = 10.
twitter.postTweet(2, 20)  # User 2 posts a new tweet with id = 20.
print(twitter.getNewsFeed(1))  # / User 1's news feed should only contain their own tweets -> [10].
print(twitter.getNewsFeed(2))  # / User 2's news feed should only contain their own tweets -> [20].
twitter.follow(1, 2)  # User 1 follows user 2.
print(twitter.getNewsFeed(1))  # / User 1's news feed should contain both tweets from user 1 and user 2 -> [20, 10].
print(twitter.getNewsFeed(2))  # / User 2's news feed should still only contain their own tweets -> [20].

print(twitter.following)
print(twitter.followedBy)

twitter.unfollow(1, 2)  # / User 1 unfollows user 2.
print(twitter.getNewsFeed(1))  # / User 1's news feed should only contain their own tweets -> [10].
