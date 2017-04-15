# coding: utf-8
from datetime import datetime as dt
from bs4 import BeautifulSoup

from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types
import evernote.edam.notestore.ttypes as NoteStore

class EvernoteDiary:
    def __init__(self, evernote_token):
        client = EvernoteClient(
            token = evernote_token,
            sandbox=False
        )

        self.noteStore = client.get_note_store()

    def createDiary(self, title):
        note = Types.Note(title=title, notebookGuid="a600f79c-f5e8-46dd-87a8-7406b134c5e9")
        note = self.noteStore.createNote(note)
        note.content = '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd"><en-note></en-note>'
        return note

    def getNotes(self, words):
        note_filter = NoteStore.NoteFilter()
        note_filter.words = words
        notes_metadata_result_spec = NoteStore.NotesMetadataResultSpec()

        notes = self.noteStore.findNotesMetadata(
                note_filter, 0, 1, notes_metadata_result_spec
        )

        return notes

    def getTodayDiary(self):
        today_diary = dt.now().strftime('%Y%m%d')
        notes = self.getNotes(today_diary)
        note = None
        if notes.totalNotes > 0:
            note = self.noteStore.getNote(notes.notes.pop().guid, True, False, False, False)
        else:
            note = self.createDiary(today_diary)

        return note

    def getBorder(self, soup):
        border = soup.new_tag('div')
        border['style'] = "border-bottom: solid 1px #eeeeee;"
        return border

    def replace_newline_with_br(self, content, soup):
        lines = content.split('\n')
        div = soup.new_tag('div')
        for line in lines:
            div.append(line)
            div.append(soup.new_tag('br'))
        div.append(self.getBorder(soup))
        soup.find("en-note").append(div)

    def setContent2Note(self, note, content):
        soup = BeautifulSoup(note.content, "html.parser")

        self.replace_newline_with_br(content, soup)

        note.content = soup.prettify()
        self.noteStore.updateNote(note)

    def keepDiary(self, content):
        note = self.getTodayDiary()
        self.setContent2Note(note, content)

