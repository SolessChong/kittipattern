import os
import shutil
import fnmatch

for path, dirs, files in os.walk('.'):
  for filename in fnmatch.filter(files, '*.xml'):
    run_id = re.match(r'\d*.*(\d{4})', """DIR""").group(1)
    shutil.move(.....)

