# people-news

Project for extracting the posts from a few Croatian portals, which contain the any of the names in the given set. 

SETUP

First install mongodb, start it and run the following:

```javascript
db.posts.createIndex( { titleHash: 1 }, { unique: true } ) // create index, do this inside mongo console
```

Then do this in the root of the project:

```bash
npm install
pip3 install flask # this is used to create an api
pip3 install pymongo

python3.8 hrlex.py <lex-file> <output-file> # process lex file and output only names in the output file

python3.8 ./api/api.py # start server for ner
python3.8 ./api/server/index.py # start server for serving posts from db
node ./scraper/index.js # start the scraping service

# TESTING
node testScrape.js # write the wanted parameters in the constants on top first, you need to have the python api running
```

Works with:
Python 3.8.10
NodeJS v14.16.0
