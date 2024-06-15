"""Model classes"""


def model(name: str, attr_names: str = ""):
    """Generate a new class with a constructor taking attr_names as parameters.

    Args:
        name (str): class name
        attr_names (str|list): attribute names
    """
    if isinstance(attr_names, str):
        attr_names = set(attr_names.split(" "))

    def constructor(self, **kwargs):
        """Checks that kwargs are valid property names
        and then assign those properties to self.
        """
        kwarg_names = set(kwargs.keys())
        unknown_attributes = kwarg_names - attr_names
        if unknown_attributes:
            raise TypeError("Unknown properties %s for %s" % (unknown_attributes, name))

        for attr_name in attr_names:
            setattr(self, attr_name, kwargs.get(attr_name))

    return type(name, (object,), {"__init__": constructor})


# Bot actions
AskDocumentAction = model("AskDocumentAction", "message documents")
AskedDocument = model("AskedDocument", "message name authorized_file_types")
AskLocationAction = model("AskLocationAction", "message callback_action")
StepTarget = model("StepTarget", "step_id name")
StoryTarget = model("StoryTarget", "story_id name")
GoToAction = model("GoToAction", "target session_values")
DocumentAttachment = model("name url")
LegacyReplyToMessageAction = model("LegacyReplyToMessageAction", "message attachments")
OpenURLAction = model("OpenURLAction", "url")
ShareAction = model("ShareAction", "")
SendImageAction = model("SendImageAction", "image_url alt")
SendTextAction = model("SendTextAction", "alternatives text")
SendJSEventAction = model("SendJSEventAction", "event payload")
SendEmailAction = model(
    "SendEmailAction",
    "from_name from_email content subject recipient reply_to_name reply_to_email user_attachments",
)
WaitAction = model("WaitAction", "duration")
PauseBotAction = model("PauseBotAction", "")
CloseIntercomConversationAction = model("CloseIntercomConversationAction", "")
AssignIntercomConversationAction = model("AssignIntercomConversationAction", "assignee_id")
SendQuickRepliesAction = model("SendQuickRepliesAction", "buttons message")
QuickReply = model("QuickReply", "title action")
Button = model("Button", "title action")
Card = model("Card", "title subtitle buttons image_url url alt")
SimpleCard = model("SimpleCard", "title subtitle buttons image_url")
SendCardsAction = model("SendCardsAction", "cards")
SendSimpleCardsAction = model("SendSimpleCardsAction", "cards")
StoreSessionValueAction = model("StoreSessionValueAction", "key value add is_int")
SetUserAttributeAction = model("SetUserAttributeAction", "key value add is_int")
GoogleCustomSearchAction = model("GoogleCustomSearchAction", "query limit custom_engine_id")
CreateZendeskTicketAction = model(
    "CreateZendeskTicketAction",
    "ticket_type ticket_priority subject description assignee_id group_id tags user",
)

CreateUserRequestAction = model("CreateUserRequestAction", "message assignee_id group_id")

ZendeskUser = model("ZendeskUser", "email name phone_number")
JumpToAction = model("JumpToAction", "default_target connections")
CustomerSatisfactionCallbackAction = model("CustomerSatisfactionCallbackAction", "target kind")
CustomerSatisfactionChoice = model(
    "CustomerSatisfactionChoice", "kind label target matching_intent_id"
)
CustomerSatisfactionAction = model("CustomerSatisfactionAction", "message choices")
WebhookRequestField = model("WebhookRequestField", "key value")
SendWebhookRequestAction = model("SendWebhookRequestAction", "url service description fields")
CloseIAdvizeConversationAction = model("CloseIAdvizeConversationAction", "")
IAdvizeDistributionRule = model("IAdvizeDistributionRule", "label id")
TransferIAdvizeConversationAction = model(
    "TransferIAdvizeConversationAction", "failed_transfer_message distribution_rule"
)

# AI Actions

AITaskEngine = model("AITaskEngine", "name opts")
AITaskBehavior = model("AITaskBehavior", "name connections")
SendAITaskAction = model(
    "SendAITaskAction", "engine behaviors select_target default_target user_attributes"
)

# Flow connection
Choice = model("Choice", "image_url title session_values")
Section = model("Section", "title choices")
SendChoicesListAction = model("SendChoicesListAction", "message placeholder sections action")
MessageGetter = model("MessageGetter")
SessionValueGetter = model("SessionValueGetter", "key")
AttachmentValueGetter = model("AttachmentValueGetter", "key")
UserAttributeGetter = model("UserAttributeGetter", "key")
FlowConnection = model("FlowConnection", "target predicates")
ConnectionPredicate = model("ConnectionPredicate", "value_getter condition")
ConnectionTeamPredicate = model("ConnectionTeamPredicate", "condition")
ConnectionUserPredicate = model("ConnectionUserPredicate", "condition")

# Conditions
IsNotSetCondition = model("IsNotSetCondition")
IsSetCondition = model("IsSetCondition")
ContainCondition = model("ContainCondition", "values")
EqualsCondition = model("EqualsCondition", "expected")
MatchRegexpCondition = model("MatchRegexpCondition", "regexp")
MatchIntentConditionIntent = model("MatchIntentConditionIntent", "id name")
MatchIntentCondition = model("MatchIntentCondition", "intent_id")
IsLessThanCondition = model("IsLessThanCondition", "maximum")
IsLessThanOrEqualCondition = model("IsLessThanOrEqualCondition", "maximum")
IsGreaterThanCondition = model("IsGreaterThanCondition", "minimum")
IsGreaterThanOrEqualCondition = model("IsGreaterThanOrEqualCondition", "minimum")
IsNumberCondition = model("IsNumberCondition")
IsOnlineCondition = model("IsOnlineCondition")
IsOfflineCondition = model("IsOfflineCondition")
IsLoggedCondition = model("IsLoggedCondition")
IsNotLoggedCondition = model("IsNotLoggedCondition")

# Webhook
URLLoadedEvent = model("URLLoadedEvent", "url")
CustomEvent = model("CustomEvent", "name")
Message = model("Message", "text attachments")
Audio = model("Audio", "url")
File = model("File", "url")
Video = model("Video", "url")
Image = model("Image", "url")
Step = model("Step", "actions name id user_data")
Coordinates = model("Coordinates", "lat long")
Interlocutor = model(
    "Interlocutor",
    "id external_id remote_id location last_name first_name email custom_attributes phone_number used_to_test is_logged",
)
ConversationSession = model("ConversationSession", "values")
StepReached = model("StepReached", "step session interlocutor channel input")
StepReachedResponse = model("StepReachedResponse", "actions session interlocutor")
WebhookRequest = model("WebhookRequest", "event bot_id timestamp topic")
