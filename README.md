# WorshipSheets

`WorshipSheets` is intended to create worship lyric sheets for bible studies by using a string of URLs from popular Christian music websites such as pnwchords, essentialworship, worshipchords, worshiptogether and other similar websites. 

`WorshipSheets` will strip out any chords and format sections such as Verse, Pre-Chorus and Chorus and output to a `.docx` file. 

## Current Websites Supported:

[WorshipChords](https://worshipchords.com/)

## Current Functionality: 

`WorshipSheets` currently only supports one website, [WorshipChords](https://worshipchords.com/). It is able to process the scraped lyrics and output to a double column `.docx` file but is currently NOT able to print out song title or song author. 

## Environment Setup

You will need to create a python virtual environment.

```
python3 -m venv .venv
source .venv/bin/activate
```

Then you will need to install the following packages

```
pip3 install python-docx
```

## Usage

```
python3 worshipsheets.py <URL>
```