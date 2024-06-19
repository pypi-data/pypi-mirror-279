import importlib
import logging
import tracemalloc
import sys
from pathlib import Path
from importlib.util import find_spec

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Initialize tracemalloc to track memory allocations
tracemalloc.start()

# Root directory of the project
ROOT_DIR = Path(__file__).resolve().parent.parent

# List of subdirectories to inspect
SUBDIRECTORIES = ["api", "cli", "core"]

# List of modules to test
MODULES = [
    "getai",
    "getai.api",
    "getai.api.datasets",
    "getai.api.models",
    "getai.api.utils",
    "getai.cli",
    "getai.cli.commands",
    "getai.cli.main",
    "getai.cli.utils",
    "getai.core",
    "getai.core.dataset_downloader",
    "getai.core.dataset_search",
    "getai.core.model_downloader",
    "getai.core.model_search",
    "getai.core.session_manager",
    "getai.core.utils",
]


# Function to print the current script path and list the contents of each subdirectory
def list_subdirectory_contents(root_dir, subdirectories):
    logger.info(f"Current script path: {Path(__file__).resolve()}")

    for subdir in subdirectories:
        subdir_path = root_dir / subdir
        logger.info(f"Contents of {subdir_path}:")

        if subdir_path.exists() and subdir_path.is_dir():
            for path in subdir_path.glob("**/*"):
                logger.info(path.resolve())
        else:
            logger.warning(f"{subdir_path} does not exist or is not a directory")


# Function to test import and export of a module
def test_import_export(module_name):
    try:
        # Attempt to import the module
        module = importlib.import_module(module_name)
        logger.info(f"Successfully imported module: {module_name}")

        # Check for __all__ attribute
        if hasattr(module, "__all__"):
            for item in module.__all__:
                if not hasattr(module, item):
                    logger.error(
                        f'Module "{module_name}" is missing "{item}" in __all__'
                    )
                else:
                    logger.info(f'Found "{item}" in module "{module_name}"')
        else:
            logger.warning(f'Module "{module_name}" does not have __all__ attribute')
    except Exception as e:
        logger.error(f'Failed to import module "{module_name}": {e}', exc_info=True)


# Function to dynamically find and check modules
def dynamic_module_check(root_dir):
    for path in root_dir.glob("**/*.py"):
        relative_path = path.relative_to(root_dir)
        module_name = "getai." + ".".join(relative_path.with_suffix("").parts)
        test_import_export(module_name)


# Main function to run the tests
def main():
    logger.info("Starting import/export alignment test")

    # List contents of subdirectories
    list_subdirectory_contents(ROOT_DIR, SUBDIRECTORIES)

    # Test predefined modules
    for module in MODULES:
        test_import_export(module)

    # Dynamically find and test modules
    dynamic_module_check(ROOT_DIR)

    # Display memory allocation snapshot
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    logger.info("Top 10 memory allocation locations:")
    for stat in top_stats[:10]:
        logger.info(stat)

    tracemalloc.stop()


if __name__ == "__main__":
    main()
