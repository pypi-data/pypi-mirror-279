"""SImple Multiparty computatiON (SIMON)
service for Federated Secure Computing"""

from federatedsecure.services.simon.microservice import MicroserviceSimon


def federatedsecure_register(registry):

    registry.register(
        {
            "namespace": "federatedsecure",
            "protocol": "Simon",
            "version": "0.6.0"
        },
        MicroserviceSimon()
    )
