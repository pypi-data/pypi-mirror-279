from dataclasses import dataclass

from .svc import svc


# --------------------
class PackageOpengl:
    # --------------------
    def find(self, pkgname):
        svc.log.line(f'finding package: {pkgname}')

        @dataclass
        class OpenGl:
            include_dir = '/usr/include'
            link_libs = ['glut', 'GLU', 'GL']

        return OpenGl
