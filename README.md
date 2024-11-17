![Space Status](https://spaceapistatusimage.hosted.quelltext.eu/status?url=https%3A%2F%2Fmembers.pawprintprototyping.org%2Fapi%2Fspacedirectory%2F)

# Administrative Documents
Administrative resources for the org

# How to use this repository
This repository includes some automation to handle monthly agenda tasks. The
automation is handled by a GitHub Action that runs on the first of every month.

## Setup
cp config-template.json config.json
vi config.json
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

## Running the automation
It magically works on the first of every month.

