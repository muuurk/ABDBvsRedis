# importing Statistics module
import statistics
import pandas as pd

scenarios = []

function_mappings = {'server_a': 0, 'server_b': 0, 'server_c': 0, 'stdev': 0}
for i in range(18, 0, -1):
    # number of function on the first server
    function_mappings['server_a'] = i
    for j in range(1, 20 - function_mappings['server_a']):
        function_mappings['server_b'] = j
        function_mappings['server_c'] = 20 - function_mappings['server_a'] - function_mappings['server_b']
        function_mappings['stdev'] = statistics.stdev(
            [function_mappings['server_a'], function_mappings['server_b'], function_mappings['server_c']])
        scenarios.append(function_mappings.copy())

scenarios_sorted = sorted(scenarios, key=lambda d: d['stdev'])
print(scenarios_sorted)

reads = [6, 13, 8, 14, 6, 10, 8, 6, 11, 7, 3, 12, 8, 13, 5, 6, 10, 7, 10, 9]
writes = [8, 8, 10, 7, 11, 7, 11, 13, 8, 13, 2, 10, 10, 10, 5, 5, 8, 12, 5, 11]
# the majority of functions are NOT co-located with the Redis
bad_df = pd.DataFrame({})
# the majority of functions are co-located with the Redis
good_df = pd.DataFrame({})

# for good locations
for scenario in scenarios_sorted:
    iter = 0
    if scenario['server_a'] >= scenario['server_b'] and scenario['server_a'] >= \
            scenario['server_c']:
        server_a = 0
        server_b = 1
        server_c = 2
    elif scenario['server_b'] >= scenario['server_a'] and scenario['server_b'] >= \
            scenario['server_c']:
        server_a = 1
        server_b = 0
        server_c = 2
    else:
        server_a = 1
        server_b = 2
        server_c = 0

    for i in range(scenario['server_a']):
        good_df = good_df.append(
            {'function': 'f{}'.format(iter), 'key': 'k1', 'Read/sec': reads[iter], 'Write/sec': writes[iter],
             'server where to deploy initially': server_a}, ignore_index=True)
        iter += 1
    for i in range(scenario['server_b']):
        good_df = good_df.append(
            {'function': 'f{}'.format(iter), 'key': 'k1', 'Read/sec': reads[iter], 'Write/sec': writes[iter],
             'server where to deploy initially': server_b}, ignore_index=True)
        iter += 1
    for i in range(scenario['server_c']):
        good_df = good_df.append(
            {'function': 'f{}'.format(iter), 'key': 'k1', 'Read/sec': reads[iter], 'Write/sec': writes[iter],
             'server where to deploy initially': server_c}, ignore_index=True)
        iter += 1

    good_df.to_csv('measurements/good_redis_scenario_stdev_{}.csv'.format(scenario['stdev']),index=False)
    print('good_redis_scenario_stdev_{}.csv'.format(scenario['stdev']))
    good_df = pd.DataFrame({})

print('\n')
# for bad locations
for scenario in scenarios_sorted:
    iter = 0
    if scenario['server_a'] >= scenario['server_b'] and scenario['server_a'] >= \
            scenario['server_c']:
        server_a = 1
        server_b = 0
        server_c = 2
    elif scenario['server_b'] >= scenario['server_a'] and scenario['server_b'] >= \
            scenario['server_c']:
        server_a = 0
        server_b = 1
        server_c = 2
    else:
        server_a = 0
        server_b = 2
        server_c = 1

    for i in range(scenario['server_a']):
        good_df = good_df.append(
            {'function': 'f{}'.format(iter), 'key': 'k1', 'Read/sec': reads[iter], 'Write/sec': writes[iter],
             'server where to deploy initially': server_a}, ignore_index=True)
        iter += 1
    for i in range(scenario['server_b']):
        good_df = good_df.append(
            {'function': 'f{}'.format(iter), 'key': 'k1', 'Read/sec': reads[iter], 'Write/sec': writes[iter],
             'server where to deploy initially': server_b}, ignore_index=True)
        iter += 1
    for i in range(scenario['server_c']):
        good_df = good_df.append(
            {'function': 'f{}'.format(iter), 'key': 'k1', 'Read/sec': reads[iter], 'Write/sec': writes[iter],
             'server where to deploy initially': server_c}, ignore_index=True)
        iter += 1

    good_df.to_csv('measurements/bad_redis_scenario_stdev_{}.csv'.format(scenario['stdev']),index=False)
    print('bad_redis_scenario_stdev_{}.csv'.format(scenario['stdev']))
    good_df = pd.DataFrame({})
