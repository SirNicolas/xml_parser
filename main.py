import time
import csv
import os
from zip_creator import create_zip
from zip_parser import parse_zip
from multiprocessing import Pool, cpu_count


def zip_template(x):
    return 'file_{}.zip'.format(x)


def parse_zip_function(i):
    zip_name = zip_template(i)
    return parse_zip(zip_name, remove_zip=True)


def create_zip_function(i):
    zip_name = zip_template(i)
    create_zip(zip_name, i)


def remove_files(*args):
    for filename in args:
        if os.path.exists(filename):
            os.remove(filename)


def prepare_csv_file(csv_filename, fields):
    file = open(csv_filename, 'a')
    file_writer = csv.DictWriter(file, fieldnames=fields)
    file_writer.writeheader()

    return file, file_writer


if __name__ == '__main__':
    timer = time.time()
    pool = Pool(cpu_count())
    header_filename = 'head.csv'
    body_filename = 'body.csv'
    zip_number = 50
    remove_files(header_filename, body_filename)

    # create zip
    pool.map(create_zip_function, range(zip_number))

    header, header_writer = prepare_csv_file(header_filename, ['id', 'level'])
    body, body_writer = prepare_csv_file(body_filename, ['id', 'object_name'])

    # parse zip
    for header_data, body_data in pool.map(parse_zip_function, range(zip_number)):
        for xml_id, xml_level in header_data:
            header_writer.writerow({'id': xml_id, 'level': xml_level})
        for xml_id, object_name in body_data:
            body_writer.writerow(
                {'id': xml_id, 'object_name': object_name})
    header.close()
    body.close()
    print('Затраченное время {}c'.format(time.time() - timer))
    print('Результаты в файлах: {} и {}'.format(header_filename, body_filename))
