import csv
import os
import re
import statistics
import sys
from datetime import datetime

def analyse(adj_error):
    dir_path = "/home/admin/logs"
    directory = os.path.join(dir_path)

    for root, dirs, files in os.walk(directory):
        for file in sorted(files):
            if not file.startswith('error'):
                if file.endswith(".log"):
                    f = open(dir_path + '/' + file, 'r')
                    list = []
                    csvreader = csv.reader(f)
                    for row in csvreader:
                            list.append(int((re.findall(r'\d+', row[4].split(';')[1])[0]))-adj_error)
                            
                    stat_info = os.stat(dir_path + '/' +file)
                    modification_time = datetime.fromtimestamp(stat_info.st_mtime)
                    date_part = modification_time.strftime("%Y-%m-%d")
                    print(u"{:s} - min: {:g}\u00b0C, max: {:g}\u00b0C,  mean: {:g}\u00b0C, median: {:g}\u00b0C".format(date_part,
                                                                                                  min(list), max(list),
                                                                                              statistics.mean(list), statistics.median(list)))

                f.close()


if __name__ == "__main__":
    adj_error = 0
    if len(sys.argv) > 1:
        adj_error = int(sys.argv[1])
    analyse(adj_error)

