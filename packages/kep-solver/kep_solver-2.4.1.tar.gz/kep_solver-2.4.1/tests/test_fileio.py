import pytest

import xmldiff.main as xmldiff  # type: ignore
import unicodedata  # Needed for xmldiff
import json
from ruamel.yaml import YAML


from unittest.mock import mock_open, patch

import kep_solver.fileio as fileio
from kep_solver.entities import BloodGroup


@pytest.fixture(
    params=[
        ("JSON", fileio.read_json("tests/test_instances/test1.json")),
        ("XML", fileio.read_xml("tests/test_instances/test1.xml")),
        ("YAML", fileio.read_yaml("tests/test_instances/test1.yaml")),
    ]
)
def test_one(request):
    yield request.param


def test_instance_one(test_one) -> None:
    instance = test_one[1]
    assert len(instance.donors()) == 4
    assert len(instance.transplants()) == 5
    firstDonor = instance.donor("1")
    assert firstDonor.age == 50
    assert firstDonor.recipient.id == "1"
    assert firstDonor.bloodGroup == BloodGroup.O
    assert len(firstDonor.transplants()) == 1
    assert instance.recipient("1").pairedWith(firstDonor)
    assert not instance.recipient("2").pairedWith(firstDonor)
    transplant = firstDonor.transplants()[0]
    assert transplant.donor.id == "1"
    assert transplant.recipient.id == "2"
    assert transplant.weight == 1
    secondDonor = instance.donor("2")
    assert secondDonor.age == 50
    assert secondDonor.recipient.id == "2"
    assert secondDonor.bloodGroup == BloodGroup.A
    assert len(secondDonor.transplants()) == 2
    thirdDonor = instance.donor("3")
    assert thirdDonor.age == 60
    assert thirdDonor.recipient.id == "3"
    assert thirdDonor.bloodGroup == BloodGroup.AB
    assert len(thirdDonor.transplants()) == 1
    # Only JSON and YAML can store patient information
    if test_one[0] in ["JSON", "YAML"]:
        assert firstDonor.recipient.bloodGroup == BloodGroup.O
        assert firstDonor.recipient.cPRA == 0.25
        assert secondDonor.recipient.bloodGroup == BloodGroup.B
        assert secondDonor.recipient.cPRA == 0
        assert thirdDonor.recipient.bloodGroup == BloodGroup.O
        assert thirdDonor.recipient.cPRA == 0.98
        fourthDonor = instance.donor("4")
        assert fourthDonor.recipient.bloodGroup == BloodGroup.AB
        assert fourthDonor.recipient.cPRA == 0.10
        assert instance.recipient("1").hasBloodCompatibleDonor()
        assert not instance.recipient("3").hasBloodCompatibleDonor()


def test_one_write_json(test_one) -> None:
    # We only test against JSON in this function
    if test_one[0] != "JSON":
        return
    instance = test_one[1]
    filename = "test-output.json"
    with open("tests/test_instances/test1.json", "r") as infile:
        real_instance_json = json.load(infile)
        with patch("builtins.open", mock_open()) as mo:
            instance.writeFileJson(filename, write_recipients=True)
            mo.assert_called_once_with(filename, "w")
            handle = mo()
            written = " ".join(call.args[0] for call in handle.write.call_args_list)
            written_json = json.loads(written)
            assert written_json == real_instance_json


def test_one_write_yaml(test_one) -> None:
    # We only test against yaml in this function
    if test_one[0] != "YAML":
        return
    instance = test_one[1]
    filename = "test-output.json"
    with open("tests/test_instances/test1.yaml", "r") as infile:
        yaml = YAML()
        real_yaml = yaml.load(infile)
        with patch("builtins.open", mock_open()) as mo:
            instance.writeFileYaml(filename)
            mo.assert_called_once_with(filename, "w")
            handle = mo()
            written = "".join(call.args[0] for call in handle.write.call_args_list)
            written_yaml = yaml.load(written)
            assert written_yaml == real_yaml


def test_one_write_xml(test_one) -> None:
    if test_one[0] != "XML":
        return
    instance = test_one[1]
    filename = "test-output.xml"
    with open("tests/test_instances/test1.xml", "r") as real_instance:
        real_xml = real_instance.read()
    with patch("builtins.open", mock_open()) as mo:
        instance.writeFileXml(filename)
        mo.assert_called_once_with(filename, "w")
        handle = mo()
        written = "".join(str(call.args[0]) for call in handle.write.call_args_list)
        diff = xmldiff.diff_texts(
            unicodedata.normalize("NFKD", real_xml).encode("ascii", "ignore"),
            unicodedata.normalize("NFKD", written).encode("ascii", "ignore"),
        )
        assert not diff


# A bit less stringent checking on these instances


@pytest.fixture(
    params=[
        ("JSON", fileio.read_json("tests/test_instances/test2.json")),
        ("XML", fileio.read_xml("tests/test_instances/test2.xml")),
        ("YAML", fileio.read_yaml("tests/test_instances/test2.yaml")),
    ]
)
def test_two(request):
    yield request.param


def test_instance_two(test_two) -> None:
    instance = test_two[1]
    assert len(instance.donors()) == 6
    assert len(instance.transplants()) == 10
    assert len(instance.donor("5").transplants()) == 2


def test_two_write(test_two) -> None:
    # We can only write JSON, so no point testing for the XML input
    if test_two[0] != "JSON":
        return
    instance = test_two[1]
    filename = "test-output.json"
    with open("tests/test_instances/test2.json", "r") as infile:
        real_instance_json = json.load(infile)
        with patch("builtins.open", mock_open()) as mo:
            # No bloodgroup info, so don't write recipients
            instance.writeFileJson(filename, write_recipients=False)
            mo.assert_called_once_with(filename, "w")
            handle = mo()
            written = " ".join(call.args[0] for call in handle.write.call_args_list)
            written_json = json.loads(written)
            assert written_json == real_instance_json


@pytest.fixture(
    params=[
        ("JSON", fileio.read_json("tests/test_instances/test3.json")),
        ("XML", fileio.read_xml("tests/test_instances/test3.xml")),
        ("YAML", fileio.read_yaml("tests/test_instances/test3.yaml")),
    ]
)
def test_three(request):
    yield request.param


def test_instance_three(test_three) -> None:
    instance = test_three[1]
    assert len(instance.donors()) == 3
    assert len(instance.transplants()) == 4
    assert len(instance.donor("1").transplants()) == 2


@pytest.fixture(
    params=[
        ("JSON", fileio.read_json("tests/test_instances/test3b.json")),
        ("XML", fileio.read_xml("tests/test_instances/test3b.xml")),
        ("YAML", fileio.read_yaml("tests/test_instances/test3b.yaml")),
    ]
)
def test_threeb(request):
    yield request.param


def test_instance_threeb(test_threeb) -> None:
    instance = test_threeb[1]
    assert len(instance.donors()) == 4
    assert len(instance.transplants()) == 9
    assert len(instance.donor("1").transplants()) == 3


@pytest.fixture(
    params=[
        ("JSON", fileio.read_json("tests/test_instances/test4.json")),
        ("XML", fileio.read_xml("tests/test_instances/test4.xml")),
        ("YAML", fileio.read_yaml("tests/test_instances/test4.yaml")),
    ]
)
def test_four(request):
    yield request.param


def test_instance_four(test_four) -> None:
    instance = test_four[1]
    assert len(instance.donors()) == 4
    assert len(instance.transplants()) == 6
    assert len(instance.donor("4").transplants()) == 2
    assert instance.transplants()[0].weight == 4


@pytest.fixture(
    params=[
        ("JSON", fileio.read_json("tests/test_instances/test5.json")),
        ("XML", fileio.read_xml("tests/test_instances/test5.xml")),
        ("YAML", fileio.read_yaml("tests/test_instances/test5.yaml")),
    ]
)
def test_five(request):
    yield request.param


def test_instance_five(test_five) -> None:
    instance = test_five[1]
    assert len(instance.donors()) == 4
    assert len(instance.transplants()) == 4
    ndd = instance.donor("1")
    assert ndd.NDD
    with pytest.raises(Exception):
        ndd.recipient()
    directed = instance.donor("2")
    assert not directed.NDD
    recip = directed.recipient
    assert not recip.pairedWith(ndd)
    assert recip.pairedWith(directed)
    assert recip.id == "2"


@pytest.fixture(
    params=[
        ("JSON", fileio.read_json("tests/test_instances/test7.json")),
        ("YAML", fileio.read_yaml("tests/test_instances/test7.yaml")),
    ]
)
def test_seven(request):
    yield request.param


def test_seven_write(test_seven) -> None:
    instance = test_seven[1]
    filename = "test-output.json"
    with open("tests/test_instances/test7.json", "r") as infile:
        real_instance_json = json.load(infile)
        with patch("builtins.open", mock_open()) as mo:
            # No bloodgroup info, so don't write recipients
            instance.writeFileJson(filename, write_recipients=False)
            mo.assert_called_once_with(filename, "w")
            handle = mo()
            written = " ".join(call.args[0] for call in handle.write.call_args_list)
            written_json = json.loads(written)
            assert written_json == real_instance_json
