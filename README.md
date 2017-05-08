# Events Hunter

Manage the diverse events happening around you in a calendar.

## Sumary

Events Hunter will feed your personal calendar from many different rss sources (also twitter) to make you easy check what's going on in your city.

**Events Hunter** does

1. Extract rss and feeds configured in `config.json`
2. Preprocess the extracted data (modules/regex_data.py) and extract links, dates, time, etc in a structured way to make easier the analysis by NLTK. 
3. Extract specific data using NLTK (modules/nltk_parse.py)

## How to use

Write the sources where you want to find the events in the `config.json` file. Twitter and rss feeds are accepted by now. Then be sure that the configuration file is in the main folder and  run: 

```
main.py 
```  

## Debug

If `debug=1`, the program will not connect to internet and will use the data on `debug/*.pickle` instead. 

## How to train the dataset

- The trained net is in the files content by `./data` folder.  
- The dataset is in ./train

## FAQ


## BUGS


## TODO

- [ ] Clean the weird text stuff (&quotes;, commas, etc.)
- [ ] Optparsing options in the main program 
- [ ] Visualization of the information in a javascript calendar

## License
