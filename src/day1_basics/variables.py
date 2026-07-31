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