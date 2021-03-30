#Run locally:

python3 -m venv .venv
source .venv/bin/activate

#Env 
export SLACK_SIGNING_SECRET=YOUR_SECRET
export SLACK_BOT_TOKEN=xoxb-BOT_TOKEN
export PORT=YOUR_PORT
export CHANNEL=YOUR_SLACK_CHANNEL


python3 app.py  



