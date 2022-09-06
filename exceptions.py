class CantSendMess(Exception):
    """Не можем достучаться до бота."""

    pass


class GetNoAnswerException(Exception):
    """Ответ апи вернул не словарь."""

    pass


class GetNot200AnswerException(Exception):
    """Ответ апи отдаёт не тот код."""

    pass


class HomeworkIsntADicException(Exception):
    """Домашка пришла не словарём."""

    pass


class HomeworksIsNtListException(TypeError):
    """Список домашек не является списком"""

    pass


class PractikumApiNotOKException(Exception):
    """Ошибка возникает в случае недоступности апи Практикума."""

    pass


class NoHomeworksInAnswerException(Exception):
    """Ошибка возникает в случае некорректного ответа апи."""

    pass


class NoDictInApiAnsewerException(TypeError):
    """Ответ апи вернул не словарь."""

    pass


class NoNameInApiAnsewerException(KeyError):
    """Ответ апи вернул не словарь."""

    pass


class NotDocumentedStatusException(Exception):
    """Пришёл недокументированный статус домашки."""

    pass


class NotEnouthSecrets(Exception):
    """Найдены не все секреты."""

    pass
