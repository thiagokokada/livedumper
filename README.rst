Livedumper
==========

Save your favorite video/streams for later
------------------------------------------


Introduction
~~~~~~~~~~~~

This program allows you to dump (a.k.a. 'download' or 'save for later') various streams/video sites like Dailymotion, YouTube, Twitch, Crunchyroll, and `many more`_. It uses the `livestreamer`_ API so I don't need to implement every new site by hand, and since the livestreamer API is very nice this makes the code lightweight and simple.

To run this program, you just need to call it like this:

::

    $ livedumper_cli http://www.crunchyroll.com/fatekaleid-liner-prisma-illya/episode-1-illya-grow-up-657285 best

This will download a video called ``episode-1-illya-grow-up-657285.mp4`` (sorry, no custom filenames yet) with the highest quality found by livestreamer in your current folder (you can change this passing the ``-d /path/to/folder`` option). You can download multiple files (unless you want different quality settings for each video) just calling the program with multiple URLs.

You can change livestreamer related options, see ``misc/settings.ini`` file for details. To login to some service, you can just use ``livestreamer`` command like:

::

    $ livestreamer --crunchyroll-username=xxxx --crunchyroll-password=xxx http://www.crunchyroll.com/fatekaleid-liner-prisma-illya/episode-1-illya-grow-up-657285 best


How to install
~~~~~~~~~~~~~~

You need to have both ``livestreamer`` and ``rtmpdump`` installed and added somewhere on your PATH. Probably the best way is to use your distribution packages to install this program. Since ``rtmpdump`` is a dependency of ``livestreamer`` your package manager should install both. Some distribution commands to install both:

::

    $ sudo apt-get install livestreamer # Debian/Ubuntu and derivates
    $ sudo pacman -S livestreamer # Arch Linux


After that you need to install ``livedumper`` per se. The easiest way to do it is using ``pip``. This downloads and installs this project from *PyPi*, completely automagically (excluding for system dependencies). If you didn't install ``livestreamer`` on the last step it will install for you (but probably without ``rtmpdump``). Just run the following command:

::

    $ sudo pip install livedumper

If you do want to install manually, you will first need to install the Python requirements. They're listed on ``requirements.txt`` file, that is compatible with Python's ``pip`` package manager. Just run the following commands:

::

    $ sudo pip install -r requirements.txt
    $ git clone https://github.com/m45t3r/livedumper.git


**Optional but recommended**: instead of running the ``pip`` commands as root (using ``sudo``) it's better to create a isolated virtual environment so you don't mess with your system Python. To do so, do the following:

::
    
    $ sudo pip install virtualenv
    $ virtualenv livedumper
    $ cd livedumper
    $ source bin/activate # You should run this command after every new terminal you open
    $ pip install livedumper


About Python versions
~~~~~~~~~~~~~~~~~~~~~

This program should be compatible both with ``Python 2.7.x`` and ``Python 3.2+``, but is only tested in ``Python 3.4.x``. Should something not work, if it's in ``Python 2.7.x`` I may drop support depending if it's too hard to fix. If it's ``Python 3.2+`` I will treat it as a bug so you can report and I will try to fix it.


Credits
~~~~~~~

This project is based on `livestreamer`_. Thanks for all developers from livestreamer for the amazing API, it was a joy to work!

.. _`livestreamer`: http://livestreamer.readthedocs.org/
.. _`many more`: http://livestreamer.readthedocs.org/en/latest/plugin_matrix.html
.. _`livestreamer config file`: http://livestreamer.readthedocs.org/en/latest/cli.html#configuration-file
