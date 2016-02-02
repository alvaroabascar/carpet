# carpet
Clarify your pipelines, hiding your temporal files behind the carpet!


### What?

So you have this case:

```python
transform("file.this", "file.that")
process("file.that", "file.final")
remove("file.that")
```

file.that is clearly a temporal file, which we don't care much about
but have to store and remove it at the end of the process.

Wouldn't it be nice to have something like this?:

```python
with Transform("file.this") as file_that:
    process(file_that, "file.final)
```

In this case the class Transform does exactly the same thing as the
`transform` function that we saw before, but it automatically handles
the temporal file, hiding it in a temporal location, and taking care
about removing it when you exit the 'with' block.

### I want it! how can I use it?

You can create your own "Context Classes" (like Transform above) using
the function `create_context_class`. For example:

```python
def transform(file_in, file_out, arg1, arg2, ...):
    ...
    ...
    ...
    (finally produces file_out)

Transform = create_context_class(transform)
```

And here is our transform function :)

### What kind of functions can I transform into a Context Class?

These are the restrictions for the function:

    - it must take at least two arguments (it can take more)
    - the second argument must be the output file


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
