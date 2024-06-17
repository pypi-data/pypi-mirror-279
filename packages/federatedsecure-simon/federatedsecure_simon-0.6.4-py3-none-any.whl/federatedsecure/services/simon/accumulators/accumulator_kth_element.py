from federatedsecure.services.simon.accumulators.accumulator import Accumulator


class AccumulatorKthElement(Accumulator):

    """an accumulator that keeps track of parameters
    used to find the kth rank of an array"""

    def __init__(self, _=None):
        self.samples = None
        self.array = None
        self.rank = None
        self.lower_bound = None
        self.upper_bound = None

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorKthElement()
        accumulator.samples = dictionary['samples']
        accumulator.array = dictionary['array']
        accumulator.rank = dictionary['rank']
        accumulator.lower_bound = dictionary['lower_bound']
        accumulator.upper_bound = dictionary['upper_bound']
        return accumulator

    def serialize(self):
        return {'samples': self.samples,
                'array': self.array,
                'rank': self.rank,
                'lower_bound': self.lower_bound,
                'upper_bound': self.upper_bound}

    def add(self, other):
        self.samples = self.samples + other.samples
        self.array = self.array + other.array
        self.rank = self.rank
        self.lower_bound = min(self.lower_bound, other.lower_bound)
        self.upper_bound = max(self.upper_bound, other.upper_bound)

    def update(self, data):
        self.samples = len(data['array'])
        self.array = data['array']
        self.rank = data['rank']
        self.lower_bound = data['lower_bound']
        self.upper_bound = data['upper_bound']

    def finalize(self):
        pass
