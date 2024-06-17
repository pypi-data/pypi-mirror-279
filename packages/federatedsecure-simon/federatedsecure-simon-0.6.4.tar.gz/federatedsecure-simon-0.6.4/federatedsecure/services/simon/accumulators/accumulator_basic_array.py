from federatedsecure.services.simon.accumulators.accumulator import Accumulator


class AccumulatorBasicArray(Accumulator):

    def __init__(self, _=None):
        self.samples = 0
        self.array = []

    def serialize(self):
        return {'samples': self.samples,
                'array': self.array}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorBasicArray
        accumulator.samples = dictionary['samples']
        accumulator.array = dictionary['array']
        return accumulator

    def add(self, other):
        self.samples += other.samples
        self.array += other.array

    def update(self, data):
        self.samples += 1
        self.array += [data]

    def finalize(self):
        pass

    def get_samples(self):
        return self.samples

    def get_array(self):
        return self.array
