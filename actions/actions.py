import requests
from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict


# def clean_name(name):
#     return "".join([c for c in name if c.isalpha()])

class ValidateNameForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    def validate_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `name` value."""

        # If the name is super short, it might be wrong.
        name = slot_value
        if len(name) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"name": None}
        return {"name": name}

    def validate_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `email` value."""

        # If the name is super short, it might be wrong.
        email = slot_value
        if len(email) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"email": None}
        return {"email": email}
        
    def validate_order_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `order_number` value."""

        # If the name is super short, it might be wrong.
        order_number = slot_value
        if len(order_number) == 0:
            dispatcher.utter_message(text="That must've been a typo.")
            return {"order_number": None}
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        if len(name) + len(email) + len(order_number) < 10:
            dispatcher.utter_message(text="That's a very short name. We fear a typo. Restarting!")
            return {"name": None, "email": None, "order_number": None}
        
        # Fetch API using user information
        url = "https://api.staging.protect.inc/lookup-order?include=order,order.line_items,order.line_items.warrantiedLineItem,claims,protectShop.shop,protectionType"
        data = {
            "email": email,
            "order_number": order_number
        }

        # Send POST request to API
        response = requests.post(url, json=data)

        # Process response and return slots accordingly
        if response.status_code == 200:
            # API call successful
            api_data = response.json()
            # Extract relevant information from the API response
            # and store it in appropriate slots
            # For example:
            order_info = api_data.get("order")

            line_items = order_info.get("line_items")
            data =  line_items.get("data")
            product_names = []
            for item in data:
                product_name = item.get("name")
                if product_name:
                    product_names.append(product_name)
            # Extract order details from the API response and store in slots
            dispatcher.utter_message(text="success to fetch order information from the API.")
            return {"order_number": slot_value, "name1": product_names}

        else:
            # API call failed
            dispatcher.utter_message(text="Your order not found.")
            return {"order_number": None}


class ValidateClaimForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_claim_form"

    def validate_items(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `items` value."""

        # If the name is super short, it might be wrong.
        items = slot_value
        return {"items": items}
    
    def validate_quantity(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `quantity` value."""

        # If the name is super short, it might be wrong.
        quantity = slot_value
        return {"quantity": quantity}
    

    def validate_reason(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `reason` value."""

        # If the name is super short, it might be wrong.
        reason = slot_value
        return {"reason": reason}
    def validate_Comment(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `Comment` value."""

        # If the name is super short, it might be wrong.
        Comment = slot_value
        return {"Comment": Comment}
    def validate_attachment(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `attachment` value."""

        # If the name is super short, it might be wrong.
        attachment = slot_value
        return {"attachment": attachment}

    