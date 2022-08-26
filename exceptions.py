class GetNoAnswerException(Exception):
    """Ответ апи вернул не словарь."""

    pass


class GetNot200AnswerException(Exception):
    """Ответ апи вернул не словарь."""

    pass


class HomeworkIsntADicException(Exception):
    """Домашка пришла не словарём."""

    pass


class PractikumApiNotOKException(Exception):
    """Ошибка возникает в случае недоступности апи Практикума."""

    pass


class NoHomeworksInAnswerException(Exception):
    """Ошибка возникает в случае некорректного ответа апи."""

    pass


class NoDictInApiAnsewerException(Exception):
    """Ответ апи вернул не словарь."""

    pass


class NotDocumentedStatusException(Exception):
    """Пришёл недокументированный статус домашки."""

    pass


class NotEnouthSecrets(Exception):
    """Найдены не все секреты."""

    pass
