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
    """
    This function is used to create context classes using a function
    (core_function) to provide some functionality.

    By context class I mean classes that can be used like this:
        with ContextClass(whatever) as something:
            do whatever with "something"
    where "something" is only available within the scope of the with block.

    core_function must accept at least two arguments:
        - input file -> input file to process
        - output fila -> output file of the processing

    A typical example of core_function will be a function that transforms
    between two data formats. For example, say we have a function jpg2png.
    Normally we would use it this way: jpg2png("photo.jpg", "photo.png"). Now
    suppose that we only need "photo.png" for a temporal step in a pipeline. In
    this case we would have to care about choosing a location for "photo.png",
    and about deleting it at the end.
    Context classes allow to handle the temporal storage and removal, and would
    be used like this:

    with Jpg2Png("photo.jpg") as tmp_png_file:
        do_whatever(tmp_png_file)...

    Here tmp_png_file would be a pathname refering to a .png file created from
    our "photo.jpg". We can use this pathname to open it, copy it, process it,
    etc. without taking care of where it is. Also, once we exit the 'with'
    block it will be deleted and we won't have to care about it anymore.
    """

    # This is our mold of Context Class :)
    class GenericContextClass(TempFileContext):

        def __init__(self, *args, **kwargs):
            self.removable_files = []

            self.tempfile = tempfile.mktemp()
            core_function(args[0], self.tempfile, *args[1:], **kwargs)
            self.remove_at_exit = True

    return GenericContextClass
