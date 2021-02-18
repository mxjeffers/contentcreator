


I have the content generator microservice. With this program it takes a primary and secondary keyword then returns a paragraph from Wikipedia with both words in it. The primary word is used to find the article.
Example: Primary =puppy Secondary=Dog would get https://en.wikipedia.org/wiki/Puppy Within that page it will look for a <p> with both puppy and dog in it returning the first one paragraph it finds. I adjusted my app to deploy on Heroku. Using a GET https://contentgenerator261w21.herokuapp.com/get/?pri=puppy&sec=dog and inputting your keywords in the pri and sec slot will return the paragraph in a JSON format.
{
"primary_keyword": "puppy",
"secondary_keyword": "dog",
"wiki": "A puppy is a juvenile dog. Some puppies can weigh 1–1.5 kg (1-3 lb), while larger ones can weigh up to 7–11 kg (15-23 lb). All healthy puppies grow quickly after birth. A puppy's coat color may change as the puppy grows older, as is commonly seen in breeds such as the Yorkshire Terrier. Puppy refers specifically to young dogs,[1] while pup may be used for other animals such as wolves, seals, giraffes, guinea pigs, rats or sharks.[2] "
} (edited)
