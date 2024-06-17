import math as _math

from federatedsecure.services.simon.caches.cache \
    import Cache
from federatedsecure.services.simon.caches.additive \
    import CacheAdditive
from federatedsecure.services.simon.microprotocols.microprotocol \
    import Microprotocol


class MicroprotocolKthElement(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)
        self.n = self.network.count
        self.i = 0
        self.array = None
        self.lower_bound = None
        self.upper_bound = None
        self.rank = None
        self.middle = None

        self.initialize_chaches()
        self.initialize_stages()

    def initialize_chaches(self):
        self.register_cache('input', Cache())
        self.register_cache('samples', CacheAdditive(minimum=self.n))
        self.register_cache('range', Cache())
        self._register_chache_lg()

    def _register_chache_lg(self):
        self.register_cache(f'l{self.i}', Cache())
        self.register_cache(f'g{self.i}', Cache())

    def initialize_stages(self):
        self.register_stage(0, ['input'], self.stage_initial)
        self._register_stage_i()

    def _register_stage_i(self):
        self.register_stage(self.i+1,
                            [f'l{self.i}',
                             f'g{self.i}',
                             'samples'],
                            self.stage_next)

    def stage_initial(self, args):
        self.network.broadcast(args['input']['samples'], 'samples')
        self.array = args['input']['array']
        self.rank = args['input']['rank']
        self.lower_bound = args['input']['lower_bound']
        self.upper_bound = args['input']['upper_bound']
        self.middle = _math.ceil((self.lower_bound+self.upper_bound)/2)
        self._compute_lg()
        return 1, None

    def stage_next(self, args):
        sum_l = args[f'l{self.i}']['sum']
        sum_g = args[f'g{self.i}']['sum']
        if sum_l <= self.rank-1 and sum_g <= args['samples']-self.rank:
            self.register_stage(self.i + 2, ['samples'], self.stage_final)
            return self.i + 2, None
        if sum_l >= self.rank:
            self.upper_bound = self.middle-1
        if sum_g >= args['samples']-self.rank+1:
            self.lower_bound = self.middle+1
        self.middle = _math.ceil((self.lower_bound+self.upper_bound)/2)
        self.i += 1
        self._register_chache_lg()
        self._register_stage_i()
        self._compute_lg()
        return self.i + 1, None

    def stage_final(self, args):
        return -1, {'inputs': self.n,
                    'result': {
                        'samples': args['samples'],
                        'item': self.middle}}

    def _compute_lg(self):
        l = sum(1 for dat in self.array if dat < self.middle)
        g = sum(1 for dat in self.array if dat > self.middle)
        self.start_pipeline('SecureSum', f'l{self.i}', l)
        self.start_pipeline('SecureSum', f'g{self.i}', g)
