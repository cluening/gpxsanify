# GPX Sanification

I've been collecting trace files from my GPS units since 2007, which I've used for various projects since then.  Sometimes these files end up with data that doesn't make sense - for example, the first track point may get written before a good satellite fix is obtained, leading to a giant jump between the first point and the last point.

Current features:
 - Clean up extraneous lines by looking for absurd speeds
 - Works on single files or directories of files
