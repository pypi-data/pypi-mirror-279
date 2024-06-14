import numpy as np
import xarray as xr
import os
from datetime import datetime as dt

from pydmsp import _makedataset as md
from pydmsp import _tablesE, _tablesG
from pydmsp._tablesG import get_G_factor
from pydmsp import unzip

ACCUMULATION_TIME_SSJ4 = 0.098
ACCUMULATION_TIME_SSJ5 = 0.05


def _convert_lat(data):
    '''
    Выполняет преобразование к физической величине переданного массива данных широты в соответствии с документацией

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: data: (массив numpy.uint16) массив значений широты в диапазоне [-90; 90]
    '''
    data = data.astype(np.float32)

    for i, elem in enumerate(data):
        data[i] = (elem - 900) / 10.0
        if elem > 1800:
            data[i] = (elem - 4995) / 10.0

    return data


def _convert_lon(data):
    '''
    Выполняет преобразование к физической величине переданного массива данных долготы в соответствии с документацией

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: data: (массив numpy.uint16) массив значений долготы в диапазоне [-180; 180]
    '''
    for i, elem in enumerate(data):
        data[i] = float(elem) / 10.0

    return data


def get_raw_geodetic_lat_converted(data):
    '''
    Выполняет преобразование массива данных геодезической широты к физическим величинам в соответствии с документацией,
    выполняет формирование переменной типа "DataArray" библиотеки "xarray"

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: da: (xarray.core.dataarray.DataArray) набор значений геодезической широты в диапазоне [-90; 90]
    '''
    data = md.get_raw_geodetic_lat(data).data
    shape = data.shape
    data = data.reshape(np.prod(shape))

    data = _convert_lat(data)
    data = data.reshape(shape)

    metadata = {
        'short_name': 'Geodetic Lat',
        'long_name': 'Geodetic latitude',
        'units': 'degrees',
        'description': 'Geodetic latitude',
        'Range': '-90.0 to 90.0',
        'Kind of data': 'Minute data'
    }

    da = xr.DataArray(data, attrs=metadata)
    return da


def get_raw_geographic_lon_converted(data):
    '''
    Выполняет преобразование массива данных географической долготы к физическим величинам в соответствии с документацией,
    выполняет формирование переменной типа "DataArray" библиотеки "xarray"

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: da: (xarray.core.dataarray.DataArray) набор значений географической долготы в диапазоне [0; 360]
    '''
    data = md.get_raw_geographic_lon(data).data
    shape = data.shape
    data = data.reshape(np.prod(shape))

    data = _convert_lon(data)
    data = data.reshape(shape)

    metadata = {
        'short_name': 'Geographic Lon',
        'long_name': 'Geographic longitude',
        'units': 'degrees',
        'description': 'Geographic longitude',
        'Range': '0.0 to 360.0',
        'Kind of data': 'Minute data'
    }

    da = xr.DataArray(data, attrs=metadata)
    return da


def get_raw_geographic_lat_110_converted(data):
    '''
    Выполняет преобразование массива данных географической широты на высоте 110 км
    к физическим величинам в соответствии с документацией,
    выполняет формирование переменной типа "DataArray" библиотеки "xarray"

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: da: (xarray.core.dataarray.DataArray) набор значений географической широты
    на высоте 110 км в диапазоне [-90; 90]
    '''
    data = md.get_raw_geographic_lat_110(data).data
    shape = data.shape
    data = data.reshape(np.prod(shape))

    data = _convert_lat(data)
    data = data.reshape(shape)

    metadata = {
        'short_name': 'Geographic Lat',
        'long_name': 'Geographic latitude',
        'units': 'degrees',
        'description': 'Geographic latitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft',
        'Range': '-90.0 to 90.0',
        'Kind of data': 'Minute data'
    }

    da = xr.DataArray(data, attrs=metadata)
    return da


def get_raw_geographic_lon_110_converted(data):
    '''
    Выполняет преобразование массива данных географической долготы на высоте 110 км
    к физическим величинам в соответствии с документацией,
    выполняет формирование переменной типа "DataArray" библиотеки "xarray"

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: da: (xarray.core.dataarray.DataArray) набор значений географической долготы
    на высоте 110 км в диапазоне [0; 360]
    '''
    data = md.get_raw_geographic_lon_110(data).data
    shape = data.shape
    data = data.reshape(np.prod(shape))

    data = _convert_lon(data)
    data = data.reshape(shape)

    metadata = {
        'short_name': 'Geographic Lon',
        'long_name': 'Geographic longitude',
        'units': 'degrees',
        'description': 'Geographic longitude at 110 km altitude and on the same magnetic field line as the DMSP spacecraft',
        'Range': '0.0 to 360.0',
        'Kind of data': 'Minute data'
    }

    da = xr.DataArray(data, attrs=metadata)
    return da


def get_raw_aacgm_lat_converted(data):
    '''
    Выполняет преобразование массива данных скорректированных геомагнитных координат широты с поправкой на высоту
    к физическим величинам в соответствии с документацией,
    выполняет формирование переменной типа "DataArray" библиотеки "xarray"

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: da: (xarray.core.dataarray.DataArray) набор значений скорректированных геомагнитных координат широты
    с поправкой на высоту в диапазоне [-90; 90]
    '''
    data = md.get_raw_aacgm_lat(data).data
    shape = data.shape
    data = data.reshape(np.prod(shape))

    data = _convert_lat(data)
    data = data.reshape(shape)

    metadata = {
        'short_name': 'Corr Geomagnetic Lat',
        'long_name': 'Corrected geomagnetic latitude',
        'units': 'degrees',
        'description': 'Corrected geomagnetic latitude at 110 km altitude',
        'Range': '-90.0 to 90.0',
        'Kind of data': 'Minute data'
    }

    da = xr.DataArray(data, attrs=metadata)
    return da


def get_raw_aacgm_lon_converted(data):
    '''
    Выполняет преобразование массива данных скорректированных геомагнитных координат долготы с поправкой на высоту
    к физическим величинам в соответствии с документацией,
    выполняет формирование переменной типа "DataArray" библиотеки "xarray"

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: da: (xarray.core.dataarray.DataArray) набор значений скорректированных геомагнитных координат долготы
    с поправкой на высоту в диапазоне [0; 360]
    '''
    data = md.get_raw_aacgm_lon(data).data
    shape = data.shape
    data = data.reshape(np.prod(shape))

    data = _convert_lon(data)
    data = data.reshape(shape)

    metadata = {
        'short_name': 'Corr Geomagnetic Lon',
        'long_name': 'Corrected geomagnetic longitude',
        'units': 'degrees',
        'description': 'Corrected geomagnetic longitude at 110 km altitude',
        'Range': '0.0 to 360.0',
        'Kind of data': 'Minute data'
    }

    da = xr.DataArray(data, attrs=metadata)
    return da


def get_raw_ss_sec_res_converted(data):
    '''
    Выполняет преобразование массива секунд наблюдений с секундным разрешением из массива данных бинарного файла
    к физическим величинам в соответствии с документацией,
    выполняет формирование переменной типа "DataArray" библиотеки "xarray"

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: da: (xarray.core.dataarray.DataArray) набор значений секунд наблюдений с секундным разрешением
    '''
    flag_ar = md.get_raw_indic_flag_for_word_18(data).data
    shape_flag = flag_ar.shape
    flag_ar = flag_ar.reshape(np.prod(shape_flag))

    data = md.get_raw_ss_sec_res(data).data
    shape_data = data.shape
    data = data.reshape(1440, 60)

    for i, flag in enumerate(flag_ar):
        if i == 60:
            break
        if flag == 1:
            data[:, i] = data[:, i] / 1000.0

    data = data.reshape(shape_data)

    metadata = {
        'short_name': 'Second',
        'long_name': 'Second for n-th second',
        'units': 'seconds',
        'description': 'Second of minute for n-th second of data',
        'Range': '0 to 59',
        'Kind of data': 'Second data'
    }

    da = xr.DataArray(data, attrs=metadata)
    return da


def _get_counts(data):
    '''
    Выполняет преобразование массива отсчетов каждого канала ионов и электронов
    к физическим величинам в соответствии с документацией

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data()
    :return: counts: (numpy.int32) 7-мерный массив количества отсчетов для каждого канала
    '''
    data = md.get_raw_second_data(data).data
    old_shape = data.shape
    new_shape = np.prod(old_shape)
    data = data.reshape(new_shape)

    counts = np.zeros(new_shape, dtype=np.float32)

    X = data % 32
    X = X.astype(int)
    Y = (data - X) / 32
    Y = Y.astype(int)
    counts = (X + 32) * 2 ** Y - 33

    counts = counts.reshape(old_shape)

    return counts


def get_Ji(data, filepath):
    '''
    Выполняет преобразование массива потока дифференциальных чисел
    к физическим величинам в соответствии с документацией

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data(),
           filepath: (string) путь к файлу gzip-архива

    :return: da: (xarray.core.dataarray.DataArray) 7-мерный массив потока дифференциальных чисел
    '''
    counts = _get_counts(data)

    flight_num = get_flight_number(filepath)
    sensor_num = get_sensor_number(filepath)
    delta_t = None
    if sensor_num == '4':
        delta_t = ACCUMULATION_TIME_SSJ4
    elif sensor_num == '5':
        delta_t = ACCUMULATION_TIME_SSJ5

    Gi_electron = get_G_factor(_tablesG.electron_G_factor)
    Gi_electron = Gi_electron[flight_num]
    Gi_ion = get_G_factor(_tablesG.ion_G_factor)
    Gi_ion = Gi_ion[flight_num]

    Ji = np.zeros(counts.shape, dtype=np.float32)

    for i in range(20):
        Ji[:, :, :, :, :, 0, i] = counts[:, :, :, :, :, 0, i] / (Gi_electron[i] * delta_t)
        Ji[:, :, :, :, :, 1, i] = counts[:, :, :, :, :, 1, i] / (Gi_ion[i] * delta_t)

    metadata = {
        'short_name': 'J_i',
        'long_name': 'Differential number flux',
        'units': '1 / (cm^2 * eV * ster * sec)',
        'description': 'Differential number flux for a specific energy channel from 1 to 20. Calculated by the formula: J_i = C_i / (G_i * delta_t), where C_i - the number of counts measured in channel i, Gi - the appropriate ion or electron channel geometric factor, ∆t - the accumulation time (0.098 sec for the SSJ4 sensor, and 0.05 sec for the SSJ5 sensor)',
        'Range': '-',
        'Kind of data': 'Second data'
    }

    da = xr.DataArray(Ji, attrs=metadata)
    return da


def get_flight_number(filepath):
    '''
    Выполняет извлечение номера спутника из пути к файлу gzip-архива

    :param filepath: (string) путь к файлу gzip-архива

    :return: flight_num: (string) символьный номер спутника миссии DMSP
    '''
    path, filename = md.get_filepath_and_filename(filepath)
    flight_num = 'F' + filename[3:5]
    return flight_num


def get_sensor_number(filepath):
    '''
    Выполняет извлечение номера датчика из пути к файлу gzip-архива

    :param filepath: (string) путь к файлу gzip-архива

    :return: sensor_num: (string) символьный номер SSJ датчика миссии DMSP
    '''
    path, filename = md.get_filepath_and_filename(filepath)
    sensor_num = filename[1]
    return sensor_num


def get_JEi(data, filepath):
    '''
    Выполняет преобразование массива дифференциального потока энергии
    к физическим величинам в соответствии с документацией

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data(),
           filepath: (string) путь к файлу gzip-архива

    :return: da: (xarray.core.dataarray.DataArray) массив дифференциального потока энергии
    '''
    Ji = get_Ji(data, filepath)
    JEi = np.zeros(Ji.shape, dtype=np.float32)

    for i in range(20):
        JEi[:, :, :, :, :, 0, i] = Ji[:, :, :, :, :, 0, i] * _tablesE.Ei[i]
        JEi[:, :, :, :, :, 1, i] = Ji[:, :, :, :, :, 1, i] * _tablesE.Ei[i]

    metadata = {
        'short_name': 'JE_i',
        'long_name': 'Differential energy flux',
        'units': '1 / (cm^2 * ster * sec)',
        'description': 'Differential energy flux for a specific energy channel from 1 to 20. Calculated by the formula: JE_i = J_i * E_i, where J_i - differential number flux, E_i - the channel central energy; It is taken from a special table "SSJ sensor values for the channel central energy (E_i) and channel spacing (delta_E_i)',
        'Range': '-',
        'Kind of data': 'Second data'
    }

    da = xr.DataArray(JEi, attrs=metadata)
    return da


def get_J(data, filepath):
    '''
    Выполняет преобразование массива потока интегрированных чисел
    к физическим величинам в соответствии с документацией

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data(),
           filepath: (string) путь к файлу gzip-архива

    :return: da: (xarray.core.dataarray.DataArray) массив потока интегрированных чисел
    '''
    Ji = get_Ji(data, filepath)
    J = np.zeros((1, 1, 24, 60, 60, 2), dtype=np.float32)

    for i in range(20):
        J[:, :, :, :, :, 0] += Ji[:, :, :, :, :, 0, i] * _tablesE.delta_Ei[i]
        J[:, :, :, :, :, 1] += Ji[:, :, :, :, :, 1, i] * _tablesE.delta_Ei[i]

    metadata = {
        'short_name': 'J',
        'long_name': 'Integrated number flux',
        'units': '1 / (cm^2 * ster * sec)',
        'description': 'Integrated number flux. Calculated by the formula: J = sum(J_i * delta_E_i), where J_i - differential number flux, delta_E_i - the channel spacing for calculating the integrated quantities; It is taken from a special table "SSJ sensor values for the channel central energy (E_i) and channel spacing (delta_E_i)"',
        'Range': '-',
        'Kind of data': 'Second data'
    }

    da = xr.DataArray(J, attrs=metadata)
    return da


def get_JE(data, filepath):
    '''
    Выполняет преобразование массива потока интегрированных энергий
    к физическим величинам в соответствии с документацией

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data(),
           filepath: (string) путь к файлу gzip-архива

    :return: da: (xarray.core.dataarray.DataArray) массив потока интегрированных энергий
    '''
    JEi = get_JEi(data, filepath)
    JE = np.zeros((1, 1, 24, 60, 60, 2), dtype=np.float32)

    for i in range(20):
        JE[:, :, :, :, :, 0] += JEi[:, :, :, :, :, 0, i] * _tablesE.delta_Ei[i]
        JE[:, :, :, :, :, 1] += JEi[:, :, :, :, :, 1, i] * _tablesE.delta_Ei[i]

    metadata = {
        'short_name': 'JE',
        'long_name': 'Integrated energy flux',
        'units': 'eV / (cm^2 * ster * sec)',
        'description': 'Integrated energy flux. Calculated by the formula: JE = sum(JE_i * delta_E_i), where JE_i - differential energy flux, delta_E_i - the channel spacing for calculating the integrated quantities; It is taken from a special table "SSJ sensor values for the channel central energy (E_i) and channel spacing (delta_E_i)"',
        'Range': '-',
        'Kind of data': 'Second data'
    }

    da = xr.DataArray(JE, attrs=metadata)
    return da


def get_E_avg(data, filepath):
    '''
    Выполняет преобразование массива средних энергий
    к физическим величинам в соответствии с документацией

    :param data: (массив numpy.uint16) массив после работы функции get_ssj_data(),
           filepath: (string) путь к файлу gzip-архива

    :return: da: (xarray.core.dataarray.DataArray) массив средних энергий
    '''
    JE = get_JE(data, filepath)
    J = get_J(data, filepath)
    E_avg = JE / J

    metadata = {
        'short_name': 'E_avg',
        'long_name': 'Mean energy',
        'units': 'eV',
        'description': 'Mean energy. Calculated by the formula: E_avg = JE / J, where JE - integrated energy flux, J - integrated number flux',
        'Range': '-',
        'Kind of data': 'Second data'
    }

    da = xr.DataArray(E_avg, attrs=metadata)
    return da


def make_transform_dataset(filepath):
    '''
    Формирует набор данных, преобразованных к физическим величинам, из файла gzip-архива DMSP

    :param filepath: (string) путь к бинарному файлу
    :return: (xarray.core.dataset.Dataset) набор данных в физических величинах
    '''
    unzip(filepath)
    path, filename = md.get_filepath_and_filename(filepath)
    data = md.get_ssj_data(filename.replace('.gz', '')).astype(float)
    year = data[0][4]+1950
    doy = data[0][0]

    iyear = np.arange(year, year + 1)
    idoy = np.arange(doy, doy + 1)
    ihour = np.arange(0, 24)
    iminute = np.arange(0, 60)
    isecond = np.arange(0, 60)
    ispecie = ['electrons', 'ions']
    ichannel = np.arange(1, 21)
    izeroblock = np.arange(0, 44)

    raw_ss_min_res = md.get_raw_ss_min_res(data)
    geodetic_lat = get_raw_geodetic_lat_converted(data)
    geographic_lon = get_raw_geographic_lon_converted(data)
    raw_altitude = md.get_raw_altitude(data)
    geographic_lat_110 = get_raw_geographic_lat_110_converted(data)
    geographic_lon_110 = get_raw_geographic_lon_110_converted(data)
    aacgm_lat = get_raw_aacgm_lat_converted(data)
    aacgm_lon = get_raw_aacgm_lon_converted(data)
    raw_aacgm_mlt_hh = md.get_raw_aacgm_mlt_hh(data)
    raw_aacgm_mlt_mm = md.get_raw_aacgm_mlt_mm(data)
    raw_aacgm_mlt_ss = md.get_raw_aacgm_mlt_ss(data)
    raw_indic_flag_for_word_18 = md.get_raw_indic_flag_for_word_18(data)
    raw_zero_block = md.get_raw_zero_block(data)

    raw_hh_sec_res = md.get_raw_hh_sec_res(data)
    raw_mm_sec_res = md.get_raw_mm_sec_res(data)
    ss_sec_res = get_raw_ss_sec_res_converted(data)
    diff_num_flux_sec_res = get_Ji(data, filepath)
    diff_energy_flux_sec_res = get_JEi(data, filepath)
    interg_num_flux_sec_res = get_J(data, filepath)
    integr_energy_flux_sec_res = get_JE(data, filepath)
    mean_energy_sec_res = get_E_avg(data, filepath)

    num_sensor, num_flight, year, doy = md.get_data_from_filename(filename)

    join_path = os.path.join(path, filename)
    file_created = os.path.getctime(join_path)
    file_created = dt.fromtimestamp(file_created).strftime('%Y-%m-%d %I:%M:%S')

    file_modified = os.path.getmtime(join_path)
    file_modified = dt.fromtimestamp(file_modified).strftime('%Y-%m-%d %I:%M:%S')

    processed_on = dt.now()

    metadata = {
        'Program': 'DMSP',
        'Discipline': ['Space Physics->Magnetospheric Science', 'Space Physics->Ionospheric Science'],
        'Descriptor': 'SSJ/' + num_sensor,
        'Flight': num_flight,
        'Time_resolution': '1 second',
        'filename': filename,
        'filepath': path,
        'file_created': file_created,
        'file_modified': file_modified,
        'processed_on': processed_on,
        'generated by': md.GENERATED_BY,
        'Note': 'Dataset converted into physical quantities'
    }

    ds = xr.Dataset(
        data_vars=dict(
            RAW_SS_MIN_RES=(['iyear', 'idoy', 'ihour', 'iminute'], raw_ss_min_res.data, raw_ss_min_res.attrs),
            GEODETIC_LAT=(['iyear', 'idoy', 'ihour', 'iminute'], geodetic_lat.data, geodetic_lat.attrs),
            GEOGRAPHIC_LON=(
            ['iyear', 'idoy', 'ihour', 'iminute'], geographic_lon.data, geographic_lon.attrs),
            ALTITUDE=(['iyear', 'idoy', 'ihour', 'iminute'], raw_altitude.data, raw_altitude.attrs),
            GEOGRAPHIC_LAT_110=(
            ['iyear', 'idoy', 'ihour', 'iminute'], geographic_lat_110.data, geographic_lat_110.attrs),
            GEOGRAPHIC_LON_110=(
            ['iyear', 'idoy', 'ihour', 'iminute'], geographic_lon_110.data, geographic_lon_110.attrs),
            AACGM_LAT=(['iyear', 'idoy', 'ihour', 'iminute'], aacgm_lat.data, aacgm_lat.attrs),
            AACGM_LON=(['iyear', 'idoy', 'ihour', 'iminute'], aacgm_lon.data, aacgm_lon.attrs),
            RAW_AACGM_MLT_HH=(['iyear', 'idoy', 'ihour', 'iminute'], raw_aacgm_mlt_hh.data, raw_aacgm_mlt_hh.attrs),
            RAW_AACGM_MLT_MM=(['iyear', 'idoy', 'ihour', 'iminute'], raw_aacgm_mlt_mm.data, raw_aacgm_mlt_mm.attrs),
            RAW_AACGM_MLT_SS=(['iyear', 'idoy', 'ihour', 'iminute'], raw_aacgm_mlt_ss.data, raw_aacgm_mlt_ss.attrs),
            RAW_INDIC_FLAG_FOR_WORD_18=(
            ['iyear', 'idoy', 'ihour', 'iminute'], raw_indic_flag_for_word_18.data, raw_indic_flag_for_word_18.attrs),
            RAW_ZERO_BLOCK=(
            ['iyear', 'idoy', 'ihour', 'iminute', 'izeroblock'], raw_zero_block.data, raw_zero_block.attrs),

            RAW_HH_SEC_RES=(
            ['iyear', 'idoy', 'ihour', 'iminute', 'isecond'], raw_hh_sec_res.data, raw_hh_sec_res.attrs),
            RAW_MM_SEC_RES=(
            ['iyear', 'idoy', 'ihour', 'iminute', 'isecond'], raw_mm_sec_res.data, raw_mm_sec_res.attrs),
            SS_SEC_RES=(
            ['iyear', 'idoy', 'ihour', 'iminute', 'isecond'], ss_sec_res.data, ss_sec_res.attrs),

            DIFF_NUM_FLUX_SEC_RES=(
                ['iyear', 'idoy', 'ihour', 'iminute', 'isecond', 'ispecie', 'ichannel'],
                diff_num_flux_sec_res.data, diff_num_flux_sec_res.attrs),
            DIFF_ENERGY_FLUX_SEC_RES=(
                ['iyear', 'idoy', 'ihour', 'iminute', 'isecond', 'ispecie', 'ichannel'],
                diff_energy_flux_sec_res.data, diff_energy_flux_sec_res.attrs),
            INTERG_NUM_FLUX_SEC_RES=(
                ['iyear', 'idoy', 'ihour', 'iminute', 'isecond', 'ispecie'],
                interg_num_flux_sec_res.data, interg_num_flux_sec_res.attrs),
            INTEGR_ENERGY_FLUX_SEC_RES=(
                ['iyear', 'idoy', 'ihour', 'iminute', 'isecond', 'ispecie'],
                integr_energy_flux_sec_res.data, integr_energy_flux_sec_res.attrs),
            MEAN_ENERGY_SEC_RES=(
                ['iyear', 'idoy', 'ihour', 'iminute', 'isecond', 'ispecie'],
                mean_energy_sec_res.data, mean_energy_sec_res.attrs)
            ),
        coords={'iyear': iyear
            , 'idoy': idoy
            , 'ihour': ihour
            , 'iminute': iminute
            , 'isecond': isecond
            , 'ispecie': ispecie
            , 'ichannel': ichannel
            , 'izeroblock': izeroblock
                },
        attrs=metadata
    )
    return ds
