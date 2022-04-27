name = "cvMayaTools"

authors = [
    "Chad Vernon"
]

# Deal with submodule:
# git submodule init
# git submodule update
#
# Now, remove submodule stuff:
# remove the .gitmodule file
# remove entry in the .git/config file
# remove the .git subdirectory inside the submodule folder


# NOTE: version = <cmt_version>.sse.<sse_version>
version = "0.1.0.sse.1.0.0"

description = \
    """
    Chad Vernon Maya Tools (cmt)
    """

with scope("config") as c:
    # Determine location to release: internal (int) vs external (ext)

    # NOTE: Modify this variable to reflect the current package situation
    release_as = "ext"

    # The `c` variable here is actually rezconfig.py
    # `release_packages_path` is a variable defined inside rezconfig.py

    import os
    if release_as == "int":
        c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_INT"]
    elif release_as == "ext":
        c.release_packages_path = os.environ["SSE_REZ_REPO_RELEASE_EXT"]

    #c.build_thread_count = "physical_cores"

requires = [
    "eigen",
]

private_build_requires = [
]

variants = [
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2022.3.sse.2", "python-2", "maya_devkit-2022"],
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2022.3.sse.3", "python-3", "maya_devkit-2022"],
    ["platform-linux", "arch-x86_64", "os-centos-7", "maya-2023", "python-3", "maya_devkit-2023"],
]

uuid = "repository.ChadVernonMayaTools_cmt"

def pre_build_commands():
    command("source /opt/rh/devtoolset-6/enable")

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
