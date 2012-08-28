from batou.component import Component
from batou.lib.download import Download
from batou.lib.archive import Extract


class Configure(Component):

    namevar = 'path'

    def verify(self):
        with self.chdir(self.path):
            # This is guesswork. Unfortunately CMMI doesn't work any better.
            self.assert_file_is_current('config.status')
            self.assert_file_is_current(
                '.batou.config.success', ['configure'])

    def update(self):
        with self.chdir(self.path):
            self.cmd(self.expand('./configure --prefix={{component.workdir}}'))
            self.touch('.batou.config.success')


class Make(Component):

    namevar = 'path'

    def verify(self):
        with self.chdir(self.path):
            self.assert_file_is_current('.batou.make.success', ['Makefile'])

    def update(self):
        with self.chdir(self.path):
            self.cmd('make install')
            self.touch('.batou.make.success')


class Build(Component):
    """Complex build definition for

    - downloading
    - extracting
    - configure
    - make install

    """

    namevar = 'uri'
    md5sum = None
    source = None

    def configure(self):
        download = Download(
            self.uri, md5sum=self.md5sum)
        self += download

        extract = Extract(download.target, strip=1)
        self += extract

        self += Configure(extract.target)
        self += Make(extract.target)