import csv


def read_recs():

    with open('data/recs.csv') as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            print(row)


if __name__ == "__main__":
    read_recs()

