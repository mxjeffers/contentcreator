# Malcolm Jeffers
# CS 361 W21

# Try added to bypass Heroku. Heroku does not support tkinter

try:
    from tkinter import *
    from tkinter.ttk import *
except:
    pass

import argparse
import csv
import sys
import urllib.request
from wikiexception import find_exception
from bs4 import BeautifulSoup
from US_States import *


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
    # Created using https://muddoo.com/tutorials/how-to-
    #               extract-data-from-a-website-using-python/

    for row in search_list:
        try:
            # Strip input of spaces and replace with underscore
            wikipage = find_exception(row[0])
            content = urllib.request.urlopen('https://en.wikipedia.org/wiki/' +
                                             wikipage.replace(" ", "_"))
            soup = BeautifulSoup(content.read(), 'html.parser')
            row = keyword_matcher(soup, row)
        # This handles 404 errors
        except urllib.error.HTTPError:
            row.append("Wikipedia article not found")
    return search_list


def keyword_matcher(soup, row):
    """Finds matching keywords in a paragraph"""
    # Search through each paragraph and look for matching keywords.
    for paragraph in soup.find_all('p'):
        if row[0].lower() in paragraph.text.lower() and \
                row[1].lower() in paragraph.text.lower():
            row.append(paragraph.text)
            break
    try:  # Add a statement to the row if no results are found
        row[2]
    except IndexError:
        row.append("Matching primary and secondary "
                   "keywords not found.")
    return row


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
    # Tkinter GUI

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
    root.geometry("600x400")
    keyWord1 = StringVar()
    keyWord2 = StringVar()

    # Primary Keyword
    Pri_label = Label(root, text='Primary Keyword')
    Primary_key = Entry(root, textvariable=keyWord1)

    # Secondary Keyword
    Sec_label = Label(root, text='Secondary Keyword')
    Secondary_key = Entry(root, textvariable=keyWord2)

    # Button
    btn = Button(root, text='Generate Content', command=get_wiki_output)
    btn.grid(row=4, column=2, sticky=W)

    # Output Box
    output_lbl = Label(root, text='Wikipedia Results')
    output = Text(root, width=75, height=6, wrap=WORD)

    # Address Results
    address_result_lbl = Label(root, text='Created Random Address')
    address_output = Text(root, width=75, height=2, wrap=WORD)
    
    # Population Results
    population_results_lbl = Label(root, text='Population of Selected State')
    population_output = Text(root, width=25,height=1)

    # Combo Box
    combo_lbl = Label(root, text='Select a State.')
    combo = Combobox(root)
    combo['values'] = (1,2,3,4,5)
    combo.current(0)
    
    # Check Box for address
    address_bool = BooleanVar()
    address_bool.set(True)
    address_chk = Checkbutton(root, text='Create a random address for a selected state',
                              var=address_bool)

    # Check box for population
    population_bool = BooleanVar()
    population_bool.set(True)
    population_chk = Checkbutton(root, text='Get population of a selected State',
                                 var=population_bool)

    # Instructions
    Inst_label = Label(root, text='Input a Primary and Secondary Keyword. '
                                  'Then press enter to generate results '
                                  'from Wikipedia.')

    # GRID LOCATIONS
    Inst_label.grid(row=0, columnspan=3, sticky=W)
    Pri_label.grid(row=1, column=0, sticky=W, pady=2)
    Primary_key.grid(row=1, column=1, pady=2, sticky=W)
    Sec_label.grid(row=2, column=0, sticky=W)
    Secondary_key.grid(row=2, column=1, sticky=W)
    output_lbl.grid(row=5, column=0, sticky=W)
    output.grid(row=6, column=0, columnspan=3, sticky=W)
    combo_lbl.grid(row=4, column=0, sticky=W)
    combo.grid(row=4, column=1, sticky=W)
    address_chk.grid(row=3, column=0, sticky=W)
    population_chk.grid(row=3, column=1, sticky=W)
    address_result_lbl.grid(row=8,column=0,sticky=W)
    address_output.grid(row=9,column=0,columnspan=3, sticky=W)
    population_results_lbl.grid(row=10, column=0, sticky=W)
    population_output.grid(row=11, column=0, columnspan=1, sticky=W)
    root.mainloop()


def get_random_address():
    pass


def get_population(state):
    state_code = Name_to_Abbreviation(state)
    try:
        pop_result = urllib.request.urlopen('http://127.0.0.1:5003/')  # Needs get parameters
        return pop_result  # Needs JSON converter?
    except urllib.error.HTTPError:
        return


if __name__ == "__main__":
    # If no system arguments on startup load GUI else try CLI
    if len(sys.argv) == 1:

        GUI()

    else:
        cli_inputs = get_input_file()
        args = cli_inputs.parse_args()

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
