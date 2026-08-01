"""
Tests for CareNote and CareNoteCollection domain models.

These tests follow the Arrange-Act-Assert (AAA) pattern:
  - Arrange: set up the data and objects needed
  - Act:     call the method being tested
  - Assert:  verify the result is what you expect

Run with:
    pytest tests/ -v
    pytest tests/ -v -k "test_flag"   # run only tests matching 'test_flag'
    pytest tests/ -v --tb=short       # shorter traceback on failure
"""


import pytest
from src.day2_functions.care_note import CareNote, CareNoteCollection

# ─────────────────────────────────────────────────────────────
# Fixtures — reusable test objects (like @BeforeEach in JUnit)
# ─────────────────────────────────────────────────────────────

@pytest.fixture
def basic_note() -> CareNote:
    """A standard care note with no risk flagging."""
    return CareNote(
        content="Patient ate well today",
        worker_id="worker-123",
        recipient_id="recipient-001"
    )

@pytest.fixture
def high_risk_note() -> CareNote:
    """A care note flagged as high risk (confidence above 0.85 threshold)."""
    note = CareNote(
        content="Patient fell near bathroom",
        worker_id="worker-123",
        recipient_id="recipient-001"
    )
    note.flag_risk(0.92)
    return note

@pytest.fixture
def empty_collection() ->CareNoteCollection:
    """An empty collection for recipient-001."""
    return CareNoteCollection("recipient-001")

# --------------------------------------------------------
# CareNote - initial state
# --------------------------------------------------------

class TestCareNoteDefaults:
    """Verify a new CareNote starts with safe default values."""

    def test_risk_flagged_is_false_by_default(self,basic_note):
        # A new note should never be risk-flagged without an explicit action
        assert basic_note.risk_flagged is False

    def test_confidence_is_zero_by_default(self,basic_note):
        # Confidence starts at 0 - only meaningful after flag_risk() is called
        assert basic_note.confidence == 0.0

    def test_content_is_stored(self,basic_note):
        assert basic_note.content == "Patient ate well today"

    def test_worker_id_is_stored(self, basic_note):
        assert basic_note.worker_id == "worker-123"


# --------------------------------------------------------
# CareNote - risk flagging
# --------------------------------------------------------

class TestCareNoteFlagRisk:
    """Verify risk flagging behaviour and validation."""

    def test_flag_risk_sets_risk_flagged_to_true(self, basic_note):
        # Arrange
        assert basic_note.risk_flagged is False

        #Act
        basic_note.flag_risk(0.92)

        # Assert
        assert basic_note.risk_flagged is True

    def test_flag_risk_stores_confidence_score(self,basic_note):
        basic_note.flag_risk(0.92)
        assert basic_note.confidence == 0.92

    def test_flag_risk_rejects_confidence_above_one(self,basic_note):
        # Confidence must be a probability - max is 1.0
        with pytest.raises(ValueError, match="Confidence must be 0-1"):
            basic_note.flag_risk(1.5)

    def test_flag_risk_rejects_negative_confidence(self,basic_note):
        with pytest.raises(ValueError):
            basic_note.flag_risk(-0.1)

    def test_flag_risk_accepts_boundary_value_zero(self,basic_note):
        # 0.0 is a valid confidence score (very uncertain)
        basic_note.flag_risk(0.0)
        assert basic_note.risk_flagged is True

    def test_flag_risk_accepts_boundary_value_one(self,basic_note):
        # 1.0 is a valice confidence score (certain)
        basic_note.flag_risk(1.0)
        assert basic_note.risk_flagged is True

# -------------------------------------------------------------
# CareNote - high risk classification
# -------------------------------------------------------------

class TestCareNotIsHighRisk:
    """
    High risk = flagged AND cofidence >= 0.85.
    Below the threshold  is flagged but not high risk - surfaces as
    a low-priority indicator only, not an alert
    """
    def test_high_confidence_flagged_note_is_high_risk(self,high_risk_note):
        # Confidence 0.92 >= 0.85 threshold -> high risk
        assert high_risk_note.is_high_risk() is True

    def test_low_confidence_flagged_note_is_not_high_risk(self,basic_note):
        # Confidence 0.79 < 0.85 threshold -> flagged but not high risk
        basic_note.flag_risk(0.78)
        assert basic_note.is_high_risk() is False

    def test_unflagged_note_is_not_high_risk(self,basic_note):
        # No flag at all -> not high risk regardless of any default values
        assert basic_note.is_high_risk() is False

    def test_exactly_at_threshold_is_high_risk(self,basic_note):
        # Boundayr:0.85 should be included (>=, not >)
        basic_note.flag_risk(0.85)
        assert basic_note.is_high_risk() is True

    def test_just_below_threshold_is_not_high_risk(self, basic_note):
        # Boundary: 0.849 should Not be high risk
        basic_note.flag_risk(0.849)
        assert basic_note.is_high_risk() is False


# ---------------------------------------------------------------
# CareNoteCollection - basic operations
# ---------------------------------------------------------------

class TestCareNoteCollection:
    """Verify collection management and recipient enforcment."""

    def test_new_collection_is_empty(self, empty_collection):
        assert empty_collection.count() == 0

    def test_add_note_increments_count(self, empty_collection,basic_note):
        empty_collection.add(basic_note)
        assert empty_collection.count() == 1

    def test_add_multiple_notes(self,empty_collection,basic_note,high_risk_note):
        empty_collection.add(basic_note)
        empty_collection.add(high_risk_note)
        assert empty_collection.count() ==2

    def test_add_rejects_note_for_wrong_recipient(self,empty_collection):
        # Recipient enforcement - prevents mixing up patient records
        wrong_note = CareNote("Note","worker-123","recipient-999")
        with pytest.raises(ValueError,match="different recipient"):
            empty_collection.add(wrong_note)


# -----------------------------------------------------------------
# CareNoteCollection - high risk filtering
# -----------------------------------------------------------------

class TestCareNoteCollectionHighRisk:
    """Verify high risk note filtering returns the right subset"""

    def test_no_high_risk_notes_returns_empty_list(self,empty_collection,basic_note):
        empty_collection.add(basic_note)
        assert empty_collection.high_risk_notes() == []

    def test_high_risk_note_is_included_in_filter(self,empty_collection,high_risk_note):
        empty_collection.add(high_risk_note)
        assert len(empty_collection.high_risk_notes()) == 1

    def test_only_high_risk_notes_returned(self, empty_collection,basic_note,high_risk_note):
        # Arrange: one safe, one risky
        empty_collection.add(basic_note)
        empty_collection.add(high_risk_note)

        # Act
        result = empty_collection.high_risk_notes()

        # Assert: only the risky one comes back
        assert len(result) == 1
        assert result[0] is high_risk_note

    def test_summary_reflects_correct_counts(self,empty_collection,basic_note,high_risk_note):
        empty_collection.add(basic_note)
        empty_collection.add(high_risk_note)

        summary = empty_collection.summary()

        assert summary["total_notes"] == 2
        assert summary["high_risk_count"] == 1
        assert summary["recipient_id"] == "recipient-001"



    