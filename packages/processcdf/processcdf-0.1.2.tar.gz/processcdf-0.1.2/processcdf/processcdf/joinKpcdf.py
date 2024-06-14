import numpy as np
import pandas as pd
import argparse


def _read_kps_hdf(filename):
    '''
    Выполняет чтение бинарного hdf-файла со значениями Kp-индекса в DataFrame, полученного с помощью утилиты "json2hdf"

    :param filename: (string) путь к бинарному hdf-файлу

    :return: df: (pandas.DataFrame) набор данных DataFrame со значениями Kp-индекса
    '''
    df = pd.read_hdf(filename, 'df')
    return df


def _read_cdf_hdf(filename):
    '''
    Выполняет чтение бинарного hdf-файла с переменными из объединенных CDF-файлов с помощью утилиты "merge_cdf"

    :param filename: (string) путь к бинарному hdf-файлу

    :return: df: (pandas.DataFrame) набор данных DataFrame с переменными CDF-файлов
    '''
    df = pd.read_hdf(filename, 'df')
    return df


def _join_dfs(filename_kps, filename_cdfs):
    '''
    Выполняет объединение двух DataFrame - со значениями Kp-индекса и с переменными CDF-файлов
    на основании периода времени (столбцов "год", "месяц", "день", "час")

    :param filename_kps: (string) путь к бинарному hdf-файлу со значениями Kp-индекса
           filename_cdfs: (string) путь к бинарному hdf-файлу с переменными CDF-файлов

    :return: df: (pandas.DataFrame) объединенный набор данных DataFrame
    '''
    df_kps = _read_kps_hdf(filename_kps)
    df_cdfs = _read_cdf_hdf(filename_cdfs)

    df = pd.merge(df_kps, df_cdfs, how='inner', on=['year', 'month', 'day', 'hour'])

    return df


def _save2hdf(filename_kps, filename_cdfs, filename):
    '''
    Выполняет сохранение объединенного DataFrame в бинарный hdf-файл

    :param filename_kps: (string) путь к бинарному hdf-файлу со значениями Kp-индекса
           filename_cdfs: (string) путь к бинарному hdf-файлу с переменными CDF-файлов
           filename: (string) имя бинарного hdf-файла для сохранения объединенного DataFrame

    :return: None
    '''
    df = _join_dfs(filename_kps, filename_cdfs)
    df.to_hdf(filename, key='df', mode='w')



if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description='Combining files with kp index data and CDF data into one new HDF file.')
    parser.add_argument('filename_kps', type=str, help='The filename with kp index values')
    parser.add_argument('filename_cdfs', type=str, help='The filename with the CDF files data')
    parser.add_argument('out_filename', type=str, help='The name of the HDF file to record the DataFrame')
    args = parser.parse_args()

    filename_kps = args.filename_kps
    filename_cdfs = args.filename_cdfs
    out_filename = args.out_filename

    _save2hdf(filename_kps, filename_cdfs, out_filename)
