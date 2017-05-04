import os
from math import modf

disks = ['disk0.txt', 'disk1.txt', 'disk2.txt', 'disk3.txt']
files_in_memory = 'files_in_memory'
def creat_file(disk_file):
    open(disk_file, 'a').close()


def read_file(disk_file):
    try:
        with open(disk_file, 'r') as txt_file:
            return txt_file.read()

    except IOError:
        print("could not read", disk_file)


def write_file(disk_name, content):
    try:
        with open(disk_name, 'a') as txt_file:
            txt_file.write(str(content) + " ")
        txt_file.close()
    except IOError:
        print("could not read", disk_name)


def write_tag(disk_name, content):
    try:
        with open(disk_name, 'a') as txt_file:
            txt_file.write("\n" + str(content) + "\n")
        txt_file.close()
    except IOError:
        print("could not read", disk_name)


def clear_disks():
    for disk in disks+[files_in_memory]:
        open(disk, 'w').close()


def shift_disks():
    temp = disks[3]
    disks[3] = disks[2]
    disks[2] = disks[1]
    disks[1] = disks[0]
    disks[0] = temp


def save(file_name):
    write_file(files_in_memory, file_name)
    text = read_file(file_name)
    text = text.split()
    length = len(text)
    count = modf(length/3)[1]
    count = int(count)
    content = [' '.join(text[:count]), ' '.join(text[count:count*2]), ' '.join(text[count*2:]), ' '.join(text)]
    for i in range(len(disks)-1):
        write_tag(disks[i], "<start" + file_name + ">")
        write_file(disks[i], content[i])
        write_tag(disks[i], "<end" + file_name + ">")
    write_tag(disks[3], "<start full" + file_name + ">")
    write_file(disks[3], content[3])
    write_tag(disks[3], "<end full" + file_name + ">")


def get(file_name):
    recover()
    start_tag = "<start full" + file_name + ">"
    end_tag = "<end full" + file_name + ">"
    for disk in disks:
        content = open(disk).read()
        if start_tag in content:
            a, b = content.find(start_tag), content.find(end_tag)
            file_content = content[a+len(start_tag):b]
            return file_content


def get_from(disk, file_name):
    start_tag = "<start" + file_name + ">"
    end_tag = "<end" + file_name + ">"

    start_full_tag = "<start full" + file_name + ">"
    end_full_tag = "<end full" + file_name + ">"
    try:
        content = open(disk).read()
        if start_tag in content:
            a, b = content.find(start_tag), content.find(end_tag)
            file_content = content[a+len(start_tag)+1:b-2]
            return file_content
        elif start_full_tag in content:
            a, b = content.find(start_full_tag), content.find(end_full_tag)
            file_content = content[a+len(start_full_tag)+1:b-2]
            return file_content
    except IOError:
        print("could not read", disk)


def check_disks():
    i = 0
    missing_disks = []
    for disk in disks:
        is_file_open = os.path.isfile(disk)
        if not is_file_open:
            i += 1
            missing_disks.append(disk)
        else:
            i += 1
    return missing_disks


def disk_recovery(missing_disk):
    files = read_file(files_in_memory).split()
    disks_contents = []
    for file in files:
        file_content = []
        for disk in disks:
            file_content.append(get_from(disk, file))
        disks_contents.append(file_content)
    full_text_index = 3
    for disk in disks_contents:
        if disk[full_text_index] is not None:
            rest = []
            for i in range(4):
                if i != full_text_index and disk[i] is not None:
                    rest += [disk[i]]
            for i in range(len(rest)):
                if " "+rest[i] in disk[full_text_index]:
                    disk[full_text_index] = disk[full_text_index].replace(" "+rest[i], '')
                elif "\n"+rest[i] in disk[full_text_index]:
                    disk[full_text_index] = disk[full_text_index].replace("\n" + rest[i], '')
                elif rest[i] in disk[full_text_index]:
                    disk[full_text_index] = disk[full_text_index].replace(rest[i], '')
            for i in range(4):
                if i != full_text_index and disk[i] is None:
                    creat_file(''.join(missing_disk[0]))
                    start_tag = "<start" + files[i] + ">"
                    end_tag = "<end" + files[i] + ">"
                    write_tag(''.join(missing_disk[0]), start_tag)
                    write_file(''.join(missing_disk[0]), disk[full_text_index])
                    write_tag(''.join(missing_disk[0]), end_tag)
        else:
            rest = []
            for i in range(4):
                if i != full_text_index and disk[i] is not None:
                    rest += disk[i]
            for i in range(4):
                if i != full_text_index and disk[i] is not None:
                    creat_file(''.join(missing_disk[0]))
                    start_tag = "<start" + files[i] + ">"
                    end_tag = "<end" + files[i] + ">"
                    write_tag(''.join(missing_disk[0]), start_tag)
                    write_file(''.join(missing_disk[0]), rest)
                    write_tag(''.join(missing_disk[0]), end_tag)
        if full_text_index == 0:
            full_text_index = 3
        else:
            full_text_index -= 1
        temp = files[0]
        del files[0]
        files.append(temp)


def load_files():
    save('test_file.txt')
    shift_disks()
    save('numbers.txt')
    shift_disks()
    save('test_file2.txt')


def recover():
    missing_disks = check_disks()
    if len(missing_disks) == 1:
        disk_recovery(missing_disks)


def main():
    #load_files()
    #clear_disks()
    print(get('test_file.txt'))
    print(get('numbers.txt'))
    print(get('test_file2.txt'))
    pass

if __name__ == "__main__":
    main()
