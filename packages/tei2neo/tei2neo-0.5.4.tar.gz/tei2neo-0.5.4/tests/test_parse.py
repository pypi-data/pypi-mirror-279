import json
import random
import re

import pytest
import time

def test_smoke(basic_header):
    assert basic_header.attrs.get('idno') == '20-MS-230'

def test_header_author(basic_header):
    FILEDESC = 0
    TITLESTMT = 0

    things_to_check = {
        'title' : 'Gottfried Semper: Der Stil. Kritische und kommentierte Ausgabe: Manuskripte: MS 215',
        'author': 'Semper, Gottfried (1803-1879)',
        'funder': 'Schweizer Nationalfond',
        'sponsor': 'Università della Svizzera italiana, Eidgenössische Technische Hochschule', 
        'principal': 'Prof. Dr. Philip Ursprung (ETH), Prof. Dr. Sonja Hildebrand (USI)',
    }
    titleStmt = basic_header.child_instances[FILEDESC].child_instances[TITLESTMT]

    for key, text in things_to_check.items():
        objects = list(filter(lambda child: child.__class__.__name__ == key, titleStmt.child_instances))
        assert len(objects) == 1
        assert objects[0].attrs['string'] == text


def test_body(basic_text): 
    body = basic_text.child_instances[0]
    paragraphs = body.child_instances 
    assert len(paragraphs) == 1
    paragraph = paragraphs[0]

    assert len(paragraph.child_instances) == 3

    lb = paragraph.child_instances[0]
    assert lb.__class__.__name__ == 'lb'
    assert lb.attrs['facs'] == '#facs_66_r1l1'
    assert lb.attrs['n'] == 'N001'

    first_token = paragraph.child_instances[1]
    assert first_token.__class__.__name__ == 'Token'
    assert first_token.attrs['string'] == '76'

    second_token = paragraph.child_instances[2]
    assert second_token.__class__.__name__ == 'Token'
    assert second_token.attrs['string'] == '.'


def test_deletion(text_with_deletion): 
    body = text_with_deletion.child_instances[0]
    paragraphs = body.child_instances 
    assert len(paragraphs) == 1
    paragraph = paragraphs[0]

    assert len(paragraph.child_instances) == 4

    lb = paragraph.child_instances[0]
    assert lb.__class__.__name__ == 'lb'
    assert lb.attrs['facs'] == '#facs_15_r3l6'
    assert lb.attrs['n'] == 'N006'

    del_obj = paragraph.child_instances[1]
    assert del_obj.__class__.__name__ == 'text.body.p.del_'
    assert 'string' in del_obj.attrs
    assert len(del_obj.child_instances) == 1

    text_in_del = del_obj.child_instances[0]
    assert text_in_del.__class__.__name__ == 'Token'
    assert text_in_del.string == 'geheimste'
    
    gebiete_text = paragraph.child_instances[2]
    assert gebiete_text.__class__.__name__ == 'Token'
    assert gebiete_text.string == 'Gebiete'



