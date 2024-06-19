from .check_library_exist import is_library_exist
from .install_library import install_library
from .get_dependencies import get_library_dependency_names
from .get_all_library_releases import get_all_releases_of_library
from .uncompress_library import uncompress_library

from ..utils.parse_package_string import parse_package_string
import os


class MagicLibraryInstaller:
    """
    Automatically installs the latest version of the specified library along with all its dependencies from PyPI.

    This class leverages available tools to seamlessly download and install the desired library 
    and its required dependencies, ensuring that the setup process is efficient and error-free. 
    Note that libraries utilizing C extensions or requiring compilation may encounter issues.
    """
    def __init__(self, library_name:str, lib_folder_path:str, print_progress:bool=True, on_progress_changed=None) -> None:
        self.print_progress = print_progress
        self.library_name = library_name
        self.lib_folder_path = lib_folder_path

        self.on_progress_changed = on_progress_changed
        # Check if the library exists in PYPI
        self.__progress_changed_event("Check if library exists")
        if not is_library_exist(library_name=library_name):
            raise Exception("The library is not exist.")
        
        # Check if the desired folder to install the package in it is exists.
        self.__progress_changed_event("Check lib folder (output folder)")
        if not os.path.isdir(lib_folder_path):
            raise Exception("The provided folder path for 'lib_folder_path' is not exist.")
        
        # get all_dependencies
        self.__progress_changed_event("Start getting dependencies")
        self.__all_dependencies = []
        self.__all_dependencies.append(self.library_name)
        self.__index_packages_to_get_dependencies(package_name=library_name)

        # install all
        self.__install_all_packages()

    def __index_packages_to_get_dependencies(self, package_name:str):
        if self.print_progress:
            if self.library_name == package_name:
                self.__progress_changed_event(f"Getting dependencies of {package_name}..")
            else:
                self.__progress_changed_event(f"Getting dependencies of {self.library_name}'s sub-packages ({package_name})..")
        deps : list = get_library_dependency_names(lib_name=package_name)

        for d in deps:
            fine_tuned_name, min_v, max_v = parse_package_string(package_string=d)
            if str(fine_tuned_name).lower() not in self.__all_dependencies:
                self.__all_dependencies.append(str(fine_tuned_name).lower())
                self.__index_packages_to_get_dependencies(package_name=fine_tuned_name)
    
    
    def __install_all_packages (self):
        for p in self.__all_dependencies:
            if self.print_progress:
                self.__progress_changed_event(f"installing {p}")
            library_latest_release = get_all_releases_of_library(library_name=p)[-1]
            install_library(lib_name=p, version=library_latest_release, download_location_path=self.lib_folder_path)

            file_path = os.path.join(self.lib_folder_path, f"{p}.tar.gz")
            new_file_path = os.path.join(self.lib_folder_path, p)
            self.__progress_changed_event(f"uncompress {p}")
            uncompress_library(tar_gz_file=file_path, dst_path=new_file_path)
    

    # Events Callers
    def __progress_changed_event (self, new_progress_name:str):
        if self.print_progress:
            print(f"{new_progress_name}..")
        if self.on_progress_changed is not None:
            self.on_progress_changed(new_progress_name)