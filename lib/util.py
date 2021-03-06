import os
import platform
import sys

def print_error(*args):
    # Stringify args
    args = [str(item) for item in args]
    sys.stderr.write(" ".join(args) + "\n")
    sys.stderr.flush()

def user_dir():
    if "HOME" in os.environ:
      return os.path.join(os.environ["HOME"], ".electrum")
    elif "LOCALAPPDATA" in os.environ:
      return os.path.join(os.environ["LOCALAPPDATA"], "Electrum")
    elif "APPDATA" in os.environ:
      return os.path.join(os.environ["APPDATA"], "Electrum")
    else:
      raise BaseException("No home directory found in environment variables.")

def appdata_dir():
    """Find the path to the application data directory; add an electrum folder and return path."""
    if platform.system() == "Windows":
        return os.path.join(os.environ["APPDATA"], "Electrum")
    elif platform.system() == "Linux":
        return os.path.join(sys.prefix, "share", "electrum")
    elif (platform.system() == "Darwin" or
          platform.system() == "DragonFly"):
        return "/Library/Application Support/Electrum"
    else:
        raise Exception("Unknown system")

def get_resource_path(*args):
    return os.path.join(".", *args)

def local_data_dir():
    """Return path to the data folder."""
    assert sys.argv
    prefix_path = os.path.dirname(sys.argv[0])
    local_data = os.path.join(prefix_path, "data")
    return local_data

def load_theme_name(theme_path):
    try:
        with open(os.path.join(theme_path, "name.cfg")) as name_cfg_file:
            return name_cfg_file.read().rstrip("\n").strip()
    except IOError:
        return None

def theme_dirs_from_prefix(prefix):
    if not os.path.exists(prefix):
        return []
    theme_paths = {}
    for potential_theme in os.listdir(prefix):
        theme_full_path = os.path.join(prefix, potential_theme)
        theme_css = os.path.join(theme_full_path, "style.css")
        if not os.path.exists(theme_css):
            continue
        theme_name = load_theme_name(theme_full_path)
        if theme_name is None:
            continue
        theme_paths[theme_name] = prefix, potential_theme
    return theme_paths

def load_theme_paths():
    theme_paths = {}
    prefixes = (local_data_dir(), appdata_dir())
    for prefix in prefixes:
        theme_paths.update(theme_dirs_from_prefix(prefix))
    return theme_paths

