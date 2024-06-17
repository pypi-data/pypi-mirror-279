import binascii as _binascii
import secrets as _secrets
import hashlib as _hashlib

from federatedsecure.services.simon.caches.cache \
    import Cache
from federatedsecure.services.simon.caches.additive \
    import CacheAdditive
from federatedsecure.services.simon.caches.functional \
    import CacheFunctional
from federatedsecure.services.simon.microprotocols.microprotocol \
    import Microprotocol
from federatedsecure.services.simon.crypto.x25519x448 \
    import X25519


class MicroprotocolSetIntersectionSize(Microprotocol):

    def __init__(self, microservice, properties, myself):
        super().__init__(microservice, properties, myself)

        self.secret_key = _secrets.token_bytes(32)

        self.num_nodes = len(properties['nodes'])

        self.register_cache('input', Cache())
        self.register_stage(0,
                            ['input'],
                            self.stage_0)

        for i in range(self.num_nodes - 1):
            self.register_cache(f'stage{i+1}', Cache())
            self.register_stage(i+1,
                                [f'stage{i+1}'],
                                self.stage_i)

        self.register_cache(f'stage{self.num_nodes}',
                            CacheFunctional(lambda x, y:
                                            set(x).intersection(set(y)),
                                            self.num_nodes, self.num_nodes))

        self.register_stage(self.num_nodes,
                            [f'stage{self.num_nodes}', 'samples'],
                            self.stage_n)

        self.register_cache('samples', CacheAdditive(minimum=self.num_nodes))

        self.sizes = [0] * self.num_nodes

    def stage_0(self, args):
        self.network.broadcast(args['input']['samples'], 'samples')
        return self.stage_i({'stage': 0,
                             'stage0': [_hashlib.sha3_256(
                                 item.encode("utf-8")).hexdigest()
                                        for item in args['input']['set']]})

    def stage_i(self, args):
        stage = args['stage']
        xh = args[f'stage{stage}']
        self.sizes[(self.network.myself-stage) % self.num_nodes] = len(xh)
        xxh = self.encrypt(xh)
        if stage+1 < self.num_nodes:
            self.network.send_to_next_node(xxh, f'stage{stage+1}')
        else:
            self.network.broadcast(xxh, f'stage{stage+1}')
        return stage+1, None

    def stage_n(self, args):
        return -1, {'inputs': self.num_nodes,
                    'result': { 'size_intersection':
                                    len(args[f'stage{args["stage"]}'])}}

    def encrypt(self, data):
        x25519 = X25519(self.secret_key)
        return [_binascii.hexlify(x25519.encrypt(
            _binascii.unhexlify(d))).decode('utf-8') for d in data]
