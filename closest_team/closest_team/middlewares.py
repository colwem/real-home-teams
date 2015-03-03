import os
import random
from bisect import bisect
from scrapy.conf import settings


class RandomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        ua  = self.weighted_choice(settings.get('USER_AGENT_LIST'))
        if ua:
            request.headers.setdefault('User-Agent', ua)

    def prepare_breakpoints(self, choices):
        self.cum_weights = []
        self.values = []
        self.total = 0
        for weight, value in choices:
            self.total += weight
            self.cum_weights.append(self.total)
            self.values.append(value)

    def weighted_choice(self, choices):
        if not hasattr(self, 'cum_weights'):
            self.prepare_breakpoints(choices)
        x = random.uniform(0, self.total)
        i = bisect(self.cum_weights, x)
        return self.values[i]


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = settings.get('HTTP_PROXY')
