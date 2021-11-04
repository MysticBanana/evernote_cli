import os


def downloadFile(noteStore, access_token, filter, meta, main_class):
    # Used to find the high-level information about a set of the notes from a user's account based on various criteria
    # (string authenticationToken, NoteFilter filter, i32 offset, i32 maxNotes, NotesMetadataResultSpec resultSpec)
    ourNoteList = noteStore.findNotesMetadata(access_token, filter, 0, 250, meta)
    guidlist = []
    titlelist = []

    logger =main_class.create_logger("FileDownloader")
    logger.info("test")

    for note in ourNoteList.notes:
        wholeNote = noteStore.getNote(access_token, note.guid, True, False, True, False)
        print note.guid
        guidlist.append(note.guid)  # Liste with all guids of Notes
        titlelist.append(note.title)
    print guidlist

    counter = 0
    for numbers in guidlist:
        note = noteStore.getNote(access_token, guidlist[counter], True, False, True, False)  # Data about Note
        resguid = ' '.join(map(str, note.resources))  # note.resources contains guid for Files; to string
        resguidcount = resguid.count("guid='")  # count Files in Notes
        print "\n\n", resguidcount
        print resguid
        offset = -1

        if not os.path.exists("Notes"):  # Folder for Notes
            os.makedirs("Notes")

        newpath = titlelist[counter]  # Folder for every Note
        if not os.path.exists('Notes/' + newpath):
            os.makedirs('Notes/' + newpath)

        while True:
            offset = resguid.find("guid='", offset + 1)  # find guid of File in resources
            if offset == -1:
                break
            offsetend = resguid.find("'", offset + 6)  # find end of guid
            tmpguid = resguid[offset + 6:offsetend]  # "safe" guid
            print tmpguid

            resource = noteStore.getResource(tmpguid, True, False, True, False)
            file_content = resource.data.body  # raw data of File

            file_name = resource.attributes.fileName  # file_name includes File extension
            f = open('Notes/' + newpath + '/' + file_name, "w+")  # create file with correspond. File extension
            f.write(file_content)  # TODO check ob beriets vorhanden -> schneller
            f.close()

        print '\n', note.content
        counter = counter + 1

# TODO prints in log schreiben ich weiss aber nicht wie
# TODO einzeln suchen und nach Notebook runterladen (funkt nicht in sandbox)
# TODO Textdownload
# TODO download mit tags (funkt nicht in sandbox)
