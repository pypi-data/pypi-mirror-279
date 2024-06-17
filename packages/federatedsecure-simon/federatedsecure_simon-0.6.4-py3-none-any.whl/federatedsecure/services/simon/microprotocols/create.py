import federatedsecure.server
import federatedsecure.server.exceptions

from federatedsecure.services.simon.microprotocols.\
    microprotocol_kth_element \
    import MicroprotocolKthElement
from federatedsecure.services.simon.microprotocols.\
    microprotocol_minimum_maximum \
    import MicroprotocolMinimumMaximum
from federatedsecure.services.simon.microprotocols.\
    microprotocol_secure_sum \
    import MicroprotocolSecureSum
from federatedsecure.services.simon.microprotocols.\
    microprotocol_secure_matrix_multiplication \
    import MicroprotocolSecureMatrixMultiplication
from federatedsecure.services.simon.microprotocols.\
    microprotocol_secure_median \
    import MicroprotocolSecureMedian
from federatedsecure.services.simon.microprotocols.\
    microprotocol_set_intersection \
    import MicroprotocolSetIntersection
from federatedsecure.services.simon.microprotocols.\
    microprotocol_set_intersection_size \
    import MicroprotocolSetIntersectionSize
from federatedsecure.services.simon.microprotocols.\
    microprotocol_statistics_bivariate \
    import MicroprotocolStatisticsBivariate
from federatedsecure.services.simon.microprotocols.\
    microprotocol_statistics_frequency \
    import MicroprotocolStatisticsFrequency
from federatedsecure.services.simon.microprotocols.\
    microprotocol_statistics_contingency \
    import MicroprotocolStatisticsContingency
from federatedsecure.services.simon.microprotocols.\
    microprotocol_statistics_univariate \
    import MicroprotocolStatisticsUnivariate
from federatedsecure.services.simon.microprotocols.\
    microprotocol_statistics_contingency_vertical \
    import MicroprotocolStatisticsContingencyVertical
from federatedsecure.services.simon.microprotocols.\
    microprotocol_statistics_regression_ols_vertical \
    import MicroprotocolStatisticsRegressionOLSVertical


def create(microprotocol):

    if microprotocol == 'KthElement':
        return MicroprotocolKthElement

    if microprotocol == 'MinimumMaximum':
        return MicroprotocolMinimumMaximum

    if microprotocol == 'SecureSum':
        return MicroprotocolSecureSum

    if microprotocol == 'SecureMatrixMultiplication':
        return MicroprotocolSecureMatrixMultiplication

    if microprotocol == 'SecureMedian':
        return MicroprotocolSecureMedian

    if microprotocol == 'SetIntersection':
        return MicroprotocolSetIntersection

    if microprotocol == 'SetIntersectionSize':
        return MicroprotocolSetIntersectionSize

    if microprotocol == 'StatisticsBivariate':
        return MicroprotocolStatisticsBivariate

    if microprotocol == 'StatisticsFrequency':
        return MicroprotocolStatisticsFrequency

    if microprotocol == 'StatisticsContingency':
        return MicroprotocolStatisticsContingency

    if microprotocol == 'StatisticsUnivariate':
        return MicroprotocolStatisticsUnivariate

    if microprotocol == 'StatisticsContingencyVertical':
        return MicroprotocolStatisticsContingencyVertical

    if microprotocol == 'StatisticsRegressionOLSVertical':
        return MicroprotocolStatisticsRegressionOLSVertical

    raise federatedsecure.server.exceptions.NotAvailable(microprotocol)
