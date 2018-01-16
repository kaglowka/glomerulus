import os

class FileStorage:
    data_path = '../data'

    def get_data(self, name):
        return open(os.path.join(self.data_path, name), 'r')

    def save_data(self, name, str, flag='w+'):
        if not os.path.exists(self.data_path):
            os.makedirs(self.data_path)

        with open(os.path.join(self.data_path, name), flag) as data_file:
            data_file.write(str)