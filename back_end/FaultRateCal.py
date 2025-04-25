import json
import re
import json
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce

from utils import get_file_encoding

from lxml import etree
import warnings

warnings.filterwarnings('ignore')

class FaultRateCal:
    def __init__(self, rps_path, weight=(5, 3, 2)):
        self.out = {}
        self.filelist = []
        self.function_fault_list = []
        self.function_fault_rate = 0
        self.file_fault_rate = 0
        self.fault_density = 0
        self.fault_num_per_KLOC = 0
        self.weight = weight
        # ((FAIL|PASS|Conditional Pass), function, file, UNIQUE VIOLATIONS )
        self.procedure_result = []
        self.comments = 0
        self.LOC = 0
        self.unCalledProcedure = 0
        self.procedure = 0
        # ( VIOLATIONS,  LDRA , CODE    , "*",  (M|O|C) , GJB CODE)
        self.o = []
        self.c = []
        self.m = []
        self.readFile(rps_path)
        self.faultNumPerKLOC()
        self.faultDensity()
        self.fileFaultRate()
        self.functionFaultRate()
        self.output()

    def readFile(self, path):
        encoding = get_file_encoding(path)
        with open(path, encoding=encoding) as r:
            contents = r.readlines()
        i = 0
        # ( VIOLATIONS,  LDRA , CODE    , "*",  (M) MANDATORY STANDARDS , GJB CODE)
        while i < len(contents):
            if contents[
                i].strip() == "VIOLATIONS    LDRA CODE        (M) MANDATORY STANDARDS                           GJB CODE":
                i += 2
                match1 = re.match("\s*(\d+|-)\s+(\d+)\s+([SDQ])\s+(\*?)\s(\S+)\s+(GJB.*)", contents[i])
                while match1 is not None:
                    self.m.append((match1.group(1), match1.group(2), match1.group(3), match1.group(4), match1.group(5),
                                   match1.group(6)))
                    i += 1
                    match1 = re.match("\s*(\d+|-)\s+(\d+)\s+([SDQ])\s+(\*?)\s(\S+)\s+(GJB.*)", contents[i])
            if contents[
                i].strip() == "VIOLATIONS    LDRA CODE        (C) CHECKING (MANDATORY) STANDARDS                GJB CODE":
                i += 2
                match2 = re.match("\s*(\d+|-)\s+(\d+)\s+([SDQ])\s+(\*?)\s(\S+)\s+(GJB.*)", contents[i])
                while match2 is not None:
                    self.c.append((match2.group(1), match2.group(2), match2.group(3), match2.group(4), match2.group(5),
                                   match2.group(6)))
                    i += 1
                    match2 = re.match("\s*(\d+|-)\s+(\d+)\s+([SDQ])\s+(\*?)\s(\S+)\s+(GJB.*)", contents[i])
            if contents[
                i].strip() == "VIOLATIONS    LDRA CODE        (O) OPTIONAL STANDARDS                            GJB CODE":
                i += 2
                match3 = re.match("\s*(\d+|-)\s+(\d+)\s+([SDQ])\s+(\*?)\s(\S+)\s+(GJB.*)", contents[i])
                while match3 is not None:
                    self.o.append((match3.group(1), match3.group(2), match3.group(3), match3.group(4), match3.group(5),
                                   match3.group(6)))
                    i += 1
                    match3 = re.match("\s*(\d+|-)\s+(\d+)\s+([SDQ])\s+(\*?)\s(\S+)\s+(GJB.*)", contents[i])
            if contents[i].strip() == "Global Basic Information":
                i += 2
                self.procedure = int(re.findall("\d+", contents[i])[0])
                i += 1
                self.unCalledProcedure = int(re.findall("\d+", contents[i])[0])
                i += 1
                self.LOC = int(re.findall("\d+", contents[i])[0])
                i += 1
                self.comments = int(re.findall("\d+", contents[i])[0])
            if contents[i].strip() == "Procedure Results":
                i += 5
                match4 = re.match("(FAIL|Conditional Pass|PASS)\s+(Global Program)", contents[i].strip())
                if match4 is not None:
                    self.procedure_result.append((match4[1], match4[2]))
                i += 1
                while True:
                    if len(contents[i].strip()) == 0:
                        break
                    line = contents[i]
                    if len(contents[i].strip()) != 66:
                        i += 1
                        line += contents[i]
                    match4 = re.match("(FAIL|Conditional Pass|PASS)\s+(\S+)\s+(.+)\s+(\d)\s+#", line.strip())
                    if match4 is not None:
                        self.procedure_result.append((match4[1], match4[2], match4[3].strip(), match4[4]))

                    i += 1
            if contents[i].strip() == "Source Files in Group":
                self.filelist = []
                i += 5
                while True:
                    if len(contents[i].strip()) == 0:
                        break
                    match5 = re.match("(\S+)\s+.*", contents[i].strip())
                    if match5 is not None:
                        self.filelist.append(match5.group(1))
                    i += 1
            if contents[i].strip() == "Standards Violation Summary - All files":
                self.file_fault_list = []
                i += 5
                while True:
                    line = contents[i].strip()
                    nextline = contents[i + 1]
                    if len(nextline.strip()) < 20 and len(nextline.strip()) > 0:
                        line += nextline
                        i += 2
                    else:
                        i += 1
                    if len(line) == 0:
                        break
                    match6 = re.match("(M|O|C)\s+(\S+):\s+(\d+)(.*)\s+(GJB.*)", line)
                    if match6 != None:
                        self.file_fault_list.append(
                            (match6[1], match6[2], match6[3], match6[4].strip(), match6[5].strip()))
            if contents[i].strip().strip("*").strip().startswith("("):
                line = contents[i - 1].strip().strip("*") + contents[i].strip().strip("*") + contents[
                    i + 1].strip().strip("*")
                match7 = re.match("(\S+)\s+\(+(\d+)\s+to\s+(\d+)\s+(\S+)\)\s+(\S+)", line.strip())
                if match7 is not None:
                    while contents[
                            i].strip() != "CODE   LINE      VIOLATION                                         STANDARD":
                        i += 1
                    i += 2
                    while True:
                        line = contents[i].strip()
                        nextline = contents[i + 1]
                        if len(nextline.strip()) < 20 and len(nextline.strip()) > 0:
                            line += nextline
                            i += 2
                        else:
                            i += 1
                        if len(line) == 0:
                            break
                        match8 = re.match("(M|O|C)\s+(\d+)\s+(.*)\s+(GJB.*)", line)
                        if match8 != None:
                            self.function_fault_list.append((match7[4], match7[1], match7[3], match7[2], match8[1],
                                                             match8[2], match8[3].strip(), match8[4]))
            i += 1

    def faultNumPerKLOC(self):
        a = 0
        b = 0
        c = 0
        for item in self.m:
            if item[0] != '-':
                a += int(item[0])
        for item in self.o:
            if item[0] != '-':
                b += int(item[0])
        for item in self.c:
            if item[0] != '-':
                c += int(item[0])
        self.m_num = a
        self.o_num = b
        self.c_num = c
        # LOC = 0
        # for key in self.project_dict["codeFileInfo"].keys():
        #     if "codeInfo" in self.project_dict["codeFileInfo"][key].keys():
        #         LOC += self.project_dict["codeFileInfo"][key]["codeInfo"]["codeLine"]
        self.fault_num_per_KLOC = (a + b + c) / self.LOC * 1000

    def faultDensity(self):
        count = 0
        for item in self.m:
            if item[0] != '-':
                count += int(item[0]) * self.weight[0]
        for item in self.c:
            if item[0] != '-':
                count += int(item[0]) * self.weight[1]
        for item in self.o:
            if item[0] != '-':
                count += int(item[0]) * self.weight[2]
        # LOC = 0
        # for key in self.project_dict["codeFileInfo"].keys():
        #     if "codeInfo" in self.project_dict["codeFileInfo"][key].keys():
        #         LOC += self.project_dict["codeFileInfo"][key]["codeInfo"]["codeLine"]
        self.fault_density = count / self.LOC * 1000

    def fileFaultRate(self):
        files = set()
        files_m = set()
        files_o = set()
        files_c = set()
        for item in self.function_fault_list:
            if item[4] == "M":
                files_m.add(item[0])
            if item[4] == "O":
                files_o.add(item[0])
            if item[4] == "C":
                files_c.add(item[0])
            files.add(item[0])
        for item in self.file_fault_list:
            if item[0] == "M":
                files_m.add(item[1])
            if item[0] == "O":
                files_o.add(item[1])
            if item[0] == "C":
                files_c.add(item[1])
            files.add(item[1])
        self.file_fault_rate = len(files) / len(self.filelist)
        self.file_fault_rate_m = len(files_m) / len(self.filelist)
        self.file_fault_rate_o = len(files_o) / len(self.filelist)
        self.file_fault_rate_c = len(files_c) / len(self.filelist)

    def functionFaultRate(self):
        funcs = set()
        funcs_m = set()
        funcs_o = set()
        funcs_c = set()
        for item in self.function_fault_list:
            if item[4] == "M":
                funcs_m.add(item[0] + "." + item[1])
            if item[4] == "O":
                funcs_o.add(item[0] + "." + item[1])
            if item[4] == "C":
                funcs_c.add(item[0] + "." + item[1])
            funcs.add(item[0] + "." + item[1])
        self.function_fault_rate = len(funcs) / self.procedure
        self.function_fault_rate_m = len(funcs_m) / self.procedure
        self.function_fault_rate_o = len(funcs_o) / self.procedure
        self.function_fault_rate_c = len(funcs_c) / self.procedure

    def output(self):
        self.out["overviewData"] = {
            "thousand_defect_num": str(round(self.fault_num_per_KLOC, 2)) + "/KLOC",
            "defect_concentration": str(round(self.fault_density, 2)) + "/KLOC",
            "file_defect_rate": str(round(self.file_fault_rate, 4) * 100) + "%",
            "function_defect_rate": str(round(self.function_fault_rate, 4) * 100) + "%"
        }
        self.out["detectTypeData"] = {
            "forced_defect": {
                "total_defect_num": self.m_num,
                "defect_proportion": str(round(100 * self.m_num / (self.m_num + self.c_num + self.o_num), 2)) + "%",
                "thousand_defect_num": str(round(1000 * self.m_num / self.LOC, 2)) + "/KLOC",
                "defect_concentration": str(self.weight[0] * round(1000 * self.m_num / self.LOC, 2)) + "/KLOC",
                "file_defect_rate": str(round(self.file_fault_rate_m, 4) * 100) + "%",
                "function_defect_rate": str(round(self.function_fault_rate_m, 4) * 100) + "%"
            },
            "optional_defect": {
                "total_defect_num": self.o_num,
                "defect_proportion": str(round(100 * self.o_num / (self.m_num + self.c_num + self.o_num), 2)) + "%",
                "thousand_defect_num": str(round(1000 * self.o_num / self.LOC, 2)) + "/KLOC",
                "defect_concentration": str(self.weight[2] * round(1000 * self.o_num / self.LOC, 2)) + "/KLOC",
                "file_defect_rate": str(round(self.file_fault_rate_o, 4) * 100) + "%",
                "function_defect_rate": str(round(self.function_fault_rate_o, 4) * 100) + "%"
            },
            "suggested_defect": {
                "total_defect_num": self.c_num,
                "defect_proportion": str(round(100 * self.c_num / (self.m_num + self.c_num + self.o_num), 2)) + "%",
                "thousand_defect_num": str(round(1000 * self.c_num / self.LOC, 2)) + "/KLOC",
                "defect_concentration": str(self.weight[1] * round(1000 * self.c_num / self.LOC, 2)) + "/KLOC",
                "file_defect_rate": str(round(self.file_fault_rate_c, 4) * 100) + "%",
                "function_defect_rate": str(round(self.function_fault_rate_c, 4) * 100) + "%"
            }
        }
        self.out["optionalTable"] = []
        for item in self.o:
            self.out["optionalTable"].append({
                "standard": item[4],
                "source": item[5],
                "num": int(item[0]) if item[0] != "-" else 0
            })
        self.out["forcedTable"] = []
        for item in self.m:
            self.out["forcedTable"].append({
                "standard": item[4],
                "source": item[5],
                "num": int(item[0]) if item[0] != "-" else 0
            })
        self.out["suggestedTable"] = []
        for item in self.c:
            self.out["suggestedTable"].append({
                "standard": item[4],
                "source": item[5],
                "num": int(item[0]) if item[0] != "-" else 0
            })


def read_html_to_json(src_url=''):
    url = src_url

    with open(url, 'r') as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, 'html.parser')

    div_elements = soup.find_all(name='div', attrs={'class': 'stitle'})
    data_dict = {}
    for div_element in div_elements:
        data_dict[div_element.text] = []
        # print(div_element.text)
        table_elements_div = div_element.find_parent('div')
        table_elements = table_elements_div.find_all('table')
        for table_element in table_elements:

            for row in table_element.find_all('tr'):
                tmp_list = []
                # head = row.find_all("th")
                # if len(head) != 0:
                #     for i in head:
                #         tmp_list.append(i.text)
                #     data_dict[div_element.text].append(tmp_list)
                #     continue
                cells = row.find_all('td')
                if len(cells) == 0:
                    continue
                for i in cells:
                    tmp_list.append(i.text)
                data_dict[div_element.text].append(tmp_list)

    return data_dict

def get_fault_dict(html_url,rcf_url):
    out = {}
    data = read_html_to_json(html_url)
    compliance_summary = pd.DataFrame({"num": pd.Series(data=[d[1] for d in data["Compliance Summary"]],
                                                        index=[d[0] for d in data["Compliance Summary"]])})
    tree = etree.parse(rcf_url)
    rule_summary = pd.DataFrame({
        "Rule": pd.Series([d[0] for d in data["Rule Summary"]]),
        "Category": pd.Series([d[1] for d in data["Rule Summary"]]),
        "Violation": pd.Series([int(d[2]) for d in data["Rule Summary"]]),
        "Deviations": pd.Series([d[3] for d in data["Rule Summary"]]),
        "Disapplied": pd.Series([d[4] for d in data["Rule Summary"]]),
        "Standard": pd.Series([tree.xpath('//rule[@id="'+d[0]+'"]/text')[0].text for d in data["Rule Summary"] ]),
        "Compliance Level": pd.Series([d[5] for d in data["Rule Summary"]])
    })
    for i in range(len(data["File Summary"])):
        if data["File Summary"][i][0] == "":
            data["File Summary"][i][0] = data["File Summary"][i - 1][0]

    file_summary = pd.DataFrame({
        "File": pd.Series([d[0] for d in data["File Summary"]]),
        "Rule": pd.Series([d[1] for d in data["File Summary"]]),
        "Violations": pd.Series([d[2] for d in data["File Summary"]]),
        "Deviations": pd.Series([d[3] for d in data["File Summary"]]),
        "Compliance Level": pd.Series([d[4] for d in data["File Summary"]]),
    })

    out["overviewData"] = {
        'thousand_defect_num': round(int(compliance_summary.loc["Total number of rule violations", "num"]) / int(
            compliance_summary.loc["Lines of Code (LOC)", "num"]) * 1000, 2),
        'defect_concentration': round(int(compliance_summary.loc["Total number of rule violations", "num"]) / int(
            compliance_summary.loc["Lines of Code (LOC)", "num"]) * 1000, 2),
        'file_defect_rate': str(round(int(compliance_summary.loc["Number of files with violations", "num"]) / int(
            compliance_summary.loc["Number of files in project (including CMA)", "num"])* 100, 2)) + "%",
    }
    joined_df = file_summary.set_index("Rule").join(rule_summary.set_index("Rule"), rsuffix="_r", how='left')
    out["detectTypeData"] = {
        'forced_defect': {
            'total_defect_num': int(rule_summary.groupby(["Category"]).sum().loc["Mandatory", "Violation"]),
            'defect_proportion': str(round(rule_summary.groupby(["Category"]).sum().loc["Mandatory", "Violation"] /
                                           rule_summary.sum().loc["Violation"]* 100, 2)) + "%",
            'thousand_defect_num': round(
                rule_summary.groupby(["Category"]).sum().loc["Mandatory", "Violation"] / int(
                    compliance_summary.loc["Lines of Code (LOC)", "num"]) * 1000, 2),
            'defect_concentration':round(
                rule_summary.groupby(["Category"]).sum().loc["Mandatory", "Violation"] / int(
                    compliance_summary.loc["Lines of Code (LOC)", "num"]) * 1000, 2),
            'file_defect_rate': str(round(joined_df.groupby("Category").nunique().loc["Mandatory", "File"] / int(
                compliance_summary.loc["Number of files in project (including CMA)", "num"])* 100, 2)) + "%" if
            rule_summary.groupby(["Category"]).sum().loc["Mandatory", "Violation"] != 0 else "0%"
        },
        'optional_defect': {
            'total_defect_num': int(rule_summary.groupby(["Category"]).sum().loc["Required", "Violation"]),
            'defect_proportion': str(round(rule_summary.groupby(["Category"]).sum().loc["Required", "Violation"] /
                                           rule_summary.sum().loc["Violation"]* 100, 2)) + "%",
            'thousand_defect_num': round(
                rule_summary.groupby(["Category"]).sum().loc["Required", "Violation"] / int(
                    compliance_summary.loc["Lines of Code (LOC)", "num"]) * 1000, 2),
            'defect_concentration': round(
                rule_summary.groupby(["Category"]).sum().loc["Required", "Violation"] / int(
                    compliance_summary.loc["Lines of Code (LOC)", "num"]) * 1000, 2),
            'file_defect_rate': str(round(joined_df.groupby("Category").nunique().loc["Required", "File"] / int(
                compliance_summary.loc["Number of files in project (including CMA)", "num"]), 4) * 100) + "%" if
            rule_summary.groupby(["Category"]).sum().loc["Required", "Violation"] != 0 else "0%"
        },
        'suggested_defect': {
            'total_defect_num': int(rule_summary.groupby(["Category"]).sum().loc["Advisory", "Violation"]),
            'defect_proportion': str(round(rule_summary.groupby(["Category"]).sum().loc["Advisory", "Violation"] /
                                           rule_summary.sum().loc["Violation"]* 100, 2) ) + "%",
            'thousand_defect_num': round(
                rule_summary.groupby(["Category"]).sum().loc["Advisory", "Violation"] / int(
                    compliance_summary.loc["Lines of Code (LOC)", "num"]) * 1000, 2),
            'defect_concentration': round(
                rule_summary.groupby(["Category"]).sum().loc["Advisory", "Violation"] / int(
                    compliance_summary.loc["Lines of Code (LOC)", "num"]) * 1000, 2),
            'file_defect_rate': str(round(joined_df.groupby("Category").nunique().loc["Advisory", "File"] / int(
                compliance_summary.loc["Number of files in project (including CMA)", "num"])* 100, 2)) + "%" if
            rule_summary.groupby(["Category"]).sum().loc["Advisory", "Violation"] != 0 else "0%"
        },
    }
    df = rule_summary.filter(["Standard","Rule","Violation","Category"])
    out["optionalTable"] = [{'standard':row["Standard"],'source':row["Rule"],'num':row["Violation"]} for index, row in df[df["Category"] == "Required"].iterrows()]
    out['forcedTable'] = [{'standard':row["Standard"],'source':row["Rule"],'num':row["Violation"]} for index, row in df[df["Category"] == "Mandatory"].iterrows()]
    out['suggestedTable'] = [{'standard':row["Standard"],'source':row["Rule"],'num':row["Violation"]} for index, row in df[df["Category"] == "Advisory"].iterrows()]
    return out

# print(json.dumps(get_fault_dict("./test2.html","./test2.rcf")))



#
