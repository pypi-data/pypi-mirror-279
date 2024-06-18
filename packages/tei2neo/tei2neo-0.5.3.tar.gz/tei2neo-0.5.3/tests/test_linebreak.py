import pytest
import json
import time
import os

from tei2neo import parse, GraphUtils

FIXTURE_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    'xml_testfiles',
)

def _load_graph(graph, filename):

    filename = os.path.join(FIXTURE_DIR, filename)
    if not os.path.isfile(filename):
        raise ValueError("File {} does not exist.".format(filename))
    doc, status, soup = parse(filename=filename)
    tx = graph.begin()
    doc.save(tx)
    tx.commit() 


def test_inner_relationships(graph):
    """Tests whether elements that refer to each other
    via "prev", "next" attributes are actually linked
    via such relationships
    """
    tei_file = 'linebreak.xml'
    _load_graph(graph, tei_file)
    gut = GraphUtils(graph)
    gut.link_inner_relationships(tei_file)
    paras = gut.paragraphs_for_filename(tei_file)
    for para in paras:
        tokens = gut.tokens_in_paragraph(para)
        gut.create_unhyphenated(tokens)
