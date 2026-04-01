# MAthoverflow and Math Steckexchange usage analysis in relation to AI

## General
With our project we want to analyse the usage and overall change that might or might not have happened due to AI.
Our goal is to determine if the release of popular generative AI like ChatGPT, Gemini or similar had a significant impact on those platforms.
Further we want to find our if a certain release of an AI like ChatGPT2 for example had a bigger impact than the initial release,
because there might have been substantial improvements to its capabilities. In our research we also want to determine the difficulty
of the questions and whether it has changed or not. Determining difficulty of mathematical questions on a large scale will not be 100% accurate,
but we will imploy multiple techniques like question length, number of fomulars, length of formulas, length of answers and their formulas and possibly more.

## Usage
This section will cover how to use the tools we built for our analysis

### Prerequisites
- Python3 (Tested on `Python3.13` and `Python 3.14`)
- Stackexchange data dump (Only mathoverflow.net.7z and math.stackexchange.com.7z was used from 2025-09-30 from the <a href="https://archive.org/details/stackexchange_20250930" title="stackexchange_20250930">Internet Archive</a>)

### Installation
To install all necessary requirements use:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage
To parse the XML files to parquet files `parser.py` will parse all XML files of a given directory:

```bash
python parser.py
```