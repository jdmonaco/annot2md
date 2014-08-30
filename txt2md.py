#!/usr/bin/env python

"""
txt2md.py -- Convert text annotations to a nicer markdown formatting
"""

from __future__ import print_function

import os
import re
import sys
import urllib2
import argparse
import subprocess

PAPERS_DIR = '~/Dropbox/Papers'
ANNOTATIONS_DIR = os.path.join(PAPERS_DIR, 'Annotations')

READER_NOTE_TYPES = ('anchor', 'text')
QUOTE_NOTE_TYPES = ('highlight', 'underline', 'strike-through')
NOTE_TYPES = READER_NOTE_TYPES + QUOTE_NOTE_TYPES


class Note(object):

    def __init__(self, page, ntype, text):
        self.page = page
        self.note_type = self._get_type(ntype)
        self.is_reader_note = self.note_type in READER_NOTE_TYPES
        self.text = self._sanitize(text)

    def add_paragraph(self, newtext):
        self.text += '\n\n%s' % self._sanitize(newtext)

    def _get_type(self, typedesc):
        note_type = None
        if 'strike' in typedesc:
            return 'strike-through'
        for test_type in NOTE_TYPES:
            if test_type in typedesc:
                note_type = test_type
                break
        return note_type

    def _sanitize(self, text):
        text = text.strip()
        text = text.replace('- ', '')
        return text


class Article(object):

    def __init__(self, note_filename):
        self.note_file = note_filename
        self.pdf_file = os.path.splitext(self.note_file)[0] + '.pdf'
        self.cite_key = self._parse_cite_key()
        self.bdsk_link = self._bdsk_link()
        self.md_bdsk_link = self._markdown_bdsk_link()
        self.pdf_path = self._pdf_path()
        self.pdf_link = self._pdf_link()

    def field(self, which):
        return bibdesk_query(which, self.cite_key)

    def _parse_cite_key(self):
        return self.note_file.split()[0]

    def _bdsk_link(self):
        return "x-bdsk://%s" % self.cite_key

    def _markdown_bdsk_link(self):
        return "[%s](%s)" % (self.cite_key, self.bdsk_link)

    def _pdf_path(self):
        papers = os.path.expanduser(PAPERS_DIR)
        return os.path.join(papers, self.field('year'), self.pdf_file)

    def _pdf_link(self):
        return urllib2.quote("file://%s" % self.pdf_path, safe='/:')


def bibdesk_query(field, cite_key):
    """Wrapper for bibdesk-query applescript"""
    bd_script = os.path.join(os.path.split(__file__)[0], 'bibdesk-query.scpt')
    cmd = [bd_script, field, cite_key]
    try:
        val = subprocess.check_output(cmd)
    except subprocess.CalledProcessError:
        raise IOError("could not retrieve field \"%s\" for "
                "cite key %s" % (field, cite_key))
    return val.strip()

def parse_notes(path):
    with file(path, 'r') as fd:
        lines = ''.join(fd.readlines()).split('\n\n')

    notes = []
    cur_note = None
    pat = re.compile('(\d+?):([\w ]+?):(.*)')
    for line in lines:
        line = line.strip()
        if line:
            match = re.match(pat, line)
            if match:
                groups = match.groups()
                page = int(groups[0])
                desc = groups[1].strip().lower()
                text = groups[2].strip()
                cur_note = Note(page, desc, text)
                notes.append(cur_note)
            elif cur_note:
                cur_note.add_paragraph(line)
    return notes

def write_header(fileh, article, notes):
    print("#", article.field('title'), '\n', file=fileh)
    print("### Authors", file=fileh)
    print('*', '\n* '.join(article.field('author').split(' and ')), file=fileh)
    print('\n### Article links', file=fileh)
    print('* Open in BibDesk:', article.md_bdsk_link, file=fileh)
    print('* Open PDF: [%s](%s)' % (article.pdf_file, article.pdf_link), file=fileh)
    print('\n### Annotation summary', file=fileh)
    for ntype in NOTE_TYPES:
        print("* %s notes:" % ntype.title(),
                len(filter(lambda n: n.note_type == ntype, notes)),
                file=fileh)

def write_notes(fileh, notes):
    pages = sorted(list(set(n.page for n in notes)))
    for page in pages:
        page_notes = filter(lambda n: n.page == page, notes)
        print('## Page %d notes\n' % page, file=fileh)
        for note in page_notes:
            if note.is_reader_note:
                print('*', note.text, '*[%s comment]*' % note.note_type, file=fileh)
            else:
                print('* **%s annotation**' % note.note_type.title(), file=fileh)
                print('\n    >%s\n' % note.text, file=fileh)
        if page != pages[-1]:
            hr(fileh)

def hr(fd):
    print('\n%s\n' % ('-'*60), file=fd)

def main(args):
    note_path = args.text_file
    dest, filename = os.path.split(note_path)
    article = Article(filename)
    notes = parse_notes(note_path)
    if args.output:
        md_file = args.output
    else:
        md_file = os.path.splitext(note_path)[0] + '.md'
    with file(md_file, 'w') as fd:
        write_header(fd, article, notes)
        hr(fd)
        write_notes(fd, notes)
    if os.path.isfile(md_file) and args.delete:
        if subprocess.call(['rm', note_path]):
            print('error: could not delete', note_path)
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="Convert notes from annot2txt to markdown format.")
    parser.add_argument("text_file", help="input text file with notes")
    parser.add_argument("-o", "--output", help="optional output file")
    parser.add_argument("-d", "--delete", action="store_true",
            help="delete the input file after conversion")
    args = parser.parse_args(sys.argv[1:])
    sys.exit(main(args))
