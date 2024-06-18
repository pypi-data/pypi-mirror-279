import json
import os
import pathlib
import platform
import pydoc
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request
import warnings
import zipfile

import appdirs
import julia


APPNAME = 'InterpretableAI'
NEEDS_RESTART = False
IAI_JULIA_SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def iswindows():
    return (appdirs.system.startswith('win32') or
            appdirs.system.startswith('cygwin'))


def isapple():
    return appdirs.system.startswith('darwin')


def islinux():
    return appdirs.system.startswith('linux')


def julia_exename():
    return 'julia.exe' if iswindows() else 'julia'


def julia_default_depot():
    if iswindows():
        key = 'USERPROFILE'
    else:
        key = 'HOME'

    return os.path.join(os.environ[key], '.julia')


def get_prefs_dir():
    depot = os.environ.get('JULIA_DEPOT_PATH', julia_default_depot())
    prefs = os.path.join(depot, 'prefs')
    pathlib.Path(prefs).mkdir(parents=True, exist_ok=True)
    return prefs


# Configure julia with options specified in environment variables
def iai_run_julia_setup(run_setup_jl=True, **kwargs):
    if NEEDS_RESTART:
        raise Exception(
            'Need to restart Python after installing the IAI system image')

    # Check if system image replacement was queued on Windows
    replace_sysimg_file = sysimage_replace_prefs_file()
    if os.path.isfile(replace_sysimg_file):
        with open(replace_sysimg_file) as f:
            lines = f.read().splitlines()
        sysimage_do_replace(*lines)
        os.remove(replace_sysimg_file)

    if 'IAI_DISABLE_COMPILED_MODULES' in os.environ:  # pragma: no cover
        kwargs['compiled_modules'] = False

    if 'IAI_JULIA' in os.environ:  # pragma: no cover
        kwargs['runtime'] = os.environ['IAI_JULIA']
    else:
        julia_path = julia_load_install_path()
        if julia_path:
            kwargs['runtime'] = os.path.join(julia_path, 'bin',
                                             julia_exename())

    if 'IAI_SYSTEM_IMAGE' in os.environ:  # pragma: no cover
        kwargs['sysimage'] = os.environ['IAI_SYSTEM_IMAGE']
    else:
        sysimage_path = sysimage_load_install_path()
        if sysimage_path:
            kwargs['sysimage'] = sysimage_path

    # Add Julia bindir to path on Windows so that DLLs can be found
    if 'runtime' in kwargs and os.name == 'nt':
        bindir = os.path.dirname(kwargs['runtime'])
        os.environ['PATH'] += os.pathsep + bindir

    # Load Julia with IAI_DISABLE_INIT to avoid interfering with stdout
    os.environ['IAI_DISABLE_INIT'] = 'True'

    # Start julia once in case artifacts need to be downloaded
    # Skip if julia is already inited, as we may not know `runtime`
    # We run the `setup.jl` process so that all required packages are installed outside
    # of the Python process to avoid conflicts with SSL/CURL libraries
    if not julia.libjulia.get_libjulia():
        args = [kwargs.get('runtime', julia_exename())]
        if 'sysimage' in kwargs:
            args.extend(['-J', kwargs['sysimage']])
        if run_setup_jl:
            args.append(os.path.join(IAI_JULIA_SCRIPT_DIR, "setup.jl"))
        else:
            args.extend(['-e', 'nothing'])
        subprocess.run(args, stdout=subprocess.DEVNULL)


    try:
        julia.Julia(**kwargs)
    except julia.core.UnsupportedPythonError:  # pragma: no cover
        # Static python binary, so we turn off pre-compiled modules.
        kwargs = {**kwargs, "compiled_modules": False}
        julia.Julia(**kwargs)
        warnings.warn(
            "Your system's Python library is static (e.g., conda), so precompilation will be turned off. For a dynamic library, try using `pyenv` and installing with `--enable-shared`: https://github.com/pyenv/pyenv/blob/master/plugins/python-build/README.md#building-with---enable-shared."
        )

    from julia import Main as _Main

    del os.environ['IAI_DISABLE_INIT']

    return _Main


def install(runtime=None, hide_non_default_warning=False, **kwargs):
    """Install Julia packages required for `interpretableai.iai`.

    This function must be called once after the package is installed to
    configure the connection between Python and Julia.

    Parameters
    ----------
    Refer to the
    `installation instructions <https://docs.interpretable.ai/v3.2.1/IAI-Python/installation/#Python-Installation-1>`
    for information on any additional parameters that may be required.

    Examples
    --------
    >>> install(**kwargs)
    """
    if runtime is None:
        runtime = os.getenv("IAI_JULIA", "julia")
        # Hide non-default warning if we loaded julia from IAI_JULIA
        if runtime != "julia":  # pragma: no cover
            hide_non_default_warning = True

    # Disable warning about needing to set runtime
    _default = julia.tools._non_default_julia_warning_message
    if hide_non_default_warning:
        def no_warning(julia):
            return ""
        julia.tools._non_default_julia_warning_message = no_warning

    os.environ['IAI_DISABLE_INIT'] = 'True'
    julia.install(julia=runtime, **kwargs)
    del os.environ['IAI_DISABLE_INIT']

    # Restore normal warning
    julia.tools._non_default_julia_warning_message = _default

# JULIA


def julia_default_install_dir():
    return os.path.join(appdirs.user_data_dir(APPNAME), 'julia')


def julia_latest_version():
    url = 'https://julialang-s3.julialang.org/bin/versions.json'
    versions_json = urllib.request.urlopen(url).read().decode('utf-8')
    versions = json.loads(versions_json)

    iai_versions = get_iai_version_info()

    valid_versions = [k for (k, v) in versions.items()
                      if v['stable'] and k in iai_versions]

    max_version = max(tuple(map(int, v.split("."))) for v in valid_versions)
    return ".".join(map(str, max_version))


def julia_tgz_url(version):
    arch = 'aarch64' if platform.processor() == 'arm' else 'x64'
    short_version = version.rsplit(".", 1)[0]
    if islinux():
        os = 'linux'
        slug = 'linux-x86_64'
        ext = 'tar.gz'
    elif isapple():
        os = 'mac'
        slug = 'macaarch64' if platform.processor() == 'arm' else 'mac64'
        ext = 'tar.gz'
    elif iswindows():
        os = 'winnt'
        slug = 'win64'
        ext = 'zip'
    else:  # pragma: no cover
        raise Exception(
            'Unsupported operating system: {0}'.format(appdirs.system))

    url = "https://julialang-s3.julialang.org/bin/{0}/{1}/{2}/julia-{3}-{4}.{5}".format(os, arch, short_version, version, slug, ext)

    return url


def julia_path_prefs_file():
    return os.path.join(get_prefs_dir(), 'IAI-pyjulia')


def julia_save_install_path(path):
    with open(julia_path_prefs_file(), 'w') as f:
        f.write(path)


def julia_load_install_path():
    path = julia_path_prefs_file()
    if os.path.isfile(path):
        with open(path) as f:
            julia_path = f.read()
        if isinstance(julia_path, bytes):  # pragma: no cover
            julia_path = julia_path.decode('utf-8')
        return julia_path
    else:
        return None


def install_julia(version='latest', prefix=julia_default_install_dir()):
    """Download and install Julia automatically.

    Parameters
    ----------
    version : string, optional
        The version of Julia to install (e.g. `'1.6.3'`).
        Defaults to `'latest'`, which will install the most recent stable
        release.
    prefix : string, optional
        The directory where Julia will be installed. Defaults to a location
        determined by
        `appdirs.user_data_dir <https://pypi.org/project/appdirs/>`.

    Examples
    --------
    >>> install_julia(**kwargs)
    """
    if version == 'latest':
        version = julia_latest_version()  # pragma: no cover
    url = julia_tgz_url(version)

    print('Downloading {0}'.format(url), file=sys.stderr)
    filename, _ = urllib.request.urlretrieve(url)

    dest = os.path.join(prefix, version)
    if os.path.exists(dest):  # pragma: no cover
        shutil.rmtree(dest)

    if islinux() or isapple():
        with tarfile.open(filename) as f:
            f.extractall(dest)
    elif iswindows():
        with zipfile.ZipFile(filename) as f:
            f.extractall(dest)

    dest = os.path.join(dest, 'julia-' + version)

    julia_save_install_path(dest)

    install(
        runtime=os.path.join(dest, 'bin', julia_exename()),
        hide_non_default_warning=True,
    )

    print('Installed Julia to {0}'.format(dest), file=sys.stderr)
    return True


# IAI SYSTEM IMAGE


def sysimage_default_install_dir():
    return os.path.join(appdirs.user_data_dir(APPNAME), 'sysimage')


def get_latest_iai_version(versions):
    return list(filter(lambda x: x != "dev", versions.keys()))[-1]


def iai_download_url(iai_versions, version):
    if version.startswith('v'):
        version = version[1:]

    try:
        return iai_versions[version]
    except KeyError:
        raise Exception(
            'IAI version {0} not available for this version of Julia. '.format(
                version) +
            'Available versions are: {0}'.format(', '.join(iai_versions)))


def get_iai_version_info():
    url = 'https://docs.interpretable.ai/versions.json'
    versions_json = urllib.request.urlopen(url).read().decode('utf-8')
    versions = json.loads(versions_json)

    if isapple():
        os_code = 'macos_aarch64' if platform.processor() == 'arm' else 'macos'
    elif iswindows():
        os_code = 'win64'
    elif islinux():
        os_code = 'linux'
    else:  # pragma: no cover
        raise Exception(
            'Unsupported operating system: {0}'.format(appdirs.system))
    return versions[os_code]


def get_iai_versions(julia_version):
    info = get_iai_version_info()
    return info[julia_version]


# Saving location of system image

def sysimage_path_prefs_file():
    return os.path.join(get_prefs_dir(), 'IAI')


def sysimage_save_install_path(path):
    with open(sysimage_path_prefs_file(), 'w') as f:
        f.write(path)


def sysimage_load_install_path():
    path = sysimage_path_prefs_file()
    if os.path.isfile(path):
        with open(path) as f:
            sysimage_path = f.read()
        if isinstance(sysimage_path, bytes):  # pragma: no cover
            sysimage_path = sysimage_path.decode('utf-8')
        return sysimage_path
    else:
        return None


# Saving replacement command

def sysimage_replace_prefs_file():
    return os.path.join(get_prefs_dir(), 'IAI-replacedefault')


def sysimage_save_replace_command(image_path, target_path):
    with open(sysimage_replace_prefs_file(), 'w') as f:
        print(image_path, file=f)
        print(target_path, file=f)


def sysimage_do_replace(image_path, target_path):
    print('Replacing default system image at {0} with IAI system image'.format(target_path), file=sys.stderr)
    os.chmod(target_path, 0o777)
    os.remove(target_path)
    shutil.copyfile(image_path, target_path)


# Top-level system image installation

def install_system_image(version='latest', replace_default=False,
                         prefix=sysimage_default_install_dir(),
                         accept_license=False):
    """Download and install the IAI system image automatically.

    Parameters
    ----------
    version : string, optional
        The version of the IAI system image to install (e.g. `'2.1.0'`).
        Defaults to `'latest'`, which will install the most recent release.
    replace_default : bool
        Whether to replace the default Julia system image with the downloaded
        IAI system image. Defaults to `False`.
    prefix : string, optional
        The directory where Julia will be installed. Defaults to a location
        determined by
        `appdirs.user_data_dir <https://pypi.org/project/appdirs/>`.
    accept_license : bool
        Set to `True` to confirm that you agree to the
        `End User License Agreement <https://docs.interpretable.ai/End_User_License_Agreement.pdf>`
        and skip the interactive confirmation dialog.

    Examples
    --------
    >>> install_system_image(**kwargs)
    """
    if not accept_license and not accept_license_prompt():
        raise Exception(
            "The license agreement was not accepted, aborting installation")

    # Cleanup any previous sysimg configuration before loading Julia in case a prior
    # installation is not functional
    for f in [sysimage_path_prefs_file(), sysimage_replace_prefs_file()]:
        if os.path.exists(f):
            os.remove(f)

    # Load Julia to get julia version
    Main = iai_run_julia_setup(run_setup_jl=False)
    julia_version = Main.string(Main.VERSION)
    # Get valid IAI versions for this julia version
    iai_versions = get_iai_versions(julia_version)

    if version == 'latest':
        version = get_latest_iai_version(iai_versions)

    url = iai_download_url(iai_versions, version)

    print('Downloading {0}'.format(url), file=sys.stderr)
    filename, _ = urllib.request.urlretrieve(url)

    if version != 'dev':
        version = 'v{0}'.format(version)
    dest = os.path.join(prefix, version)
    if os.path.exists(dest):  # pragma: no cover
        shutil.rmtree(dest)

    with zipfile.ZipFile(filename) as f:
        f.extractall(dest)

    if islinux():
        image_name = 'sys.so'
    elif isapple():
        image_name = 'sys.dylib'
    elif iswindows():
        image_name = 'sys.dll'
    else:  # pragma: no cover
        raise Exception(
            'Unsupported operating system: {0}'.format(appdirs.system))
    image_path = os.path.join(dest, image_name)

    sysimage_save_install_path(image_path)
    print('Installed IAI system image to {0}'.format(dest), file=sys.stderr)

    artifacts_toml_path = os.path.join(dest, "Artifacts.toml")
    if os.path.exists(artifacts_toml_path):
        # Make sure we have a valid path on windows after interpolation
        artifacts_toml_path = artifacts_toml_path.replace("\\", "/")
        print("Installing artifacts for system image...")
        julia_cmd = f"""
            using Pkg;
            Pkg.activate(temp=true);
            Pkg.add(url="https://github.com/InterpretableAI/IAISystemImages.jl");
            using IAISystemImages;
            IAISystemImages.install_artifacts("{artifacts_toml_path}")
        """
        args = [Main.eval('Base.julia_cmd()[1]'), "-e", julia_cmd]
        subprocess.run(args)
        print("Installed artifacts for system image")


    if replace_default:
        target_path = os.path.join(
            Main.eval('unsafe_string(Base.JLOptions().julia_bindir)'),
            '..', 'lib', 'julia', image_name,
        )
        # Windows can't replace the current sysimg as it is loaded into this
        # session so we save a command to run later
        if iswindows():
            sysimage_save_replace_command(image_path, target_path)
        else:
            sysimage_do_replace(image_path, target_path)

    # Need to restart R to load with the system image before IAI can be used
    global NEEDS_RESTART
    NEEDS_RESTART = True
    return True


def cleanup_installation():
    """Remove all files created by :meth:`interpretableai.install_julia` and
    :meth:`interpretableai.install_system_image`.

    Examples
    --------
    >>> cleanup_installation()
    """
    for f in (
            julia_path_prefs_file(),
            sysimage_path_prefs_file(),
            sysimage_replace_prefs_file(),
    ):
        if os.path.exists(f):
            os.remove(f)

    for path in (
            julia_default_install_dir(),
            sysimage_default_install_dir(),
    ):
        if os.path.exists(path):
            shutil.rmtree(path)


def accept_license_prompt():
    if hasattr(sys, 'ps1'):  # pragma: no cover
        print("In order to continue the installation process, please review",
              "the license agreement.")
        input("Press [ENTER] to continue...")

        url = "https://docs.interpretable.ai/End_User_License_Agreement.md"
        filename, _ = urllib.request.urlretrieve(url)

        with open(filename) as f:
            pydoc.pager(f.read())
        os.remove(filename)

        while True:
            prompt = "Do you accept the license terms? [yes|no] "
            resp = input(prompt).strip().lower()
            if resp in ("y", "yes"):
                return True
            elif resp in ("n", "no"):
                return False
            else:
                print("Please respond with 'yes' or 'no'.\n")
    else:
        print("Python is not running in interactive mode, so cannot show",
              "license confirmation dialog. Please run in an interactive",
              "Python session, or pass `accept_license=True` to",
              "`install_system_image`.")
        return False
