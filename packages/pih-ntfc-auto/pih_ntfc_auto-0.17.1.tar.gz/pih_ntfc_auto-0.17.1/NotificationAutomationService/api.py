import ipih

from pih import A
from pih.tools import ne

from pih.collections import (
    WhatsAppMessage,
    PolibasePersonNotificationConfirmation as PPNC,
)


class NotificationApi:
    @staticmethod
    def check_for_notification_confirmation(
        telephone_number: str, sender: str, test: bool = False
    ) -> bool | None:
        if A.C.telephone_number_international(telephone_number):
            notification_confirmation: PPNC | None = A.R_P_N_C.by(
                telephone_number, sender
            ).data
            has_notification_confirmation: bool = ne(notification_confirmation)
            if not has_notification_confirmation:
                previous_message_list: list[WhatsAppMessage] = (
                    [] if test else A.ME_WH_W.get_message_list(telephone_number, sender)
                )
                has_message_from_recipient: bool = False
                if ne(previous_message_list):
                    for whatsapp_message in previous_message_list:
                        has_message_from_recipient = not whatsapp_message.from_me
                        if has_message_from_recipient:
                            break
                A.A_P_N_C.update(
                    telephone_number, sender, 1 if has_message_from_recipient else 2
                )
            return not A.S.get(
                A.CT_S.POLIBASE_PERSON_REVIEW_NOTIFICATION_ASK_WITHOUT_CHECK_FOR_CONFIRMATION
            ) and (
                has_notification_confirmation and notification_confirmation.status != 2
            )
        return None
