import xlsxwriter
import datetime
import Settings as s
from Joint import joint
# from openpyxl import Workbook


def create_workbook():
    current_time = datetime.datetime.now()
    worksheet_name = str(current_time.day) + "." + str(current_time.month) + " " + str(current_time.hour) + "." + \
                     str(current_time.minute) + "." + str(current_time.second) + ".xlsx"
    s.excel_workbook = xlsxwriter.Workbook(worksheet_name)
    s.ex_list = []

def wf_joints(ex_name, list_joints):
    '''
    Writing joints data for an exercise in Excel file in two versions
    :param ex_name:
    :param list_joints:
    :return:
    '''
    current_time = datetime.datetime.now()
    name = ex_name + str(current_time.minute) + str(current_time.second)
    s.worksheet = s.excel_workbook.add_worksheet(name)
    frame_number = 1

    for l in range(1, len(list_joints)):
        row = 1
        s.worksheet.write(0, frame_number, frame_number)
        for j in list_joints[l]:
            if type(j) == joint:
                j_ar = j.joint_to_array()
                for i in range(len(j_ar)):
                    s.worksheet.write(row, frame_number, str(j_ar[i]))
                    row += 1
            else:
                s.worksheet.write(row, frame_number, j)
                row += 1
        frame_number += 1

    name2 = ex_name + "v2" + str(current_time.minute) + str(current_time.second)
    s.worksheet = s.excel_workbook.add_worksheet(name2)
    row = 0
    frame_number = 0
    for l in range(1, len(list_joints)):
        for j in list_joints[l]:
            if type(j) == joint:
                j_ar = j.joint_to_array()
                s.worksheet.write(row, 0, frame_number)
                for i in range(len(j_ar)):
                    s.worksheet.write(row, i + 1, str(j_ar[i]))
                row += 1
            else:
                s.worksheet.write(row-1, i + 2,j)
        frame_number += 1

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
