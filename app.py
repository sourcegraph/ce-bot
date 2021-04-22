import os 
import logging
from datetime import datetime
from msg_templates import ce_request_form_template, ce_request_submission_success__template,denial_form_template
from slack_bolt.async_app import AsyncApp

# Initialize logging 
logging.basicConfig(level=logging.DEBUG)

# Initializes your app with your bot token and signing secret
app = AsyncApp()
CHANNEL = os.environ.get("CHANNEL")
international_lead = os.environ.get("INTERNATIONAL_ID")
west_lead = os.environ.get("WEST_ID")
east_lead = os.environ.get("EAST_ID")

# @app.shortcut() decorator for allowing user to trigger a global shortcut that will open a modal with CE Request form 
@app.shortcut({"callback_id": "ce_request", "type": "shortcut"})
async def open_modal(ack, shortcut, client, logger):
    #Initializes user that triggered the shortcut event
	user = shortcut["user"]["username"]

	#Modal form layout payload
	msg = ce_request_form_template(user)
    
	# Acknowledge the shortcut request
	await ack()
    
	# Call the views_open method using one of the built-in WebClients
	await client.views_open(trigger_id=shortcut["trigger_id"],view=msg,)


# Handle a submission of Request for CE Form 
@app.view("ce_request_form")
async def handle_submission(ack, body, client, view, logger):
	#parse values from form response using `block_id` and `action_id`
	ce_request_values = view["state"]["values"]
	
	#parse values from ce_request_values using `block_id` and `action_id`
	customer_name = ce_request_values["customer_name"]["customer_name_input-action"]["value"] 
	region = ce_request_values["region_select"]["region_select-action"]["selected_option"]["text"]["text"]
	sales_stage =ce_request_values["sales_stage"]["sales_stage_select-action"]["selected_option"]["text"]["text"]
	opp_link = ce_request_values["opp_link"]["opp_link_input-action"]["value"] 
	notes_link = ce_request_values["notes_link"]["notes_link_input-action"]["value"] 
	additional_info = ce_request_values["additional_info"]["additional_info_input-action"]["value"] 
    
	#timestamp of todays date
	now = datetime.now()
	ts = now.strftime("%Y-%m-%d")

	#retrieve username from body of the response from the from submission
	username = body["user"]["username"]
    
	errors = {}
	#TODO: Validate the inputs

	if len(errors) > 0:
		ack(response_action="errors", errors=errors)
		return


    # Acknowledge the submission event and close the modal
	await ack()

	try:
		channel_msg = ce_request_submission_success__template(username,customer_name,ts,region,sales_stage,opp_link,notes_link,additional_info)
	except Exception as e:
   		# Handle error
		err_msg = f"There was an error with your submission: {e}"
		logger.error(err_msg)
	finally:
   		# Message the channel
		channel_post = await client.chat_postMessage(channel=CHANNEL, blocks=channel_msg)
		logger.info("CHANNEL POST SUCCESSFUL")
		msg_link = await client.chat_getPermalink(channel=CHANNEL, message_ts=channel_post["ts"])

		user_msg = f'You have a new request for CE. Please review opp submission details and select a CE :  {msg_link["permalink"]}'
		logger.info(msg_link)
		if region == "Americas - West" or region == "Americas - West":
			await client.chat_postMessage(channel=west_lead, text=user_msg)
		elif region == "Americas - East":
			await client.chat_postMessage(channel=east_lead, text=user_msg)
		else:
			await client.chat_postMessage(channel=international_lead, text=user_msg)
    		
    			



#Replies to message of CE request from with the name of the CE that has been selected
@app.action("users_select-action")
async def select_user(ack, action,client,body, respond,logger):
    
	#Set message with CE mention
	msg = f"<@{action['selected_user']}> you have been assigned to this opp. Please review the above details and touch base with the AE for next steps."

	select_user = action['selected_user']
	
	# Acknowledge user selection
	await ack()

	#timestamp for when the request for CE was made so that the bot knows what message to reply to
	msg_ts = body['container']['message_ts']

	try:
		msg_link = await client.chat_getPermalink(channel=CHANNEL, message_ts=msg_ts)
		user_msg = f'you have been assigned to this opp. Please review the details within the link and touch base with the AE for next steps. {msg_link["permalink"]}'
	except Exception as e:
   		# Handle error
		err_msg = f"There was an error geting the link to message: {e}"
		logger.error(err_msg)

	finally:
		#Send reply message with CE mention
		await client.chat_postMessage(channel=CHANNEL, text=msg, thread_ts=msg_ts)
		await client.chat_postMessage(channel=select_user, text=user_msg)
  

# is triggered with approve button is clicked. Will react with a check mark emoji to CE request and notify requester
@app.action("approve_button")
async def approve_request(ack, client,body, respond,logger):
	#timestamp for when the request for CE was made so that the bot knows what message to reply to
	msg_ts = body['container']['message_ts']
	
	#Acknowledge user approval
	await ack()

	#bot replies back with emoji
	await client.reactions_add(channel=CHANNEL,name="white_check_mark", timestamp=msg_ts)

   
@app.action("deny_button")
async def deny_request(ack, action, body, client,logger):
    # Acknowledge deny request
	await ack()

	#timestamp for when the request for CE was made so that the bot knows what message to reply to	
	msg_ts = body['container']['message_ts']

	#Retrieve user info from message blocks
	username = body["message"]["blocks"][1]["block_id"]
	
	#id for launching a modal
	trigger_id = body["trigger_id"]

	#denial form template
	denial_form = denial_form_template(msg_ts,username)

    #Open denial request form 
	await client.views_open(trigger_id=trigger_id,view=denial_form,)

	
#handles ce denial form submission by message requeseter why their request was denied 
@app.view("ce_denial_form")
async def handle_denial_submission(ack, body, client, view, logger):
	#parse values from ce_denial_form using `block_id` and `action_id`
	denial_detials_values = view["state"]["values"]["denial_details"]["denial_details_input-action"]["value"]
	
	#Retrieve user info from message blocks
	user_tag = body["view"]["blocks"][1]["text"]["text"]
	user_id = user_tag[2:len(user_tag)-1]
	username = body["view"]["blocks"][1]["block_id"]


	errors = {}
	msg_ts = view["private_metadata"]
	#validate submission was longer than 5 characters
	if denial_detials_values is not None and len(denial_detials_values) <= 5:
		errors["denial_details"] = "The value must be longer than 5 characters"

	#Acknowledge user with the errors
	if len(errors) > 0:
		await ack(response_action="errors", errors=errors)
		return
	# Acknowledge the view_submission event and close the modal
	await ack()

	#denial message
	denial_msg = f"<@{username}> Your request for CE has been denied\n\n  *Reasons for Denial:*\n{denial_detials_values}\n\n"
	msg = "This request has been Denied. Awaiting an info update before selecting a CE"
	try:
		msg_link = await client.chat_getPermalink(channel=CHANNEL, message_ts=msg_ts)
		if msg_link:
			denial_msg = denial_msg + f"*View CE Request:*\n{msg_link['permalink']}"
    			
	except Exception as e:
   		# Handle error
		denial_msg = denial_msg + "*View CE Request:*\n there was an error geting the link to message"
		err_msg = f"There was an error geting the link to message: {e}"
		logger.error(err_msg)
	finally:
		# Message the user
		await client.chat_postMessage(channel=user_id, text=denial_msg,)
		await client.chat_postMessage(channel=CHANNEL, text=msg, thread_ts=msg_ts)
	





# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", int(os.environ.get("PORT", 3000)))))
