import os
import sys
import tempfile

path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(path, '..'))
import carpet

#### Accessory functions ####

# This is an example of a core function, which takes a file and produces
# an output file.
def puts_hello_into_file(file_in, file_out):
    """Appends hello to a file content and writes it to another file."""
    with open(file_in) as fi:
        content = fi.read()

    content += "hello"
    with open(file_out, "w") as fo:
        fo.write(content)

def create_dummy_file(extension=""):
    tmp = tempfile.mktemp() + extension
    with open(tmp, "w") as tf:
        tf.write("hello!")
    return tmp

###############
#### Tests ####
###############

PutsHello = carpet.create_context_class(puts_hello_into_file)

### Tests again TempFileContext ###

def test_base_class_right_extension_string():
    extension = ".nii"
    with carpet.TempFileContext(file_extension=extension, remove_at_exit=False)\
         as tmp_file:
        assert tmp_file.endswith(extension)

def test_conserves_docstring():
    assert puts_hello_into_file.__doc__ in PutsHello.__doc__
