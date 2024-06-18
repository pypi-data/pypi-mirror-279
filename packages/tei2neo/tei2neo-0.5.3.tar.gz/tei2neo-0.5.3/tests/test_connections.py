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


def _test_inner_relationships(graph):
    """Tests whether elements that refer to each other
    via "prev", "next" attributes are actually linked
    via such relationships
    """
    tei_file = 'inner_links.xml'
    _load_graph(graph, tei_file)
    
    cursor = graph.run("""
    CREATE (:p {filename:"other.xml", `xml:id`:"p.EE"})
    """)
    gut = GraphUtils(graph)
    gut.link_inner_relationships(tei_file)

    cursor = graph.run("""
    MATCH (:body)-[:CONTAINS*]->(n)
    RETURN n
    """)
    assert len(cursor.data()) == 4

def test_join_elements(graph):
    gut = GraphUtils(graph)

    tei_file = 'A.xml'
    _load_graph(graph, tei_file)
    gut.handle_join_elements(tei_file)
    gut.link_inner_relationships(tei_file)

    tei_file = 'B.xml'
    _load_graph(graph, tei_file)
    gut.handle_join_elements(tei_file)
    gut.link_inner_relationships(tei_file)

    tei_file = 'C.xml'
    _load_graph(graph, tei_file)
    gut.handle_join_elements(tei_file)
    gut.link_inner_relationships(tei_file)
