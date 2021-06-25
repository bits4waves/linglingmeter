#!/bin/bash

xmllint --xpath '//div[contains(concat(" ", @class, " "), " c02 ")]' catgut-papers.html > catgut-papers.txt

