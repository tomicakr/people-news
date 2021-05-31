# people-news

First install mongodb, start it and run the following:

```javascript
db.posts.createIndex( { titleHash: 1 }, { unique: true } ) // create index, do this inside mongo console
```

Then do this in the root of the project:

```bash
npm install
pip3 install flask # this is used to create an api

python hrlex.py <lex-file> <output-file> # process lex file and output only names in the output file

python ./api/api.py ./api/names.txt # start server for ner, names.txt contains all names in croatian language, along with their frequencies
node ./scraper/index.js # start the scraping service

# TESTING
node testScrape.js # write the wanted parameters in the constants on top first, you need to have the python api running
```
