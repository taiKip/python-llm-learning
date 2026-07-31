#Day 1 - Variables and types

#Strings - care note text, prompts, API responses

care_note = "Patient was agitated during morning routine"
recipient_name = "Mrs Johnson"
model_name = "claude-sonnet-4-6"



# Numbers - confidence scores, token counts, response times
confidence_score = 0.87
max_tokesn = 1000
shift_id = 42

#Booleans - flags you'll use everywhere
is_risk_flagged = True
pii_scrubbed = False


#None - absence of value (like null)
summary = None

# Print them all
print(f"Note: {care_note}")
print(f"Recipient: {recipient_name}")
print(f"Model: {model_name}")
print(f"Confidence: {confidence_score}")
print(f"Risk flagged: {is_risk_flagged}")
print(f"Summary: {summary}")

# Check types  - Python is dynamically typed unlike Java

print(f"\nTypes:")
print(f" care_note is {type(care_note)}")
print(f" confidence_score is {type(confidence_score)}")
print(f" is_risk_flagged is {type(is_risk_flagged)}")
print(f" summary is {type(summary)}")

# STRINGS
# Three ways to write strings - you'll use all three

single = 'single quotes work'
double = "double quotes work"
multiline = """
This is a multiline string.
Perfect for writing LLM prompts
that span several lines
"""

# f-strings - use these everywhere,like Java's String.format()
worker = "Tarus"
shift = "morning"
message = f"Woker {worker} confirmed the {shift} shift"
print(message)

# Usefull string methods
note = "  Patient was AGITATED and refused breakfast "
print(note.strip())
print(note.strip().lower())
print(note.strip().upper())
print(note.strip().replace("AGITATED","agitated")) # replace

# Check content
print("agitated" in note.lower())
print(note.strip().startswith("Patient"))
print(len(note.strip()))

#-- LISTS ------------

care_notes = [
    "Patient was agitated during morning routine",
    "Refused breakfast",
    "Calmed after music therapy at 10am",
    "Ate full lunch",
    "Complained of knee pain at 3pm"
]

# Access by index

print(care_notes[0])
print(care_notes[-1])

# Slice
print(care_notes[1:3])

# Loop 
for note in care_notes:
    print(f" - {note}")


# Add and remove
care_notes.append("Settled for the evening")
care_notes.remove("Refused breakfast")
print(f"\n{len(care_notes)} notes remaining")

# Check membership
print("Refused breakfast" in care_notes)  # False - we removed it

# DICTIONARIES
# Key-value pairs - like Java's  Hashmap

worker = {
    "id": "worker-123",
    "name": "Tarus",
    "skills": ["dementia_care","hoist_trained","wound_care"],
    "on_time_rate": 0.98,
    "available": True
}

# Access values
print(worker["name"])
print(worker.get("email"))
print(worker.get("email","no email on file")) # with default

# Add and update
worker["email"]  = "tarus@example.com"
worker["on_time_rate"] =0.99 # update existing

# Check if key exists
print("skills" in worker)
print("phone" in worker)

#Loop over keys and values

for key, value in worker.items():
    print(f"  {key}:{value}")


# Nested dict 
shift_match = {
    "shift_id": "shift-456",
    "top_match":{
        "worker_id": "worker-123",
        "score":87,
        "reason": "8 prior shifts with recipient · 4.2km · 98% on time ",
        "confidence_flage":False
    },
    "model_version":"shift-matching-v4.2.1"
}

# Access nested values
print(shift_match["top_match"]["score"])
print(shift_match["top_match"]["reason"])