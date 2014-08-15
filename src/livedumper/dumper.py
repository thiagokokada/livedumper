"Livestreamer main class"

from __future__ import print_function, division

import os
import sys
# Python 2/3 compatibility
try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit
try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser

from livestreamer import Livestreamer, StreamError, PluginError, NoPluginError

from livedumper import common

# This is just a guess, don't know if it's optimal.
KB = 1024
READ_BUFFER = 512 * KB  # 512kB

# http://livestreamer.readthedocs.org/en/latest/api.html
AVAILABLE_OPTIONS = {'hds-live-edge': 'float',
                     'hds-segment-attempts': 'int',
                     'hds-segment-timeout': 'float',
                     'hds-timeout': 'float',
                     'hls-live-edge': 'int',
                     'hls-segment-attempts': 'int',
                     'hls-segment-timeout': 'float',
                     'hls-timeout': 'float',
                     'http-proxy': 'str',
                     'https-proxy': 'str',
                     'http-cookies': 'str',
                     'http-headers': 'str',
                     'http-query-params': 'str',
                     'http-trust-env': 'bool',
                     'http-ssl-verify': 'bool',
                     'http-ssl-cert': 'str',
                     'http-timeout': 'float',
                     'http-stream-timeout': 'float',
                     'subprocess-errorlog': 'bool',
                     'ringbuffer-size': 'int',
                     'rtmp-proxy': 'str',
                     'rtmp-rtmpdump': 'str',
                     'rtmp-timeout': 'float'}

VIDEO_EXTENSIONS = {'AkamaiHDStream': '.flv',  # http://bit.ly/1Bfa6Qc
                    'HDSStream': '.f4f',  # http://bit.ly/1p7Ednb
                    'HLSStream': '.ts',  # http://bit.ly/1t0oVBn
                    'HTTPStream': '.mp4',  # Can be WebM too?
                    'RTMPStream': '.flv'}  # http://bit.ly/1nQwWUd


class LivestreamerDumper(object):
    "Main class for dumping streams"

    def __init__(self, config_path):
        self.fd = None
        self.config_path = config_path

    def open(self, url, quality):
        """Attempt to open stream from the *url*.

        Exits with '-1' (using sys.exit()) in case of error, including
        an error msg.
        """

        self.original_url = url
        try:
            self.livestreamer = Livestreamer()
            self._load_config()
            streams = self.livestreamer.streams(url)
        except NoPluginError:
            self.exit("Livestreamer is unable to handle the URL '{}'".
                      format(url))
        except PluginError as err:
            self.exit("Plugin error: {}".format(err))

        if quality not in streams:
            print("Unable to find '{}' stream on URL '{}'"
                  .format(quality, url), file=sys.stderr)
            self.exit("List of available streams: {}".
                      format(sorted(streams.keys())))

        self.stream = streams[quality]
        try:
            self.fd = self.stream.open()
        except StreamError as err:
            self.exit("Failed to open stream: {}".format(err))

    def _load_config(self):
        "Load and parse config file, pass options to livestreamer"
        
        config = SafeConfigParser()
        config_file = os.path.join(self.config_path, 'settings.ini')
        config.read(config_file)

        for option, type in list(AVAILABLE_OPTIONS.items()):
            if config.has_option('DEFAULT', option):
                if type == 'int':
                    value = config.getint('DEFAULT', option)
                if type == 'float':
                    value = config.getfloat('DEFAULT', option)
                if type == 'bool':
                    value = config.getboolean('DEFAULT', option)
                if type == 'str':
                    value = config.get('DEFAULT', option)

                self.livestreamer.set_option(option, value)


    def get_title(self):
        """Returns the end of video url to be used as a title, for
        example: http://www.example.com/path1/path2?q=V1 -> path2_q=V1
        """

        stream_type = self.stream.__class__.__name__
        try:
            extension = VIDEO_EXTENSIONS[stream_type]
        except KeyError:
            print('No extension found...', file=sys.stderr)
            extension = ''

        # http://www.example.com/path1/path2?q=V1 ->
        # 'http', 'www.example.com', '/path1/path2', 'q=V1'
        split_url = urlsplit(self.original_url)
        # /path1/path2 -> path2
        filename = split_url.path.split('/')[-1]
        # path2 -> path2_q=V1
        if split_url.query:
            filename = filename + '_' + split_url.query
        return filename + extension

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
                    file_size = file_size + (READ_BUFFER / KB)
                    print("Downloaded {} KB of file '{}'".
                          format(file_size, filename), end='\r')
            except KeyboardInterrupt:
                self.exit("\nPartial download of file '{}'".format(filepath))

        print("\nComplete download of file '{}'".format(filepath))
