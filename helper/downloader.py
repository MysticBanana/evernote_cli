import os
import codecs

from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec, NoteFilter

"""    @property
    def api_key(main_class):
        # getter for api key
        return main_class.global_data_manager.get_api_key()"""
#TODO eine klasse

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
        resguid = ' '.join(map(str, note.resources))  # note.resources contains guid for Files; to string

        bodyhash = note.resources[0].data.bodyHash

        print bodyhash.decode()

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
            f = open('Notes/' + booktitle[counter] + '/' + newpath + '/' + file_name,
                     "w+")  # create file with correspond. File extension
            #logger.info("File " + file_name + " created")
            #logger.info(
            #    "Path of File " + file_name + ": " + 'Notes/' + booktitle[
            #        counter] + '/' + newpath + '/' + file_name)
            f.write(file_content)  # TODO check ob beriets vorhanden
            #logger.info("File " + file_name + " written")
            f.close()
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
