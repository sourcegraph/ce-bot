def ce_request_form_template(user ):
    msg = { "type": "modal",
    "callback_id": "ce_request_form",
	"submit": {
		"type": "plain_text",
		"text": "Submit",
		"emoji": True
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"title": {
		"type": "plain_text",
		"text": "Request a CE",
		"emoji": True
	},
	"blocks": [
		{
			"type": "section",
			"block_id": f"{user}",
			"text": {
				"type": "plain_text",
				"text": f":wave: Hey <@{user}>!\n\n Please fill out the following details to get a CE Assigned",
				"emoji": True
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "input",
  "block_id": "customer_name",
			"element": {
				"type": "plain_text_input",
				"action_id": "customer_name_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Customer Name",
				"emoji": True
			}
		},
		{
			"type": "input",
  "block_id": "region_select",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Americas - West",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Americas - East",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "International - West",
							"emoji": True
						},
						"value": "value-2"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "International - East",
							"emoji": True
						},
						"value": "value-3"
					}
				],
				"action_id": "region_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Select Region",
				"emoji": True
			}
		},
		{
			"type": "input",
  "block_id": "sales_stage",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Stage 0 - Prospecting",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Stage 1 - Interest",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Stage 2 - Qualification",
							"emoji": True
						},
						"value": "value-2"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Stage 3 - Solution Mapping",
							"emoji": True
						},
						"value": "value-3"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Stage 4 - Technical & Business Validation",
							"emoji": True
						},
						"value": "value-4"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Stage 5 - EB Sign Off",
							"emoji": True
						},
						"value": "value-5"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Stage 6 - Contract Negotiation",
							"emoji": True
						},
						"value": "value-6"
					}
				],
				"action_id": "sales_stage_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Sales Stage",
				"emoji": True
			}
		},
		{
			"type": "input",
  "block_id": "opp_link",
			"element": {
				"type": "plain_text_input",
				"action_id": "opp_link_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Opp Link",
				"emoji": True
			}
		},
		{
			"type": "input",
  "block_id": "notes_link",
			"element": {
				"type": "plain_text_input",
				"action_id": "notes_link_input-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Running Notes Link",
				"emoji": True
			}
		},
		{
			"type": "input",
  "block_id": "additional_info",
			"label": {
				"type": "plain_text",
				"text": "Anything else you want to tell us?",
				"emoji": True
			},
			"element": {
				"type": "plain_text_input",
				"multiline": True,
 "action_id": "additional_info_input-action"
			},
			"optional": True
		}
	]
}
    return msg

def ce_request_submission_success__template(username,customer_name,ts,region,sales_stage,opp_link,notes_link,additional_info):
    msg = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"You have a new request from:"
			}
		},		
		{
			"type": "section",
			"block_id": f"{username}",
			"text": {
				"type": "plain_text",
				"text": f"<@{username}>",
				"emoji": True
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*Customer:*\n{customer_name}"
				},
				{
					"type": "mrkdwn",
					"text": f"*When:*\nSubmitted {ts}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Region:*\n{region}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Sales Stage:*\n{sales_stage}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Opp Link:*\n{opp_link}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Notes Link:*\n{notes_link}"
				},
				{
					"type": "mrkdwn",
					"text": f"*Additional Info:*\n{additional_info}"
				}
			]
		},
   {
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "Assign a CE"
					},
					"accessory": {
						"type": "users_select",
						"placeholder": {
							"type": "plain_text",
							"text": "Select a user",
							"emoji": True
						},
						"action_id": "users_select-action"
					}
				},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"action_id":"approve_button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Approve"
					},
					"style": "primary",
					"value": "assign_ce"
				},
				{
					"type": "button",
					"action_id":"deny_button",
					"text": {
						"type": "plain_text",
						"emoji": True,
						"text": "Deny"
					},
					"style": "danger",
					"value": "click_me_123"
				}
			]
		}
	]
    return msg


def denial_form_template(private_metadata , username):
	msg = {
	"type": "modal",
	"callback_id": "ce_denial_form",
	"private_metadata" : f"{private_metadata}",
	"submit": {
		"type": "plain_text",
		"text": "Submit",
		"emoji": True
	},
	"close": {
		"type": "plain_text",
		"text": "Cancel",
		"emoji": True
	},
	"title": {
		"type": "plain_text",
		"text": "Request For CE - Denial",
		"emoji": True
	},
	"blocks": [
	{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": "Request from:",
				"emoji": True
			}
		},
		{
			"type": "section",
			"block_id": f"{username}",
			"text": {
				"type": "plain_text",
				"text": f"<@{username}>",
				"emoji": True
			}
		},
		{
			"type": "input",
			"block_id": "denial_details",
			"label": {
				"type": "plain_text",
				"text": "Reasons for rejection? (more than 5 charcters)",
				"emoji": True
			},
			"element": {
				"type": "plain_text_input",
				"action_id": "denial_details_input-action",
				"multiline": True
			}
		}
	]
	}
	return msg
