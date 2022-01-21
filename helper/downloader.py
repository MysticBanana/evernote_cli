import os
from datetime import datetime
from evernote.api.client import EvernoteClient
from evernote.edam.notestore.ttypes import NotesMetadataResultSpec, NoteFilter
from helper import krypto_manager
from data import file_loader


class EvernoteAccess(EvernoteClient):
    # used to interact with the api
    def __init__(self, controller, user_data, **kwargs):
        self.controller = controller
        self.user_data = user_data
        self.access_token = self.user_data.user_token
        self.logger = self.user_data.controller.create_logger("Downloader")
        super(EvernoteAccess, self).__init__(token=self.user_data.user_token, **kwargs)


class EvernoteUser(EvernoteAccess):
    # for getting user specific data from evernote
    def __init__(self, controller, user_data, **kwargs):
        super(EvernoteUser, self).__init__(controller, user_data, sandbox=controller.sandbox, **kwargs)

        self.user_store = self.get_user_store()
        self.user_info = self.user_store.getUser()

    def get_user_info(self):
        return vars(self.user_info)


class EvernoteNote(EvernoteAccess):
    def __init__(self, controller, user_data, **kwargs):
        super(EvernoteNote, self).__init__(controller, user_data, sandbox=controller.sandbox, **kwargs)

        self.note_store = self.get_note_store()
        self.filter = NoteFilter(ascending=True)
        self.meta = NotesMetadataResultSpec(*[True for i in range(10)])

        self.path = self.user_data.file_path
        self.path = self.path + "/" if self.path[-1] != "/" else self.path
        
    def download(self, ressources=True):
        note_list = self.note_store.findNotesMetadata(self.access_token, self.filter, 0, 250, self.meta).notes

        # iterate all notebooks
        for _note in note_list:
            note = self.note_store.getNote(self.access_token, _note.guid, True, False, True, False)
            note_book = self.note_store.getNotebook(self.access_token, note.notebookGuid)

            # dict for storing metadata in meta.json
            note_meta = {
                "title": note.title,
                "created": "Created: " + datetime.fromtimestamp(note.created / 1000).strftime("%A, %B %d, %Y %H:%M:%S"),
                "updated": datetime.fromtimestamp(note.updated / 1000).strftime("%A, %B %d, %Y %H:%M:%S"),
                "tags": self.note_store.getNoteTagNames(note.guid),
                "attributes": vars(note.attributes),
                "resources": []
            }

            # path for every note in utf-8 encoding
            note_dir = "{note_book}/{note_name}/".format(note_book=note_book.name, note_name=note.title).decode("utf-8")

            if ressources and note.resources is not None:

                # downloading every resource in note
                for res_guid in note.resources:
                    res = self.note_store.getResource(res_guid.guid, True, True, True, True)
                    res_name = res.attributes.fileName

                    overwrite = False
                    if os.path.exists("{}{}res/{}".format(self.path, note_dir, res_name)):
                        overwrite = self.user_data.get_default("overwrite_files")
                        if self.user_data.overwrite:
                            overwrite = True

                        if not overwrite:
                            if self.user_data.force_mode:
                                self.logger.info("File {} already exist, skipping --force".format(res_name))
                                continue
                            else:
                                overwrite = self.controller.display_manager.get_user_input("The file {} already exists. Do you want to overwrite?".format(res_name))

                    f = file_loader.FileHandler(res_name, "{}{}res/".format(self.path, note_dir), create=True, mode=None, binary=True, overwrite=overwrite)
                    f.set_all(res.data.body)
                    f.dump()

                    if f.file_hash != res.data.bodyHash:
                        self.logger.warn("hash of file: {} is not correct".format(res_name))

                    note_meta["resources"].append(vars(res.attributes))

            # main content file of note
            f = file_loader.FileHandler("content", self.path + note_dir, create=True, mode="xml")
            f.set_all(note.content).dump()

            # stores metadata of note
            f = file_loader.FileHandler("meta", self.path + note_dir, create=True, mode="json")
            f.set_all(note_meta).dump()

            self.logger.info("downloaded note: {}".format(note_book.name))

# TODO einzeln suchen und nach Notebook runterladen (funkt nicht in sandbox)
# TODO download mit tags (funkt nicht in sandbox)
