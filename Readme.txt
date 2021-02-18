Package Requirements

Beautiful Soup 4
Run the following command in your terminal.
pip install bs4

Flask
pip install flask

To Run content-generator.py as CLI have a csv with
primary and secondary keyword in the same folder.

python content-generator.py input.csv

To run as a GUI
python content-generator.py

To run as a microservice on your system
python server_app.py
This will start a service on local host port 5001


This is the content-generator microservice. With this program it takes a primary and secondary keyword
then returns a paragraph from Wikipedia with both words in it. The primary word is used to find the article.
Example: Primary =puppy Secondary=Dog would get https://en.wikipedia.org/wiki/Puppy. Within that page it will
look for a <p> with both puppy and dog in it. returning the first paragraph it finds.
Using a GET request to http://127.0.0.1:5001/get?pri=puppy&sec=dog and
inputting your keywords in the pri and sec slot will return the paragraph in a JSON format.


{
"primary_keyword": "puppy",
"secondary_keyword": "dog",
"wiki": "A puppy is a juvenile dog. Some puppies can weigh 1–1.5 kg (1-3 lb), while larger ones...
}
