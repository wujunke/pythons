#coding=utf-8
from snownlp import SnowNLP



s = SnowNLP(u'虽然说等了好久才收到货，不错等待是对的。就是没有送我东西（我明明买了那么多东西）跑分37万，棒棒的。')


print s.sentiments

from snownlp import sentiment

sentiment.train()
sentiment.save()