# Malcolm Jeffers
# CS 361 W21

try:
    from tkinter import *
except:
    pass

import argparse
import csv
import sys
import urllib.request
from wikiexception import find_exception
from bs4 import BeautifulSoup


def csv_opener(filename):
    """ This function opens a csv file."""
    with open(filename, newline='') as f:
        csv_keywords = csv.reader(f)

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
        try:
            # Strip input of spaces and replace with underscore
            wikipage = find_exception(row[0])
            content = urllib.request.urlopen('https://en.wikipedia.org/wiki/' + wikipage.replace(" ","_"))
            read_content = content.read()
            soup = BeautifulSoup(read_content, 'html.parser')
            pAll = soup.find_all('p')

            # Go through each paragraph and look for keywords.
            for paragraph in pAll:
                if row[0].lower() in paragraph.text.lower() and row[1].lower() in paragraph.text.lower():
                    row.append(paragraph.text)
                    break
            # Add a statement to the row if no results are found
            try:
                row[2]
            except IndexError:
                row.append("Matching primary and secondary keywords not found.")

        # This handles 404 errors
        except urllib.error.HTTPError:
            row.append("Wikipedia article not found")

    return search_list


def csv_file_writer(content):
    """ This function writes data to a csv file."""
    header = ['input_keywords', 'output_content']

    # Create and overwrite the csv file.
    with open('output.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

        # Combine keywords with semicolon then write row
        for row in content:
            row[0] += ";" + row[1]
            row.pop(1)
            writer.writerow(row)


def get_input_file():
    """ Parses the input file on startup"""
    parser = argparse.ArgumentParser(description='input.csv filename')
    parser.add_argument("filename")
    return parser


def GUI():
    #Tkinter GUI

    def get_wiki_output():
        output.delete('1.0', END)
        content = [[keyWord1.get(), keyWord2.get()]]
        results = wikiscraper(content)

        # Place results in output container
        output.insert(END, results[0][2])
        csv_file_writer(results)

    # Root is main window
    root = Tk()
    root.title("Content Generator")
    root.geometry("600x200")
    keyWord1 = StringVar()
    keyWord2 = StringVar()

    # Primary Keyword
    Pri_label = Label(root, text='Primary Keyword')
    Primary_key = Entry(root, textvariable=keyWord1)

    # Secondary Keyword
    Sec_label = Label(root, text='Secondary Keyword')
    Secondary_key = Entry(root, textvariable=keyWord2)

    # Button
    btn = Button(root, text='Enter', bd='5', command=get_wiki_output)
    btn.grid(row=4, column=0, sticky=W)

    # Output Box
    output = Text(root, width=75, height=6, wrap=WORD)

    # Instructions
    Inst_label = Label(root, text='Input a Primary and Secondary Keyword. Then press enter '
                                  'to generate results form Wikipedia.')
    # GRID LOCATIONS
    Inst_label.grid(row=0,columnspan=3, sticky=W)
    Pri_label.grid(row=1, column=0, sticky=W, pady=2)
    Primary_key.grid(row=1, column=1, pady=2, sticky=W)
    Sec_label.grid(row=2, column=0, sticky=W)
    Secondary_key.grid(row=2, column=1, sticky=W)
    output.grid(row=3, column=0, columnspan=4)
    root.mainloop()


if __name__ == "__main__":
    # GUI section
    # If no system arguments on startup load GUI else try CLI
    if len(sys.argv) == 1:
        try:
            GUI()
        except:
            pass
    else:
        parser = get_input_file()
        args = parser.parse_args()

        if args.filename != "input.csv":
            print("Please enter input.csv file.")
            exit()
        else:
            # CLI section
            input_list = csv_opener(args.filename)
            print("Searching for keyword pairs from input.csv")
            input_list = wikiscraper(input_list)
            csv_file_writer(input_list)
            print("Search completed successfully. See output.csv for results.")
