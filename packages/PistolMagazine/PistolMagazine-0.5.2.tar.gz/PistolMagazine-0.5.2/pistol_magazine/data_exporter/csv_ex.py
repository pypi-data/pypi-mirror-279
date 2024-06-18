import csv
from .exporter import Exporter


class CSVExporter(Exporter):
    def export(self, data, filename):
        if isinstance(data, dict):
            data = [data]
        keys = data[0].keys()
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
