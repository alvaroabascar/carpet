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

def create_context_class(core_function, output_extension):
    """
    Creates a context class, which implements the functionality provided
    by the function core_function.
    Inputs:
        - core_function: a function with the following restrictions.
            + it must take AT LEAST 2 arguments
            + the first argument is an input file to be processed
            + the second argument is the output file
        - output_extension: sometimes the output file of a process must have
                            a given extension. You can specify it here.
                            output_extension can be:
                    a) A string specifying the extension (with dot, eg. ".jpg")
                    b) A function that given the input file name, produces the
                       extension. Example: lambda file: file.split('.')[-1]
    """

    def get_extension(f_in):
        if hasattr(output_extension, '__call__'):
            return output_extension(f_in)
        return output_extension

    # This is our mold of Context Class :)
    class GenericContextClass(TempFileContext):

        def __init__(self, *args, **kwargs):
            self.removable_files = []

            self.tempfile = tempfile.mktemp() + get_extension(args[0])
            core_function(args[0], self.tempfile, *args[1:], **kwargs)
            self.remove_at_exit = True

    return GenericContextClass
