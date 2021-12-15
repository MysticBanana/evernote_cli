import os
from datetime import datetime

# TODO: Tags in Meta funkt nicht aber kp warum
# TODO: "a mit punkten drueber" in meta nicht richtig / irgendwas mit unicode
# TODO einzeln suchen und nach Notebook runterladen (funkt nicht in sandbox)
# TODO download mit tags (funkt nicht in sandbox)

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec, NoteFilter

from helper import krypto_manager


class EvernoteAccess(EvernoteClient):
    # used to interact with the api
    def __init__(self, user_data, **kwargs):
        self.user_data = user_data
        self.access_token = self.user_data.user_key
        super(EvernoteAccess, self).__init__(token=self.user_data.user_key, **kwargs)


class EvernoteUser(EvernoteAccess):
    # for getting user specific data from evernote
    def __init__(self, user_data, **kwargs):
        super(EvernoteUser, self).__init__(user_data, **kwargs)

        self.user_store = self.get_user_store()
        self.user_info = self.user_store.getUser()

    def get_user_info(self):
        return vars(self.user_info)


class EvernoteNote(EvernoteAccess):
    def __init__(self, user_data, **kwargs):
        super(EvernoteNote, self).__init__(user_data, **kwargs)

        self.note_store = self.get_note_store()
        self.filter = NoteFilter(ascending=True)
        self.meta = NotesMetadataResultSpec(*[True for i in range(10)])

        self.path = self.user_data.file_path

    def download(self):
        ourNoteList = self.note_store.findNotesMetadata(self.access_token, self.filter, 0, 250, self.meta)
        guidlist = []
        titlelist = []
        booktitle = []

        # logger = main_class.create_logger("FileDownloader")

        for note in ourNoteList.notes:
            wholeNote = self.note_store.getNote(self.access_token, note.guid, True, False, True, False)
            # logger.info("Note guid: " + note.guid)
            # logger.info("Notebook guid: " + str(wholeNote.notebookGuid))
            guidlist.append(note.guid)  # Liste with all guids of Notes
            titlelist.append(note.title)
            booktitle.append(self.note_store.getNotebook(self.access_token, wholeNote.notebookGuid).name)

        counter = 0
        for numbers in guidlist:
            note = self.note_store.getNote(self.access_token, guidlist[counter], True, False, True,
                                           False)  # Data about Note
            resguid = ""
            if note.resources is not None:
                resguid = ' '.join(map(str, note.resources))  # note.resources contains guid for Files; to string

        for notes in guidlist:

            meta_note = ""

            note = self.note_store.getNote(self.access_token, guidlist[counter], True, False, True,
                                           False)  # Data about Note

            newpath = titlelist[counter].decode('utf-8')

            if not os.path.exists(self.path + booktitle[counter].decode('utf-8') + '/' + newpath):
                os.makedirs(self.path + booktitle[counter].decode('utf-8') + '/' + newpath)

            # meta of Note
            meta_note = "Title: " + note.title + " " + \
                        "Created: " + datetime.fromtimestamp(note.created / 1000).strftime("%A, %B %d, %Y %H:%M:%S") \
                        + " " + "Updated: " \
                        + datetime.fromtimestamp(note.updated / 1000).strftime("%A, %B %d, %Y %H:%M:%S") + " "
            if note.tagNames is not None:
                meta_note = meta_note + note.tagNames + "\n"
            meta_note = meta_note + str(note.attributes) + "\n"

            if note.resources is not None:
                for guids in note.resources:
                    # logger.info("File guid: " + guids.guid)

                    resource = self.note_store.getResource(guids.guid, True, True, True, True)
                    file_name = resource.attributes.fileName.decode('utf-8')  # file_name includes File extension
                    file_namepath = self.path + booktitle[counter].decode('utf-8') + '/' + newpath + '/' + file_name

                    if os.path.exists(file_namepath) and resource.data.bodyHash == krypto_manager.md5(file_namepath):
                        print(file_namepath + " schon da")  # tmp
                    else:
                        file_content = resource.data.body  # raw data of File
                        with open(file_namepath, "wb") as f:  # create file with corresponding File extension
                            f.write(file_content)

                    if resource.data.bodyHash != krypto_manager.md5(file_namepath):  # Hash check
                        print("ALARM")  # tmp

                    # meta of file
                    meta_note = meta_note + str(resource.attributes) + "\n"

            with open(self.path + booktitle[counter].decode('utf-8') + '/' + newpath + '/' + 'text.txt', "w+") as f:
                f.write(note.content)  # download txt of file

            with open(self.path + booktitle[counter].decode('utf-8') + '/' + newpath + '/' + 'meta.txt', "w+") as f:
                f.write(meta_note)  # write meta.txt with metadata

            counter = counter + 1


