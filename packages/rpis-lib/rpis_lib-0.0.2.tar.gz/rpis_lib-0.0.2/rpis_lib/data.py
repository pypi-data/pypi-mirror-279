import csv


class DataFabricator:
    def __init__(self, n: int):
        """
        :param n: length of data
        """
        self.n = n

    def mean(self, mean: float) -> list[float]:
        """
        :param mean: mean of data
        :return: generated data
        """
        return [mean] * self.n

    def p(self, p: int) -> list[float]:
        """
        :param p: number of successes in data
        :return: generated data
        """
        return [0] * (self.n - p) + [1] * p


class DataImporter:
    def __init__(self, sep=" ", decimal=","):
        """
        Creates DataImporter for importing data form string
        :param sep: separator between columns
        :param decimal: char use for decimal values
        """
        self.sep = sep
        self.decimal = decimal

    def get(self, string: str) -> list[float]:
        """
        Imports data from string
        :param string: data to import
        :return: imported data
        """
        return [float(x) for x in string.strip().replace(self.decimal, ".").split(self.sep)]


class CSVImporter:
    def __init__(self, filename, delimiter=";"):
        """
        Creates CSVImporter for importing data from CSV file
        :param filename: Filename of CSV file
        :param delimiter: char use for delimiter values
        """
        with open(filename) as csvfile:
            r = csv.reader(csvfile, delimiter=delimiter)
            data = [[ele for ele in row] for (i, row) in enumerate(r)]
            self.headers = data[0]
            self.data = data[1:]

    def __getitem__(self, key: str | int) -> list[float]:
        """
        Gets key from CSV file
        :param key: key to get
        :return: data from CSV file
        """
        if isinstance(key, str):
            key = self.headers.index(key)
        return [ele[key] for ele in self.data]

    def __len__(self):
        """
        Gets length of data
        :return: length of data
        """
        return len(self.data)

    def keys(self):
        """
        Returns keys of data
        :return: list of keys
        """
        return self.headers

    def __repr__(self):
        return "\t".join(self.headers) + "\n\n" + "\n".join("\t".join(row) for row in self.data)
