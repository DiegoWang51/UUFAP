## Project introduction

UUFAP is a stupid acronym for University Undergraduate Freshman Admission Prediction. We intend to use this system to predict the admission results based on a set of standardized test scores and unquantifiable qualities, via currently undecided AI algorithms.

We intend to crawl answers from a hot ZhiHu question,

https://www.zhihu.com/question/66515131,

and analyze information from it. Then we process the obtained data. Then we use AI algorithms to analyze it.

Currently we did the first step, to crawl answers from the above question.

## Files in this repository

### README.md

This file is README.md.

### crawler.ipynb

This is the crawler script. There are two entries in the script.

The code in the first entry attempted via a superficial crawling way, and failed to hack against the paging in the question. However, we left it there in case for future need.

The code in the second entry work well. It stores the crawling answers in rawAnswer.csv. Currently this is the only functioning code.

### crawler.py

The code in this file is identical with the code in the second entry in crawler.ipynb. However, due to the difference of python interpreters, it failed to function.

### rawAnswer.csv

A storage of all the crawling 1078 answers.

### rawAnswerBackup.csv

A backup file of rawAnswer.csv, since it is written automatically by code.

### process.ipynb

Code to process the crawled answers down to features.

To be finished.
