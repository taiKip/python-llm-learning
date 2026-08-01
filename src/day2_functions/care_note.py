class CareNote:
    """Represents a single care note entry."""

    #__init__ is the constructor - like Java's CareNote(){}
    def __init__(self,content:str, worker_id: str, recipient_id:str):
        self.content = content
        self.worker_id = worker_id
        self.recipient_id = recipient_id
        self.risk_flagged = False
        self.confidence = 0.0

    # Regular method - self is always first, like Java's this
    def flag_risk(self, confidence: float) ->None:
        if not 0.0 <= confidence <= 1.0:
            raise ValueError(f"Confidence must be 0-1, got {confidence}")
        self.risk_flagged = True
        self.confidence = confidence

    def is_high_risk(self) -> bool:
        return self.risk_flagged and self.confidence >= 0.85
    # __str__ is like Java's toString()
    def __str__(self) -> str:
        status = "⚠️ HIGH RISK" if self.is_high_risk() else "✅ clear"
        return f"[{status}] {self.content[:50]}..."
    #__repr__ - usefull for debugging, shows in lists
    def __repr__(self):
        return f"CareNote(worker={self.worker_id},risk = {self.risk_flagged})"



class CareNoteCollection:
    """Manages a  list of care notes for one recipient."""

    def __init__(self, recipient_id: str):
        self.recipient_id = recipient_id
        self._notes: list[CareNote] = [] # _ prefix means private,like Java's private keyword

    def add(self, note: CareNote)  -> None:
        if note.recipient_id != self.recipient_id:
            raise ValueError("Note belongs to a different recipient")
        self._notes.append(note)

    def high_risk_notes(self) -> list[CareNote]:
        return [n for n in self._notes if n.is_high_risk()]

    def count(self) -> int:
        return len(self._notes)

    def summary(self) -> dict:
        return{
            "recipient_id": self.recipient_id,
            "total_notes":self.count(),
            "high_risk_count": len(self.high_risk_notes())
        }


# Test
note1 = CareNote("Patient ate well today", "worker-123","recipient-001")
note2 = CareNote("Patient fell near bathroom", "worker-123", "recipient-001")
note3 = CareNote("Patient refused medication", "worker-456", "recipient-001")

# Flag risks
note2.flag_risk(0.92)
note3.flag_risk(0.78)


#Print using __str__
print(note1)
print(note2)
print(note3)

# Collection
collection = CareNoteCollection("recipient-001")
collection.add(note1)
collection.add(note2)
collection.add(note3)

print(f"\nTotal notes: {collection.count()}")
print(f"High risk: {collection.high_risk_notes()}")
print(f"Summary: {collection.summary()}")


# Error case
try:
    wrong_note = CareNote("Note for someone else", "worker-123","recipient-999")
    collection.add(wrong_note)
except ValueError as e:
    print(f"\nCaught: {e}")

    