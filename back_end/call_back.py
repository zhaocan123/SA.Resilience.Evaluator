# calculate the call-back architecture graph
# 获取函数注释

import os
from warnings import catch_warnings
import numpy as np
import random
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import calinski_harabasz_score
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation
import networkx as nx
import json

from utils import get_file_encoding


pwd = os.getcwd()
pwd = pwd.replace("\\", "/")
os.environ['NLTK_DATA'] = os.path.abspath(pwd+'/nltk_data/')
import nltk

class Function:
    def __init__(self, name, param_list, file, start, end):
        self.name = name
        self.param_list = param_list
        self.file = ""
        file_list = file.split(':')
        self.file = file_list[0]+":"+file_list[1]
        self.start = start
        self.end = end
        self.anno = ""

# if a function name string is named use camel case, remove the camel case and return a new string


def remove_camel_case(text: str) -> list:
    words = []
    word = ''
    for char in text:
        if char.isupper() and len(word) > 1:
            if word:
                words.append(word)
            word = char.lower()
        else:
            word += char
    if word:
        words.append(word)
    return " ".join(words)


class FunctionInfo:
    def __init__(self, name: str, parameters: list, comments: str) -> None:
        self.name = name
        self.parameters = parameters
        self.comments = comments
        self.processed_name = None
        self.processed_parameters = []
        self.processed_comments = None
        self.name_weight = 1
        self.parameters_weight = 1
        self.comments_weight = 1
        self.header_file = None
        self.source_file = None
        self.call_libraires = None

    def process_text(self) -> None:
        self.processed_name = remove_camel_case(self.name).replace("_", " ")
        self.processed_parameters = [remove_camel_case(parameter).replace("_", " ") for parameter in self.parameters]
        self.processed_comments = self.comments.replace("_", " ")  # remove_camel_case(self.comments).replace("_", " ")

        # # remove all none alpha characters in data
        # self.processed_name = re.sub("\W+", "", self.processed_name, flags= re.ASCII)
        # self.processed_parameters = [re.sub("\W+", "", parameter, flags= re.ASCII) for parameter in self.processed_parameters]
        # self.processed_comments = re.sub("\W+", "", self.processed_comments, flags= re.ASCII)

        # remove all numbers in the strings
        self.processed_name = ''.join([i for i in self.processed_name if not i.isdigit()])
        self.processed_parameters = [''.join([i for i in parameter if not i.isdigit()]) for parameter in self.processed_parameters]
        self.processed_comments = ''.join([i for i in self.processed_comments if not i.isdigit()])
        # use nltk to tokenize the strings
        self.processed_name = nltk.word_tokenize(self.processed_name)
        self.processed_parameters = [nltk.word_tokenize(parameter) for parameter in self.processed_parameters]
        self.processed_comments = nltk.word_tokenize(self.processed_comments)
        # convert all the words to lower case
        self.processed_name = [word.lower() for word in self.processed_name]
        self.processed_parameters = [[word.lower() for word in parameter] for parameter in self.processed_parameters]
        self.processed_comments = [word.lower() for word in self.processed_comments]
        # remove all the punctuations with nltk
        self.processed_name = [word for word in self.processed_name if word.isalnum()]
        self.processed_parameters = [[word for word in parameter if word.isalnum()] for parameter in self.processed_parameters]
        self.processed_comments = [word for word in self.processed_comments if word.isalnum()]
        # remove all the stop words with nltk
        stop_words = set(nltk.corpus.stopwords.words('english'))
        self.processed_name = [word for word in self.processed_name if word not in stop_words]
        self.processed_parameters = [[word for word in parameter if word not in stop_words] for parameter in self.processed_parameters]
        self.processed_comments = [word for word in self.processed_comments if word not in stop_words]
        # use nltk to stem the words
        stemmer = nltk.stem.PorterStemmer()
        self.processed_name = [stemmer.stem(word) for word in self.processed_name]
        self.processed_parameters = [[stemmer.stem(word) for word in parameter] for parameter in self.processed_parameters]
        self.processed_comments = [stemmer.stem(word) for word in self.processed_comments]

        self.words = set(self.processed_name + self.processed_comments + [word for parameter in self.processed_parameters for word in parameter])
        self.word_counts = self.count_words()
        self.text = " ".join(self.processed_name + self.processed_comments + [word for parameter in self.processed_parameters for word in parameter])
        if self.call_libraires is not None:
            self.text += " " + " ".join(self.call_libraires)

    def count_words(self) -> None:
        # count the number of self.words' occurance in the processed text
        word_counts = {}
        for word in self.words:
            word_counts[word] = 0
        for word in self.processed_name:
            word_counts[word] += 1 * self.name_weight
        for word in self.processed_comments:
            word_counts[word] += 1 * self.comments_weight
        for parameter in self.processed_parameters:
            for word in parameter:
                word_counts[word] += 1 * self.parameters_weight
        return word_counts

    def print_processed_text(self) -> None:
        print("function name:", self.name)
        print("file name:", self.header_file, self.source_file)
        # print("parameters:", self.parameters)
        # print("comments:", self.comments)
        print("parameters:", self.processed_parameters)
        print("comments:", self.processed_comments)
        print("processed words count:", self.word_counts)
        # print(" ".join(self.processed_name + self.processed_comments + [word for parameter in self.processed_parameters for word in parameter]))
        print(self.text)


class dealed_function:
    def __init__(self, name, header_file, source_file):
        self.name = name
        self.anno = ""
        self.param_list = []
        self.header_file = header_file
        self.source_file = source_file


def get_func_anno(FILE, function_header_source):
    file_list, _ = getfilelist(FILE)  # (os.path.join(FILE,"code"))

    function_list = []

    for file in file_list:
        call_txt = file+".call"
        parameter_txt = file+".parameter"
        temp_func_list = []

        start_list = []
        end_list = []
        # 按行读取call_txt和parameter_txt，去掉空行
        call_list = []
        parameter_list = []
        encoding = get_file_encoding(call_txt)
        with open(call_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                if line.strip() != '':
                    call_list.append(line.strip())
        encoding = get_file_encoding(parameter_txt)
        with open(parameter_txt, 'r', encoding=encoding) as f:
            for line in f.readlines():
                if line.strip() != '':
                    parameter_list.append(line.strip())

        for i in range(len(call_list)):
            func_info = call_list[i].split('],')[0][2:]
            func_param = parameter_list[i]
            func_name = func_info.split(' ;; ')[2]
            start = func_param.split(';')[1]
            start_list.append(int(start))
            end = func_param.split(';')[2]
            end_list.append(int(end))
            param_list = []
            if len(func_param.split(';')) > 6:
                # 从第四个分号开始，每两个分号为一组，分别为参数类型和参数名
                for j in range(5, len(func_param.split(';')), 2):
                    if func_param.split(';')[j] != "" and func_param.split(';')[j+1] != "":
                        param_list.append((func_param.split(';')[j].split('$$')[-1], func_param.split(';')[j+1]))

            new_func = Function(func_name, param_list, file, start, end)
            function_list.append(new_func)
            temp_func_list.append(new_func)

        # start_list从小到大排序
        start_list.sort()
        end_list.sort

        # 获取函数注释
        # 按行读取file，不去掉空行
        code = []
        encoding = get_file_encoding(file)
        with open(file, 'r', encoding=encoding) as f:
            for line in f.readlines():
                code.append(line)
        for func in temp_func_list:
            # 获取函数注释
            start_line = int(func.start)
            last_end_line = 0
            for line in end_list:
                if line < start_line:
                    last_end_line = line
            # if func.name == 'CU_set_suite_cleanup_failure_handler':
            #     print(last_end_line)
            anno = []
            # 遍历函数之前行，找到注释，注释结束行为函数开始行的前一行 如果开头为//，则为单行注释，如果开头为/*，则为多行注释
            for i in range(start_line-1, -1, -1):
                # 如果前一行为空行，则不含注释
                if code[i].strip() == '' or i+1 == last_end_line:
                    break
                # 如果前一行为单行注释，则将注释加入anno
                if code[i].strip().startswith('//'):
                    anno.append(code[i])
                # 如果前一行结尾为*/，则将注释加入anno，往前遍历，每一行都加入anno，直到遇到/*，则停止遍历
                elif code[i].strip().endswith('*/'):
                    anno.append(code[i])
                    for j in range(i, -1, -1):
                        if j != i:
                            anno.append(code[j])
                        if code[j].strip().startswith('/*'):
                            # 修改i，使得i为多行注释的第一行
                            i = j
                            break
            # 将注释倒序
            anno.reverse()
            # 遍历函数之后行，找到注释，注释开始行为函数结束行的后一行 如果开头为//，则为单行注释，如果开头为/*，则为多行注释
            end_line = int(func.end)
            next_start_line = 0
            for line in start_list:
                if line > end_line:
                    next_start_line = line
                    break
            # 如果函数结束行为文件最后一行，则不含注释
            if start_line == end_line:
                for i in range(end_line, len(code)):
                    # 如果后一行为空行，则不含注释
                    if code[i].strip() == '' or i+1 == next_start_line:
                        break
                    # 如果后一行为单行注释，则将注释加入anno
                    if code[i].strip().startswith('//'):
                        anno.append(code[i])
                    # 如果后一行开头为/*，则将注释加入anno，往后遍历，每一行都加入anno，直到遇到*/，则停止遍历
                    elif code[i].strip().startswith('/*'):
                        anno.append(code[i])
                        for j in range(i, len(code)):
                            if j != i:
                                anno.append(code[j])
                            if code[j].strip().endswith('*/'):
                                # 修改i，使得i为多行注释的最后一行
                                i = j
                                break
            func.anno = anno

    fun_def_txt = os.path.join(FILE, "graphs", "fun_definitions.txt").replace('\\', '/')
    # 按行读取fun_def_txt，去掉空行
    dealed_func_list = []
    for function, (source, header) in function_header_source.items():
        func_name = function.split(':')[-1]

        new_func = FunctionInfo(func_name, [], "")
        new_func.header_file = header
        new_func.source_file = source
        dealed_func_list.append(new_func)

        # with open(fun_def_txt, 'r', encoding='utf-8') as f:
        # for line in f.readlines():
        #     if line.strip() != '':
        #         info_list = line.strip().split('::')
        #         func_name = info_list[0]
        #         header = info_list[1]
        #         source = info_list[2]

        #         new_func = FunctionInfo(func_name, [], "")
        #         new_func.header_file = header
        #         new_func.source_file = source
        #         dealed_func_list.append(new_func)

    for func in function_list:
        for dealed_func in dealed_func_list:
            if func.name == dealed_func.name and (func.file == dealed_func.header_file or func.file == dealed_func.source_file):
                for anno in func.anno:
                    dealed_func.comments += anno

                if dealed_func.parameters == []:
                    for param in func.param_list:
                        dealed_func.parameters.append(param[1])

                break

    return dealed_func_list


def getfilelist(path):
    # Convert relative path to absolute path
    path = os.path.abspath(path)
    # Get all files in the path
    filelist = []
    fileTypes = {
        "c": [],
        "cpp": [],
        "header": [],
        # "other": []

    }
    file_select = None
    ctypelist = (".c")
    cpptypelist = (".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    sourcetypelist = (".c", ".C", ".cc", ".CC", ".cp", ".c++", ".C++", ".cxx", ".cpp", ".CPP", ".CXX")
    headertypelist = (".h", ".H", ".hh", ".hpp", ".hxx")
    with open(path + "/analyze_files.json", 'r', encoding="utf-8") as f:
        file_select = json.load(f)
    filelist += file_select['header']
    filelist += file_select['source']
    for file_path in file_select['source']:
        if file_path.endswith(ctypelist):
            fileTypes['c'].append(file_path)
        else:
            fileTypes["cpp"].append(file_path)
    fileTypes['header'] = file_select['header']
    # for root, dirs, files in os.walk(path):
    #     for file in files:
    #         # if os.path.splitext(file)[1] == '.c' or os.path.splitext(file)[1] == '.h' or os.path.splitext(file)[1] == '.l' or os.path.splitext(file)[1] == '.C' or os.path.splitext(file)[1] == '.H' or os.path.splitext(file)[1] == '.cpp' or os.path.splitext(file)[1] == '.hpp' or os.path.splitext(file)[1] == '.CPP' or os.path.splitext(file)[1] == '.HPP':
    #         if file.endswith(sourcetypelist) or file.endswith(headertypelist):
    #             filelist.append(os.path.join(root, file).replace('\\', '/'))
    #         if file.endswith(ctypelist):
    #             fileTypes['c'].append(os.path.join(root, file).replace('\\', '/'))
    #         elif file.endswith(cpptypelist):
    #             fileTypes['cpp'].append(os.path.join(root, file).replace('\\', '/'))
    #         elif file.endswith(headertypelist):
    #             fileTypes['header'].append(os.path.join(root, file).replace('\\', '/'))
    #         else:
    #             fileTypes['other'].append(os.path.join(root, file).replace('\\', '/'))
    # new_filelist = []
    # for file in filelist:
    #     # 先存储头文件
    #     # if (file.find('.h') != -1 or file.find('.H') != -1 or file.find('.hpp') != -1 or file.find('.HPP') != -1) and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
    #     if file.endswith(headertypelist) and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
    #         new_filelist.append(file)
    # for file in filelist:
    #     # 再存储源文件
    #     # if (file.find('.c') != -1 or file.find('.C') != -1 or file.find('.cpp') != -1 or file.find('.CPP') != -1 or os.path.splitext(file)[1] == '.l') and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
    #     if file.endswith(sourcetypelist) and file.find('ncurses') == -1 and file.find('ncursesw') == -1:
    #         new_filelist.append(file)
    return filelist, fileTypes


class FunctionClusterGA:
    def __init__(self, function_vectors, other_vectors, other_labels, size_pop=200, max_iter=501, prob_mut=0.25, keep_ratio=0.25, init_method="random"):
        print(function_vectors.shape)
        self.func_vectors = function_vectors
        self.other_vectors = other_vectors
        self.other_labels = other_labels
        self.size_pop = size_pop
        self.max_iter = max_iter
        self.prob_mut = prob_mut
        self.keep_ratio = keep_ratio
        self.func_num = function_vectors.shape[0]
        self.topic_num = function_vectors.shape[1]
        self.population = []
        self.init_method = init_method
        if self.init_method == "random":
            for _ in range(self.size_pop):
                self.population.append(np.random.randint(0, self.topic_num, size=(self.func_num,)))
        elif self.init_method == "add" or "noga":
            population = [self.topic_num + i for i in range(self.func_num)]
            for _ in range(self.size_pop):
                random.shuffle(population)
                self.population.append(population)
        elif self.init_method == "one":
            population = [self.topic_num for _ in range(self.func_num)]
            for _ in range(self.size_pop):
                self.population.append(population)
        self.population = sorted(self.population, key=lambda x: self.ga_score(x), reverse=True)

    def ga_score(self, function_labels):
        # find the score

        feature_vectors = np.concatenate((self.func_vectors, self.other_vectors), axis=0)
        labels = np.concatenate((function_labels, self.other_labels), axis=0)
        return calinski_harabasz_score(feature_vectors, labels)

    def select(self):
        # random select 2 from first half of population
        index1 = np.random.randint(0, self.size_pop // 2)
        index2 = np.random.randint(0, self.size_pop // 2)
        return index1, index2

    def crossover(self, i1: np.ndarray, i2: np.ndarray):
        newx = self.population[i2].copy()
        for i in range(self.func_num):
            if i < self.func_num // 2:
                newx[i] = self.population[i1][i]
        return newx

    def mutation(self, x: np.ndarray):
        # random choose a node in x and change its topic or swap it with another function
        if random.random() < self.prob_mut:
            if random.random() < 0.5:
                index1 = np.random.randint(0, self.func_num)
                index2 = np.random.randint(0, self.func_num)
                x[index1], x[index2] = x[index2], x[index1]
            else:
                index = np.random.randint(0, self.func_num)
                x[index] = np.random.randint(0, self.topic_num + 1)
                if x[index] == self.topic_num:
                    self.topic_num += 1
        return x

    def run(self):
        if self.init_method == "noga":
            return self.population[0]
        for i in range(self.max_iter):
            # for k in range(5):
            #     print(i, self.lag.cal_architecture_fitness(self.population[k*5]), end = "")
            if i % 50 == 0:
                print(i, self.ga_score(self.population[0]))
            for j in range(self.size_pop):
                if j > self.keep_ratio * self.size_pop:
                    i1, i2 = self.select()
                    newx = self.crossover(i1, i2)
                    newx = self.mutation(newx)
                    self.population[j] = newx
            # sort the population
            self.population = sorted(self.population, key=lambda x: self.ga_score(x), reverse=True)
        return self.population[0]


class ProjectFunctionInfos:
    def __init__(self, name: str, project_name: str) -> None:
        self.name = name
        self.project_name = project_name
        self.function_infos = []
        self.name_weight = 1
        self.parameters_weight = 1
        self.comments_weight = 1
        self.function_matrix = None

    def add_function(self, function_info: FunctionInfo) -> None:
        self.function_infos.append(function_info)

    def count_vectorize(self, use_tf_idf: bool = False):
        # use sklearn count vectorizer to vectorize the text

        vectorizer = CountVectorizer()
        self.vectorizer = vectorizer
        self.function_matrix = vectorizer.fit_transform([function_info.text for function_info in self.function_infos])
        if use_tf_idf:

            transformer = TfidfTransformer()
            self.function_matrix = transformer.fit_transform(self.function_matrix)
        print(self.function_matrix)

    def lda_analysis(self, max_topic_num: int = 25):
        # use sklearn lda to do the topic modeling

        lda_model = LatentDirichletAllocation(n_components=max_topic_num, random_state=5).fit(self.function_matrix)
        self.function_matrix = lda_model.transform(self.function_matrix)
        # print(self.function_matrix)

    def lda_analysis_cv(self, random_seed):
        # use sklearn lda to do the topic modeling

        best_model = None
        best_perplexity = float("inf")
        perplexities = []
        for n in range(2, 100):
            lda_model = LatentDirichletAllocation(n_components=n, random_state=random_seed).fit(self.function_matrix)
            print(n, lda_model.perplexity(self.function_matrix))
            perplexities.append(lda_model.perplexity(self.function_matrix))
            # print(self.function_matrix.sum())
            if lda_model.perplexity(self.function_matrix) < best_perplexity:
                best_model = lda_model
                best_perplexity = best_model.perplexity(self.function_matrix)
            # print(lda_model.fit_transform(self.function_matrix).shape)
        self.function_matrix = best_model.transform(self.function_matrix)
        # save the perplexity figure to file

        # plt.plot(np.arange(2, 100), perplexities)
        # plt.xlabel("Number of Topics")
        # plt.ylabel("Perplexity")
        # plt.savefig("./data/"+self.project_name+"/perplexity.png")

        # save components of best model to a pandas dataframe
        best_lda_pd = pd.DataFrame(best_model.components_, columns=self.vectorizer.get_feature_names_out())
        # 将每行的数值最大的10个元素的列名提取出来
        best_lda_pd = best_lda_pd.apply(lambda x: pd.Series(x.nlargest(10).index), axis=1)
        self.topic_words_df = best_lda_pd
        # 转换成list
        self.topic_words = best_lda_pd.values.tolist()
        # 输出topic numbers
        print("topic numbers:", self.function_matrix.shape[1])
        # 输出
        # print("主题向量：")
        # for i in range(len(self.function_infos)):
        #     print("函数:", self.function_infos[i].name)
        #     print("主题向量：",self.function_matrix[i,:])

    def topic_clustering(self, confidence_level: float = 0.5, init_method="random"):
        # init function labels
        self.function_labels = [None for _ in range(len(self.function_infos))]
        self.is_ga = [True for _ in range(len(self.function_infos))]

        if init_method == "zero":
            confidence_level = 0

        # firstly, use the confidence level to filter functions that is not needed to be clustered by cluster algorithm
        names = []
        for i in range(len(self.function_infos)):
            if np.max(self.function_matrix[i, :]) > confidence_level:
                self.function_labels[i] = np.argmax(self.function_matrix[i, :])
                names.append(self.function_infos[i].name)
                self.is_ga[i] = False

        print("confident functions: ", len(names))
        names = []
        # print names of related functions
        for i in range(len(self.function_infos)):
            if self.function_labels[i] == None:
                names.append(self.function_infos[i].name)
        print("unconfident functions: ", len(names))
        if len(names) > 0:
            labels_np = np.array(self.function_labels)
            rest_features = self.function_matrix[labels_np == None]
            labeled_features = self.function_matrix[labels_np != None]
            # for the rest of the functions which still has no labels, use genetic algorithm
            rest_labels = FunctionClusterGA(function_vectors=rest_features, other_vectors=labeled_features, other_labels=labels_np[labels_np != None], init_method=init_method).run()
            # print(rest_labels)
            for l in rest_labels:
                # print('\nl:', l)
                for i in range(len(self.function_labels)):
                    # print(i,end=" ")
                    if self.function_labels[i] == None:
                        self.function_labels[i] = l
                        # print(f"setting {i} to {l}")
                        break
        print(self.function_labels)

    def clustering(self, check_perplexity: bool = True, init_method="random", random_seed=0, use_tf_idf: bool = False):
        # perform count vectorization first
        self.count_vectorize(use_tf_idf=use_tf_idf)
        # run lda analysis
        if check_perplexity:
            self.lda_analysis_cv(random_seed)
        else:
            self.lda_analysis()
        # run topic clustering
        self.topic_clustering(init_method=init_method)
        # use sklearn GMM to do the clustering
        # from sklearn.mixture import GaussianMixture
        # gmm = GaussianMixture(n_components=cluseter_num, covariance_type='full',random_state=0).fit(self.function_matrix)
        # self.function_labels = gmm.predict(self.function_matrix)
        # print("function labels:", self.function_labels)

    def print_clustering_result(self, show_cluster: bool = True):
        if show_cluster:
            # print function num and names in each cluster
            for c in set(self.function_labels):
                print("cluster", c, ":", len([x for x in self.function_labels if x == c]), "fucntions")
                print([self.function_infos[i].name for i in range(len(self.function_labels)) if self.function_labels[i] == c])
                print()
        else:
            if self.function_labels is None:
                print("please run clustering first")
                return
            else:
                for function_info, label in zip(self.function_infos, self.function_labels):
                    print("function name:", function_info.name)
                    print("function cluster label:", label)
                    # print("function text:", function_info.text)
                    # print most frequent 5 words in the function
                    print("function most frequent 5 words:", [x[0] for x in sorted(function_info.word_counts.items(), key=lambda x: x[1], reverse=True)[:5]])
                    # print("function words:", function_info.words)
                    print()

    def save_to_csv(self, path="data.csv"):  # , topic_path="topic.csv"):
        # save current clustering result to csv file
        function_names = [function_info.name for function_info in self.function_infos]
        function_parameters = [function_info.parameters for function_info in self.function_infos]
        function_comments = [function_info.comments for function_info in self.function_infos]
        function_processd_words = [function_info.text for function_info in self.function_infos]
        function_counts = [function_info.word_counts for function_info in self.function_infos]
        # function topic vectors
        function_topic_vectors = [self.function_matrix[i, :] for i in range(len(self.function_infos))]
        function_header_file = [function_info.header_file for function_info in self.function_infos]
        function_source_file = [function_info.source_file for function_info in self.function_infos]
        function_folder = [function_info.source_file.split('/')[-3:-1] for function_info in self.function_infos]
        function_libraries = [function_info.call_libraires for function_info in self.function_infos]
        function_topic = self.function_labels
        function_ga = self.is_ga
        # save all above to a dataframe
        function_data = pd.DataFrame({"name": function_names, "parameters": function_parameters, "comments": function_comments, "text": function_processd_words, "folder": function_folder, "libs": function_libraries,
                                     "counts": function_counts, "topic_vectors": function_topic_vectors, "headerfile": function_header_file, "sourcefile": function_source_file, "topic": function_topic, "is_ga": function_ga})
        # save dataframe to csv file
        function_data.to_csv(path, index=False)
        # save topic words to csv file
        # self.topic_words_df.to_csv(topic_path, index=False)


interface_libs = ["stdio.h", "graphics.h", "windows.h", "stdafx.h", "ncurses.h", "curses.h", "lcui.h", "cuiliet.h", "gtk.h", "xlib.h", "socket.h"]
mid_comp_libs = ["ngx_config.h", "ngx_core.h", "ngx_http.h", "rocketmq.h", "rdkafaka.h", "amqp.h", "thrift_binary_protocol.h", "thrift_framed_transport.h", "thrift_socket.h"]
database_libs = ["sql.h", "sqltypes.h", "sqlext.h", "mysql.h", "mongoc.h", "memcache.h", "Neo4j-clint.h", "hiredis.h", "odbcss.h", "odbcinst.h"]


def add_call_libraries(function_info: FunctionInfo, plcg):
    # find node with the same name and header in the function info
    for node in plcg.nodes:
        if node != "\\n":
            func_name = plcg.nodes[node]["label"].strip('"').split(":")[1].strip()
            header_name = plcg.nodes[node]['file'].strip('"')
            if func_name == function_info.name and header_name == function_info.header_file:
                c_node = node
                call_libraries = set(plcg.nodes[node]['libs_file'].strip('"').split("@@@"))
                call_libraries.remove('')
                return list(call_libraries)
    return []
    #             break
    # if c_node is None:
    #     return []
    # # find all nodes that are called by the function
    # call_libraries = set()
    # for edge in plcg.edges:
    #     if edge[0] == c_node:
    #         node = edge[1]
    #         if node != "\\n" and plcg.nodes[node]['file'].strip('"') == "Library function":
    #             if plcg.nodes[node]['Lib'].strip('"') in interface_libs + mid_comp_libs + database_libs:
    #                 call_libraries.add(plcg.nodes[node]['Lib'].strip('"'))
    # return list(call_libraries)


def main(project_path, plcg: nx.DiGraph, function_header_source, init_method="add", random_seed=42, use_tfidf=False, project_floder_name=""):
    # nltk.download('punkt')
    # nltk.download('stopwords')
    print("call back main: ", project_path)
    try:
        funciton_lists = get_func_anno(project_path, function_header_source=function_header_source)
        for function_info in funciton_lists:
            # print(function_info.name)
            function_info.call_libraires = add_call_libraries(function_info, plcg)
            # print(function_info.call_libraires)

        # create a ProjectFunctionInfos object
        project_function_infos = ProjectFunctionInfos("test_project_cunit", project_floder_name)

        # file numbers
        file_num = len(getfilelist(project_path))
    except Exception as e:
        print(e)

    print("number of functions:", file_num, len(funciton_lists))

    # add all the function infos to the ProjectFunctionInfos object
    for function_info in funciton_lists:
        # if function_info.name == "run_single_suite":
        function_info.process_text()
        # function_info.print_processed_text()
        project_function_infos.add_function(function_info)

    # perform clustering
    project_function_infos.clustering(check_perplexity=True, init_method=init_method, random_seed=random_seed, use_tf_idf=use_tfidf)
    project_function_infos.print_clustering_result()
    comp_data_csv_path = os.path.join("temp", f"{init_method}_{random_seed}.csv")
    project_function_infos.save_to_csv(comp_data_csv_path)

    return comp_data_csv_path


def if_exist(relationship_list, start, end, style):
    count = 0
    find = False
    for re in relationship_list:
        if re["source"] == start and re["target"] == end:
            count += 1
            if style == re["lineStyle"]["normal"]["type"]:
                find = True
        if re["target"] == start and re["source"] == end:
            count += 1

    if style == "dotted":
        find = False
    return find, count


def comp2json(PLCG: nx.DiGraph, comp_csv):
    json_data = {}
    # PLCG = nx.DiGraph(nx.nx_pydot.read_dot(PLCG_file))
    # 读取csv文件
    comp_df = pd.read_csv(comp_csv)

    function_list = comp_df["name"].tolist()
    function_file_list = comp_df["headerfile"].tolist()
    function_comp_list = comp_df["topic"].tolist()
    # 构建key为组件名，value为（函数名，文件名）的字典
    comp_dict = {}
    for i in range(len(function_list)):
        if function_comp_list[i] not in comp_dict.keys():
            comp_dict[function_comp_list[i]] = []
        comp_dict[function_comp_list[i]].append((function_list[i], function_file_list[i]))

    comp_list = list(set(function_comp_list))
    # 从小到大排序
    comp_list.sort()
    # 添加节点
    node_list = []
    relationship_list = []
    nodesize = 45

    # 添加组件节点
    for comp in comp_list:
        node_name = str(comp)
        node_id = comp
        category = str(comp)
        echarts_node = {"name": node_name,
                        "id": node_id,
                        "symbolSize": 85,
                        # "value": value,
                        "category": category,
                        "comp": 1,
                        "fixed": False,
                        # "itemStyle":{"normal":{"color":"#0000FF"}}#blue
                        # 如果类别为1，即为库函数，则隐藏该节点
                        "itemStyle": {"normal": {"opacity": 1}},
                        # 形状为圆角矩形
                        "symbol": "roundRect",
                        }
        node_list.append(echarts_node)
    # 添加函数节点
    for node in PLCG.nodes:
        if node == '\\n':
            continue
        node_info = PLCG.nodes[node]
        node_name = node_info["label"].replace('"', '').split(":")[-1]
        file = node_info["file"].replace('"', '')
        if file == "Library function":
            continue
        node_id = node
        category = 0
        for i in range(len(function_list)):
            if node_name == function_list[i] and node_info['file'].replace('"', '') == function_file_list[i]:
                category = str(function_comp_list[i])
                nodesize = 45
                break
        echarts_node = {"name": node_name,
                        "id": node_id,
                        "symbolSize": nodesize,
                        # "value": value,
                        "category": category,
                        "comp": 0,
                        "fixed": False,
                        # "itemStyle":{"normal":{"color":"#0000FF"}}#blue
                        # 如果类别为1，即为库函数，则隐藏该节点
                        "itemStyle": {"normal": {"opacity": 0}},
                        "label": node_info["label"].replace('"', ''),
                        }
        node_list.append(echarts_node)

    # 添加边
    # 添加函数到函数的边
    for edge in PLCG.edges:
        style = "solid"
        start_node = edge[0]
        end_node = edge[1]
        file = PLCG.nodes[end_node]["file"].replace('"', '')
        if file == "Library function":
            continue
        _, countff = if_exist(relationship_list, start_node, end_node, style)
        ff_relationship = {"source": start_node,
                           "target": end_node,
                           "value": 200,
                           # 箭头
                           "symbol": ["none", "arrow"],
                           # 线条样式
                           "lineStyle": {"normal": {"width": 2, "distance": 150, "curveness": 0.1*countff, "type": style, "opacity": 0}},
                           # 线条长度
                           # "label": {"normal": {"show": True, "formatter": "{c}", "position": "middle", "distance": line_length}},
                           }
        relationship_list.append(ff_relationship)

        # 添加函数到组件，组件到函数，组件到组件的边
        start_comp = None
        end_comp = None
        for node in node_list:
            if node["id"] == start_node:
                start_comp = node["category"]
            if node["id"] == end_node:
                end_comp = node["category"]

            if start_comp != None and end_comp != None:
                break

        findcf, countcf = if_exist(relationship_list, start_comp, end_node, style)
        findfc, countfc = if_exist(relationship_list, start_node, end_comp, style)
        findcc, countcc = if_exist(relationship_list, start_comp, end_comp, style)
        if findcf == False:
            # 不存在，构建边
            cf_relationship = {"source": start_comp,
                               "target": end_node,
                               # 箭头
                               "symbol": ["none", "arrow"],
                               # 线条样式
                               "lineStyle": {"normal": {"width": 2, "distance": 150, "curveness": 0.1*countcf, "type": style, "opacity": 0}},
                               # 线条长度
                               # "label": {"normal": {"show": True, "formatter": "{c}", "position": "middle", "distance": line_length}},
                               }
            relationship_list.append(cf_relationship)
        if findfc == False:
            # 不存在，构建边
            cf_relationship = {"source": start_node,
                               "target": end_comp,
                               # 箭头
                               "symbol": ["none", "arrow"],
                               # 线条样式
                               "lineStyle": {"normal": {"width": 2, "distance": 150, "curveness": 0.1*countfc, "type": style, "opacity": 0}},
                               # 线条长度
                               # "label": {"normal": {"show": True, "formatter": "{c}", "position": "middle", "distance": line_length}},
                               }
            relationship_list.append(cf_relationship)
        if findcc == False:
            # 不存在，构建边
            cf_relationship = {"source": start_comp,
                               "target": end_comp,
                               # 箭头
                               "symbol": ["none", "arrow"],
                               "value": 200,
                               # 线条样式
                               "lineStyle": {"normal": {"width": 2, "distance": 150, "curveness": 0.1*countcc, "type": style, "opacity": 1}},
                               # 线条长度
                               # "label": {"normal": {"show": True, "formatter": "{c}", "position": "middle", "distance": line_length}},
                               # 设置为折线
                               }
            relationship_list.append(cf_relationship)

    # 构建categories
    categories = []
    for comp in comp_list:
        categories.append({"name": str(comp)})

    colors = []
    while len(colors) < len(categories):
        color = "#%06x" % random.randint(0, 0xFFFFFF)
        if color not in colors:
            colors.append(color)

    # 构建echarts的json
    echarts_json = {"data": node_list, "categories": categories, "links": relationship_list, "color": colors}
    # 保存json
    return json.dumps(echarts_json, indent=4)


if __name__ == "__main__":
    pass
    # FILE = sys.argv[1]
    # main()
