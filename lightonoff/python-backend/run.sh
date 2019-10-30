#!/bin/bash
# virtualenv needs bash. sh do not work

# Configure you actions here

# ---------------------------
# Before testing exp/test mode
pre_run(){
  xset -dpms s off
  cd /home/pi/Downloads/exp70/lightonoff/python-backend/
  source .env/bin/activate
  FLASK_APP=web.py flask run &
  sleep 5
  chromium-browser http://localhost:5000  
}

# ---------------------------
# Run if exp mode
exp_run(){
  echo "."
}

# Run if test mode
test_run(){
  echo "."
}

# ---------------------------
# Run after exp mode
after_exp_run(){
  echo "."
}

# Run after test mode
after_test_run(){
  echo "."
}

# ---------------------------
# Run at the end
at_end(){
  echo "."
}

if [ "$1" = '-h' ]; then
  echo '  Script to simple boot project folder.'
  echo
  echo '  ./run.sh'
  echo '    starts in test mode. Closes the ENV after exit.'
  echo
  echo '  ./run.sh'
  echo '    starts in exp mode.'
  exit
fi

pre_run
if [ "$1" = "exp" ]; then
  echo "exp mode"
  exp_run
  after_exp_run
else
  echo "test mode"
  test_run
  after_test_run
fi
at_end

