# -*- coding: utf-8 -*-
"""
A routing layer for the onboarding bot tutorial built using
[Slack's Events API](https://api.slack.com/events-api) in Python
"""
import json
import bot
from flask import Flask, request, make_response, render_template
import pandas as pd
pyBot = bot.Bot()
slack = pyBot.client

app = Flask(__name__)


def _event_handler(event_type, slack_event):
    """
    A helper function that routes events from Slack to our Bot
    by event type and subtype.
    Parameters
    ----------
    event_type : str
        type of event recieved from Slack
    slack_event : dict
        JSON response from a Slack reaction event
    Returns
    ----------
    obj
        Response object with 200 - ok or 500 - No Event Handler error
    """
    team_id = slack_event["team_id"]
    # ================ Team Join Events =============== #
    # When the user first joins a team, the type of event will be team_join

#     user_id = slack_event["event"]["user"]
    user_id = slack_event["event"].get("user")
    print('\nUserID: ' + str(user_id))
    if user_id is None:
        return make_response("Retry", 404, {"X-Slack-No-Retry": 1})

    # Send the onboarding message
    if event_type == "message":
        print(slack_event["event"]['text'])
    msg = slack_event["event"]['text']
    ts = slack_event["event"]['event_ts']
    print('\nTimestampp = ', ts)
    pyBot.onboarding_message(team_id, user_id, msg, ts)
    return make_response("Welcome Message Sent", 200,)


@app.route("/install", methods=["GET"])
def pre_install():
    """This route renders the installation page with 'Add to Slack' button."""
    # Since we've set the client ID and scope on our Bot object, we can change
    # them more easily while we're developing our app.
    client_id = pyBot.oauth["client_id"]
    print(client_id)
    scope = pyBot.oauth["scope"]
    # Our template is using the Jinja templating language to dynamically pass
    # our client id and scope
    return render_template("install.html", client_id=client_id, scope=scope)


@app.route("/thanks", methods=["GET", "POST"])
def thanks():
    """
    This route is called by Slack after the user installs our app. It will
    exchange the temporary authorization code Slack sends for an OAuth token
    which we'll save on the bot object to use later.
    To let the user know what's happened it will also render a thank you page.
    """
    print(request.data)
    print(request)
    # Let's grab that temporary authorization code Slack's sent us from
    # the request's parameters.
    code_arg = request.args.get('code')
    # The bot's auth method to handles exchanging the code for an OAuth token
    pyBot.auth(code_arg)
    return render_template("thanks.html")


@app.route("/listening", methods=["GET", "POST"])
def hears():
    """
    This route listens for incoming events from Slack and uses the event
    handler helper function to route events to our Bot.
    """
    slack_event = json.loads(request.data)
    print('Slack event:' + str(slack_event))

    # ============= Slack URL Verification ============ #
    # In order to verify the url of our endpoint, Slack will send a challenge
    # token in a request and check for this token in the response our endpoint
    # sends back.
    # For more info: https://api.slack.com/events/url_verification
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                             "application/json"
                                                             })

    # ============ Slack Token Verification =========== #
    # We can verify the request is coming from Slack by checking that the
    # verification token in the request matches our app's settings
    if pyBot.verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s \npyBot has: \
                   %s\n\n" % (slack_event["token"], pyBot.verification)
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
        # Slack's automatic retries during development.
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    # ====== Process Incoming Events from Slack ======= #
    # If the incoming request is an Event we've subcribed to
    # if "event" in slack_event:
    event_type = slack_event["event"]["type"]
    # Then handle the event by event_type and have your bot respond
    return _event_handler(event_type, slack_event)

#     event_type = slack_event["event"]["type"]
#     team_id = slack_event["team_id"]
#     print('Team ID: '+team_id)
    # print('Event type:'  +str(event_type))
    if event_type == "message":
        print(slack_event["event"])

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    # return make_response("Data Scientist", 404, {"X-Slack-No-Retry": 1})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8080)
