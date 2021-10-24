import csv

def read_cat():

    with open('data/cat.csv', encoding="utf8") as File:
        reader = csv.reader(File, delimiter=',', quotechar=',',
                        quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            title = str(row[7])
            clear_title = title.replace('"', "")
            id = str(row[1])
            author = str(row[6])
            
            print('id: ' + id + ' title: ' + clear_title + ' author: ' + author)


if __name__ == "__main__":
    read_cat()

