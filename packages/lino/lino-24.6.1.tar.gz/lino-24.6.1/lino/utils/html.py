# -*- coding: UTF-8 -*-
# Copyright 2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
"""
Some HTML utilities for Lino.
"""

import types
from lxml import etree
from etgen.html import E, to_rst, fromstring, iselement, join_elems, forcetext, lines2p

# from etgen.html import tostring as et_tostring
from html2text import HTML2Text
from django.utils.html import SafeString, mark_safe, escape
# from lino.utils import tostring


def html2text(html, **kwargs):
    """
    Convert the given HTML-formatted text into equivalent Markdown-structured
    text using `html2text <https://pypi.org/project/html2text/>`__.

    """

    text_maker = HTML2Text()
    text_maker.unicode_snob = True
    for k, v in kwargs.items():
        setattr(text_maker, k, v)
    return text_maker.handle(html)


def py2html(obj, name):
    for n in name.split("."):
        obj = getattr(obj, n, "N/A")
    if callable(obj):
        obj = obj()
    if getattr(obj, "__iter__", False):
        obj = list(obj)
    return escape(str(obj))


def tostring(v, *args, **kw):
    """
    Render the given ElementTree element `v` as an escaped ("safe")
    :class:`str` containing HTML.

    If the value is not an ElementTree element, just convert it into a
    :class:`str`.

    If the value is a generator, convert each item individually and concatenate
    their HTML.

    This started as a copy of :func:`etgen.html.tostring` but uses Django's
    concept of safe strings.
    """
    if isinstance(v, SafeString):
        return v
    if isinstance(v, (types.GeneratorType, list, tuple)):
        return mark_safe("".join([tostring(x, *args, **kw) for x in v]))
    if etree.iselement(v):
        # kw.setdefault('method', 'html')
        kw.setdefault("encoding", "unicode")
        return mark_safe(etree.tostring(v, *args, **kw))
    return escape(str(v))


def assert_safe(s):
    """Raise an exception if the given text `s` is not a safe string."""
    assert isinstance(s, SafeString)
