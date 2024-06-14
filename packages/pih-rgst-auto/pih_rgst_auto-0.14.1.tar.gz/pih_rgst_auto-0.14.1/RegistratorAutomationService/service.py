from typing import Any

import ipih

from pih import A, send_message
from pih.consts.errors import NotFound
from pih.collections import (
    User,
    EventDS,
    Message,
    NewMailMessage,
    PolibasePerson,
    EmailInformation,
    InaccesableEmailInformation,
)
from RegistratorAutomationService.const import SD
from pih.tools import ParameterList, nl, j, b, js, e, ne, nn, one, lw, esc


SC = A.CT_SC

ISOLATED: bool = False


def start(as_standalone: bool = False) -> None:

    print(as_standalone)
    from MobileHelperService.api import MobileOutput
    from MobileHelperService.client import Client as MIO

    email_control_output: MobileOutput = MIO.create_output(
        A.CT_ME_WH.GROUP.EMAIL_CONTROL
    )

    def _send_message(
        telephone_number: str, message: str, queued: bool = False
    ) -> None:
        send_message(
            message, telephone_number, A.CT_ME_WH_W.Profiles.CALL_CENTRE, queued
        )

    def service_call_handler(_, pl: ParameterList) -> Any:
        if A.D_Ex.subscribtion_result(pl).result:
            event: A.CT_E | None = None
            parameters: list[Any] | None = None
            event, parameters = A.D_Ex_E.with_parameters(pl)
            if event in [
                A.E_B.polibase_person_with_inaccessable_email_was_detected(),
                A.E_B.polibase_person_email_was_added(),
            ]:
                email_information: InaccesableEmailInformation = (
                    A.D.fill_data_from_source(
                        InaccesableEmailInformation(),
                        A.E.get_parameter(event, parameters),
                    )
                )
                if event == A.E_B.polibase_person_email_was_added():
                    email_control_output.write_line(
                        f" {A.CT_V.GOOD} Адресс электронной почта пациента {b(email_information.person_name)} ({email_information.person_pin}): {email_information.email} добавлен в карту пациента!"
                    )
                else:
                    email: str = email_information.email
                    workstation_name: str = email_information.workstation_name
                    registrator_person_name: str = (
                        email_information.registrator_person_name
                    )
                    polibase_person_name: str = email_information.person_name
                    polibase_person_pin: int = email_information.person_pin
                    A.ME_WS.by_workstation_name(
                        workstation_name,
                        f" {A.CT_V.WARNING} Внимание! {registrator_person_name}, Вы внесли адресс электронной почты пациента {b(polibase_person_name)} ({polibase_person_pin}): {email}, который определяется как НЕДОСТУПНЫЙ. Проверьте, пожалуйста, внесённые данные или переспросите пациента.",
                    )
                    email_control_output.write_line(
                        f" {A.CT_V.WARNING} День добрый, {b(A.D.to_given_name(email_information.registrator_person_name))}, я бот-помощник Регистратора. Вы внесли адресс электронную почту пациента {polibase_person_name} ({polibase_person_pin}): {b(email)}, которая определяется как {b('недоступная')}. Проверьте внесённые данные или переспросите пациента."
                    )
                return True
            elif event == A.E_B.ask_for_polibase_person_email():
                print(A.E_B.create_parameters_map(event, parameters))
                polibase_person: PolibasePerson = A.D_P.person_by_pin(parameters[1])
                polibase_person_registrator: PolibasePerson = one(
                    A.R_P.person_operator_by_pin(polibase_person.pin)
                ) or one(A.R_P.person_registrator_by_pin(polibase_person.pin))
                eventDS: EventDS | None = one(
                    A.R_E.get_last_by_key(
                        *A.E_B.ask_for_polibase_person_email(polibase_person)
                    )
                )
                telephone_number: str = polibase_person.telephoneNumber
                if nn(eventDS):
                    _send_message(
                        telephone_number,
                        j(
                            (
                                "День добрый, ",
                                b(A.D.to_given_name(polibase_person)),
                                ".",
                                nl(),
                                "Регистратор ",
                                b(A.D.to_given_name(polibase_person_registrator)),
                                " запросил у Вас адресс электронной почты.",
                                nl(),
                                "Для этого - скопируйте код ",
                                A.CT_V.HAND_DOWN,
                                ":",
                            )
                        ),
                    )
                    _send_message(
                        telephone_number,
                        str(eventDS.parameters[A.CT_PI.SECRET.name]),
                    )
                    _send_message(
                        telephone_number,
                        j(
                            (
                                "И отправьте этот код в теме или теле письма на почту: ",
                                nl(),
                                A.CT_EML.ADD_EMAIL,
                                nl(),
                                A.CT_V.HAND_UP,
                                " нажмите на ссылку",
                            )
                        ),
                    )
                return True
            elif event == A.CT_E.NEW_EMAIL_MESSAGE_WAS_RECEIVED:
                new_email_message: NewMailMessage = A.D_Ex.new_mail_message(
                    parameters[3]
                )
                mailbox_address: str = new_email_message.mailbox_address
                subject: str = new_email_message.subject
                text: str = new_email_message.text
                from_: str = new_email_message.from_

                if mailbox_address == A.CT_EML.ADD_EMAIL:
                    secret: int | None = A.D_Ex.decimal(subject) or A.D_Ex.decimal(text)
                    if nn(secret):
                        eventDS: EventDS | None = one(
                            A.R_E.get_last_by_key(
                                *A.E_B.ask_for_polibase_person_email(secret=secret)
                            )
                        )
                        if nn(eventDS):
                            polibase_person_pin: int = eventDS.parameters[
                                A.CT_PI.PERSON_PIN.name
                            ]
                            polibase_person: PolibasePerson = A.D_P.person_by_pin(
                                polibase_person_pin
                            )
                            telephone_number: str = polibase_person.telephoneNumber
                            current_email: str = polibase_person.email
                            if lw(current_email) != from_:
                                if A.A_P.email(from_, polibase_person):
                                    _send_message(
                                        telephone_number,
                                        j(
                                            (
                                                "День добрый, ",
                                                b(A.D.to_given_name(polibase_person)),
                                                ", ",
                                                "адресс электронной почты была добавлена в Вашу карту",
                                            )
                                        ),
                                    )
                    return True
                if (
                    mailbox_address == A.CT_EML.EXTERNAL
                    and from_ == A.CT_EML.MAIL_RU_DAEMON
                ):
                    if subject.startswith(
                        "Ваше сообщение не доставлено. Mail failure."
                    ):
                        error_text: str = (
                            "SMTP error from remote mail server after RCPT TO:<"
                        )
                        index: int = text.find(error_text)
                        email_value: str | None = None
                        if index != -1:
                            email_value = A.D_Ex.email(
                                text[
                                    index
                                    + len(error_text) : text.find(
                                        ">:", index + len(error_text)
                                    )
                                ]
                            )
                        else:
                            email_value = A.D_Ex.email(text)
                        if ne(email_value):
                            message_test: str = b(
                                js(
                                    (
                                        "",
                                        A.CT_V.WARNING,
                                        "Внимание! Сообщение для",
                                        email_value,
                                        "не доставлено",
                                    )
                                )
                            )
                            try:
                                polibase_person: PolibasePerson | None = one(
                                    A.R_P.person_by_email(email_value)
                                )
                                if ne(polibase_person):
                                    message_test += j(
                                        (
                                            nl(),
                                            "Клиент: ",
                                            b(polibase_person.FullName),
                                            " (",
                                            polibase_person.pin,
                                            ")",
                                            nl(),
                                            "Проверьте, пожалуйста, внесённые данные или переспросите пациента.",
                                        )
                                    )
                                email_control_output.write_line(message_test)
                            except NotFound:
                                pass
                return True
            elif event == A.E_B.polibase_person_set_card_registry_folder():
                polibase_person_pin: int = parameters[0]
                polibase_person_card_folder: str = parameters[1]
                registrator_polibase_person_pin: int = parameters[-1]
                try:
                    registrator_user: User = A.R_U.by_polibase_pin(
                        registrator_polibase_person_pin
                    ).data
                    polibase_person: PolibasePerson = A.R_P.person_by_pin(
                        polibase_person_pin
                    ).data
                    set_by_polibase_parameters = (
                        A.E_B.polibase_person_set_card_registry_folder(
                            person=polibase_person, set_by_polibase=False
                        )
                    )
                    if A.C_E.has(*set_by_polibase_parameters):
                        A.A_E.remove(*set_by_polibase_parameters)
                    else:
                        A.ME_WS.by_login(
                            registrator_user.samAccountName,
                            j(
                                (
                                    A.D.to_given_name(registrator_user.name),
                                    ", карта пациента ",
                                    polibase_person.FullName,
                                    " (",
                                    polibase_person.pin,
                                    ") добавлена в папку ",
                                    nl(polibase_person_card_folder, 2),
                                    "ВЛОЖИТЕ КАРТУ В КОНЕЦ ПАПКИ!",
                                )
                            ),
                        )
                except NotFound as _:
                    pass
                return True
            elif event == A.E_B.mail_to_polibase_person_was_sent():
                polibase_note_id: int = parameters[0]
                polibase_person_pin: int = parameters[1]
                try:
                    email_address: str | None = None
                    allow_for_notification: bool = False
                    polibase_person: PolibasePerson | None = A.R_P.person_by_pin(
                        polibase_person_pin
                    ).data
                    event_success_ds: EventDS | None = one(
                        A.R_E.get(
                            *A.E_B.polibase_person_email_was_added(
                                value_for_search=polibase_person
                            )
                        )  # type: ignore
                    )  # type: ignore
                    event_not_success_ds: EventDS | None = None
                    if e(event_success_ds):
                        event_not_success_ds = one(
                            A.R_E.get(
                                *A.E_B.polibase_person_with_inaccessable_email_was_detected(
                                    polibase_person
                                )
                            )  # type: ignore
                        )  # type: ignore
                        if e(event_not_success_ds):
                            allow_for_notification = A.C.email(
                                polibase_person.email, check_accesability=True  # type: ignore
                            )  # type: ignore
                        else:
                            email_address = A.D.fill_data_from_source(
                                EmailInformation(), event_not_success_ds.parameters  # type: ignore
                            ).email  # type: ignore
                            if lw(polibase_person.email) != lw(email_address):  # type: ignore
                                allow_for_notification = A.C.email(
                                    polibase_person.email, check_accesability=True  # type: ignore
                                )  # type: ignore
                    else:
                        email_address = A.D.fill_data_from_source(
                            EmailInformation(), event_success_ds.parameters  # type: ignore
                        ).email  # type: ignore
                        allow_for_notification = lw(polibase_person.email) == lw(
                            email_address
                        )  # type: ignore
                        if not allow_for_notification:
                            allow_for_notification = A.C.email(
                                polibase_person.email, check_accesability=True
                            )

                    polibase_note_title: str = A.D_P.note_title(polibase_note_id)
                    if allow_for_notification:
                        _send_message(
                            j(
                                (
                                    A.S.get(A.CT_S.PERSON_VISIT_NOTIFICATION_HEADER),
                                    b(
                                        A.D.to_given_name(
                                            polibase_person.FullName  # type: ignore
                                        )
                                    ),
                                    ", на Вашу электронную почту отправлено письмо с медицинской записью ",
                                    esc(
                                        polibase_note_title,
                                    ),
                                    ".",
                                    nl(count=2),
                                    b("Важно:"),
                                    " если письма нет на почте, посмотрите в папке ",
                                    b("Спам"),
                                    ".",
                                )
                            ),
                            polibase_person.telephoneNumber,  # type: ignore
                            True,
                        )
                    else:
                        email_address = polibase_person.email
                        email_control_output.write_line(
                            j(
                                (
                                    js(
                                        (
                                            "",
                                            A.CT_V.WARNING,
                                            "При отправке письма",
                                            b(polibase_note_title),
                                            "пациенту",
                                            b(polibase_person.FullName),
                                            j(("(", polibase_person.pin, "),")),
                                            j(
                                                (
                                                    "был выявлен адресс электронной почты: ",
                                                    b(email_address),
                                                    ", который определяется как НЕДОСТУПНЫЙ.",
                                                )
                                            ),
                                            nl(),
                                        )
                                    ),
                                    "Проверьте, пожалуйста, внесённые данные или переспросите пациента.",
                                )
                            )
                        )
                except NotFound as _:
                    pass
                return True
            return True

    def service_starts_handler() -> None:
        A.SRV_A.subscribe_on(SC.send_event)

    A.SRV_A.serve(
        SD,
        service_call_handler,
        service_starts_handler,
        isolate=ISOLATED,
        as_standalone=as_standalone,
    )


if __name__ == "__main__":
    start()
