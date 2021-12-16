import os
from datetime import datetime
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
        self.path = self.path + "/" if self.path[-1] != "/" else self.path
        
    def download(self):
        notelist = self.note_store.findNotesMetadata(self.access_token, self.filter, 0, 250, self.meta)
        booktitlelist = []

        # logger = main_class.create_logger("FileDownloader")

        counter = 0

        for wholenote in notelist.notes:

            meta_note = ""

            wholenote = self.note_store.getNote(self.access_token, wholenote.guid, True, False, True, False)
            # logger.info("Note guid: " + wholenote.guid)
            # logger.info("Notebook guid: " + str(wholenote.notebookGuid))
            booktitlelist.append(self.note_store.getNotebook(self.access_token, wholenote.notebookGuid).name)

            if not os.path.exists(self.path + booktitlelist[counter].decode('utf-8') + '/' + wholenote.title):
                os.makedirs(self.path + booktitlelist[counter].decode('utf-8') + '/' + wholenote.title)

            # meta of Note
            meta_note = "Title: " + wholenote.title + " " + \
                        "Created: " + datetime.fromtimestamp(wholenote.created / 1000).strftime(
                "%A, %B %d, %Y %H:%M:%S") + " " + \
                        "Updated: " + datetime.fromtimestamp(wholenote.updated / 1000).strftime(
                "%A, %B %d, %Y %H:%M:%S") + "\n"
            meta_note = meta_note + "Tags: " + str(self.note_store.getNoteTagNames(wholenote.guid)) + "\n"
            meta_note = meta_note + str(wholenote.attributes) + "\n"

            if wholenote.resources is not None:
                for guids in wholenote.resources:

                    # logger.info("File guid: " + guids.guid)
                    resource = self.note_store.getResource(guids.guid, True, True, True, True)

                    # path with filename and File extension
                    file_namepath = self.path + booktitlelist[counter].decode(
                        'utf-8') + '/' + wholenote.title + '/' + resource.attributes.fileName.decode('utf-8')

                    if os.path.exists(file_namepath) and resource.data.bodyHash == krypto_manager.md5(file_namepath):
                        print(file_namepath + " schon da")  # !!!tmp!!!
                    else:
                        file_content = resource.data.body  # raw data of File
                        with open(file_namepath, "wb") as f:  # create file with corresponding File extension
                            f.write(file_content)

                    if resource.data.bodyHash != krypto_manager.md5(file_namepath):  # Hash check
                        print("ALARM")  # !!!tmp!!!

                    meta_note = meta_note + str(resource.attributes) + "\n"  # meta of file

            with open(self.path + booktitlelist[counter].decode('utf-8') + '/' + wholenote.title + '/' + 'text.txt',
                      "w+") as f:
                f.write(wholenote.content)  # write and download txt of file

            with open(self.path + booktitlelist[counter].decode('utf-8') + '/' + wholenote.title + '/' + 'meta.txt',
                      "w+") as f:
                f.write(meta_note)  # write meta.txt with metadata

            counter = counter + 1

# TODO: Tags in Meta funkt nicht aber kp warum
# TODO: "a mit punkten drueber" in meta nicht richtig / irgendwas mit unicode
# TODO einzeln suchen und nach Notebook runterladen (funkt nicht in sandbox)
# TODO download mit tags (funkt nicht in sandbox)
