TextQueue
================================================================================
TextQueue is a text-based message queue, meant to be a sqlite or json~esque
human readable daemonless file that represents a message queue. It has some
additional features that allow it to be slightly parallelizable as well.

The goals of TextQueue are
* To be human readable, like json
* To be human editable at rest, like json
* To function as a file based daemonless service, like sqlite
* To be a text based message queue.
* To be forwards and backwards compatable with all future and previous versions of TextQueue

TextQueue looks like this
```
# A comment begins with a '#' sign
=An already processed message begins with an '=' character
=An already processed message can have multiple lines
 if each sequential line begins with a ' ' space
=Processed message 3
=Processed message 4
-A queued message begins with a '-' character

-Blank lines are allowed
-Queued message 7 fist line
 Queued message 7 second line
 Queued message 7 third line
 Queued message 7 fouth line
# Multiline comments are possible
  Using space as the starting character for the
  following lines
=Processed messages can apear after queued messages.
=Sometimes later jobs will finish before earlier ones
-Some message 10
# Messages are space sensitive, so this message will read "  Some message 11  "
-  Some message 11  
-Some message 12
# Comment's leading spaces are optional here, they are not parsed the same way
# Multiple Comments can also be next to each other
# which can also be used for multi line comments. But they will
# each be read as a single line if the user is trying to read comments.

```

* `#` A coment, these lines will be compleetly ignored
* `=` the denotion of a new messae in the queue that has already been processed
* `-` the denotion of a new message in the queue
* ` ` the denotion of a continuation of the previous message onto the next line


Textqueue plays nicely with other text-based serialized systems. Is lightweight
on the disk, only updating single characters or appending lines, and is easily
human manipulatable.
Due to the nature of textqueue's syntax, we do not need to escape any control
characters inside the message becuase each control character will start in the
first column of the message. Any control characters that exist inside the
message will be treated as their reguar utf8 characters
Any newlines inside the message are treated as the end of the message. But if
the control sequence of the next line is a ` ` space, then that newline and the
next line are added to previous message.
If any new control characters need to be added in the future they will always
start in column 0, even if they need to extend to further columns down the
line later.


Queueform does not have any specification for a lockfile making it not fully
thread safe yet, though there are some threadsafe guarentees that arise from
the current methodology.
* Any message that is being marked as processed will never be marked as queued
* Multiple message can be marked as processed simultaniously.

However it does not protect against:
* once and only once - Two processes reading the same control caracter, picking
  up the same message, and both marking the message as handled
* Manual human editable tools accessing the file, causing full file rewrites
  that can alter the entire saved state.

Each line must match something like the regex

```
[-=# ][^\n]*(?:\n|EOF)|\n
```

Except nothing after EOF


Parallelism
================================================================================
Some concurrent access is possible. Specifically a concurrent read and write.
The current schema loses some functionality with multiple concurrent reads.
Multiple concurrent writers would require a mutex lock using a separate mutex
file. If the user is so concurrent they need message-level concurrent writes,
then they are probably better off using a daemon based message passing solution
instead. A per-message mutex file could also be possible to allow for full
once-and-only-once MQTTT QOL2 style messages by using the message offsets in
the mutex. Adding a mutex file would not change or alter the current schema.

| Readers | Writers | Stability                                                             |
|---------|---------|-----------------------------------------------------------------------|
| 0       | 0       | Stable - At Rest                                                      |
| 1       | 0       | Stable - Only Reading                                                 |
| 0       | 1       | Stable - Only Writing                                                 |
| 1       | 1       | Stable - Writes are only appends and reads are only byte flips        |
| 2+      | 0+      | All jobs are run at least once but may be run multiple times          |
| 0+      | 2+      | OS may mangle messages being written to a single file corrupting data |


Multiple Writer Mitigation - MultiFile
--------------------------------------------------------------------------------
If you want multiple writers to be able to write jobs in parallel then the
writers must be using different files to write to, or the write operations must
somehow be serialized to prevent overwriting each other.


Multiple Writer Mitigation - Mutex
--------------------------------------------------------------------------------
You can create a mutex for the entire file to prevent more than one program
from writing to it at once. This will require changes to the library to create,
release, and respect the mutex.


Multiple Reader Mitigation - Mutex
--------------------------------------------------------------------------------
Mutex file using the message offset to block individual messages from being
read twice. This will require changes to the reader so that it can re-check
released mutexes to see if the mutex was released because the process crashed,
errored, or timed out or because it finished processing.

A mutex file just using the queue filename to prevent multiple people from
reading at once is less good becuase you will need to keep the file locked
until the processing is done.


Other Features and Discussion
================================================================================

Message Errors
--------------------------------------------------------------------------------
Our vision is that any errors in processing a message get handled by the
program that is reading the queue. However, there is a good use case argument
for some sort of control character that represents “This message cannot ever be
processed”. In that case, we might not want to mark the message as processed,
because it was not, and we might not want to leave it queued, because it cannot
be processed so would constantly and repeatedly error. When this feature
becomes necessary, we will add a new control character, maybe `X`, to represent
this state.

The control characters `X` is not finalized and merits discussion.


Inserted Timestamps
--------------------------------------------------------------------------------
Inserted timestamps seem quite useful in some use cases. Some use cases do not
have, want, or need timestamps, meaning that timestamps should not be required.
The entire body of the message is an arbitrary utf8 string. With the only
restriction being the `\n` newline character, those require a following ` `
space to be included in the message. Any user who wanted timestamps could
easily create their own sub-schema for their own messages that included
timestamps. If or when we ever find a compelling reason to add timestamps as
first-class data, we can add a new control character for it.


Prefix Syntax
--------------------------------------------------------------------------------
Similarly to timestamps, we might want other forms of fixed metadata. We could
easily add this in the future by creating new control sequences that apply
their content to the following message, for example, an ISO 8601 prefix or a
unix epoch timestamp prefix.

```
T2024-06-13T19:26:15+00:00-Some message with an iso 8601 timestamp as metadata
T2024-06-13T19:26:15+00:00
-Also some message with an iso 8601 timestamp as metadata
U1718306775=Some completed message with a unix epoch timestamp
U1718306775
=Also some completed message with a unix epoch timestamp
```

Prefixes might stress backwards compatability though, parsing a newer queue
on an older parser would still work. However the prefix metadata would not
be associated with the message inside the parser and instead would be ignored.

To avoid this you can trigger an error when reading messages that have control
characters you do not recognize, specificlly breaking backwards compatability.
We may be able to do something to prevent this from causing an error, instead
making the entire line one line and having the entire message ignored, not
allowing prefixes to exist on their own line the way that ` ` space suffexes do.
Or by making a new control character to control all prefixes, such as `>`.
Getting that into the spec in the earliest version.

```
T2024-06-13T19:26:15+00:00-Some message with an iso 8601 timestamp as metadata
>T2024-06-13T19:26:15+00:00
-Also some message with an iso 8601 timestamp as metadata
```
Or requiring that prefixes on their own line have to be followed by a special
control sequence such as `>` before the next line.
```
T2024-06-13T19:26:15+00:00
>-Also some message with an iso 8601 timestamp as metadata
```

The same-line-only option seems pretty good honestly compared to the others


The control characters `T`, `U`, and `>` are not finalized and merits discussion.


Fixed Metadata
--------------------------------------------------------------------------------
Timestamps *could* be considered a special usecase. But we could also expand on
this functionality to allow for arbitrary metadata tags on messages.

```
*tagname:tagvalue
*source:john
*timestamp:1995 July 5th at 5:30pm
*language:en-us
-My Message
 and another line of my message
```

We can add arbitrary metadata tags like this as well if we find a compelling
reason to add them.

The control character `*` or syntax is not finalized and merits discussion.


Retries
--------------------------------------------------------------------------------
There is a valid usecase where the user wants to show that a job is worth
retrying, but only worth retrying so many times. Therefore marking it as
processed, error, or leaving it queued would be incorrect. In order to avoid
reserving a bunch of control characters for each quantity of retry, we can
instead reserve one, such as `!`, followed by any number of arabic numerals and
use the prefix syntax style above. Arabic numerals will always decrease in
length as the value they represent approaches zero. We can confidently decrease
this number in-place until it reaches 0 without worrying about shifting the
offset of any other characters. Every time the item is pulled from the queue,
we can automatically decrease the number of retries.

```
!12-Some Queued message with 12 retries remaining
!08-Some queued message with 8 retries remaining, that used to have 10 or more
! 8-An alternative message syntax with 8 retries remaining that used to have 10 or more
!5=A processed message that still had 5 retries remaining when it was fully processed
```

The control character `!` or syntax is not finalized and merits discussion.


Editable Metadata
--------------------------------------------------------------------------------
We could add some sort user editable in-queue data. Much like the fixed
metadata before we could add some sort of editable tag system. This would come
with some additional restrictions, though. Primarily, a tag could never
increase in size beyond its original maximum size. Examples of things we could
put in editable metadata would be statuses, processed timestamps, error codes,
or retry counts. This would require some more planning before implementation,
but just like all the previous features, we could easily add it using a new
control character.


FAQ
================================================================================
**Q: Why do your queues not have schema version numbers?**  
**A:** We intentionally excluded versions, instead making sure the schema is
forwards and backwards compatible forever. We rely on the starting character of
each line to determine functionality as a “control character”. The schema today
only consumes a few of the characters. We leave all the other utf8 characters
open to extend the syntax with other future features. However, adding new
control characters to the schema should be done with intention. If not, we
could enter a situation where we have added too many features with short
control sequences, and newer features would require multi-character
control sequences.

**Q: How do I put an error message for an unprocessable message in the queue?**  
**A:** The processor program should handle error messages for any message that
fails, probably in one of their logs. Error messages do not belong in the queue
itself. If we ever changed our minds about this, then the error messages would
still need to be stored in an external log file anyway, or risk shifting the
index of later messages. A possible in-queue solution could be fixed-length
error codes using something similar to editable metadata.

**Q: Will you support other languages?**
**A:** Eventually this should become a library with c bindings that any language
can call into, just like how sqlite does it. But that is pretty far down
the line.


