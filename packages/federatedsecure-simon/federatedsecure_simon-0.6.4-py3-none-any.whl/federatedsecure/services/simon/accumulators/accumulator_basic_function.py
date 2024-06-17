from federatedsecure.services.simon.accumulators.accumulator import Accumulator


class AccumulatorBasicFunction(Accumulator):

    """an accumulator that stores type X and is defined by an update
    function that takes X and Y as input and returns a result of type X.
    often X and Y will be the same type."""

    def __init__(self, initial, function):
        self.samples = 0
        self.data = initial
        self.function = function

    def add(self, other):
        """combine another accumulator storing
        data type Y into this one"""
        self.samples = self.samples + other.samples
        self.data = self.function(self.data, other.data)

    def update(self, data):
        """update this accumulator by a list of
        data items or by a single data item"""
        if isinstance(data, list):
            self.samples = self.samples + len(data)
            for datum in data:
                self.data = self.function(self.data, datum)
        else:
            self.samples = self.samples + 1
            self.data = self.function(self.data, data)

    def finalize(self):
        pass

    def get_samples(self):
        return self.samples

    def get_data(self):
        return self.data
