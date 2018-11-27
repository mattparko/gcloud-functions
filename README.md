# gcloud-functions

A dumping ground for random Google Cloud Functions

#### get-dad-joke.py
* Returns a dad joke retrieved from icanhazdadjoke.com
* Uses the Python 3.7 (Beta) runtime
* Supports Google Hangouts Chat, with bot name `@DadBot`
* Usage:
  * Get a random joke: `@DadBot random`  
  * Search for a joke: `@DadBot search <query>`  
  * Show this help message: `@DadBot help`  

#### xkcd.py
* Returns an xkcd comic, formatted using a Hangouts "card"
* Uses the Python 3.7 (Beta) runtime
* Supports Google Hangouts Chat, with bot name `@xkcd`
* Usage:
  * Get the latest comic: `@xkcd latest`
  * Get a random comic: `@xkcd random`
  * Get a specific comic: `@xkcd <number>`
  * Show this help message: `@xkcd help`
