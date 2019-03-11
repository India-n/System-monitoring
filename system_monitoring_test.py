import unittest
import os
import time
from system_monitoring.system_monitoring import System_monitoring

class Testsystem_monitoring(unittest.TestCase):

    def test_monitor_pass(self):
        sm01 = System_monitoring(1)
        data = sm01.monitor()
        self.assertEqual(data, "final_file.csv")
        os.remove("import_1.csv")
        os.remove("import_2.csv")
        os.remove("final_file.csv")

    def test_monitor_fail_for_string(self):
        sm01 = System_monitoring("test")
        with self.assertRaises(ValueError): sm01.monitor()

    def test_monitor_fail_for_float(self):
        sm01 = System_monitoring(0.7)
        with self.assertRaises(ValueError): sm01.monitor()

    def test_sort_csv_pass(self):
        sm01 = System_monitoring(3)
        sm01.execute_ps("final_file")
        ascend_data = sm01.sort_csv("final_file.csv", 10, "ascend")
        self.assertEqual(type(ascend_data), list)
        descend_data = sm01.sort_csv("final_file.csv", 10, "descend")
        self.assertEqual(type(descend_data), list)
        os.remove("final_file.csv")

    def test_sort_csv_fail_by_value_error_for_number(self):
        sm01 = System_monitoring("test")
        sm01.execute_ps("final_file")
        with self.assertRaises(ValueError): sm01.sort_csv("final_file.csv", "10", "ascend")
        os.remove("final_file.csv")

    def test_sort_csv_fail_by_file_not_found(self):
        sm01 = System_monitoring("test")
        with self.assertRaises(FileNotFoundError): sm01.sort_csv("test.csv", 10, "ascend")

    def test_sort_csv_fail_by_value_error_for_sort_order(self):
        sm01 = System_monitoring("test")
        sm01.execute_ps("final_file")
        with self.assertRaises(ValueError): sm01.sort_csv("final_file.csv", 10, 90)
        os.remove("final_file.csv")

    def test_sort_csv_fail_for_sort_order_by_wrong_value(self):
        sm01 = System_monitoring("test")
        sm01.execute_ps("final_file")
        with self.assertRaises(ValueError): sm01.sort_csv("final_file.csv", 10, "test")
        os.remove("final_file.csv")

    def test_execute_ps_pass(self):
        sm01 = System_monitoring(4)
        sm01.execute_ps("testfile")
        self.assertEqual(os.path.isfile("testfile.csv"), True)
        os.remove("testfile.csv")

    def test_execute_ps_fail_by_value_error(self):
        sm01 = System_monitoring(4)
        with self.assertRaises(ValueError) : sm01.execute_ps(10)

    def test_calculate_process_pass(self):
        sm01 = System_monitoring(4)
        sm01.execute_ps("testfile01")
        time.sleep(10)
        sm01.execute_ps("testfile02")
        data = sm01.calculate_process("testfile01.csv" , "testfile02.csv")
        self.assertEqual(type(data), list)
        os.remove("testfile01.csv")
        os.remove("testfile02.csv")

    def test_calculate_process_fail_for_invalid_input_format(self):
        sm01 = System_monitoring(4)
        open("empty.csv","w+").close()
        with self.assertRaises(ValueError) : sm01.calculate_process("empty.csv" , 1)
        with self.assertRaises(ValueError) : sm01.calculate_process(1 , "empty.csv")
        os.remove("empty.csv")

    def test_calculate_process_fail_for_file_not_found(self):
        sm01 = System_monitoring(4)
        open("empty.csv","w+").close()
        with self.assertRaises(FileNotFoundError) : sm01.calculate_process("no_file.csv" , "empty.csv")
        with self.assertRaises(FileNotFoundError) : sm01.calculate_process("empty.csv" , "no_file.csv")
        os.remove("empty.csv")

    def test_calculate_process_fail_for_empty_file(self):
        sm01 = System_monitoring(4)
        open("empty.csv","w+").close()
        sm01.execute_ps("testfile")
        with self.assertRaises(ValueError) : sm01.calculate_process("testfile.csv" , "empty.csv")
        with self.assertRaises(ValueError) : sm01.calculate_process("empty.csv" , "testfile.csv")
        os.remove("empty.csv")


    def test_write_csv_pass(self):
        sm01 = System_monitoring(4)
        file_name = "test_file.csv"
        array = [['1', '0', '0.0', '0.2', 'systemd'], ['60', '2', '0.0', '0.3', 'kworker/1:1'], ['362', '1', '0.3', '0.0', 'systemd-journal'], ['445', '1', '0.0', '0.3', 'systemd-udevd']]
        sm01.write_csv(array,file_name)
        self.assertEqual(os.path.isfile(file_name), True)
        os.remove("test_file.csv")

    def test_write_csv_fail_value_error(self):
        sm01 = System_monitoring(4)
        with self.assertRaises(ValueError) : sm01.write_csv("","unknown.csv")
        with self.assertRaises(ValueError) : sm01.write_csv([],1)

    def test_print_csv_pass(self):
        sm01 = System_monitoring(4)
        array = [['1', '0', '0.0', '0.2', 'systemd'], ['60', '2', '0.0', '0.3', 'kworker/1:1'], ['362', '1', '0.3', '0.0', 'systemd-journal'], ['445', '1', '0.0', '0.3', 'systemd-udevd']]
        self.assertEqual(sm01.print_csv(array),None)

    def test_print_csv_fail(self):
        sm01 = System_monitoring(4)
        with self.assertRaises(ValueError) : sm01.print_csv("array")



if __name__ == '__main__':
    unittest.main()
