import tempfile
import os

class TempFileContext:
    remove_at_exit = True
    removable_files = []
    """
    Base class to create 'with' contexts.

    The __init__ method must define:

        - self.removable_files <list>. This list will hold a list of filenames which will
        removed at the end of the context, or when calling self.delete().
        - self.tempfile <string>. Temporary file of interest, returned by "with" statement.
    """

    def __init__(self, file_extension=""):
        self.tempfile = tempfile.mktemp() + file_extension

    def __enter__(self):
        return self.tempfile

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.remove_at_exit:
            self.delete()
        else:
            self.remove_intermediate_files()

    def delete(self):
        self.remove_tempfile()
        self.remove_intermediate_files()

    def remove_tempfile(self):
        os.remove(self.tempfile)

    def remove_intermediate_files(self):
        map(os.remove, self.removable_files)

def create_context_class(core_function):

    # This is our mold of Context Class :)
    class GenericContextClass(TempFileContext):

        def __init__(self, *args, **kwargs):
            self.removable_files = []

            self.tempfile = tempfile.mktemp() + '.nii'
            core_function(args[0], self.tempfile, *args[1:], **kwargs)
            self.remove_at_exit = True

    return GenericContextClass
