"Livestreamer main class"

import os
import sys
from urllib.parse import urlsplit

from livestreamer import Livestreamer, StreamError, PluginError, NoPluginError

from livedumper import common

# This is just a guess, don't know if it's optimal.
READ_BUFFER = 512 * 1024  # 512kB


class LivestreamerDumper(object):
    "Main class for dumping streams"

    def __init__(self):
        self.fd = None

    def open(self, url, quality):
        """Attempt to open stream from the *url*.

        Exits with '-1' (using sys.exit()) in case of error, including
        an error msg.
        """

        self.current_url = url

        try:
            livestreamer = Livestreamer()
            streams = livestreamer.streams(url)
        except NoPluginError:
            self.exit("Livestreamer is unable to handle the URL "
                      "'{}'".format(url))
        except PluginError as err:
            self.exit("Plugin error: {0}".format(err))

        if quality not in streams:
            self.exit("Unable to find '{}' stream on URL "
                      "'{}'".format(quality, url))

        try:
            self.fd = streams[quality].open()
        except StreamError as err:
            self.exit('Failed to open stream: {}'.format(err))

    def get_title(self):
        """Returns the end of video url to be used as a title, for
        example: http://www.example.com/path1/path2-> path2
        """

        # http://www.example.com/path1/path2 -> /path1/path2
        path = urlsplit(self.current_url).path
        # /path1/path2 -> path2
        return path.split('/')[-1]

    def stop(self):
        "Close current opened file"

        if self.fd:
            self.fd.close()

        self.fd = None

    def exit(self, msg=''):
        "Close an opened file and call sys.exit(msg)."

        self.stop()
        sys.exit(msg)

    def dump(self, filepath):
        "Attempt to dump an opened stream to path *filepath*."

        common.ask_overwrite(filepath)

        filename = os.path.basename(filepath)
        file_size = 0
        with open(filepath, 'ab') as f:
            try:
                while True:
                    buf = self.fd.read(READ_BUFFER)
                    if not buf:
                        break
                    f.write(buf)
                    file_size = file_size + READ_BUFFER / 1024.0  # 1KB
                    sys.stdout.write('\rDownloaded {} KB of file '
                                     '{}'.format(file_size, filename))
            except KeyboardInterrupt:
                self.exit('\nPartial download of file {}'.format(filepath))

        print('\nComplete download of file {}'.format(filepath))
