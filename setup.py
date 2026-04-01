import os
import shutil
import subprocess
from pathlib import Path

from setuptools import Extension, setup
from setuptools.command.build_ext import build_ext


__version__ = "0.0.1"


class BuildPangolinExt(build_ext):
    """Build (or reuse) pangolin Python extension for pip installs."""

    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        project_root = Path(__file__).resolve().parent
        target_path = Path(self.get_ext_fullpath(ext.name))
        target_path.parent.mkdir(parents=True, exist_ok=True)

        module_file = self._find_built_module(project_root)
        if module_file is None:
            self._build_with_cmake(project_root)
            module_file = self._find_built_module(project_root)

        if module_file is None:
            raise RuntimeError(
                "Unable to locate built pangolin extension after CMake build. "
                "Expected a file matching 'pangolin*.so' in project root."
            )

        print(f"copying {module_file} -> {target_path}")
        shutil.copy2(module_file, target_path)

    @staticmethod
    def _find_built_module(project_root: Path):
        candidates = sorted(project_root.glob("pangolin*.so"))
        if not candidates:
            return None
        return candidates[0]

    def _build_with_cmake(self, project_root: Path):
        build_dir = project_root / "build"
        build_dir.mkdir(parents=True, exist_ok=True)

        configure_cmd = ["cmake", ".."]
        build_cmd = [
            "cmake",
            "--build",
            ".",
            "--target",
            "pangolin",
            "--",
            f"-j{os.cpu_count() or 2}",
        ]

        subprocess.check_call(configure_cmd, cwd=str(build_dir))
        subprocess.check_call(build_cmd, cwd=str(build_dir))


setup(
    name="pangolin",
    version=__version__,
    description="python binding for lightweight 3D visualization library Pangolin.",
    url="https://github.com/uoip/pangolin",
    license="MIT",
    ext_modules=[Extension("pangolin", sources=[])],
    cmdclass={"build_ext": BuildPangolinExt},
    keywords="Pangolin, binding, OpenGL, 3D, visualization, Point Cloud",
    long_description="""This is a Python binding for c++ library Pangolin
        (https://github.com/stevenlovegrove/Pangolin).

        Pangolin is a lightweight portable rapid development library for managing
        OpenGL display / interaction and abstracting video input. At its heart is
        a simple OpenGl viewport manager which can help to modularise 3D visualisation
        without adding to its complexity, and offers an advanced but intuitive 3D navigation
        handler. Pangolin also provides a mechanism for manipulating program variables through
        config files and ui integration, and has a flexible real-time plotter for visualising
        graphical data.""",
)
