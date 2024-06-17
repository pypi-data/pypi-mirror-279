import secrets as _secrets

from federatedsecure.services.simon.caches.cache import Cache
from federatedsecure.services.simon.caches.additive import CacheAdditive
from federatedsecure.services.simon.caches.functional import CacheFunctional
from federatedsecure.services.simon.microprotocols.microprotocol \
    import Microprotocol
from federatedsecure.services.simon.accumulators.\
    accumulator_statistics_frequency import AccumulatorStatisticsFrequency


class MicroprotocolStatisticsFrequency(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)

        self.secret_key = _secrets.token_bytes(32)

        self.n = self.network.count

        self.register_cache('input', Cache())
        self.register_cache('keys', CacheFunctional(
            lambda x, y: set(x).union(set(y)), self.n, self.n))
        self.register_cache('checkpoint2',
                            CacheAdditive(minimum=self.n))
        self.register_cache('checkpoint3',
                            CacheAdditive(minimum=self.n))

        self.register_stage(0, ['input'], self.stage_0)
        self.register_stage(1, ['keys'], self.stage_1)
        self.register_stage(2, ['checkpoint2'], self.stage_2)
        self.register_stage(3, ['checkpoint3'], self.stage_3)

        self.input = None
        self.result_cache = AccumulatorStatisticsFrequency()

        self.histogram = {}
        self.keys = []
        self.tags = {}

    def stage_0(self, args):

        self.histogram = args['input']['histogram']
        self.network.broadcast([*self.histogram.keys()], 'keys')
        return 1, None

    def stage_1(self, args):
        self.keys = args['keys']
        for key in args['keys']:
            s = self.histogram.get(key, 0)
            tag = 'sum_{}'.format(key)
            self.tags[tag] = s
            self.register_cache(tag, Cache())
        self.network.broadcast(0, 'checkpoint2')
        return 2, None

    def stage_2(self, _):
        self.register_stage(4, self.tags.keys(), self.stage_final)
        self.network.broadcast(0, 'checkpoint3')
        return 3, None

    def stage_3(self, _):
        for tag in self.tags:
            self.start_pipeline('SecureSum', tag, self.tags[tag])
        return 4, None

    def stage_final(self, args):

        histogram = {}
        mode = None
        maxi = -1
        for tag in args:
            if tag == 'stage':
                continue
            histogram[tag[4:]] = args[tag]['sum']
            if args[tag]['sum'] > maxi:
                maxi = args[tag]['sum']
                mode = tag[4:]

        return -1, {'inputs': self.n, 'result': {
                       'mode': mode,
                       'histogram': histogram}}
