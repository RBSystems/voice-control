# -*- coding: utf-8 -*-
"""Skill for voice control support for the classrooms"""

import logging
import requests
import json
# Six covers things from python2.6 to python3
import six
import avresources

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import (
    AbstractRequestHandler, AbstractExceptionHandler,
    AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# =====================================================================
# Constants and Other Data, Vars, etc...
# =====================================================================
SKILL_NAME = "Classroom Assistant"
HELP_MESSAGE = "You can tell me to power a display on or off, you can tell me to adjust the volume."
HELP_REPROMPT = "What can I help you with?"
STOP_MESSAGE = "Goodbye!"
FALLBACK_MESSAGE = "I cannot help you with that, if you need help, say help."
FALLBACK_REPROMPT = "What can I help you with?"
EXCEPTION_MESSAGE = "Sorry, I am unable to help with that."

# Slot names and keys
power_slot = "power"
volume_slot = "volume"

# =====================================================================
# Helper Functions
# =====================================================================
def PowerRequest(powerValue):

    # Data is the put body that is parameterized for power value. powerValue should be on or standby
    data = {
        "displays": [
            {
                "name": "D1",
                "power": powerValue
            },
            {
                "name": "D2",
                "power": powerValue
            },
            {
                "name": "D3",
                "power": powerValue
            }
        ]
    }
    data = json.dumps(data)
    url = avresources.ENDPOINT
    token = avresources.API_KEY
    headers = {'x-av-access-key': token, 'x-av-user': avresources.API_USER, "Content-Type": "application/json", 'data':data}
    r = requests.put(url, headers=headers, data=data)
    if r.status_code / 100 != 2:
        print("OOOOF")
    return None
    
    # VolumeRequest is the json put body and the commands to send that command.
def VolumeRequest(voulmeValue):
        # Data is the put body that is parameterized for power value. powerValue should be on or standby
    data = {
        "displays": [
            {
                "name": "D1"
            },
            {
                "name": "D3"
            },
            {
                "name": "D2"
            }  
        ],
        "audioDevices": [
            {
                "name": "D1",
                "muted": False,
                "volume": int(voulmeValue)
            },
            {
                "name": "D2",
                "muted": False,
                "volume": int(voulmeValue)
            },
            {
                "name": "D3",
                "muted": False,
                "volume": int(voulmeValue)
            }
        ]
    }
    data = json.dumps(data)
    # Log out the data that is being sent to see if it is formatted correct.
    logger.info(data)
    url = avresources.ENDPOINT
    token = avresources.API_KEY
    headers = {'x-av-access-key': token, 'x-av-user': avresources.API_USER, "Content-Type": "application/json", 'data':data}
    r = requests.put(url, headers=headers, data=data)
    if r.status_code / 100 != 2:
        print("OOOOF")
    return None



# =====================================================================
# Handlers
# =====================================================================

# Standard Launch Function
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for skill launch."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In LaunchRequestHandler")
        speech = ('Welcome to classroom assistant, how can I help?')
        reprompt = "What would you like me to do?"
        handler_input.response_builder.speak(speech).ask(reprompt)
        return handler_input.response_builder.response

# Power Handler deals with powering on and off a display
class PowerHandler(AbstractRequestHandler):
    """Handler for the power stuff of the skill."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("PowerHandler")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In PowerHandler")

        # Get the slot values for the intent
        slots = handler_input.request_envelope.request.intent.slots
        
        # The status code should I ever need it for any reason.
        # logger.info("Status Code: {}" .format(slots["power"].resolutions.resolutions_per_authority[0].status.code))
        
        #SHOULD be either standby or on...And so it was, and all rejoiced.
        # logger.info("Actual Slot Value: {}" .format(slots["power"].resolutions.resolutions_per_authority[0].values[0].value.name))
        
        #power_slot is "power" just as a reminder...That could have saved me 1 hour...
        if power_slot in slots:
            # powerRequest and the subsequent logger.info was used for testing. Leaving in for future use
            # powerRequest = slots[power_slot].value
            # logger.info("powerRequest{}." .format(powerRequest))
            powerValue = slots[power_slot].resolutions.resolutions_per_authority[0].values[0].value.name
            speech = ("Turning the display to {}. ".format(powerValue))
            PowerRequest(powerValue)
        else:
            speech = "I'm not sure what you want. Please try asking again."

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, "Power Handler"))
        return handler_input.response_builder.response
      

# Volume Handler deals with powering on and off a display
class VolumeHandler(AbstractRequestHandler):
    """Handler for all the volume stuff of the skill"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("VolumeHandler")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In Volume Handler")

        slots = handler_input.request_envelope.request.intent.slots

        if volume_slot in slots:
            volumeNum = slots[volume_slot].value
            logger.info("volumeRequest {}." .format(volumeNum))
            speech = ("Setting the volume to {}. ".format(volumeNum))
            VolumeRequest(volumeNum)
        else:
            speech = "I'm not sure what you want. Please try asking again."

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, "Volume Level: {}" .format(volumeNum)))
        return handler_input.response_builder.response

# ChangeInputHandler takes care of switching inputs
class ChangeInputHandler(AbstractRequestHandler):
    """Handler for changing the inputs for a display"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("ChangeInputHandler")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In ChangeInput Handler")

        slots = handler_input.request_envelope.request.intent.slots

        if volume_slot in slots:
            volumeNum = slots[volume_slot].value
            logger.info("Input Request: {}." .format(volumeNum))
            speech = ("Changing Input to  {}. ".format(volumeNum))
            VolumeRequest(volumeNum)
        else:
            speech = "I'm not sure what you want. Please try asking again."

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, "Current Input: "))
        return handler_input.response_builder.response

# BlankHandler takes care of blanking and unblanking a display
class BlankHandler(AbstractRequestHandler):
    """Handler for blanking and unblanking the screen"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_request_type("LaunchRequest")(handler_input) or
                is_intent_name("BlankHandler")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In Blank Handler")

        slots = handler_input.request_envelope.request.intent.slots

        if volume_slot in slots:
            volumeNum = slots[volume_slot].value
            logger.info("Blank Request: {}." .format(volumeNum))
            speech = ("Setting the display to {}. ".format(volumeNum))
            VolumeRequest(volumeNum)
        else:
            speech = "I'm not sure what you want. Please try asking again."

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard(SKILL_NAME, "Blank Status: "))
        return handler_input.response_builder.response

# InfoHandler will hopefully help get information about the room so I can get room ID stuff for A4B
class InfoHandler(AbstractRequestHandler):
    """Handler for getting information"""
    def can_handle(self, handler_input):
        return (is_request_type("LaunchRequest")(handler_input) or
        is_intent_name("InfoHandler")(handler_input))

    def handle(self, handler_input):
        logger.info("In InfoHandler")

        info = handler_input.request_envelope

        logger.info("Skill Info returned: {}" .format(info))
        speech = "I gave you your info, what else do you want from me?!"
        
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


# Help handler (AmazonHelpIntent)
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In HelpIntentHandler")

        handler_input.response_builder.speak(HELP_MESSAGE).ask(
            HELP_REPROMPT).set_card(SimpleCard(
                SKILL_NAME, HELP_MESSAGE))
        return handler_input.response_builder.response

# Cancel or Stop Handler (AmazonCancel or AmazonStop Intent)
class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In CancelOrStopIntentHandler")

        handler_input.response_builder.speak(STOP_MESSAGE)
        return handler_input.response_builder.response

# Fallback Handler (AmazonFallbackIntent)
class FallbackIntentHandler(AbstractRequestHandler):
    """Handler for Fallback Intent.
    AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")

        handler_input.response_builder.speak(
            FALLBACK_MESSAGE).ask(FALLBACK_REPROMPT)
        return handler_input.response_builder.response


# Session End Handler (AmazonStopIntent)
class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In SessionEndedRequestHandler")

        logger.info("Session ended reason: {}".format(
            handler_input.request_envelope.request.reason))
        return handler_input.response_builder.response


# Exception Handler
class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.info("In CatchAllExceptionHandler")
        logger.error(exception, exc_info=True)

        handler_input.response_builder.speak(EXCEPTION_MESSAGE).ask(
            HELP_REPROMPT)
        return handler_input.response_builder.response

# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""

    def process(self, handler_input):
        # type: (HandlerInput) -> None
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))


class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""

    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))


# Skill Builder object
sb = SkillBuilder()

# Register intent handlers for the skill builder (sb)
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(PowerHandler())
sb.add_request_handler(VolumeHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

# Add exception handler to the skill.
sb.add_exception_handler(CatchAllExceptionHandler())

# Add response interceptor to the skill.
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())

# Expose the lambda handler to register in AWS Lambda.
lambda_handler = sb.lambda_handler()
