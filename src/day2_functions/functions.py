# Day 2  - Functions
# In  Python, functions are defined with def

# Basic function - no types required

def greet_worker(name:str) -> str:
    return f"Good morning, {name}"

print(greet_worker("Tarus"))

def create_care_note(content: str, 
                     risk_flagged:bool = False,
                     confidence: float = 0.0) -> dict:
    return{
        "content": content,
        "risk_flagged":risk_flagged,
        "confidence":confidence,
    }
# Call with defaults
note1 = create_care_note("Patient ate well today")
print(note1)

# Call with explicit values
note2 = create_care_note("Patient fell near bathroom",risk_flagged=True, confidence=0.92)
print(note2)

# Multiple return values - Python can return tuples
def scrub_pii(text:str) -> tuple[str,int]:
    """Remove names and return scrubbed 
    text plus count of replacements."""
    replacements = 0
    names = ["Mrs Johnson","John Smith","Mary"]
    for name in names:
        if name in text:
            text = text.replace(name,"[PERSON]")
            replacements += 1
    return text,replacements

scrubbed,count = scrub_pii("Mrs Johnson was agitated, John Smith visited.")
print(f"Scrubbed: {scrubbed}")
print(f"Replacements: {count}")


# -- ERROR HANDLING -------------------------
# Python uses try/except

# Basic try/except
def parse_confidence(value: str) -> float:
    try:
        return float(value)
    except ValueError:
        print(f" Warning: '{value}' is not a valid number , defaulting to 0.0")
        return 0.0

print(parse_confidence("0.87")) # works
print(parse_confidence("high")) # fails gracefully

# Multiple except blocks 

def get_note_by_index(notes: list, index: int)->str:
    try:
        return notes[index]
    except IndexError:
        return "No note at that index"
    except TypeError:
        return "Index must be a number"


notes = ["Patient ate well","Refused medication"]
print(get_note_by_index(notes,0))
print(get_note_by_index(notes,99))
print(get_note_by_index(notes,"a"))

# raise   - java's throw

def validate_confidence(score:float) -> float:
    if not 0.0 <= score <= 1.0:
        raise ValueError(f"Confidence must be between 0 and 1, got {score}")
    return score

try:
    validate_confidence(1.5)
except ValueError as e:
    print(f"Validation error: {e}")

# finally - runs whether or not an exception
# You'll use this to close API connection and clean up resources

def call_fake_api(endpoint:str)->dict:
    connection = None
    try:
        print(f" Opening connection  to {endpoint}")
        connection = {"url":endpoint, "open": True}
        if "bad" in endpoint:
            raise ConnectionError("Endpoint not available")
        return {"status":"ok","data":"some response"}
    except ConnectionError as e:
        print(f" Connect failed: {e}")
        return {"status" : "error","data":None}
    finally:
        if connection:
            connection["open"] = False
            print(f" Connection  closed")

result = call_fake_api("https://api.example.com/summarise")
print(result)

result = call_fake_api("https://bad.endpoint.com")
print(result)