import setuptools

def long_description():
    with open('README.md') as f:
        return f.read()

class SourceInfo:

    class PYXPath:

        suffixes = '.pyx', '.c'

        def __init__(self, module, path):
            self.module = module
            self.path = path

        def buildrequires(self):
            if self.path.endswith('.pyx'):
                yield 'Cython<3'

        def make_ext(self):
            g = {}
            with open(self.path + 'bld') as f: # Assume project root.
                exec(f.read(), g)
            return g['make_ext'](self.module, self.path)

    def __init__(self, rootdir):
        import os, setuptools, subprocess
        self.packages = setuptools.find_packages(rootdir)
        extpaths = {}
        def addextpaths(dirpath, moduleprefix):
            names = sorted(os.listdir(os.path.join(rootdir, dirpath)))
            for suffix in self.PYXPath.suffixes:
                for name in names:
                    if name.endswith(suffix):
                        module = "%s%s" % (moduleprefix, name[:-len(suffix)])
                        if module not in extpaths:
                            extpaths[module] = self.PYXPath(module, os.path.join(dirpath, name))
        addextpaths('.', '')
        for package in self.packages:
            addextpaths(package.replace('.', os.sep), "%s." % package)
        extpaths = extpaths.values()
        if extpaths and os.path.isdir(os.path.join(rootdir, '.git')): # We could be an unpacked sdist.
            check_ignore = subprocess.Popen(['git', 'check-ignore'] + [p.path for p in extpaths], cwd = rootdir, stdout = subprocess.PIPE)
            ignoredpaths = set(check_ignore.communicate()[0].decode().splitlines())
            assert check_ignore.wait() in [0, 1]
            self.extpaths = [path for path in extpaths if path.path not in ignoredpaths]
        else:
            self.extpaths = extpaths

def lazy(clazz, init, *initbefore):
    from threading import Lock
    initlock = Lock()
    init = [init]
    def overridefactory(name):
        orig = getattr(clazz, name)
        def override(*args, **kwargs):
            with initlock:
                if init:
                    init[0](obj)
                    del init[:]
            return orig(*args, **kwargs)
        return override
    Lazy = type('Lazy', (clazz, object), {name: overridefactory(name) for name in initbefore})
    obj = Lazy()
    return obj

# FIXME: The idea was to defer anything Cython/numpy to pyximport time, but this doesn't achieve that.
def cythonize(extensions):
    def init(ext_modules):
        ordinary = []
        cythonizable = []
        for e in extensions:
            (cythonizable if any(s.endswith('.pyx') for s in e.sources) else ordinary).append(e)
        if cythonizable:
            from Cython.Build import cythonize
            ordinary += cythonize(cythonizable)
        ext_modules[:] = ordinary
    return lazy(list, init, '__getitem__', '__iter__', '__len__')

def ext_modules():
    extensions = [path.make_ext() for path in sourceinfo.extpaths]
    return dict(ext_modules = cythonize(extensions)) if extensions else {}

sourceinfo = SourceInfo('.')
setuptools.setup(
        name = 'pym2149',
        version = '33',
        description = 'YM2149 emulator supporting YM files, OSC to JACK, PortAudio, WAV',
        long_description = long_description(),
        long_description_content_type = 'text/markdown',
        url = 'https://github.com/combatopera/pym2149',
        author = 'Andrzej Cichocki',
        packages = sourceinfo.packages,
        py_modules = [],
        install_requires = ['aridity>=48', 'diapyr>=18', 'lagoon>=31', 'Lurlene>=13', 'minBlepy>=13', 'outjack>=15', 'pyrbo>=5', 'splut>=4', 'timelyOSC>=4'],
        package_data = {'': ['*.pxd', '*.pyx', '*.pyxbld', '*.arid', '*.aridt']},
        entry_points = {'console_scripts': ['bpmtool=pym2149.scripts.bpmtool:main', 'dosound2jack=pym2149.scripts.dosound2jack:main', 'dosound2txt=pym2149.scripts.dosound2txt:main', 'dosound2wav=pym2149.scripts.dosound2wav:main', 'dsd2wav=pym2149.scripts.dsd2wav:main', 'lc2jack=pym2149.scripts.lc2jack:main', 'lc2portaudio=pym2149.scripts.lc2portaudio:main', 'lc2txt=pym2149.scripts.lc2txt:main', 'lc2wav=pym2149.scripts.lc2wav:main', 'ym2jack=pym2149.scripts.ym2jack:main', 'ym2portaudio=pym2149.scripts.ym2portaudio:main', 'ym2txt=pym2149.scripts.ym2txt:main', 'ym2wav=pym2149.scripts.ym2wav:main', 'mkdsd=ymtests.mkdsd:main']},
        **ext_modules())
