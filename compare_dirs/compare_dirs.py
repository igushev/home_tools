import datetime
import filecmp
import os
import sys


class CompareDirs(object):

  def __init__(self):
    self.started = datetime.datetime.now()
    self.log_file = open('log.txt', 'w', encoding='utf-8')
    self.result_file = open('result.txt', 'w', encoding='utf-8')

  def __del__(self):
    msg = 'Elapsed time: %s\n' % (datetime.datetime.now() - self.started)
    self.PrintAndLog(msg, result=True)
    self.log_file.close()
    self.result_file.close()

  def PrintAndLog(self, msg, result=False):
    # NOTE(igushev): Print non-english latters.
    print(msg, end='')
    self.log_file.write(msg)
    if result:
      self.result_file.write(msg)
  
  def GetRelpaths(self, dir_):
    relpaths = set()
    for rootpath, dirnames, filenames in os.walk(dir_):
      for filename in filenames:
        filepath = os.path.join(rootpath, filename)
        filerelpath = os.path.relpath(filepath, dir_)
        relpaths.add(filerelpath)
    return relpaths


  def CompareRelpaths(self, dir_, extra_relpaths):
    if extra_relpaths:
      msg = 'Extra files in %s:\n' % dir_
      msg += ''.join(extra_relpath + '\n' for extra_relpath in extra_relpaths)
      msg += 'Total %d\n' % len(extra_relpaths)
    else:
      msg = 'No extra files found in %s\n' % dir_
    self.PrintAndLog(msg, result=True)
    

  def CompareFiles(self, dir_1, dir_2, filerelpaths):
    count = len(filerelpaths)
    different_filerelpaths = []
    for i, filerelpath in enumerate(filerelpaths):
      msg = 'Comparing %d/%d: %s...' % (i + 1, count, filerelpath)
      filepath_1 = os.path.join(dir_1, filerelpath)
      filepath_2 = os.path.join(dir_2, filerelpath)
      if not filecmp.cmp(filepath_1, filepath_2):
        different_filerelpaths.append(filerelpath)
        msg += 'DIFFERENT\n'
      else:
        msg += 'OK\n'
      self.PrintAndLog(msg)
    if different_filerelpaths:
      msg = 'Files different in %s and %s:\n' % (dir_1, dir_2)
      msg += ''.join(different_filerelpath + '\n'
                     for different_filerelpath in different_filerelpaths)
      msg += 'Total %d\n' % len(different_filerelpaths)
    else:
      msg = 'No different files\n'
    self.PrintAndLog(msg, result=True)

  def __call__(self, dir_1, dir_2, content_only):
    relpaths_1 = self.GetRelpaths(dir_1)
    relpaths_2 = self.GetRelpaths(dir_2)
    self.CompareRelpaths(dir_1, sorted(relpaths_1 - relpaths_2))
    self.CompareRelpaths(dir_2, sorted(relpaths_2 - relpaths_1))
    if content_only:
      return
    self.CompareFiles(dir_1, dir_2, sorted(relpaths_1 & relpaths_2))


def main(argv):
  content_only = (
    True if len(argv) == 4 and argv[3] == 'content_only' else False)
  compare_dirs = CompareDirs()
  compare_dirs(argv[1], argv[2], content_only)


if __name__ == '__main__':
  main(sys.argv)
