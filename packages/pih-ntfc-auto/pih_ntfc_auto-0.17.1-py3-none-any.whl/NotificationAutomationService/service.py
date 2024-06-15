import ipih

from pih import A, PIHThread, serve, subscribe_on
from NotificationAutomationService.const import SD

SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:

    import random
    from time import sleep
    from collections import defaultdict
    from datetime import datetime, timedelta

    from pih.consts import (
        MessageTypes,
        MessageStatuses,
    )
    from pih.consts.polibase import (
        PolibasePersonVisitStatus,
        PolibasePersonVisitNotificationType as PPVNType,
    )
    from pih.collections import (
        Result,
        DelayedMessageDS,
        MessageSearchCritery,
        DelayedMessage as DM,
        PolibasePersonVisitDS as PPVDS,
        PolibasePersonVisitNotification as PPVN,
        PolibasePersonVisitNotificationDS as PPVNDS,
    )
    from pih.tools import (
        j,
        e,
        n,
        b,
        ne,
        nn,
        js,
        nl,
        jnl,
        nnt,
        FullNameTool,
        while_not_do,
        ParameterList,
    )
    from NotificationAutomationService.api import (
        NotificationApi as Api,
    )

    SENDER: str = A.D.get(A.CT_ME_WH_W.Profiles.CALL_CENTRE)

    class DH:
        message_stack: list[DelayedMessageDS] = []
        action_at_work: bool = False

    def create_message_search_critery(
        status: MessageStatuses | None = None, date: datetime | str | None = None
    ) -> MessageSearchCritery:
        return MessageSearchCritery(
            None,
            None,
            date,
            A.D.get(MessageTypes.WHATSAPP),
            None if e(status) else A.D.get(status),
            SENDER,
        )

    def fetch_delayed_messages(datetime: datetime) -> None:
        search_critery: MessageSearchCritery = create_message_search_critery(
            MessageStatuses.REGISTERED, datetime
        )
        DH.message_stack += A.R_ME_D.get(search_critery, True).data or []
        search_critery.date = ""
        DH.message_stack += A.R_ME_D.get(search_critery, True).data or []

    def send_delayed_message(message: DelayedMessageDS) -> bool:
        sender: str = nnt(message.sender)
        has_notification_confirmation: bool = A.C_P_N_С.exists(
            nnt(message.recipient), sender, True
        )
        message_id: int = nnt(message.id)
        if nn(message_id):
            person_visit_notification: PPVN | None = A.R_P_N.by_message_id(
                message_id
            ).data
            if nn(person_visit_notification):
                person_visit: PPVDS | None = A.R_P_V.by_id(
                    person_visit_notification.visitID
                ).data
                appointment_information: str | None = None
                if nn(person_visit):
                    is_prerecording: bool = (
                        nnt(person_visit).pin == A.CT_P.PRERECORDING_PIN
                    )
                    if nnt(person_visit).serviceGroupID == 0:
                        appointment_information = js(
                            ("приём к специалисту", b(person_visit.doctorFullName))
                        )
                    else:
                        appointment_information = A.CT_P.APPOINTMENT_SERVICE_GROUP_NAME[
                            A.D.get_by_value(
                                A.CT_P.AppointmentServiceGroupId,
                                person_visit.serviceGroupID,
                            )
                        ]
                    message_text: str | None = None
                    person_name: str = FullNameTool.to_given_name(
                        person_visit_notification.FullName
                    )
                    type: PPVNType = A.D.get_by_value(
                        PPVNType, nnt(person_visit_notification).type
                    )
                    if type in [PPVNType.GREETING, PPVNType.DEFAULT]:
                        if A.D.now() <= nnt(
                            A.D.datetime_from_string(
                                person_visit_notification.beginDate,
                                A.CT.ISO_DATETIME_FORMAT,
                            )
                        ):
                            visit_date_time: datetime = A.D.datetime_from_string(
                                nnt(person_visit).beginDate, A.CT.ISO_DATETIME_FORMAT
                            )
                            day_string: str = str(visit_date_time.day)
                            month_string: str = [
                                "января",
                                "февраля",
                                "марта",
                                "апреля",
                                "мая",
                                "июня",
                                "июля",
                                "августа",
                                "сентября",
                                "октября",
                                "ноября",
                                "декабря",
                            ][visit_date_time.month - 1]
                            hour_string: str = str(visit_date_time.hour)
                            minute_string: str = str(visit_date_time.minute)
                            if minute_string == "0":
                                hour_string += " часов"
                                minute_string = ""
                            else:
                                minute_string = j((":", minute_string))
                            if type == PPVNType.GREETING:
                                message_text = str(
                                    A.S.get(
                                        A.CT_S.POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT_FOR_CONFIRMED_NOTIFICATION
                                        if has_notification_confirmation
                                        else A.CT_S.POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT
                                    )
                                )
                            else:
                                message_text = str(
                                    A.S.get(
                                        A.CT_S.POLIBASE_PERSON_VISIT_NOTIFICATION_TEXT
                                    )
                                )
                            message_text = message_text.format(
                                name=person_name,
                                appointment_information=appointment_information,
                                day_string=day_string,
                                month_string=month_string,
                                hour_string=hour_string,
                                minute_string=minute_string,
                            )
                            if is_prerecording:
                                message_text = j(
                                    (
                                        message_text,
                                        A.S.get(
                                            A.CT_S.POLIBASE_PERSON_PRERECORDING_VISIT_NOTIFICATION
                                        ),
                                    )
                                )
                        else:
                            message_text = A.S.get(
                                A.CT_S.POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT_WITHOUT_DATE_FOR_CONFIRMED_NOTIFICATION
                                if has_notification_confirmation
                                else A.CT_S.POLIBASE_PERSON_VISIT_GREETING_NOTIFICATION_TEXT_WITHOUT_DATE
                            )
                            message_text = nnt(message_text).format(
                                name=person_name,
                                appointment_information=appointment_information,
                            )
                    elif type == PPVNType.REMINDER:
                        if person_visit.status == PolibasePersonVisitStatus.CONFIRMED:
                            visit_date_time: datetime = A.D.datetime_from_string(
                                person_visit.beginDate, A.CT.ISO_DATETIME_FORMAT
                            )
                            hour_string: str = str(visit_date_time.hour)
                            minute_string: str = str(visit_date_time.minute)
                            if minute_string == "0":
                                hour_string += " часов"
                                minute_string = ""
                            else:
                                minute_string = j((":", minute_string))
                            message_text = str(
                                A.S.get(A.CT_S.POLIBASE_PERSON_VISIT_REMINDER_TEXT)
                            ).format(
                                name=person_name,
                                visit_time=j(("в ", hour_string, minute_string)),
                                appointment_information=appointment_information,
                            )
                        else:
                            A.L.polibase(
                                js(
                                    (
                                        "Сообщение:",
                                        message_id,
                                        "было сброшено. Причина: отказ от приёма",
                                    )
                                ),
                                A.CT_L_ME_F.ERROR,
                            )
                            A.A_ME_D.abort(message)
                    if ne(message_text):
                        message.message = message_text
                        recipient: str = (
                            A.S_P.test_recipient(message.sender) or message.recipient
                        )
                        while_not_do(
                            lambda: A.ME_WH_W.send(
                                recipient, message.message, message.sender
                            ),
                            2,
                            lambda: complete_buffered_message_sending_action(message),
                        )
                        return True
        return False

    def server_call_handler(sc: SC, pl: ParameterList) -> bool | None:
        if sc == SC.heart_beat:
            fetch_delayed_messages(A.D_Ex.parameter_list(pl).get())
            heat_beat_handler()
            return True
        return None

    def complete_buffered_message_sending_action(message: DelayedMessageDS) -> bool:
        message_id: int | None = message.id
        if e(message_id):
            A.L.polibase(
                j(
                    (
                        "Сообщение (id: ",
                        message_id,
                        ") не было отправлено клиенту: ",
                        message.recipient,
                    )
                ),
                A.CT_L_ME_F.ERROR,
            )
        else:
            A.L.polibase(
                js(
                    (
                        "Сообщение: ",
                        message_id,
                        "было отправлено клиенту:",
                        message.recipient,
                    )
                )
            )
            if message_id == 0:
                return True
            return A.A_ME_D.complete(message)
        return True

    def messages_sending_action() -> None:
        while True:
            if ne(DH.message_stack):
                message: DelayedMessageDS | None = None
                try:
                    if A.S.get(A.CT_S.WHATSAPP_SENDING_MESSAGES_VIA_WAPPI_IS_ON):
                        message = DH.message_stack.pop(0)
                        if send_delayed_message(message):
                            delay: int = random.randint(
                                A.S.get(
                                    A.CT_S.WHATSAPP_BUFFERED_MESSAGE_MIN_DELAY_IN_MILLISECONDS
                                ),
                                A.S.get(
                                    A.CT_S.WHATSAPP_BUFFERED_MESSAGE_MAX_DELAY_IN_MILLISECONDS
                                ),
                            )
                            sleep(delay / 1000)
                except Exception as error:
                    A.L.polibase(
                        js(
                            (
                                "Ошибка при отправке сообщения:",
                                message.id,
                                "клиенту",
                                message.recipient,
                                nl("Ошибка: "),
                                error,
                            )
                        ),
                        A.CT_L_ME_F.ERROR,
                    )
            else:
                sleep(1)

    def service_starts_handler() -> None:
        subscribe_on(SC.heart_beat)
        search_critery: MessageSearchCritery = create_message_search_critery(
            MessageStatuses.AT_WORK
        )
        DH.message_stack += A.R_ME_D.get(search_critery).data or []
        search_critery.date = ""
        search_critery.status = A.D.get(MessageStatuses.REGISTERED)
        DH.message_stack += A.R_ME_D.get(search_critery, True).data or []
        PIHThread(messages_sending_action)
        heat_beat_handler()

    def new_person_visits_action() -> None:
        last_visit_id: int | None = A.D.if_not_empty(
            A.R_P_V_DS.last().data, lambda item: item.id
        )
        visit_list_result: Result[list[PPVDS]] | None = None
        if n(last_visit_id):
            visit_list_result = A.R_P_V.today()
        else:
            visit_list_result = A.R_P_V.after_id(nnt(last_visit_id))
        if ne(visit_list_result):
            visit_map: dict[str | int, list] = defaultdict(list)

            def fill_person_visits_map(visit: PPVDS) -> None:
                if visit.pin == A.CT_P.PRERECORDING_PIN:
                    visit_map[visit.telephoneNumber].append(visit)
                else:
                    visit_map[visit.pin].append(visit)

            A.R.every(fill_person_visits_map, visit_list_result)

            def visit_sort(value: PPVDS) -> str:
                return value.beginDate or ""

            for key in visit_map:
                visit_list: list[PPVDS] = visit_map[key]
                if len(visit_list) > 1:
                    visit_list.sort(key=visit_sort)
                for visit_item in visit_list:
                    new_person_visit_action(visit_item)

    def heat_beat_handler() -> None:
        sc: SC = SC.heart_beat
        if not DH.action_at_work:
            DH.action_at_work = True

            def action() -> None:
                new_person_visits_action()
                DH.action_at_work = False

            PIHThread(action)

    def new_person_visit_action(visit: PPVDS) -> None:
        def set_visit_notification_unique_property(
            visit: PPVDS, notification: PPVN
        ) -> None:
            notification.telephoneNumber = visit.telephoneNumber

        result_visit_ds: Result[PPVDS] = A.R_P_V_DS.search(PPVDS(id=visit.id))
        if ne(result_visit_ds):
            A.L.polibase(j(("Визит-дубликат: ", visit, nl(), result_visit_ds.data)))
        if A.A_P_V_DS.update(visit):
            if visit.status == PolibasePersonVisitStatus.CANCELED:
                return
            telephone_number: str | None = visit.telephoneNumber
            if nn(telephone_number) and A.C.telephone_number(telephone_number):
                telephone_number = A.D_F.telephone_number_international(
                    telephone_number
                )
                Api.check_for_notification_confirmation(telephone_number, SENDER)
                A.E.polibase_person_visit_was_registered(visit)
                type_value: int | None = None
                visit_notification: PPVNDS
                visit_notification_check_for_unique_per_date: PPVN | None = None
                message: DM = DM(None, telephone_number, SENDER)
                if A.S.get(
                    A.CT_S.POLIBASE_PERSON_VISIT_NEED_REGISTER_GREETING_NOTIFICATION
                ):
                    type_value = A.D.get(PPVNType.GREETING)
                    visit_notification_check_for_unique_per_date = PPVN(
                        type=type_value,
                        registrationDate=A.D.to_date_string(visit.registrationDate),
                    )
                    set_visit_notification_unique_property(
                        visit, visit_notification_check_for_unique_per_date
                    )
                    if not A.C_P_N.exists(visit_notification_check_for_unique_per_date):
                        visit_notification = PPVNDS(
                            visit.id, A.ME_D.register(message), type_value
                        )
                        if A.A_P_N.register(visit_notification):
                            A.E.polibase_person_visit_notification_was_registered(
                                visit, visit_notification
                            )
                    else:
                        if A.D.now() <= nndt(
                            A.D.datetime_from_string(
                                visit.beginDate, A.CT.ISO_DATETIME_FORMAT
                            )
                        ):
                            visit_notification = PPVNDS(
                                visit.id,
                                A.ME_D.register(message),
                                PPVNType.DEFAULT.value,
                            )
                            if A.A_P_N.register(visit_notification):
                                A.E.polibase_person_visit_notification_was_registered(
                                    visit, visit_notification
                                )
                        else:
                            # abort
                            pass
                if A.S.get(
                    A.CT_S.POLIBASE_PERSON_VISIT_NEED_REGISTER_REMINDER_NOTIFICATION
                ):
                    type_value = PPVNType.REMINDER.value
                    visit_notification_check_for_unique_per_date = PPVN(
                        type=type_value, beginDate=A.D.to_date_string(visit.beginDate)
                    )
                    set_visit_notification_unique_property(
                        visit, visit_notification_check_for_unique_per_date
                    )
                    if not A.C_P_N.exists(visit_notification_check_for_unique_per_date):
                        message.date = A.D.datetime_from_string(
                            visit.beginDate
                        ) - timedelta(
                            minutes=A.S.get(
                                A.CT_S.POLIBASE_PERSON_VISIT_TIME_BEFORE_REMINDER_NOTIFICATION_IN_MINUTES
                            )
                        )
                        if A.D.now() < message.date:
                            visit_notification = PPVNDS(
                                visit.id, A.ME_D.register(message), type_value
                            )
                            if A.A_P_N.register(visit_notification):
                                A.E.polibase_person_visit_notification_was_registered(
                                    visit, visit_notification
                                )
                        else:
                            # abort
                            pass
            else:
                # wrong telephone number - not for whatsapp sending
                pass

    serve(
        SD,
        server_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":
    start()
