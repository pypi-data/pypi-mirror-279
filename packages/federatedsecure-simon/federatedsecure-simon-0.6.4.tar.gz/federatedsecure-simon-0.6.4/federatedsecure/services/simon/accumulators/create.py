import federatedsecure.server

from federatedsecure.services.simon.accumulators.\
    accumulator_kth_element import AccumulatorKthElement
from federatedsecure.services.simon.accumulators.\
    accumulator_basic_minimum_maximum import AccumulatorBasicMinimumMaximum
from federatedsecure.services.simon.accumulators.\
    accumulator_basic_sum import AccumulatorBasicSum
from federatedsecure.services.simon.accumulators.\
    accumulator_generic import AccumulatorGeneric
from federatedsecure.services.simon.accumulators.\
    accumulator_basic_array import AccumulatorBasicArray
from federatedsecure.services.simon.accumulators.\
    accumulator_set_intersection import AccumulatorSetIntersection
from federatedsecure.services.simon.accumulators.\
    accumulator_set_intersection_size import AccumulatorSetIntersectionSize
from federatedsecure.services.simon.accumulators.\
    accumulator_statistics_bivariate import AccumulatorStatisticsBivariate
from federatedsecure.services.simon.accumulators.\
    accumulator_statistics_frequency import AccumulatorStatisticsFrequency
from federatedsecure.services.simon.accumulators.\
    accumulator_statistics_contingency import AccumulatorStatisticsContingency
from federatedsecure.services.simon.accumulators.\
    accumulator_statistics_univariate import AccumulatorStatisticsUnivariate
from federatedsecure.services.simon.accumulators.\
    accumulator_generic_dictionary import AccumulatorGenericDictionary
from federatedsecure.services.simon.accumulators.\
    accumulator_generic import AccumulatorGeneric

from federatedsecure.server.exceptions import NotAvailable


def create(accumulator_name):

    if accumulator_name == 'KthElement':
        return AccumulatorKthElement

    if accumulator_name == 'MinimumMaximum':
        return AccumulatorBasicMinimumMaximum

    if accumulator_name == 'SecureSum':
        return AccumulatorBasicSum

    if accumulator_name == 'SecureMatrixMultiplication':
        return AccumulatorGeneric

    if accumulator_name == 'SecureMedian':
        return AccumulatorBasicArray

    if accumulator_name == 'SetIntersection':
        return AccumulatorSetIntersection

    if accumulator_name == 'SetIntersectionSize':
        return AccumulatorSetIntersectionSize

    if accumulator_name == 'StatisticsBivariate':
        return AccumulatorStatisticsBivariate

    if accumulator_name == 'StatisticsFrequency':
        return AccumulatorStatisticsFrequency

    if accumulator_name == 'StatisticsContingency':
        return AccumulatorStatisticsContingency

    if accumulator_name == 'StatisticsUnivariate':
        return AccumulatorStatisticsUnivariate

    if accumulator_name == 'StatisticsContingencyVertical':
        return AccumulatorGenericDictionary

    if accumulator_name == 'StatisticsRegressionOLSVertical':
        return AccumulatorGeneric

    raise federatedsecure.server.exceptions.NotAvailable(accumulator_name)
