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
    with open(file_in) as fi:
        content = fi.read()

    content += "hello"
    with open(file_out, "w") as fo:
        fo.write(content)

def create_dummy_file():
    tmp = tempfile.mktemp()
    with open(tmp, "w") as tf:
        tf.write("hello!")
    return tmp

#### Tests ####

PutsHello = carpet.create_context_class(puts_hello_into_file)

def test_creates_tmp_file():
    dummy_file = create_dummy_file()
    with PutsHello(dummy_file) as tmp_file:
        assert os.path.isfile(tmp_file)

def test_removes_tmp_file():
    dummy_file = create_dummy_file()
    with PutsHello(dummy_file) as tmp_file:
        pass
    assert not os.path.exists(tmp_file)

def test_functionality_is_conserved():
    fname_in = create_dummy_file()

    fname_out_fn = tempfile.mktemp()
    puts_hello_into_file(fname_in, fname_out_fn)

    with PutsHello(fname_in) as tmp_file_hello:
        with open(fname_out_fn) as fh, open(tmp_file_hello) as ftmp:
            assert fh.read() == ftmp.read()
