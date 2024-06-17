from federatedsecure.services.simon.accumulators.\
     accumulator_basic_function import AccumulatorBasicFunction


class AccumulatorBasicSum(AccumulatorBasicFunction):

    """an accumulator that simply adds all numbers it is fed"""

    def __init__(self, _=None):
        """use AccumulatorBasicFunction where the updating function is a sum"""
        super().__init__(0, lambda x, y: x+y)

    def serialize(self):
        return {'samples': self.samples,
                'sum': self.data}

    @staticmethod
    def deserialize(dictionary):
        accumulator = AccumulatorBasicSum()
        accumulator.samples = dictionary['samples']
        accumulator.data = dictionary['sum']
        return accumulator

    def get_sum(self):
        return self.data
