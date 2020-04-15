# Monitoring the Interplanetary File System

The Python script used to analyze the IPFS swarm exploits the HTTP API
provided by IPFS (in particular the ```ipfs swarm peers``` one. The script is made
by two main modules:

[```main.py```](main.py) : the module that effectively logs data, manipulating them a bit before
writing them on a CSV file.

[```graphs.py```](graphs.py) : the module that plots the data logged by ```main.py``` into different
types of charts, explained in the next section.

For all the other ”sub-modules” see the docs and comments into the files them-
selves.

## How to run the code

I’ve set up a ```requirements.txt``` file to install all the dependecies, so my advice
is to use a virtual environment in which to install these requirements:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python main.py # to start logging
python graphs.py # to see the results for the logged data
                 # (it can take a while to start)
```