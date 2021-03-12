# Malcolm Jeffers
# CS 361 W21
import subprocess

from flask import json
from tkinter import *
from tkinter.ttk import *
import argparse
import csv
import sys
import urllib.request
from Utilties.wikiexception import find_exception
from bs4 import BeautifulSoup
from Utilties.US_States import *


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
    """Finds matching keywords in a paragraph."""
    # Search through each paragraph and look for matching keywords.
    for paragraph in soup.find_all('p'):
        if row[0].lower() in paragraph.text.lower() and \
                row[1].lower() in paragraph.text.lower():
            row.append(paragraph.text)
            break
    try:  # Add a statement to the row if no results are found
        row[2]
    except IndexError:
        row.append('Matching primary and secondary keywords not found.')
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


def get_random_address(state):
    """Gets a random address from the person generator
    microservice."""
    if state in person_gen_states:
        try:
            address_result = urllib.request.urlopen('http://127.0.0.1:5002/get?state=' + state + '&number=1')
            address_data = address_result.read()
            address_response = json.loads(address_data)
            return address_response
        except urllib.error.HTTPError:
            return
    else:
        return {"addresses": ["Selected state is not currently supported."]}
    pass


def get_population(state):
    """Gets a population from the population generator
    microservice."""
    try:
        pop_result = urllib.request.urlopen('http://127.0.0.1:5003/get?state=' + state + '&year=2019')
        data = pop_result.read()
        response = json.loads(data)
        return response
    except urllib.error.URLError:
        return {"population": "Population not found"}


def cli(csv_file):
    """Process command line csv file."""
    input_list = csv_opener(csv_file)
    print("Searching for keyword pairs from input.csv")
    input_list = wikiscraper(input_list)
    csv_file_writer(input_list)
    print("Search completed successfully. See output.csv for results.")


class Controller:
    """This class controls the GUI"""

    def __init__(self):
        self.root = Tk()
        self.model = Model(self.root, self)
        self.view = View(self.root, self, self.model)
        self.root.title("Content Generator")
        self.root.geometry("600x400")
        self.root.mainloop()


class Model:
    """This class controls the functions in th GUI"""

    def __init__(self, main, controller):
        self.main = main
        self.cont = controller
        self.keyWord1 = StringVar()
        self.keyword2 = StringVar()
        self.address_bool = BooleanVar(self.main, True)
        self.population_bool = BooleanVar(self.main, True)

    def get_wiki_output(self, pri_keyword, sec_keyword):
        """This function gets wikipedia results for the
        primary and secondary keywords."""
        content = [[pri_keyword.get(), sec_keyword.get()]]
        results = wikiscraper(content)
        self.cont.view.output.insert(END, results[0][2])
        csv_file_writer(results)

    def generate_content(self):
        """Generates content for wiki, address, and population."""
        self.clear_content()
        state_code = Name_to_Abbreviation(self.cont.view.state_box.get())
        self.get_wiki_output(self.keyWord1, self.keyword2)
        if self.address_bool.get():
            self.get_address_output(state_code)
        if self.population_bool.get():
            self.get_state_population(state_code)

    def get_address_output(self, state):
        """Gets a random address from the person gen microservice."""
        rand_address = get_random_address(state)
        self.cont.view.address_output.insert(END, rand_address['addresses'][0])

    def get_state_population(self, state):
        """Gets a states population from the population generator
        microservice."""
        pop_result = get_population(state)
        self.cont.view.population_output.insert(END, state + " " + pop_result["population"])

    def clear_content(self):
        """Clears content from output cells."""
        self.cont.view.population_output.delete('1.0', END)
        self.cont.view.address_output.delete('1.0', END)
        self.cont.view.output.delete('1.0', END)

    def open_help(self):
        """Opens documentation"""
        subprocess.Popen("documentation.pdf", shell=True)


class View:
    """Creates and places objects on the GUI"""

    def __init__(self, main, controller, model):
        self.controller = controller
        self.model = model
        self.frame = main
        self.setup()

    def setup(self):
        self.create_content_gen_widgets()
        self.create_pop_gen_widgets()
        self.create_person_gen_widgets()
        self.create_menu()

    def create_content_gen_widgets(self):
        self.create_primary_widget()
        self.create_secondary_widget()
        self.create_instruction()
        self.create_wiki_output()

    def create_pop_gen_widgets(self):
        self.create_population_output()
        self.create_output_button()

    def create_person_gen_widgets(self):
        self.create_state_select_box()
        self.create_address_output()

    def create_instruction(self):
        inst_label = Label(self.frame, text='Input a Primary and Secondary Keyword. '
                                            'Then press enter to generate results '
                                            'from Wikipedia.')
        inst_label.grid(row=0, columnspan=3, sticky=W)

    def create_primary_widget(self):
        pri_label = Label(self.frame, text='Primary Keyword')
        self.primary_key = Entry(self.frame, textvariable=self.model.keyWord1)
        pri_label.grid(row=1, column=0, sticky=W, pady=2)
        self.primary_key.grid(row=1, column=1, pady=2, sticky=W)

    def create_secondary_widget(self):
        sec_label = Label(self.frame, text='Secondary Keyword')
        self.secondary_key = Entry(self.frame, textvariable=self.model.keyword2)
        sec_label.grid(row=2, column=0, sticky=W)
        self.secondary_key.grid(row=2, column=1, sticky=W)

    def create_wiki_output(self):
        output_lbl = Label(self.frame, text='Wikipedia Results')
        output_lbl.grid(row=5, column=0, sticky=W)
        self.output = Text(self.frame, width=75, height=6, wrap=WORD)
        self.output.grid(row=6, column=0, columnspan=3, sticky=W)

    def create_state_select_box(self):
        state_label = Label(self.frame, text='Select a State.') \
            .grid(row=4, column=0, sticky=W)
        self.state_box = Combobox(self.frame, values=state_list)
        self.state_box.grid(row=4, column=1, sticky=W)
        self.state_box.current(0)

    def create_address_output(self):
        self.address_chk = Checkbutton(self.frame, text='Create a random address for a selected state',
                                       var=self.model.address_bool)
        self.address_chk.grid(row=3, column=0, sticky=W)
        address_result_lbl = Label(self.frame, text='Created Random Address') \
            .grid(row=8, column=0, sticky=W)
        self.address_output = Text(self.frame, width=75, height=2, wrap=WORD)
        self.address_output.grid(row=9, column=0, columnspan=3, sticky=W)

    def create_population_output(self):
        population_chk = Checkbutton(self.frame, text='Get population of a selected State',
                                     var=self.model.population_bool)
        population_chk.grid(row=3, column=1, sticky=W)
        population_results_lbl = Label(self.frame, text='Population of Selected State in 2019')
        population_results_lbl.grid(row=10, column=0, sticky=W)
        self.population_output = Text(self.frame, width=25, height=1)
        self.population_output.grid(row=11, column=0, columnspan=1, sticky=W)

    def create_output_button(self):
        self.btn = Button(self.frame, text='Generate Content', command=self.model.generate_content) \
            .grid(row=4, column=2, sticky=W)

    def create_menu(self):
        menubar = Menu(self.frame)
        self.create_file_menu(menubar)
        self.create_help_menu(menubar)
        self.frame.config(menu=menubar)

    def create_file_menu(self, menubar):
        file = Menu(menubar, tearoff=False)
        file.add_command(label="Exit", command=self.frame.destroy)
        menubar.add_cascade(label="File", menu=file, underline=0)

    def create_help_menu(self, menubar):
        menu_help = Menu(menubar, tearoff=False)
        menu_help.add_command(label="View Documentation", command=self.model.open_help)
        menubar.add_cascade(label="Help", menu=menu_help, underline=0)


if __name__ == "__main__":
    # If no system arguments on startup load GUI else try CLI
    if len(sys.argv) == 1:
        Controller()
    else:
        cli_inputs = get_input_file()
        args = cli_inputs.parse_args()
        if args.filename != "input.csv":
            print("Please select an input.csv file.")
        else:
            cli(args.filename)
