# Investing-News-Scraping
This repo contain the python code for scraping news form investing website. There are two types of file generated news-meta data file and main-article file.

## Setup

To run this project, install all the dependencies in the requirments.txt:

```
$ pip install -r requirements.txt
```

## Usage
```
>> from investing import Investing
```
Add company's name.
reliance-industries is code of Reliance Industries.
```
>> obj = MoneyControl("reliance-industries")
```
Get headline and url link of content
```
>> obj.headline("file-name.csv")
```
Get the content of each article and store it in separate file
```
>> obj.content("file-name.csv)
```
