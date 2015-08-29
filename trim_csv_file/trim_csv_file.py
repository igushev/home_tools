import csv


def TrimCsvFile(filename_in, filename_out):
  data = []
  with open(filename_in, 'r') as file_in:
    csv_in = csv.reader(file_in)
    for row in csv_in:
      data.append([s.strip() for s in row])

  with open(filename_out, 'w', newline='') as file_out:
    csv_out = csv.writer(file_out)
    for data_row in data:
      csv_out.writerow(data_row)
