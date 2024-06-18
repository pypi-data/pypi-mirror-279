import os
import re
from distutils import log
from setuptools.command.bdist_egg import bdist_egg, walk_egg, _get_purelib


class bdist_fixegg(bdist_egg):
    def remove_py(self, path):
        if path not in self.install_data_outputs:
            os.unlink(path)

    def do_install_data(self):
        # Hack for packages that install data to install's --install-lib
        self.get_finalized_command('install').install_lib = self.bdist_dir

        site_packages = os.path.normcase(os.path.realpath(_get_purelib()))
        old, self.distribution.data_files = self.distribution.data_files, []

        for item in old:
            if isinstance(item, tuple) and len(item) == 2:
                if os.path.isabs(item[0]):
                    realpath = os.path.realpath(item[0])
                    normalized = os.path.normcase(realpath)
                    if normalized == site_packages or normalized.startswith(
                            site_packages + os.sep
                    ):
                        item = realpath[len(site_packages) + 1:], item[1]
                        # XXX else: raise ???
            self.distribution.data_files.append(item)

        try:
            log.info("installing package data to %s", self.bdist_dir)
            cmd = self.call_command('install_data', force=0, root=None)
            self.install_data_outputs = set(cmd.get_outputs())
        finally:
            self.distribution.data_files = old

    def zap_pyfiles(self):
        log.info("Removing .py files from temporary directory")
        for base, dirs, files in walk_egg(self.bdist_dir):
            for name in files:
                path = os.path.join(base, name)

                if name.endswith('.py'):
                    log.debug("Deleting %s", path)
                    self.remove_py(path)

                if base.endswith('__pycache__'):
                    path_old = path

                    pattern = r'(?P<name>.+)\.(?P<magic>[^.]+)\.pyc'
                    m = re.match(pattern, name)
                    path_new = os.path.join(base, os.pardir, m.group('name') + '.pyc')
                    log.info("Renaming file from [%s] to [%s]" % (path_old, path_new))
                    try:
                        os.remove(path_new)
                    except OSError:
                        pass
                    os.rename(path_old, path_new)
