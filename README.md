# carpet
Clarify your pipelines, hiding your temporal files under the carpet!

### Install

```python
pip install carpet
```

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
    produce file_out

Transform = create_context_class(transform)
```

And here is our transform function :):

```python
with Transform(file_in, arg1, arg2, ...) as transformed_file:
    do_whatever(transformed_file)
```

### What kind of functions can I transform into a Context Class?

These are the restrictions for the function:

    - It must take at least two arguments (it can take more).
    - The second argument must be the output file.
