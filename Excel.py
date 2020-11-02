import xlsxwriter
import datetime
import Settings as s
import Joint
# from openpyxl import Workbook


def create_workbook():
    current_time = datetime.datetime.now()
    worksheet_name = str(current_time.day) + "." + str(current_time.month) + " " + str(current_time.hour) + "." + \
                     str(current_time.minute) + "." + str(current_time.second) + ".xlsx"
    s.excel_workbook = xlsxwriter.Workbook(worksheet_name)
    s.ex_list = []

def wf_joints(ex_name, list_joints):
    current_time = datetime.datetime.now()
    name = ex_name + str(current_time.minute) + str(current_time.second)
    s.worksheet = s.excel_workbook.add_worksheet(name)
    row = 1
    for j in list_joints:
        if type(j) is Joint:
            j_ar = j.joint_to_array()
            # print("it's joint")
        else:
            # print(type(j))
            j_ar = j
        for i in range (len(j_ar)):
            s.worksheet.write(row, i, str(j_ar[i]))
        row += 1

#write to execl file exercises names and the successful repetition number
def wf_exercise():
    row = 1
    col = 0
    s.worksheet = s.excel_workbook.add_worksheet("success")
    for ex in s.ex_list:
        s.worksheet.write(row, col, ex[0])
        s.worksheet.write(row, col+1, ex[1])
        row += 1

def close_workbook():
    s.excel_workbook.close()

if __name__ == "__main__":
    create_workbook()
    s.ex_list = [
        ['raise up', 8],
        ['bend', 8],
        ['raise up', 3],
        ['raise up', 8],
    ]
    # join = [[12, 496.793, 98.652, 927.991],
    # [6, 457.266, 80.806, 757.736],
    # [12, 496.610, 91.162, 930.897]]
    # wf_joints("m",join)

    wf_exercise()
    close_workbook()