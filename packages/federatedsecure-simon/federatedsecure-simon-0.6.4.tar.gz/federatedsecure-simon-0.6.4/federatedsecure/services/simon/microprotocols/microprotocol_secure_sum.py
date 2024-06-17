import secrets as _secrets

from federatedsecure.services.simon.caches.cache \
    import Cache
from federatedsecure.services.simon.caches.additive \
    import CacheAdditive
from federatedsecure.services.simon.microprotocols.microprotocol \
    import Microprotocol


class MicroprotocolSecureSum(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)

        self.n = self.network.count

        self.digits_before = properties['parameters'].get('digits_before', 12)
        self.digits_after = properties['parameters'].get('digits_after', 12)

        self.register_cache('input',
                            Cache())
        self.register_cache('intermediate',
                            CacheAdditive(minimum=self.n))
        self.register_cache('final',
                            CacheAdditive(minimum=self.n))

        self.register_stage(0,
                            ['input'],
                            self.stage_0)
        self.register_stage(1,
                            ['intermediate'],
                            self.stage_1)
        self.register_stage(2,
                            ['final'],
                            self.stage_2)

    def stage_0(self, args):
        o = args['input']['sum']
        s = 0
        for i in range(self.network.count - 1):
            r = _secrets.randbelow(10 **
                                   (self.digits_after+self.digits_before))
            s = s + r
            self.network.send_to_node(r, i, 'intermediate')
        self.network.send_to_node(int(o * (10 ** self.digits_after)) - s,
                                  self.network.count - 1, 'intermediate')
        return 1, None

    def stage_1(self, args):
        self.network.broadcast(args['intermediate'], 'final')
        return 2, None

    def stage_2(self, args):
        return -1, {'inputs': self.n,
                    'result': {
                        'sum': args['final'] / (10 ** self.digits_after)}}
