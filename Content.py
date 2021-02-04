# Malcolm Jeffers
# DO args for cli input

import argparse
import csv
import urllib.request
from bs4 import BeautifulSoup


def csv_opener(filename):
    """ This function opens a csv file."""
    with open('input.csv', newline='') as f:
        csv_keywords = csv.reader(f)
        f.close()
        csv_list = []
        # Convert the csv.reader object to a python list
        for row in csv_keywords:
            csv_list.append(row[0].split(';'))
        # Remove header row
        csv_list.pop(0)
        return csv_list


def wikiscraper(search_list):
    """ This function searches Wikipedia for a paragraph matching
        both a primary and secondary keyword."""
    # Created using https://muddoo.com/tutorials/how-to-extract-data-from-a-website-using-python/

    for row in search_list:
        content = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + row[0])
        read_content = content.read()
        soup = BeautifulSoup(read_content, 'html.parser')
        pAll = soup.find_all('p')

        # Go through each paragraph and look for keywords.
        for paragraph in pAll:
            if row[0].lower() in paragraph.text.lower() and row[1].lower() in paragraph.text.lower():
                row.append(paragraph.text)
                break
        # Add a blank to the row if no results are found
        try:
            row[2]
        except IndexError:
            row.append("")


def csv_file_writer(content):
    header = ['input_keywords', 'output_content']

    # Create and overwrite the csv file.
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        # Combine keywords with semicolon then write row
        for row in content:
            row[0] += ";" + row[1]
            row.pop(1)
            writer.writerow(row)


def get_input_file():
    parser = argparse.ArgumentParser(description=('get filename'))
    parser.add_argument("filename")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_input_file()
    print(args.filename)
    test = [["Puppy", "Large", "THis is, a test2"]]
    csv_file_writer(test)
