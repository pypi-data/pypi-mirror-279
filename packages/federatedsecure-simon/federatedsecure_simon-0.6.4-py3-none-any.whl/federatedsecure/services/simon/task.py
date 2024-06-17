from federatedsecure.services.simon.microprotocols.create \
    import create as create_microprotocol
from federatedsecure.services.simon.accumulators.create \
    import create as create_accumulator


class TaskSimon:

    def __init__(self, microservice, network, microprotocol,
                 parameters, task_id, parent):

        self.microservice = microservice
        self.task_id = task_id
        self.nodes = network['nodes']
        self.myself = network['myself']
        self.microprotocol_name = microprotocol
        self.microprotocol_class = create_microprotocol(microprotocol)
        self.microprotocol = None
        self.parent = parent
        self.parameters = parameters
        self.accumulator = create_accumulator(microprotocol)()

    def invite(self):
        ret = {'task_id': self.task_id,
               'microprotocol': self.microprotocol_name,
               'invitation_id': None,
               'parameters': self.parameters,
               'parent': self.parent}
        return ret

    def input(self, data):
        if isinstance(data, list):
            for datum in data:
                self.accumulator.update(datum)
        else:
            self.accumulator.update(data)
        return None

    def start(self):
        self.accumulator.finalize()
        args = {'task': {
            'microprotocol': self.microprotocol_name,
            'parent': self.parent,
            'parameters': self.parameters,
            'nodes': [node for node in self.nodes]},
            'message': {
                'token': 'input',
                'sender': self.myself,
                'receiver': self.myself,
                'body': self.accumulator.serialize()}}
        self.peer_to_peer(args)
        return None

    def progress(self):
        return None

    def result(self):
        return self.microprotocol.get_result()

    def peer_to_peer(self, body=None):
        properties = {**body['task'], 'task_id': self.task_id}
        message = body['message']

        if self.microprotocol is None:
            self.microprotocol = self.microprotocol_class(
                self.microservice, properties, message['receiver'])

        self.parent = body['task']['parent']
        self.parameters = body['task']['parameters']

        self.microprotocol.process(message)
        return None
