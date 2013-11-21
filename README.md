EventedPy
=========

Usage
-----

EventedPy is very simple to use

    import eventedpy as e
    from sys import version_info

    if version_info < (3,0):
    	from __future__ import print_function

    loop = e.EventLoop()
    loop.start()

    loop.on('.+', print) # Will print every event
    loop.on('message', echo_message) # Will print every message event

    loop.event("message", "a", "b") # prints "a b" twice

It is also possible to add some slightly more advanced possibility to event handlers
You can use *args and **kwargs to transport addition variables
The example below is a continuation of the above

	def print_object(*args, **kwargs):
		print(
			str(args),
			str(kwargs)
		)

	loop.on("object", print_object)

	loop.event("object", 1, 2, third = 3)
	# Will print [1, 2] {"third": 3} in one thread
	# The other thread will raise an Exception as the keyword "third"
	# is not an accepted keyword argument for the print function


Creator
-------

Jack Stephenson [@jackatbancast](https://twitter.com/jackatbancast)

License
-------

The MIT License (MIT)

Copyright (c) 2012-2013 Jack Stephenson (@jackatbancast)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

