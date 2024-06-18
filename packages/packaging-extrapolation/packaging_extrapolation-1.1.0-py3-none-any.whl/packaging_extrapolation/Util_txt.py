import os
import re
import shutil
from packaging_extrapolation import UtilTools
import numpy as np
import pandas as pd


def update_card(source_folder, target_folder, chk_sym, key_word, new_chk_sym, new_key_word=None):
    if new_chk_sym == 'avdz':
        new_key_word = 'aug-cc-pvdz'
    elif new_chk_sym == 'avtz':
        new_key_word = 'aug-cc-pvtz'
    elif new_chk_sym == 'avqz':
        new_key_word = 'aug-cc-pvqz'
    elif new_chk_sym == 'av5z':
        new_key_word = 'aug-cc-pv5z'
    elif new_chk_sym == 'av6z':
        new_key_word = 'aug-cc-pv6z'

    # 创建目标文件夹
    os.makedirs(target_folder, exist_ok=True)

    # 遍历源文件夹中的文件
    for filename in os.listdir(source_folder):
        source_file_path = os.path.join(source_folder, filename)
        target_file_path = os.path.join(target_folder, filename)

        with open(source_file_path, 'r') as source_file:
            lines = source_file.readlines()

        modified_lines = []
        for line in lines:
            modified_line = line.replace(chk_sym, new_chk_sym).replace(key_word, new_key_word)
            modified_lines.append(modified_line)

        with open(target_file_path, 'w') as target_file:
            target_file.writelines(modified_lines)


# 修改文件名，替换文件名中的file_word为new_file_word
def update_filename(source_folder, file_word, new_file_word):
    # 获取文件夹中的所有文件名
    file_names = os.listdir(source_folder)

    # 遍历文件名列表并修改文件名
    for file_name in file_names:
        # 判断文件名中是否包含'avdz'
        if file_word in file_name:
            # 构造新的文件名
            new_file_name = file_name.replace(file_word, new_file_word)

            # 构造旧文件路径和新文件路径
            old_file_path = os.path.join(source_folder, file_name)
            new_file_path = os.path.join(source_folder, new_file_name)

            # 重命名文件
            os.rename(old_file_path, new_file_path)

            print(f"文件名已修改：{file_name} -> {new_file_name}")

    print("文件名修改完成。")


# 复制文件夹到新的文件夹,并重命名
def copy_file(source_file, target_folder, new_filename):
    # 构造新的文件路径
    target_file_path = os.path.join(target_folder, new_filename)
    shutil.copy(source_file, target_file_path)


# 更改gjf，由上一次波函数作为初猜进行计算
def update_chk(source_gjf, target_gjf, *, new_chk, old_method, new_method,
               old_card, new_card):
    # 遍历文件夹文件
    for filename in os.listdir(source_gjf):
        # 拼接路径
        source_gjf_path = os.path.join(source_gjf, filename)

        # 读取文件
        with open(source_gjf_path, 'r') as source_file:
            lines = source_file.readlines()

        modified_lines = []

        # 遍历文本行
        for i, line in enumerate(lines):
            # 当遍历到%chk这一行时，更改
            if line.startswith("%chk="):
                modified_line = line.replace(old_method, new_method).replace(old_card, new_card)
                modified_lines.append(modified_line)
            # 当遍历到第4行，更改行
            elif line.startswith("#p"):
                modified_line = new_chk
                modified_lines.append(modified_line)
                modified_lines.append('\n')
            else:
                modified_lines.append(line)

            # 判断是否读入到0 1
            if i == 7:
                modified_lines.append('\n')
                break

        # 目标文件绝对路径
        target_gif_path = os.path.join(target_gjf, filename)

        # 将gjf文件写入新的文件夹
        with open(target_gif_path, 'w') as target_file:
            target_file.writelines(modified_lines)

    # 更改文件名
    update_filename(target_gjf, old_method, new_method)
    update_filename(target_gjf, old_card, new_card)


# 修改命令行
def update_com(*, com, source_gjf, target_gjf, old_method, new_method):
    for filename in os.listdir(source_gjf):
        # 拼接路径
        source_gjf_path = os.path.join(source_gjf, filename)

        # 读取文件
        with open(source_gjf_path, 'r') as source_file:
            lines = source_file.readlines()
        modified_lines = []
        for i, line in enumerate(lines):
            if line.startswith("#p"):
                modified_lines.append(com)
                modified_lines.append('\n')

            elif line.startswith("%chk="):
                temp = line.replace(old_method, new_method)
                modified_lines.append(temp)
            else:
                modified_lines.append(line)
        modified_lines.append("\n")
        # 目标文件绝对路径
        target_gif_path = os.path.join(target_gjf, filename)
        # 将gjf文件写入新的文件夹
        with open(target_gif_path, 'w') as target_file:
            target_file.writelines(modified_lines)

        update_filename(target_gjf, old_method, new_method)


# 文件夹获取hf,mp2,ccsd,ccsd(t)能量
def get_energy_values(source_folder):
    for filename in os.listdir(source_folder):
        # 读取文件内容
        data = get_log_values(filename)


# 文件夹获取极化率
def get_polar_values(source_folder):
    for filename in os.listdir(source_folder):
        # 读取文件内容
        data = get_log_values_polar(filename)


# 获取单个文件能量
def get_log_values(source_file):
    # 读取文件内容
    with open(source_file, 'r') as file:
        content = file.read()

    # 开始位置
    start_index = content.find('1\\1')
    # 存储数据的列表
    data = []
    # 判断找到指定位置
    if start_index != -1:
        # 从指定位置开始按 `\` 分割内容
        split_content = content[start_index:].split('\\')
        # 遍历分割结果
        for item in split_content:
            # 判断是否遇到结束标记
            if item == '@':
                break
            item = item.replace('\n', '').replace(' ', '')
            # 存储数据
            data.append(item)
    HF = get_HF(data)
    MP2 = get_MP2(data)
    MP4 = get_MP4(data)
    CCSD = get_CCSD(data)
    CCSD_T = get_CCSD_T(data)
    CBSQB3 = get_cbsqb3(data)
    energy_dict = {'HF': HF, 'MP2': MP2, 'MP4': MP4, 'CCSD': CCSD,
                   'CCSD(T)': CCSD_T, 'CBSQB3': CBSQB3}
    return energy_dict


# 获取CBSQB3值
def get_log_cbsqb3(source_file):
    # 读取文件内容
    with open(source_file, 'r') as file:
        content = file.read()

    # 开始位置
    start_index = content.find('CBS-QB3\\CBS-QB3')
    # 存储数据的列表
    data = []
    # 判断找到指定位置
    if start_index != -1:
        # 从指定位置开始按 `\` 分割内容
        split_content = content[start_index:].split('\\')
        # 遍历分割结果
        for item in split_content:
            # 判断是否遇到结束标记
            if item == '@':
                break
            item = item.replace('\n', '').replace(' ', '')
            # 存储数据
            data.append(item)
    HF = get_HF(data)
    MP2 = get_MP2(data)
    MP4 = get_MP4(data)
    CCSD = get_CCSD(data)
    CCSD_T = get_CCSD_T(data)
    CBSQB3 = get_cbsqb3(data)
    energy_dict = {'HF': HF, 'MP2': MP2, 'MP4': MP4, 'CCSD': CCSD,
                   'CCSD(T)': CCSD_T, 'CBSQB3': CBSQB3}
    return energy_dict


def get_cbsqb3(data):
    for i in range(len(data)):
        item = data[i]
        if 'CBSQB3=' in item:
            return re.search(r'-?\d+\.\d+', item).group()
    return ValueError('No cbsqb3-energy can get')


# 获取单个文件的基函数数量
def get_log_basisFunction_single(source_file):
    # 存储包含关键字的行的列表
    temp = ""
    # 打开文件并逐行查找
    with open(source_file, 'r') as file:
        for line in file:
            # 检查是否包含关键字
            if 'basis functions,' in line:
                # 将包含关键字的行添加到列表中
                temp = line
                break

    # 打印存储的行
    return temp


# 获取当前文件夹所有文件的基函数数量
def get_log_basisFunction(source_gjf):
    df = pd.DataFrame(columns=['mol', 'basis functions', 'primitive gaussians',
                               'cartesian basis functions'])
    i = 0
    count1 = []
    count2 = []
    count3 = []
    count4 = []
    # 遍历文件夹
    for filename in os.listdir(source_gjf):
        # 拼接路径
        source_gjf_path = os.path.join(source_gjf, filename)
        print(filename)
        temp = get_log_basisFunction_single(source_gjf_path)
        temp = temp.split(',')
        count1.append(filename)
        count2.append(get_strNum(temp[0]))
        count3.append(get_strNum(temp[1]))
        count4.append(get_strNum(temp[2]))
    df['mol'] = count1
    df['basis functions'] = count2
    df['primitive gaussians'] = count3
    df['cartesian basis functions'] = count4
    return df


# 取出一个字符串中的数字
def get_strNum(string):
    pattern = r'\b\d+\b'
    # 提取数字
    numbers = re.findall(pattern, string)
    return int(numbers[0])


# 获取单个文件极化率
def get_log_values_polar(source_file):
    # 读取文件内容
    with open(source_file, 'r') as file:
        content = file.read()

    # 开始位置
    start_index = content.find('1\\1')
    # 存储数据的列表
    data = []
    # 判断找到指定位置
    if start_index != -1:
        # 从指定位置开始按 `\` 分割内容
        split_content = content[start_index:].split('\\')
        # 遍历分割结果
        for item in split_content:
            # 判断是否遇到结束标记
            if item == '@':
                break
            item = item.replace('\n', '').replace(' ', '')
            # 存储数据
            data.append(item)
    polar = get_polar(data)
    polar_split = polar[0].split(',')
    polar_split_num = [float(value) for value in polar_split]
    avg_polar = (polar_split_num[0] + polar_split_num[2] + polar_split_num[5]) / 3
    return avg_polar


# 批量更改gjf内存
def update_mem(folder_path, output_folder_path, old_value, new_value):
    # 创建新文件夹
    os.makedirs(output_folder_path, exist_ok=True)

    # 遍历文件夹中的文件
    for filename in os.listdir(folder_path):
        # 拼接文件路径
        file_path = os.path.join(folder_path, filename)
        output_file_path = os.path.join(output_folder_path, filename)

        # 判断是否为文件
        if os.path.isfile(file_path):
            # 读取文件内容
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # 修改等号后面的值
            for i, line in enumerate(lines):
                if line.startswith(old_value):
                    parts = line.split("=")
                    if len(parts) > 1:
                        value = new_value  # 替换为你想要的新值
                        new_line = parts[0] + "=" + value + "\n"
                        lines[i] = new_line

            # 将修改后的内容写入新文件
            with open(output_file_path, 'w') as file:
                file.writelines(lines)

            print(f"文件 {filename} 修改并保存成功！")

    print("所有文件修改并保存完成！")


# 获取极化率
def get_polar(data):
    for i in range(len(data)):
        item = data[i]
        if 'Polar=' in item:
            value = [item[6:]]
            return value
    return ValueError('No Polar can get')


# 获取单个能量
def get_HF(data):
    for i in range(len(data)):
        item = data[i]
        if 'HF=' in item:
            return re.search(r'-?\d+\.\d+', item).group()
    return ValueError('No HF-energy can get')


def get_MP2(data):
    for i in range(len(data)):
        item = data[i]
        if 'MP2=' in item:
            return re.search(r'-?\d+\.\d+', item).group()
    return ValueError('No MP2-energy can get')


def get_MP4(data):
    for i in range(len(data)):
        item = data[i]
        if 'MP4SDQ=' in item:
            return re.search(r'-?\d+\.\d+', item).group()
    return ValueError('No MP4-energy can get')


def get_CCSD(data):
    for i in range(len(data)):
        item = data[i]
        if 'CCSD=' in item:
            return re.search(r'-?\d+\.\d+', item).group()
    return ValueError('No HF-energy can get')


def get_CCSD_T(data):
    for i in range(len(data)):
        item = data[i]
        if 'CCSD(T)=' in item:
            return re.search(r'-?\d+\.\d+', item).group()
    return ValueError('No CCSD(T)-energy can get')


def update_method(source_gjf, target_gjf, *, new_chk, old_method, new_method,
                  old_card, new_card):
    # 遍历文件夹文件
    for filename in os.listdir(source_gjf):
        # 拼接路径
        source_gjf_path = os.path.join(source_gjf, filename)

        # 读取文件
        with open(source_gjf_path, 'r') as source_file:
            lines = source_file.readlines()

        modified_lines = []

        # 遍历文本行
        for i, line in enumerate(lines):
            # 当遍历到%chk这一行时，更改
            if line.startswith("%chk="):
                modified_line = line.replace(old_method, new_method).replace(old_card, new_card)
                modified_lines.append(modified_line)
            # 当遍历到第4行，更改行
            elif line.startswith("#p"):
                modified_line = new_chk
                modified_lines.append(modified_line)
                modified_lines.append('\n')
            else:
                modified_lines.append(line)

        # 目标文件绝对路径
        target_gif_path = os.path.join(target_gjf, filename)

        # 将gjf文件写入新的文件夹
        with open(target_gif_path, 'w') as target_file:
            target_file.writelines(modified_lines)

    # 更改文件名
    update_filename(target_gjf, old_method, new_method)
    update_filename(target_gjf, old_card, new_card)


# 提取BSIE中的坐标生成gjf文件
def xyz_to_gjf(*, source_path, target_path, mem="128GB", nproc_shared="32",
               p="#p opt b3lyp/cc-pvtz\n", opt_str="b3lyp_pvtz"):
    for filename in os.listdir(source_path):
        # 拼接路径
        source_gjf_path = os.path.join(source_path, filename)

        atom_number, index, smile, xyz = xyz_file(source_gjf_path)

        # 构造文件名
        rename = index + "_" + atom_number + "_" + opt_str

        # 构造前4行
        modified_lines = []
        modified_lines.append("%nprocshared=" + nproc_shared + "\n")
        modified_lines.append("%mem=" + mem + "\n")
        modified_lines.append("%chk=" + rename + ".chk" + "\n")
        modified_lines.append(p)

        # 第五行 空行
        modified_lines.append("\n")
        # 第六行 描述
        modified_lines.append(f"Index: {index}, atom numbers: {atom_number}, smile: {smile}\n")
        # 第七行 换行
        modified_lines.append("\n")

        # 第八行 自旋多重度
        modified_lines.append("0 1" + "\n")

        # 第九行开始 重新编辑原子坐标
        result_lines = atoms_coordinate(modified_lines, xyz)

        # 在末尾添加空行
        result_lines.append("\n")
        result_lines.append("\n")

        # 保存文件
        save_gjf(target_path, rename, result_lines)


def save_gjf(target_path, rename, result_lines):
    rename = rename + ".gjf"
    # 最终文件路径
    target_file_path = os.path.join(target_path, rename)
    with open(target_file_path, "w") as file:
        for line in result_lines:
            file.write(line)


def atoms_coordinate(modified_lines, xyz):
    for i in range(len(xyz)):
        # 每行以五个空格分隔
        xyz_sp = xyz[i].split("\t  ")
        x = xyz_sp[1]
        y = xyz_sp[2]
        z = xyz_sp[3]
        # 第一个是原子
        modified_lines.append(f" {xyz_sp[0]}                 {x}   {y}   {z}")
    return modified_lines


def xyz_file(gjf_file):
    # 读取文件
    with open(gjf_file, 'r') as source_file:
        lines = source_file.readlines()

    # 原子数量
    atom_number = lines[0].replace("\n", "")
    # 第二行
    line2 = lines[1].split(" ")
    index = line2[1].replace(",", "")
    mol_index = line2[3].replace(",", "")
    g_index = line2[5].replace(",", "")
    smile = line2[7].replace("\"", "").replace("}", "").replace("\n", "")

    xyz = lines[2:]
    print(xyz)
    return atom_number, index, smile, xyz


# 分隔文件，每100个文件存储一个文件夹
def merge_files(*, source_path, target_path, merge_number=100):
    # 获取当前文件夹中的所有文件
    files = os.listdir(path=source_path)

    files = sorted(files, key=lambda x: x[0])

    # 定义每个文件夹中包含的文件数量
    files_per_folder = merge_number

    # 计算需要创建的文件夹数量
    num_folders = len(files) // files_per_folder + (1 if len(files) % files_per_folder != 0 else 0)

    # 创建文件夹并复制文件
    for i in range(num_folders):
        folder_name = f'folder_{i + 1}'  # 文件夹名称
        folder_path = os.path.join(target_path, folder_name)
        # print(folder_name)
        os.makedirs(folder_path, exist_ok=True)  # 创建文件夹，如果已存在则忽略
        # 复制文件到新创建的文件夹中
        for file in files[i * files_per_folder: (i + 1) * files_per_folder]:
            file_path = os.path.join(source_path, file)
            shutil.copy(file_path, folder_path)

# 提取单点能log的HOMO和LUMO
def get_HOMO_LUMO(*,source_path):

    df = pd.DataFrame()
    mol_name_list = []
    HOMO_list = []
    LUMO_list = []
    # 遍历文件夹文件
    for filename in os.listdir(source_path):
        # 获取体系名
        filenames = filename.split('_')
        mol_name = filenames[0]
        # 判断是否是开壳
        flag = is_openShell(mol_name)
        mol_name_list.append(mol_name)

        # 拼接路径
        source_log_path = os.path.join(source_path, filename)
        # 读取文件
        with open(source_log_path, 'r') as source_log:
            lines = source_log.readlines()

        # 如果是开壳体系，走Beta
        if flag == True:
            temp = 'Beta  occ.'
        else:
            temp = 'Alpha  occ.'

        for i in range(len(lines)):
            # 找到位置
            if temp in lines[i]:
                if temp in lines[i+1]:
                    continue
                split_content = lines[i].split(' ')
                HOMO = split_content[-1].replace('\n','')
                split_content2 = lines[i+1].split(' ')
                # 寻找LUMO
                LUMO = get_LUMO(split_content2)
                break
        HOMO_list.append(HOMO)
        LUMO_list.append(LUMO)
    df['mol'] = mol_name_list
    df['HOMO'] = HOMO_list
    df['LUMO'] = LUMO_list
    return df

# 寻找LUMO
def get_LUMO(split_list):
    for string in split_list:
        # 判断当前字符串是否包含数字
        if any(char.isdigit() for char in string):
            # 获取第一个包含数字的字符串在列表中的索引
            first_digit_index = split_list.index(string)
            # print("第一次出现数字的位置为：", first_digit_index)
            break  # 找到后退出循环
    else:
        # 如果列表中没有包含数字的字符串，则输出提示信息
        print("列表中没有包含数字的字符串")
    return split_list[first_digit_index]



# 判断是否是开壳
def is_openShell(mol_name):
    temp = Util_Tools.count_ele_one(mol_name)
    return True if temp%2 != 0 else False


# 提取轨道能量：Alpha occ. Alpha virt. Beta occ. Beta virt.
def get_orbital_energy(source_path):
    df = pd.DataFrame()
    Alpha_occ = []
    Alpha_virt = []
    Beta_occ = []
    Beta_virt = []
    mol_list = []
    # 遍历文件夹
    for filename in os.listdir(source_path):
        # 体系名称
        filenames = filename.split('_')
        mol_name = filenames[0]
        mol_list.append(mol_name)
        # 拼接路径
        source_log_path = os.path.join(source_path,filename)

        # 读取文件
        with open(source_log_path, 'r') as source_log:
            lines = source_log.readlines()

        Alpha_occ.append(get_single_orbit(lines,'Alpha  occ.'))
        Alpha_virt.append(get_single_orbit(lines,'Alpha virt.'))
        Beta_occ.append(get_single_orbit(lines,'Beta  occ.'))
        Beta_virt.append(get_single_orbit(lines,'Beta virt.'))

    df['mol'] = mol_list
    df['Alpha occ.'] = Alpha_occ
    df['Alpha virt.'] = Alpha_virt
    df['Beta occ.'] = Beta_occ
    df['Beta virt.'] = Beta_virt

    return df



def get_single_orbit(lines, temp):
    energy_list = []
    for i in range(len(lines)):
        if temp in lines[i]:
            split_content = lines[i].split(' ')
            for j in range(len(split_content)-1,-1,-1):
                string = split_content[j].replace('\n','')
                if is_number(string):
                    string_float = float(string)
                    energy_list.append(string_float)
    return np.sum(energy_list)

# 判断一个字符串是不是数字
def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False


