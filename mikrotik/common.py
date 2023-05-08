#!/usr/bin/env python3
# -*- coding: utf-8 -*-
def printError(text):
    # Print in red text
    print("\033[91m{}\033[00m".format(text))

def printWarning(text):
    # Print in yellow text
    print("\033[93m{}\033[00m".format(text))

def printOK(text):
    # Print in green text
    print("\033[92m{}\033[00m".format(text))

def printHeadline(text):
    # Print text in bold
    print("\033[1m{}\033[00m".format(text))


