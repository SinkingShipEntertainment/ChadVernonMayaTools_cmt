name = "cvMayaTools"

authors = [
    "Chad Vernon"
]

# NOTE: version = <cmt_version>.sse.<sse_version>
version = "0.1.0.sse.1.0.0"

description = \
    """
    Chad Vernon Maya Tools (cmt)
    """

with scope("config") as c:
    import os
    c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

requires = [
    "eigen",
]

private_build_requires = [
]

variants = [
    ["maya-2024", "python-3.9", "maya_devkit-2024"],
    ["maya-2024", "python-3.10", "maya_devkit-2024"],
]

uuid = "repository.ChadVernonMayaTools_cmt"

def pre_build_commands():

    info = {}
    with open("/etc/os-release", 'r') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue
            line_info = line.replace('\n', '').split('=')
            if len(line_info) != 2:
                continue
            info[line_info[0]] = line_info[1].replace('"', '')
    linux_distro = info.get("NAME", "centos")
    print("Using Linux distro: " + linux_distro)

    if linux_distro.lower().startswith("centos"):
        command("source /opt/rh/devtoolset-6/enable")
    elif linux_distro.lower().startswith("rocky"):
        pass

def commands():

    # NOTE: REZ package versions can have ".sse." to separate the external
    # version from the internal modification version.
    split_versions = str(version).split(".sse.")
    external_version = split_versions[0]
    internal_version = None
    if len(split_versions) == 2:
        internal_version = split_versions[1]

    env.CVMAYATOOLS_VERSION = external_version
    env.CVMAYATOOLS_PACKAGE_VERSION = external_version
    if internal_version:
        env.CVMAYATOOLS_PACKAGE_VERSION = internal_version

    env.CVMAYATOOLS_ROOT.append("{root}")
    env.CVMAYATOOLS_LOCATION.append("{root}")

    # For Maya to locate the .mod file to setup env variables for plugins and libraries
    env.MAYA_MODULE_PATH.append("{root}")

    # For `scripts`
    env.PYTHONPATH.append("{root}/scripts")

    # For any MEL or other Python scripts that we want to make available at startup
    env.MAYA_SCRIPT_PATH.append("{root}/scripts")
