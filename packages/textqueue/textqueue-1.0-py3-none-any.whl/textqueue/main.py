from dataclasses import dataclass
from io import TextIOWrapper
from typing import List, Tuple, Optional
import enum


class MessageStatus(enum.Enum):
    cleared = enum.auto
    queued = enum.auto
    comment = enum.auto


@dataclass
class QueueItem:
    source_filename: str
    source_file: TextIOWrapper
    control_offset: int
    value: str
    status: MessageStatus

    ############################################################################
    # mark_as_cleared
    #
    # Mark a specific queue item as cleared in memory and save it to disk.
    ############################################################################
    def mark_as_cleared(self) -> None:
        position = self.source_file.tell()
        self.source_file.seek(self.control_offset)
        self.source_file.write("=")
        self.source_file.seek(position)
        self.status = MessageStatus.cleared


class TextQueue:
    input_files: List[Tuple[str, TextIOWrapper]]

    def __init__(self) -> None:
        self.input_files = []

    ############################################################################
    # get_next
    #
    # Gets the next item in the queue
    ############################################################################
    def get_next(self) -> Optional[QueueItem]:
        for i in range(len(self.input_files)):
            val = self.get_next_in_file(i)
            if val is None:
                continue
            return val
        return None

    ############################################################################
    # get_next_in_file
    #
    # A helper function to get the next item in the queue for a given file.
    ############################################################################
    def get_next_in_file(
        self,
        file_index: int,
        include_cleared_items: bool = False,
        include_comment_items: bool = False,
    ) -> Optional[QueueItem]:
        while True:
            file = self.input_files[file_index][1]
            filename = self.input_files[file_index][0]
            control_character_index = file.tell()
            line: str = file.readline()

            # End of file
            if line == "":
                return None

            # Blank Line, ignored
            if line == "\n":
                continue

            control_character = line[0]

            message: List[str]
            message_status: MessageStatus

            # Parse out cleared, queued, and comments and handle them accordingly
            if control_character == "=":
                if not include_cleared_items:
                    continue
                message_status = MessageStatus.cleared
                message = [line[1:]]
            elif control_character == "-":
                message_status = MessageStatus.queued
                message = [line[1:]]
            elif control_character == "#":
                if not include_comment_items:
                    continue
                message_status = MessageStatus.comment
                message = [line[1:]]

            else:
                raise ValueError("Unexpected Control Character")

            # Add all of the extra continued lines if any exist
            while self._peek_at_next_character(file) == " ":
                line = file.readline()
                message.append(line[1:])

            return QueueItem(
                source_filename=filename,
                source_file=file,
                control_offset=control_character_index,
                value="".join(message),
                status=message_status,
            )

    ############################################################################
    # _peek_at_next_character
    #
    # A helper function to peek at the next character in a file if one exists.
    ############################################################################
    def _peek_at_next_character(self, file: TextIOWrapper) -> str:
        start = file.tell()
        val = file.read(1)
        file.seek(start)
        return val

    ############################################################################
    # add_input
    #
    # Adds a file as a possible input
    ############################################################################
    def add_input(self, filename: str) -> None:
        self.input_files.append((filename, open(filename, 'r')))


################################################################################
#
################################################################################
def main() -> None:
    text_queue = TextQueue()
    text_queue.add_input("test.tq")

    print(text_queue.get_next())
    print(text_queue.get_next())
    print(text_queue.get_next())
    print(text_queue.get_next())
    print(text_queue.get_next())
    print(text_queue.get_next())
    print(text_queue.get_next())
    print(text_queue.get_next())
    print(text_queue.get_next())
    print(text_queue.get_next())
    print(text_queue.get_next())


if __name__ == "__main__":
    main()
