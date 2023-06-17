class Card:
    def __init__(self, card_number: int, exp_date: str, cvv: int, issue_date: str, user_id: str, card_status: str):
        self.card_number = card_number
        self.exp_date = exp_date[-4:] + '-' + exp_date[:2] + '-01'
        self.cvv = cvv
        self.issue_date = issue_date
        self.user_id = user_id
        self._card_status = card_status

    @property
    def card_status(self):
        return self._card_status
    @card_status.setter
    def card_status(self,value ):
        exp_status = 'new', 'blocked', 'active'
        if value.lower() not in exp_status:
            raise ValueError("Unexpected card status!")
        elif value.lower() == 'active' and self._card_status == 'blocked':
            raise ValueError("[Error] You cannot interact with a blocked card!")
        else:
            self._card_status = value.lower()

    def attributes(self) -> tuple:
        return (self.card_number,
                self.exp_date,
                self.cvv,
                self.issue_date,
                self.user_id,
                self._card_status)