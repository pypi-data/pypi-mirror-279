import os.path
import tempfile
from pathlib import Path
from dektools.file import list_dir, read_text, remove_path
from dekprompt.cfg import CfgFile

path_dir = Path(__file__).resolve().parent
if __name__ == '__main__':
    path_out = os.path.join(tempfile.mktemp())
    CfgFile(
        path_out,
        *sorted(list_dir(path_dir / 'samples'))
    ).apply()
    print('\n\n===Result is===:\n')
    print(read_text(path_out))
    remove_path(path_out)
