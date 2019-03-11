import time
import csv
import os , operator

class System_monitoring():

    def __init__(self, mintues):
        self.mintues = mintues


    def monitor(self):
        if type(self.mintues) is not int:
            raise ValueError("Please Provide value in Integer format")
        iteration = self.mintues * 6
        for i in range(iteration):
            array = []
            if i == 0:
                self.execute_ps("import_1")
                time.sleep(10)
            if i == 1:
                self.execute_ps("import_2")
                array = self.calculate_process("import_1.csv","import_2.csv")
                self.write_csv(array,"import_1.csv")
                time.sleep(10)
            if i > 1 and i <= (iteration - 2):
                self.execute_ps("import_2")
                array = self.calculate_process("import_1.csv","import_2.csv")
                self.write_csv(array,"import_1.csv")
                time.sleep(10)
            if i == iteration - 1:
                self.execute_ps("import_2")
                array = self.calculate_process("import_1.csv","import_2.csv")
                self.write_csv(array,"final_file.csv")
                time.sleep(10)
        return "final_file.csv"


    def sort_csv(self, file_name, number, sort_order):
        if type(number) is not int:
            raise ValueError("Please Provide number value in Integer format")
        if type(file_name) is not str:
            raise ValueError("Please Provide valid value for file name in string format")
        if not os.path.isfile(file_name):
            raise FileNotFoundError ("Provided file is not found, Provide vaild file path")
        if type(sort_order) is not str:
            raise ValueError("Please Provide valid value for sort_order in string format (ascend/descend)")
        if sort_order != "ascend" and sort_order != "descend":
            raise ValueError("Please Provide sort_order value it must be (ascend/descend)")
        order = True
        if sort_order == "ascend":
            order = False
        with open(file_name, mode='r') as csv_file:
            data = csv.reader(csv_file)
            sorted_list = sorted(data, key=operator.itemgetter(2) and operator.itemgetter(3), reverse=order)
        csv_file.close()
        return sorted_list[:number]



    def execute_ps(self, file_name):
        if type(file_name) is not str:
            raise ValueError("Please Provide valid value for file name in string format")
        cmd = "ps -eo pid,ppid,%mem,%cpu,comm | awk '($3 > 0 ) ||  ($4 > 0)' | awk  '{print $1 \",\" $2 \",\" $3 \",\" " \
              "$4 \",\" $5}' >" + file_name + ".csv"
        os.system(cmd)

    def print_csv(self, csv_list):
        if type(csv_list) is not list:
            raise ValueError("Please Provide cvs list in valid format. It would be in list format")
        print("PID  PPID  %MEM  %CPU  COMMAND")
        for process_list in csv_list:
            print(process_list[0] + " " + process_list[1] + " " + process_list[2] + " " + process_list[3] + " " + \
                  process_list[4])

    def write_csv(self, csv_array, file_name):
        if type(file_name) is not str:
            raise ValueError("Please Provide valid value for file name in string format")
        if type(csv_array) is not list:
            raise ValueError("Please Provide valid value for csv_file in array format")
        open(file_name, 'w').close()

        with open(file_name, mode='w') as final_file:
            final_file_writer = csv.writer(final_file)
            if file_name == "final_file.csv":
                final_file_writer.writerow(['PID', 'PPID', '%MEM', '%CPU', 'COMMAND'])
            final_file_writer.writerows(csv_array)
        final_file.close()


    def calculate_process(self, file1, file2):
        if type(file1) is not str:
            raise ValueError("Please Provide valid value for file1 name in string format")
        if type(file2) is not str:
            raise ValueError("Please Provide valid value for file2 name in string format")
        final_file_array = []

        with open(file1, 'r') as file_one:
            file_one_reader = csv.reader(file_one)
            file_one_array = list(file_one_reader)
        with open(file2, 'r') as file_two:
            file_two_reader = csv.reader(file_two)
            file_two_array = list(file_two_reader)
        file_one.close()
        file_two.close()
        if len(file_one_array) == 0 or len(file_one_array[0]) != 5:
            raise ValueError("Please Provide file1 is not valid format to read, It must contain output of ps command in specified format")
        if len(file_two_array) == 0 or len(file_two_array[0]) != 5:
            raise ValueError("Please Provide file2 is not valid format to read, It must contain output of ps command in specified format")

        for i in file_one_array:
            flag = False
            for j in file_two_array:
                if i[0] == j[0] and i[1] == j[1] and i[4] == j[4]:
                    i[2] = str((float(i[2]) + float(j[2]))/2)
                    i[3] = str((float(i[3]) + float(j[3]))/2)
                    final_file_array.append(i)
                    flag = True
                    file_two_array.remove(j)
                    break
            if not flag:
                final_file_array.append(i)
        final_file_array = final_file_array + file_two_array
        return final_file_array

def main():
    try:
        min = int(input("Enter monitoring time limit in mintues : "))
    except ValueError:
        raise ValueError("Oops!  That was no valid number.  Try again...")

    sm01 = System_monitoring(min)
    output_filename = sm01.monitor()
    data = sm01.sort_csv(output_filename, 10 , "descend")

if __name__ == '__main__':
    main()
