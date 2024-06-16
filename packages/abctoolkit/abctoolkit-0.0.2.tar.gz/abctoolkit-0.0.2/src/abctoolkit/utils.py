import os
import re
import jellyfish
from unidecode import unidecode
from rapidfuzz import fuzz


Barlines = ["|:", "::", ":|", "[|", "||", "|]", "|", "|]:", ":[|"]
Barline_regexPattern = '(' + '|'.join(map(re.escape, Barlines)) + ')'

Exclaim_re = r'![^!]+!'
Quote_re = r'"[^"]*"'
SquareBracket_re = r'\[[^\]]+\]'
Brace_re = r'\{[^}]+\}'


def find_all_abc(directory):
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            if file_path.endswith('.abc') or file_path.endswith('txt'):
                yield file_path


def extract_metadata_and_tunebody(abc_lines: list):
    # 分割为 metadata 和 tunebody
    tunebody_index = None
    for i, line in enumerate(reversed(abc_lines)):
        if line.strip() == 'V:1':
            tunebody_index = len(abc_lines) - 1 - i
            break
    if tunebody_index is None:
        raise Exception('tunebody index not found.')

    metadata_lines = abc_lines[:tunebody_index]
    tunebody_lines = abc_lines[tunebody_index:]

    return metadata_lines, tunebody_lines


def extract_metadata_and_tunebody_rotated(abc_lines: list):
    # 分割为 metadata 和 tunebody（rotate过后的版本）
    tunebody_index = None
    for i, line in enumerate(abc_lines):
        if line.startswith('[V:1]'):
            tunebody_index = i
            break

    metadata_lines = abc_lines[:tunebody_index]
    tunebody_lines = abc_lines[tunebody_index:]

    return metadata_lines, tunebody_lines


def extract_metadata_and_parts(abc_lines: list):

    metadata_lines, tunebody_lines = extract_metadata_and_tunebody(abc_lines)

    part_symbol_list = []
    part_text_list = []

    last_start_index = None
    for i, line in enumerate(tunebody_lines):
        if i == 0:
            last_start_index = 1
            part_symbol_list.append(line.strip())
            continue
        if line.startswith('V:'):
            last_end_index = i
            part_text_list.append(''.join(tunebody_lines[last_start_index:last_end_index]))
            part_symbol_list.append(line.strip())
            last_start_index = i + 1
    part_text_list.append(''.join(tunebody_lines[last_start_index:]))

    part_text_dict = {}
    for i in range(len(part_symbol_list)):
        part_text_dict[part_symbol_list[i]] = part_text_list[i]

    return metadata_lines, part_text_dict


def extract_barline_and_bartext_dict(abc_lines: list):
    '''
    提取 metadatalines，以及各个声部的 part_text, prefix, left_barline, bar_text, right_barline
    '''
    metadata_lines, part_text_dict = extract_metadata_and_parts(abc_lines)

    prefix_dict = {key: '' for key in part_text_dict.keys()}
    left_barline_dict = {key: [] for key in part_text_dict.keys()}
    right_barline_dict = {key: [] for key in part_text_dict.keys()}
    bar_text_dict = {key: [] for key in part_text_dict.keys()}

    for symbol, voice_text in part_text_dict.items():
        prefix, left_barlines, bar_texts, right_barlines = split_into_bars_and_barlines(voice_text)
        prefix_dict[symbol] = prefix
        left_barline_dict[symbol] = left_barlines
        right_barline_dict[symbol] = right_barlines
        bar_text_dict[symbol] = bar_texts

    return metadata_lines, prefix_dict, left_barline_dict, bar_text_dict, right_barline_dict


def extract_barline_and_bartext_dict_rotated(abc_lines: list):
    '''
    提取 metadatalines，以及各个声部的 part_text, prefix, left_barline, bar_text, right_barline (rotated版)
    '''

    metadata_lines, tunebody_lines = extract_metadata_and_tunebody(abc_lines)

    part_symbol_list = []
    for line in metadata_lines:
        if line.startswith('V:'):
            part_symbol_list.append(line.split()[0])
    part_symbol_list = sorted(part_symbol_list)

    prefix_dict = {key: '' for key in part_symbol_list}
    left_barline_dict = {key: [] for key in part_symbol_list}
    right_barline_dict = {key: [] for key in part_symbol_list}
    bar_text_dict = {key: [] for key in part_symbol_list}

    for i, line in enumerate(tunebody_lines):

        for j, symbol in enumerate(part_symbol_list):

            start_sign = '[' + part_symbol_list[j] + ']'
            start_index = line.index(start_sign) + len(start_sign)
            if j < len(part_symbol_list) - 1:
                end_sign = '[' + part_symbol_list[j+1] + ']'
                end_index = line.index(end_sign)
                bar_patch = line[start_index : end_index]
            else:
                bar_patch = line[start_index : ]

            bar_eles = re.split(Barline_regexPattern, bar_patch)
            bar_eles[-2] = bar_eles[-2] + bar_eles[-1]  # 必为 right_barline
            bar_eles = bar_eles[:-1]

            if i == 0:  # 第一行，需要单独考虑 prefix 和 left_barline
                if len(bar_eles) == 4:  # 有prefix（可能为空）和left_barline
                    prefix_dict[symbol] = bar_eles[0]
                    # 处理 left_barline
                    if re.match(r'\d', bar_eles[2]) or bar_eles[2][0] == ':':
                        k = 0
                        for k in range(len(bar_eles[2])):
                            if not bar_eles[2][k] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', '-', ':']:
                                break
                        affix = bar_eles[2][:k]
                        bar_eles[2] = bar_eles[2][k:].strip()
                        bar_eles[1] = bar_eles[1] + affix
                    left_barline_dict[symbol].append = bar_eles[1]
                elif len(bar_eles) == 3:    # 无 prefix 和 left_barline
                    left_barline_dict[symbol].append('')
                else:
                    raise Exception('这什么情况我真没见过')
            else:
                left_barline_dict[symbol].append(right_barline_dict[symbol][-1])    # 上一小节的右小节线

            bar_text_dict[symbol].append(bar_eles[-2])
            right_barline_dict[symbol].append(bar_eles[-1])

    return metadata_lines, prefix_dict, left_barline_dict, bar_text_dict, right_barline_dict


def extract_global_and_local_metadtata(metadata_lines: list):
    '''
    提取 global metadata 和各声部的 local_metadata
    '''
    for i, line in enumerate(metadata_lines):
        if line.startswith('V:'):
            global_metadata_index = i

    global_metadata_lines = metadata_lines[ : global_metadata_index]
    local_metadata_lines = metadata_lines[global_metadata_index : ]

    global_metadata_dict = {}
    for i, line in enumerate(global_metadata_lines):
        if line.startswith('%%'):
            key = line.split()[0]
            value = line.lstrip(key).strip()
            global_metadata_dict[key] = value
        elif line[0].isalpha and line[1] == ':':
            key = line[0]
            value = line[2:].strip()
            global_metadata_dict[key] = value

    local_metadata_dict = {}
    for i, line in enumerate(local_metadata_lines):
        symbol = None
        if line.startswith('V:'):
            symbol = line.split()[0]
            local_metadata_dict[symbol] = {}
            key = 'V'
            value = line.lstrip(symbol).strip()
            local_metadata_dict[symbol][key] = value
        elif line[0].isalpha and line[1] == ':':
            key = line[0]
            value = line[2:].strip()
            local_metadata_dict[symbol][key] = value

    return global_metadata_dict, local_metadata_dict


def extract_a_part(abc_lines: list, part: str):
    '''
    在多轨abc中提取某一个声部，结合 global 和 local metadata，生成一条完整的单轨的abc
    '''
    pass


def remove_information_field(abc_lines: list, info_fields: list):
    # info_fields: ['X:', 'T:', 'C:', '%%MIDI', ...]
    filtered_abc_lines = []
    for line in abc_lines:
        save_flag = True
        for symbol in info_fields:
            if line.startswith(symbol):
                save_flag = False
        if save_flag:
            filtered_abc_lines.append(line)

    return filtered_abc_lines


def remove_bar_no_annotations(abc_lines: list):
    # 去掉行末的小节号

    metadata_lines, tunebody_lines = extract_metadata_and_tunebody(abc_lines)

    for i, line in enumerate(tunebody_lines):
        tunebody_lines[i] = re.sub(r'%\d+$', '', line)
    abc_lines = metadata_lines + tunebody_lines

    return abc_lines


def remove_wrapped_content(abc_text: str, wrap_symbols: list):
    '''
    注意！本函数非常粗放：[]会移除多音和弦，""会移除和弦记号，请谨慎使用
    '''

    if r'""' in wrap_symbols:
        abc_text = re.sub(Quote_re, '', abc_text)
    if r"!!" in wrap_symbols:
        abc_text = re.sub(Exclaim_re, '', abc_text)
    if r"[]" in wrap_symbols:
        abc_text = re.sub(SquareBracket_re, '', abc_text)
    if r"{}" in wrap_symbols:
        abc_text = re.sub(Brace_re, '', abc_text)

    return abc_text


def remove_square_bracket_information_field(abc_text: str):
    # 去掉[]包裹的 information field，如[K:][M:]
    square_bracket_matches = re.findall(SquareBracket_re, abc_text)
    for match in square_bracket_matches:
        if match[1].isalpha() and match[2] == ':':
            abc_text = abc_text.replace(match, '')

    return abc_text


def remove_quote_text_annotations(abc_text: str):
    # 移除""包裹的 text annotation，不移除和弦记号
    quote_matches = re.findall(Quote_re, abc_text)
    for match in quote_matches:
        if match[1] in ['^', '_', '<', '>', '@']:
            abc_text = abc_text.replace(match, '')

    return abc_text


def split_into_bars(abc_text: str):
    '''
    Split a voice text into bars (with barline on right side)
    '''

    bars = re.split(Barline_regexPattern, abc_text.strip())
    bars = [bar for bar in bars if bar.strip() != ''] # remove empty strings
    bars = [bars[0]] + [bars[i] for i in range(1, len(bars)) if bars[i] != bars[i-1]] # 防止出现连续小节线的情况

    if bars[0] in Barlines:
        bars[1] = bars[0] + bars[1]
        bars = bars[1:]
    elif remove_square_bracket_information_field(bars[0]).strip() == '':   # 如果开头是纯[information field]
        bars[2] = bars[0] + bars[1] + bars[2]

    bars = [bars[i * 2] + bars[i * 2 + 1] for i in range(len(bars) // 2)]

    for j in range(len(bars)):
        bars[j] = bars[j].strip().replace('\n', '')        # strip，去掉\n
        # 如果以数字或冒号开头，则提取数字之后的字符串，直到非数字/,/./-出现，把它加到上一个patch末尾
        if re.match(r'\d', bars[j]) or bars[j][0] == ':':
            k = 0
            for k in range(len(bars[j])):
                if not bars[j][k] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', '-', ':']:
                    break
            affix = bars[j][:k]
            bars[j] = bars[j][k:].strip()
            bars[j - 1] = bars[j - 1] + affix

    return bars


def split_into_bars_and_barlines(abc_text: str):
    '''
    Split a voice text into bars / left_barlines / right_barlines
    '''

    bars = re.split(Barline_regexPattern, abc_text.strip())
    bars = [bar for bar in bars if bar.strip() != ''] # remove empty strings
    bars = [bars[0]] + [bars[i] for i in range(1, len(bars)) if bars[i] != bars[i - 1]]  # 防止出现连续小节线的情况

    prefix = '' # 前缀，用来容纳最开头的[K:]这种
    if bars[0] in Barlines:
        bar_content_start_id = 1
    elif remove_square_bracket_information_field(bars[0]).strip() == '':
        bar_content_start_id = 2
        prefix = bars[0].strip()
    else:
        bar_content_start_id = 0

    j = bar_content_start_id
    while j < len(bars):
        bars[j] = bars[j].strip().replace('\n', '')        # strip，去掉\n
        # 如果以数字或冒号开头，则提取数字之后的字符串，直到非数字/,/./-出现，把它加到上一个小节线的末尾
        if re.match(r'\d', bars[j]) or bars[j][0] == ':':
            k = 0
            for k in range(len(bars[j])):
                if not bars[j][k] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '.', '-', ':']:
                    break
            affix = bars[j][:k]
            bars[j] = bars[j][k:].strip()
            bars[j - 1] = bars[j - 1] + affix
        j += 2

    if bars[0] in Barlines:
        left_barlines  = [bars[i * 2] for i in range(len(bars) // 2)]
        bar_texts      = [bars[i * 2 + 1] for i in range(len(bars) // 2)]
        right_barlines = [bars[i * 2 + 2] for i in range(len(bars) // 2)]
    elif prefix == '':
        left_barlines  = [''] + [bars[i * 2 + 1] for i in range(len(bars) // 2 - 1)]
        bar_texts      = [bars[i * 2] for i in range(len(bars) // 2)]
        right_barlines = [bars[i * 2 + 1] for i in range(len(bars) // 2)]
    else:
        left_barlines  = [bars[i * 2 + 1] for i in range(len(bars) // 2 - 1)]
        bar_texts      = [bars[i * 2 + 2] for i in range(len(bars) // 2 - 1)]
        right_barlines = [bars[i * 2 + 3] for i in range(len(bars) // 2 - 1)]

    if not (len(left_barlines) == len(bar_texts) == len(right_barlines)):
        raise Exception('Unequal bar elements')

    return prefix, left_barlines, bar_texts, right_barlines


def strip_empty_bars(abc_lines: list):
    '''
    Strip empty bars in an abc piece. Retain the first left barline and the last right barline.
    '''

    metadata_lines, prefix_dict, left_barline_dict, bar_text_dict, right_barline_dict = \
        extract_barline_and_bartext_dict(abc_lines)

    # 这里小小检查一下各声部小节线和小节长度是否相等。
    # 小节线不相等问题不大，只是提示一下
    # 小节长度不相等则返回None
    barline_equal_flag = True
    bar_no_equal_flag = True
    for symbol in prefix_dict.keys():
        if left_barline_dict[symbol] != left_barline_dict['V:1']:
            barline_equal_flag = False
        if right_barline_dict[symbol] != right_barline_dict['V:1']:
            barline_equal_flag = False
        if len(bar_text_dict[symbol]) != len(bar_text_dict['V:1']):
            bar_no_equal_flag = False
    if not barline_equal_flag:
        print('Unequal barlines.')
    if not bar_no_equal_flag:
        print('Unequal bar numbers.')
        return None, None

    # 寻找各个声部非空bar index范围，然后得到一个并集
    left_valid_index_4all = len(bar_text_dict['V:1'])
    right_valid_index_4all = -1

    for symbol in bar_text_dict.keys():
        left_valid_index, right_valid_index = find_valid_bar_index(bar_text_dict[symbol])
        if left_valid_index < left_valid_index_4all:
            left_valid_index_4all = left_valid_index
        if right_valid_index > right_valid_index_4all:
            right_valid_index_4all = right_valid_index

    if left_valid_index_4all >= right_valid_index_4all:
        print('Empty piece.')
        return None, None

    stripped_left_barline_dict = {key: [] for key in prefix_dict.keys()}
    stripped_right_barline_dict = {key: [] for key in prefix_dict.keys()}
    stripped_bar_text_dict = {key: [] for key in prefix_dict.keys()}

    for symbol in prefix_dict.keys():
        stripped_left_barline_dict[symbol] = [left_barline_dict[symbol][0]] + \
                                             left_barline_dict[symbol][left_valid_index_4all + 1 : right_valid_index_4all]
        stripped_right_barline_dict[symbol] = right_barline_dict[symbol][left_valid_index_4all : right_valid_index_4all - 1] + \
                                              [right_barline_dict[symbol][-1]]
        stripped_bar_text_dict[symbol] = bar_text_dict[symbol][left_valid_index_4all : right_valid_index_4all]

    # 重新组装，每列不要超过100字符
    stripped_abc_lines = metadata_lines
    for symbol in prefix_dict.keys():
        stripped_abc_lines.append(symbol + '\n')
        bar_index = 0
        line_len = 0
        line = prefix_dict[symbol] + stripped_left_barline_dict[symbol][0] + ' '
        while bar_index < len(stripped_bar_text_dict[symbol]):
            bar = stripped_bar_text_dict[symbol][bar_index] + ' ' + \
                  stripped_right_barline_dict[symbol][bar_index] + ' '
            if line_len == 0 or line_len + len(bar) <= 100:
                line += bar
                line_len += len(bar)
                bar_index += 1
            else:
                line += '\n'
                stripped_abc_lines.append(line)
                line = ' '
                line_len = 0
        if line.strip() != '':
            line += '\n'
            stripped_abc_lines.append(line)

    return stripped_abc_lines, right_valid_index_4all - left_valid_index_4all


def find_valid_bar_index(bar_text_list: list):

    left_valid_index = -1
    right_valid_index = len(bar_text_list)

    left_valid_flag = False
    while not left_valid_flag:
        left_valid_index += 1
        if left_valid_index >= len(bar_text_list):
            break
        bar_text = bar_text_list[left_valid_index]
        bar_text = remove_wrapped_content(abc_text=bar_text, wrap_symbols=['!!'])
        # bar_text = remove_square_bracket_information_field(bar_text)  # 这里做一下区别对待：左侧如有[]，则视为有效小节，因为可能对后续小节有影响
        bar_text = remove_quote_text_annotations(bar_text)
        for char in bar_text:
            if char.isalpha() and not char in ['Z', 'z', 'X', 'x']:
                left_valid_flag = True
                break

    right_valid_flag = False
    while not right_valid_flag:
        right_valid_index -= 1
        if right_valid_index < 0:
            break
        bar_text = bar_text_list[right_valid_index]
        bar_text = remove_wrapped_content(abc_text=bar_text, wrap_symbols=['!!'])
        bar_text = remove_square_bracket_information_field(bar_text)    # 右侧要滤掉[]，因为如果后面都是休止符，也没什么意思
        bar_text = remove_quote_text_annotations(bar_text)
        for char in bar_text:
            if re.match(r'^[A-Ga-g]$', char):
                right_valid_flag = True
                break

    return left_valid_index, right_valid_index + 1


def ld_sim(str_a: str, str_b: str):
    ld = jellyfish.levenshtein_distance(str_a, str_b)
    sim = 1 - ld / (max(len(str_a), len(str_b)))
    return sim


def fast_ld_sim(str_a: str, str_b: str):
    return fuzz.ratio(str_a, str_b) / 100




def add_control_codes(abc):
    meta_data, merged_body_data = split_abc_original(abc)
    control_codes, abc = add_tokens(meta_data, merged_body_data)

    return control_codes, abc


def extract_notes(input_string):
    # Regular expression pattern for single notes, rests, and decorated notes
    note_pattern = r"(x[0-9]*/*[0-9]*|z[0-9]*/*[0-9]*|[\^_=]*[A-G][,']*[0-9]*/*[0-9]*\.*|[\^_=]*[a-g][']*/*[0-9]*/*[0-9]*\.*)"
    
    # Regular expression pattern for chord notes
    chord_note_pattern = r"(?<!:)\[[^\]]*\]"
    
    # Regular expression pattern for headers
    header_pattern = r"\[[A-Za-z]:[^\]]*\]"
    
    # Regular expression pattern for decorations
    decoration_pattern = r"!.*?!"
    
    # Regular expression pattern for quoted content
    quoted_pattern = r"\".*?\""

    # Remove quoted content from input
    input_string = re.sub(quoted_pattern, '', input_string)
    
    # Remove decoration information from input
    input_string = re.sub(decoration_pattern, '', input_string)
    
    # Remove header information from input
    input_string = re.sub(header_pattern, '', input_string)
    
    # Extract notes, rests, and decorated notes using regex
    note_matches = re.findall(note_pattern, input_string)
    
    # Extract chord notes using regex
    chord_notes = re.findall(chord_note_pattern, input_string)
    
    # Combine single notes, rests, decorated notes, and chord notes
    notes = [note for note in note_matches if note.strip() != '']
    
    notes = notes + chord_notes

    return notes


def num_alph(line):
    num_flag = False
    alpha_flag = False
    valid_flag = False

    for char in line:
        if char.isnumeric() and alpha_flag==False and valid_flag==False:
            return True
        elif char.isalpha() and num_flag==False:
            return False
        elif char=='(' or char=='\"' or char=='!':
            valid_flag = True


def split_abc_original(abc):
    lines = re.split('(\n)', abc)
    lines = [lines[i * 2] + lines[i * 2 + 1] for i in range(int(len(lines) / 2))]
    meta_flag = False
    meta_idx = 0

    for line in lines:
        if len(line) > 1 and line[0].isalpha() and line[1] == ':':
            meta_idx += 1
            meta_flag = True
        else:
            if meta_flag:
                break
            else:
                meta_idx += 1

    meta_data = ''.join(lines[:meta_idx])
    body_data = abc[len(meta_data):]

    delimiters = ":|", "||", "|]", "::", "|:", "[|"
    regexPattern = '(' + '|'.join(map(re.escape, delimiters)) + ')'
    body_data = re.split(regexPattern, body_data)
    body_data = list(filter(lambda a: a != '', body_data))
    if len(body_data) == 1:
        body_data = [abc[len(meta_data):][::-1].replace('|', ']|', 1)[::-1]]
    else:
        if body_data[0] in delimiters:
            body_data[1] = body_data[0] + body_data[1]
            body_data = body_data[1:]
        body_data = [body_data[i * 2] + body_data[i * 2 + 1] for i in range(int(len(body_data) / 2))]

    merged_body_data = []

    for line in body_data:
        if num_alph(line):
            try:
                merged_body_data[-1] += line
            except:
                return None, None
        else:
            merged_body_data.append(line)

    return meta_data, merged_body_data


def run_strip(line, delimiters):
    for delimiter in delimiters:
        line = line.strip(delimiter)
        line = line.replace(delimiter, '|')
    return line

def add_tokens(meta_data, merged_body_data):
    if merged_body_data==None:
        return "", ""
    delimiters = ":|", "||", "|]", "::", "|:", "[|"
    sec = len(merged_body_data)
    bars = []
    sims = []

    for line in merged_body_data:
        line = run_strip(line, delimiters)
        bars.append(line.count('|')+1)

    for anchor_idx in range(1, len(merged_body_data)):
        sim = []
        for compar_idx in range(anchor_idx):
            sim.append(ld_sim(merged_body_data[anchor_idx], merged_body_data[compar_idx]))
        sims.append(sim)

    header = "S:" + str(sec) + "\n"
    for i in range(len(bars)):
        if i > 0:
            for j in range(len(sims[i-1])):
                header += "E:" + str(round(sims[i-1][j] * 10)) + "\n"
        header += "B:" + str(bars[i]) + "\n"
    return unidecode(header), unidecode(meta_data + ''.join(merged_body_data))



if __name__ == '__main__':
    bar_eles = re.split(Barline_regexPattern, "[K:C]||abc||1")
    print(bar_eles)

    bar_eles = re.split(Barline_regexPattern, "abc||:")
    print(bar_eles)



