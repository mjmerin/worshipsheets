# WorshipSheets

`WorshipSheets` is intended to create worship lyric sheets for bible studies by using a string of URLs from popular Christian music websites such as pnwchords, essentialworship, worshipchords, worshiptogether and other similar websites. 

`WorshipSheets` will strip out any chords and format sections such as Verse, Pre-Chorus and Chorus and output to a `.docx` file. 

The inspiration behind the project is having to lead worship at [New Hope International Church](https://newhic.org/) on our Wednesday night discipleship classes and needing a simple way to create lyrics sheets. 

The app is currently hosted on [Render](https://render.com/) and you can access it on [WorshipSheets](https://worshipsheets.onrender.com)

## Current Websites Supported:

[WorshipChords](https://worshipchords.com/)

[PNWChords](https://pnwchords.com)

[EssentialWorship](https://essentialworship.com/)

## Current Functionality: 

`WorshipSheets` currently only supports three websites. Other websites may work but needs additional testing and most likely addtional logic. It is able to process the scraped lyrics and output to a double column `.docx` file but is currently NOT able to print out song author. 

As each website shows the lyrics/tabs differently, formatting still needs to be customized per website. 

## Environment Setup

You will need to create a python virtual environment.

```
python3 -m venv .venv
source .venv/bin/activate
```

Then you will need to install the following packages

```
python3 -m pip install -r requirements.txt
```

## Usage

For command line usage: 
```
python3 worshipsheets.py <URL>
```

To kick off the web app:
```
python3 main.py
```

### Command Line Examples

#### Single Songs
```
python3 worshipsheets.py https://worshipchords.com/how-great-is-our-god-chords/

python3 worshipsheets.py https://pnwchords.com/i-need-you-more-kim-walker/
```

#### Multi Songs
```
python3 worshipsheets.py https://worshipchords.com/how-great-is-our-god-chords/ https://pnwchords.com/i-need-you-more-kim-walker/
```