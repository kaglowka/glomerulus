import os
import csv

class FileStorage:
    data_path = '../data'

    def get_data(self, name):
        return open(os.path.join(self.data_path, name), 'r', encoding='utf-8')

    def save_data(self, name, str, flag='w+'):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        with open(os.path.join(self.data_path, name), flag, encoding='utf-8') as data_file:
            data_file.write(str)

    def save_csv(self, row, file_name, flag='a'):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        with open(os.path.join(self.data_path, file_name), flag, newline='', encoding='utf-8') as csv_file:
            article_writer = csv.writer(csv_file, delimiter="|", quotechar="^")
            article_writer.writerow(row)
