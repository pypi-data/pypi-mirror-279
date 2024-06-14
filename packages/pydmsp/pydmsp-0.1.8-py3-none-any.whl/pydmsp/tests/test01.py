from pydmsp import unzip
from pydmsp import make_xr_dataset
from pydmsp import make_transform_dataset


def get_num_of_hours_mins_secs(filepath, mode='to_ram'):
    res = unzip(filepath, mode=mode)
    print(res)
    print('Общее количество записей:', res.shape)
    records_count, _reminder = divmod(res.shape[0], 2640)
    print(records_count, _reminder)

    res = res.reshape(records_count, 2640)
    print(res)

    hours = set(res[:, 1])
    print('hours:\n', *hours)
    print(len(hours))

    mins = res[:, 2]
    print('mins:\n', *mins)
    print(mins.shape)

    secs = res[:, 3]
    print('secs:\n', *secs)
    print(secs.shape)


filepath = 'j4f0682362.gz'
get_num_of_hours_mins_secs(filepath)





# res = res[:, 15:2595]
# print(res.shape)

# print(res1.shape[1]/60, res1.shape[1]%60)
# res1 = res1[:, 15:2595].reshape(shape1, 43, 60)
# print(shape1, shape1/2640, shape1%2640, res1/60, res1%60)
#
# shape2, res2 = print_raw_and_shape(filepath2)
# res2 = res2[:, 15:2595].reshape(shape2, 43, 60)
# print(shape2, shape2/2640, shape2%2640)
#
# shape3, res3 = print_raw_and_shape(filepath3)
# res3 = res3[:, 15:2595].reshape(shape3, 43, 60)
# print(shape3, shape3/2640, shape3%2640)


# res1 = unzip(filepath1, mode='to_ram')
# print(res1)
# print(res1.shape)
# print()

# res2 = unzip(filepath2, mode='to_ram')
# print(res2)
# print(res2.shape)

# xr_dataset = make_xr_dataset(filepath)
# print(xr_dataset)
# print('\n')
#
# xr_transform = make_transform_dataset(filepath)
# print(xr_transform)
