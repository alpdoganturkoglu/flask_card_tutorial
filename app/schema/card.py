from dataclasses import dataclass

@dataclass
class CardSchema:

    topic: str
    question: str
    typ: str

    def validate_form(self) -> bool:
        if not self.topic or not self.question:
            return False
        if self.typ == 'general' or self.typ == 'code':
            return True
        return False
