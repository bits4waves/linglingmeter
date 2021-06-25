#!/bin/bash

# /html/body/div/div/div[2]/div[2]/div[5]/div[1]/div/div/div[2]/div[2]
# /html/body/div/div/div[2]/div[2]/div[5]/div[1]/div/div/div[635]/div[2]
xmllint --xpath '//div[contains(concat(" ", @class, " "), " c02 ")]' catgut-papers.html > catgut-papers.txt

