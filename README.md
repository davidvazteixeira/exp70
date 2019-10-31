# New instalation:

Every project has a folder "python_backend", which runs the python counterpart, that can be a CLI, GUI or webserver.

# Virtualenv

## System Install

Basic commands for all projects

```
sudo apt-get install python3-pip
sudo pip3 install virtualenv
# (...)
```

Some projects needs more packages installations at "(...)". See "README-MORE.md", if it exists, inside each project folder.

## On each "python_backend" folder, just once:

```
python3 -m virtualenv .env -p python3
source .env/bin/activate
pip install -r requirements.txt
```

## before running a project

if running on terminal, testing:

```
./run.sh        # start the project in TEST mode.
```

if running standing alone, in exposition/autorun:

```
./run.sh exp    # start the project in EXPOSITION mode.
```
