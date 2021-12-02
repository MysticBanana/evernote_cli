import os
import codecs

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec, NoteFilter

from helper import krypto_manager

"""    @property
    def api_key(main_class):
        # getter for api key
        return main_class.global_data_manager.get_api_key()"""
#TODO eine klasse


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
        bookguid = []
        booktitle = []

        # logger = main_class.create_logger("FileDownloader")

        for note in ourNoteList.notes:
            wholeNote = self.note_store.getNote(self.access_token, note.guid, True, False, True, False)
            # logger.info("Note guid: " + note.guid)
            # logger.info("Notebook guid: " + str(wholeNote.notebookGuid))
            bookguid.append(wholeNote.notebookGuid)
            guidlist.append(note.guid)  # Liste with all guids of Notes
            titlelist.append(note.title)
            booktitle.append(self.note_store.getNotebook(self.access_token, wholeNote.notebookGuid).name)

        counter = 0
        for numbers in guidlist:
            note = self.note_store.getNote(self.access_token, guidlist[counter], True, False, True, False)  # Data about Note
            resguid = ""
            if note.resources is not None:
                resguid = ' '.join(map(str, note.resources))  # note.resources contains guid for Files; to string

            resguidcount = resguid.count("guid='")  # count Files in Notes
            # logger.info("Files in Note: " + str(resguidcount))
            # logger.info("Note Resources: " + resguid)

            offset = -1
            newpath = titlelist[counter]
            if not os.path.exists(self.path + booktitle[counter] + '/' + newpath):
                os.makedirs(self.path + booktitle[counter] + '/' + newpath)

            while True:
                offset = resguid.find("guid='", offset + 1)  # find guid of File in resources
                if offset == -1:
                    break
                offsetend = resguid.find("'", offset + 6)  # find end of guid
                tmpguid = resguid[offset + 6:offsetend]  # "safe" guid
                # logger.info("File guid: " + tmpguid)

                resource = self.note_store.getResource(tmpguid, True, False, True, False)
                file_content = resource.data.body  # raw data of File

                file_name = resource.attributes.fileName  # file_name includes File extension
                file_namepath = self.path + booktitle[counter] + '/' + newpath + '/' + file_name  # tmp for hash test


                with open(file_namepath, "wb") as f: # create file with correspond. File extension
                    f.write(file_content)
                if resource.data.bodyHash != krypto_manager.md5(file_namepath):  # Hash check
                    print("ALARM")  # tmp

            counter = counter + 1



def downloadstart(token):
    access_token = token
    client = EvernoteClient(token=access_token, sandbox=True)  # sandbox=True for devtoken
    noteStore = client.get_note_store()
    # find all Guids:
    filter = NoteFilter()  # Suchfilter
    # filter.words = testsuche          to narrow down note download
    filter.ascending = True  # results ascending
    meta = NotesMetadataResultSpec()
    meta.includeTitle = True
    downloadFile(noteStore, access_token, filter, meta)
    downloadText(noteStore, access_token, filter, meta)

def downloadFile(noteStore, access_token, filter, meta):
    # Used to find the high-level information about a set of the notes from a user's account based on various criteria
    # (string authenticationToken, NoteFilter filter, i32 offset, i32 maxNotes, NotesMetadataResultSpec resultSpec)
    ourNoteList = noteStore.findNotesMetadata(access_token, filter, 0, 250, meta)
    guidlist = []
    titlelist = []
    bookguid = []
    booktitle = []

    #logger = main_class.create_logger("FileDownloader")

    for note in ourNoteList.notes:
        wholeNote = noteStore.getNote(access_token, note.guid, True, False, True, False)
        #logger.info("Note guid: " + note.guid)
        #logger.info("Notebook guid: " + str(wholeNote.notebookGuid))
        bookguid.append(wholeNote.notebookGuid)
        guidlist.append(note.guid)  # Liste with all guids of Notes
        titlelist.append(note.title)
        booktitle.append(noteStore.getNotebook(access_token, wholeNote.notebookGuid).name)

    counter = 0
    for numbers in guidlist:
        note = noteStore.getNote(access_token, guidlist[counter], True, False, True, False)  # Data about Note
        resguid = ""
        if note.resources is not None:
            resguid = ' '.join(map(str, note.resources))  # note.resources contains guid for Files; to string

        resguidcount = resguid.count("guid='")  # count Files in Notes
        #logger.info("Files in Note: " + str(resguidcount))
        #logger.info("Note Resources: " + resguid)

        offset = -1

        if not os.path.exists("Notes"):  # Folder for Notes
            os.makedirs("Notes")

        if not os.path.exists("Notes/" + booktitle[counter]):  # Folder for Notes
            os.makedirs("Notes/" + booktitle[counter])

        newpath = titlelist[counter]  # Folder for every Note
        if not os.path.exists('Notes/' + booktitle[counter] + '/' + newpath):
            os.makedirs('Notes/' + booktitle[counter] + '/' + newpath)

        while True:
            offset = resguid.find("guid='", offset + 1)  # find guid of File in resources
            if offset == -1:
                break
            offsetend = resguid.find("'", offset + 6)  # find end of guid
            tmpguid = resguid[offset + 6:offsetend]  # "safe" guid
            #logger.info("File guid: " + tmpguid)

            resource = noteStore.getResource(tmpguid, True, False, True, False)
            file_content = resource.data.body  # raw data of File

            file_name = resource.attributes.fileName  # file_name includes File extension
            file_namepath = 'Notes/' + booktitle[counter] + '/' + newpath + '/' + file_name # tmp for hash test
            f = open('Notes/' + booktitle[counter] + '/' + newpath + '/' + file_name,
                     "w+")  # create file with correspond. File extension
            #logger.info("File " + file_name + " created")
            #logger.info(
            #    "Path of File " + file_name + ": " + 'Notes/' + booktitle[
            #        counter] + '/' + newpath + '/' + file_name)
            f.write(file_content)  # TODO check ob beriets vorhanden
            #logger.info("File " + file_name + " written")
            f.close()

            if resource.data.bodyHash != krypto_manager.md5(file_namepath):     # Hash check
                print("ALARM") # tmp

        counter = counter + 1


def downloadText(noteStore, access_token, filter, meta):
    counter = 0
    ourNoteList = noteStore.findNotesMetadata(access_token, filter, 0, 250, meta)
    guidlist = []
    titlelist = []
    booktitle = []

    #logger = main_class.create_logger("TextDownloader")

    for note in ourNoteList.notes:
        wholeNote = noteStore.getNote(access_token, note.guid, True, False, True, False)
        #logger.info("Note guid: " + note.guid)
        guidlist.append(note.guid)  # Liste with all guids of Notes
        titlelist.append(note.title)
        booktitle.append(noteStore.getNotebook(access_token, wholeNote.notebookGuid).name)

    counter = 0
    for numbers in guidlist:
        note = noteStore.getNote(access_token, guidlist[counter], True, False, True, False)  # Data about Note

        if not os.path.exists("Notes"):  # Folder for Notes
            os.makedirs("Notes")

        if not os.path.exists("Notes/" + booktitle[counter]):  # Folder for Notes
            os.makedirs("Notes/" + booktitle[counter])

        newpath = titlelist[counter]  # Folder for every Note
        if not os.path.exists('Notes/' + booktitle[counter] + '/' + newpath):
            os.makedirs('Notes/' + booktitle[counter] + '/' + newpath)

        f = open('Notes/' + booktitle[counter] + '/' + newpath + '/' + "text.txt", "w+")  # create file
        #logger.info("text.txt of " + titlelist[counter] + " created")
        #logger.info(
        #    "Path of File text.txt: " + 'Notes/' + booktitle[counter] + '/' + newpath + '/text.txt')

        f.write(note.content)  # TODO check ob beriets vorhanden
        #logger.info("text.txt of " + titlelist[counter] + " written")
        f.close()

        counter = counter + 1

# TODO einzeln suchen und nach Notebook runterladen (funkt nicht in sandbox)
# TODO download mit tags (funkt nicht in sandbox)
# TODO fixen: funkt. nicht ohne bild etc
