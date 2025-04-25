import json
from bs4 import BeautifulSoup


def read_html_to_json(src_url):
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

            trs = table_element.find_all('tr')
            for row in table_element.find_all('tr'):
                cells = row.find_all('td')
                tmp_list = []
                if len(cells) == 0:
                    continue
                for i in cells:
                    text_tmp = i.text
                    tmp_list.append(i.text)

                data_dict[div_element.text].append(tmp_list)
    return data_dict


if __name__ == '__main__':
    dest_url = r"D:\Code\VScode\CPP_Support\test.json"
    data_dict = read_html_to_json(src_url=r"D:\Code\VScode\CPP_Support\test.html")
    with open(dest_url, 'w', encoding='utf-8') as res:
        json.dump(data_dict, res, ensure_ascii=False, indent=4)
