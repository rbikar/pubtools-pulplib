import datetime
import pytest

from pubtools.pulplib import Repository, Distributor, InvalidDataException


def test_missing_props():
    """from_data raises if input data misses necessary data"""
    with pytest.raises(InvalidDataException):
        Repository.from_data({"missing": "necessary props"})


def test_bad_id():
    """from_data raises if input data has id of wrong type"""
    with pytest.raises(InvalidDataException):
        Repository.from_data({"id": ["foo", "bar", "baz"]})


def test_attr_id():
    """from_data sets id attribute appropriately"""
    repo = Repository.from_data({"id": "some-repo"})
    assert repo.id == "some-repo"


def test_default_created():
    """from_data results in None created by default"""
    repo = Repository.from_data({"id": "some-repo"})
    assert repo.created is None


def test_bad_created():
    """from_data raises if input data has created of wrong type"""
    with pytest.raises(InvalidDataException):
        Repository.from_data({"id": "some-repo", "notes": {"created": "whoops"}})


def test_attr_created():
    """from_data sets created attribute appropriately"""
    repo = Repository.from_data(
        {"id": "some-repo", "notes": {"created": "2019-06-11T12:10:00Z"}}
    )

    expected = datetime.datetime(2019, 6, 11, 12, 10, 0, tzinfo=None)
    assert repo.created == expected


def test_distributors_created():
    """from_data sets distributors attribute appropriately"""
    repo = Repository.from_data(
        {
            "id": "some-repo",
            "distributors": [
                {"id": "dist1", "distributor_type_id": "type1"},
                {"id": "dist2", "distributor_type_id": "type1"},
            ],
        }
    )

    assert repo.distributors == (
        Distributor(id="dist1", type_id="type1"),
        Distributor(id="dist2", type_id="type1"),
    )