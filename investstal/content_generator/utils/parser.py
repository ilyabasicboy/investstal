# -*- coding:utf-8 -*-
import re
import random


class TextGenerator:

    """ Новый парсер сделан на генераторах для экономии оперативной памяти.
        Для примера, как работал старый, я оставил код в файле parser.py
    """

    OR = 0  # операция возвращает список операндов
    AND = 1  # операция создает все комбинации операндов и возвращает их список
    BRACKET_TYPES = {
        "{": OR, "}": OR,
        "[": AND, "]": AND,
    }

    class NodeHolder:
        def __init__(self):
            self.buffer = dict()
            self.nodelist_key_template = ":node%d:"

        def save(self, node):
            nodelist_key = self.nodelist_key_template % len(self.buffer)
            self.buffer[nodelist_key] = node
            return nodelist_key

        def get(self, nodelist_key):
            return self.buffer[nodelist_key]

        @staticmethod
        def get_pattern():
            return re.compile(r':node\d+:')

    def __init__(self, seo_template):
        """
            seo_template - это seo-шаблон
            Класс для генерирования текста по seo-шаблону.
            шаблон seo_template может содержать следующие допустимые операции:
            1. {a |b |z } => a b z
            2. [a|b] => ab ba
            2. [+<separator>+a|b] a<separator>b b<separator>a

        """

        self.template = seo_template
        self.node_holder = self.NodeHolder()

    def __complete_combinations(self, combinations=None, combination=None, tail=None, separator=" "):
        """
            Рекурсивно достраивает комбинацию, на каждом шаге рекурсии добавляется один
            свободный элемент из tail. Когда свободные элементы заканчиваются - комбинация готова
            записывает комбинацию в список комбинаций
        """
        combinations = [] if combinations is None else combinations
        combination = [] if combination is None else combination
        tail = [] if tail is None else tail
        for node in tail:
            combination1 = combination[:]
            combination1.append(node)
            tail1 = list(set(tail) - set(combination1))
            if len(tail1):
                self.__complete_combinations(combinations, combination1, tail1, separator)
            else:
                combinations.append(separator.join(combination1))
        return combinations

    def __generate_combinations(self, nodelist, separator=" "):
        """
            Запускает первую итерацию сборки комбинаций из элементов списка nodelist
            элементы комбинации объединяются указанным в separator разделителем
        """

        tail = nodelist[:]
        combinations = self.__complete_combinations(tail=tail, separator=separator)
        return combinations

    def __resolve_simple_template(self, simple_template):
        """
            Принимает простой шаблон,
            применяет операцию согласно типу скобок,
            возвращает список простых элементов(не шаблонов)
        """
        operation_type = self.BRACKET_TYPES[simple_template[0]]
        template_content = simple_template[1:-1]

        nodelist = None
        if operation_type == self.OR:
            nodelist = template_content.split("|")

        elif operation_type == self.AND:
            separator_pattern = re.compile(r'\+(.+)\+')
            separator = re.match(separator_pattern, template_content)
            if separator:
                separator = separator.group(True)
                template_content = re.sub(separator_pattern, "", template_content)
            else:
                separator = ""
            nodelist = template_content.split("|")
            for i in range(len(nodelist)):
                nodelist[i] = nodelist[i]
            nodelist = self.__generate_combinations(nodelist, separator)

        return nodelist

    def __prepare_template(self, template):
        """
            Подготовка шаблона, содержащего шаблонные операторы {}, []
            Поиск простоых операторов, запись их в node_holder, замена на переменную в исходном шаблоне
            шаблон подготовлен когда все операторы вычеселны и заменены на переменные
            Пример:
            [a|{b|c}]e => [a|:node0:]e => :node1:e
                :node0: = {b|c} => resolve_simple_template => ["b","c"]
                :node1: = [a|:node0:] => resolve_simple_template => ["a node0","node0 a" ]
            node_holder:
                :node0: ["b","c"]
                :node1: ["a node0","node0 a" ]
        """

        simple_template_pattern = re.compile(r'\[[^\[\]\{\}]+\]|\{[^\[\]\{\}]+\}')
        # поиск простого шаблона в переданной строке
        simple_template_finded = re.search(simple_template_pattern, template)
        # если найден простой шаблон в шаблоне
        if simple_template_finded:
            simple_template = simple_template_finded.group(0)
            simple_template_nodelist = self.__resolve_simple_template(simple_template)
            nodelist_key = self.node_holder.save(simple_template_nodelist)
            nodelist = template.split(simple_template)
            nodelist.insert(1, nodelist_key)
            # подставляем в шаблон вместо найденного простого шаблона переменную
            template2 = "".join(nodelist)
            # снова ищем простой шаблон
            return self.__prepare_template(template2)
        else:
            return template

    def __simplify_nodelist(self, nodelist):
        """
            Упрощение сложного списка нод в список простых,
            после подтановки вместо переменных их значений(нод)

            prepared_template = :node2:  a  e.
            :node2:  = ["b", "c"] =>
            nodelist = [["b", "c"], "a  e."]

            simplify_nodelist(nodelist):
            [["b", "c"], "a  e."] => ["b a e.", "c a e."]
        """

        buf = []                # в буфере накапливаем простые элементы nodelist (не списки)
        for node in nodelist:
            if isinstance(node, list):

                rand_idx = random.randint(0, len(node)-1)

                buf += [node[rand_idx]]
            else:
                buf += [node]

        return ''.join(buf)

    def __construct_nodelist(self, prepared_template):
        """
            По приготовленному шаблону(содержит переменные шаблона) составляет список нод
            (заменяет переменные на их значения(ноды))

            Пример:
            prepared_demplate = :node1: e.
            node_holder:
                :node1: ["a :node2:", ":node2: a"]
                :node0: ["b", "c"]

            construct_nodelist(prepared_template)
                nodelist = [["a node0","node0 a" ], "e"]
                simplify_nodelist(nodelist)
                    nodelist = [["a node0","node0 a" ], "e"] => ["a node0 e", "node0 a e"]
                рекурсивно повторяем процедуру construct_nodelist + simplify_nodelist
                для каждой ноды из nodelist и в конечном счете получим nodelist не содержащий
                переменных и сложных нод:

                nodelist = ['a b e.', 'a c e.', 'b a e.', 'c a e.']

        """

        nodelist_key_pattern = self.node_holder.get_pattern()
        keys = re.findall(nodelist_key_pattern, prepared_template)

        if keys:

            right_part = prepared_template
            nodelist = []
            for key in keys:
                left_part, right_part = right_part.split(key)
                simple_nodelist = self.node_holder.get(key)

                if left_part:
                    nodelist += [left_part]
                nodelist += [simple_nodelist]

            # добавим последние элементы правой части
            if right_part:
                nodelist.append(right_part)

            # упростить сложные ноды (содержащие списки элементов) в простые
            random_node = self.__simplify_nodelist(nodelist)

            # рекурсивно ищем и заменяем переменные
            node = self.__construct_nodelist(random_node)

            try:
                yield next(node)
            except StopIteration:
                pass
        else:
            # если нет шаблонных переменных
            yield prepared_template

    def generate_textlist(self):

        """ Возвращает генератор из одного элемента с рандомным текстом """
        try:
            prepared_template = self.__prepare_template(self.template)
        except:
            raise Exception("Seo-template has are syntax error")

        try:
            textlist = self.__construct_nodelist(prepared_template)
        except:
            raise Exception("Could not create text from template, see the error in log")
        return textlist
