class CourtCase:
    def __init__(self, case_number: str):
        # обязательный параметр
        self.case_number = case_number
        # атрибуты по умолчанию
        self.case_participants = []
        self.listening_datetimes = []
        self.is_finished = False
        self.verdict = ""

    def set_a_listening_datetime(self, datetime_str: str):
        """Добавить заседание (например: '2025-09-22 10:00')"""
        self.listening_datetimes.append(datetime_str)

    def add_participant(self, participant: str):
        """Добавить участника (например: ИНН или ФИО)"""
        if participant not in self.case_participants:
            self.case_participants.append(participant)

    def remove_participant(self, participant: str):
        """Удалить участника"""
        if participant in self.case_participants:
            self.case_participants.remove(participant)

    def make_a_decision(self, verdict: str):
        """Вынести решение и закрыть дело"""
        self.verdict = verdict
        self.is_finished = True

    def __str__(self):
        """Красивый вывод информации о деле"""
        return (f"Дело №{self.case_number}\n"
                f"Участники: {self.case_participants}\n"
                f"Заседания: {self.listening_datetimes}\n"
                f"Завершено: {self.is_finished}\n"
                f"Решение: {self.verdict}")
