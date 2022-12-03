class Answer:
    """Base class for answers"""
    __slots__ = ("answer",)
    answer: int | str
    submit = True

    def __init__(self, answer):
        if not isinstance(answer, int) and not isinstance(answer, str):
            raise TypeError("Answer must be int or str")
        self.answer = answer

    def __str__(self):
        return str(self.answer)

    def __repr__(self):
        return self.answer


class NoSubmit(Answer):
    """Do not submit the answer"""
    submit = False

    def __init__(self, answer):
        super().__init__(repr(answer))
