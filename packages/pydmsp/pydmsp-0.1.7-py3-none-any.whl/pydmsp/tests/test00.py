from pydmsp import unzip
from pydmsp import make_xr_dataset
from pydmsp import make_transform_dataset

import os

filepath = 'C:\\Users\\HOME\\PycharmProjects\\dmspreader_repo\\pydmsp\\tests\\j5f1607276.gz'
unzip(filepath)

xr_dataset = make_xr_dataset(filepath)
print(xr_dataset)
print('\n')

xr_transform = make_transform_dataset(filepath)
print(xr_transform)




# mypath = 'C:\\Users\\HOME\\PycharmProjects\\dmspreader_repo\\pydmsp\\tests\\'
# files = os.listdir(mypath)
# files = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f)) and '.gz' in f]
# for f in files:
#     print(f)
#     unzip(f)
#     xr_dataset = make_transform_dataset(f)
