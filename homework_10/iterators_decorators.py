# %% [markdown]
# # Задание 1 (2 балла)

# %% [markdown]
# Напишите класс `MyDict`, который будет полностью повторять поведение обычного словаря, за исключением того, что при итерации мы должны получать и ключи, и значения.
# 
# **Модули использовать нельзя**

# %%
class MyDict(dict):
    def __iter__(self):
        return iter(self.items())

# %%
dct = MyDict({"a": 1, "b": 2, "c": 3, "d": 25})
for key, value in dct:
    print(key, value)   

# %%
for key, value in dct.items():
    print(key, value)

# %%
for key in dct.keys():
    print(key)

# %%
dct["c"] + dct["d"]

# %% [markdown]
# # Задание 2 (2 балла)

# %% [markdown]
# Напишите функцию `iter_append`, которая "добавляет" новый элемент в конец итератора, возвращая итератор, который включает изначальные элементы и новый элемент. Итерироваться по итератору внутри функции нельзя, то есть вот такая штука не принимается
# ```python
# def iter_append(iterator, item):
#     lst = list(iterator) + [item]
#     return iter(lst)
# ```
# 
# **Модули использовать нельзя**

# %%
def iter_append(iterator, item):
    yield from iterator
    yield item
    

my_iterator = iter([1, 2, 3])
new_iterator = iter_append(my_iterator, 4)

for element in new_iterator:
    print(element)

# %% [markdown]
# # Задание 3 (5 баллов)

# %% [markdown]
# Представим, что мы установили себе некотурую библиотеку, которая содержит в себе два класса `MyString` и `MySet`, которые являются наследниками `str` и `set`, но также несут и дополнительные методы.
# 
# Проблема заключается в том, что библиотеку писали не очень аккуратные люди, поэтому получилось так, что некоторые методы возвращают не тот тип данных, который мы ожидаем. Например, `MyString().reverse()` возвращает объект класса `str`, хотя логичнее было бы ожидать объект класса `MyString`.
# 
# Найдите и реализуйте удобный способ сделать так, чтобы подобные методы возвращали экземпляр текущего класса, а не родительского. При этом **код методов изменять нельзя**
# 
# **+3 дополнительных балла** за реализацию того, чтобы **унаследованные от `str` и `set` методы** также возвращали объект интересующего нас класса (то есть `MyString.replace(..., ...)` должен возвращать `MyString`). **Переопределять методы нельзя**
# 
# **Модули использовать нельзя**

# %%
# Ваш код где угодно, но не внутри методов


class MyString(str):
    def reverse(self):
        return type(self)(self[::-1])
    
    def make_uppercase(self):
        return type(self)("".join([chr(ord(char) - 32) if 97 <= ord(char) <= 122 else char for char in self]))
    
    def make_lowercase(self):
        return type(self)("".join([chr(ord(char) + 32) if 65 <= ord(char) <= 90 else char for char in self]))
    
    def capitalize_words(self):
        return type(self)(" ".join([word.capitalize() for word in self.split()]))
    
    
class MySet(set):
    def is_empty(self):
        return len(self) == 0
    
    def has_duplicates(self):
        return len(self) != len(set(self))
    
    def union_with(self, other):
        return type(self)(self.union(other))
    
    def intersection_with(self, other):
        return type(self)(self.intersection(other))
    
    def difference_with(self, other):
        return type(self)(self.difference(other))

# %%
string_example = MyString("Aa Bb Cc")
set_example_1 = MySet({1, 2, 3, 4})
set_example_2 = MySet({3, 4, 5, 6, 6})

print(type(string_example.reverse()))
print(type(string_example.make_uppercase()))
print(type(string_example.make_lowercase()))
print(type(string_example.capitalize_words()))
print()
print(type(set_example_1.is_empty()))
print(type(set_example_2.has_duplicates()))
print(type(set_example_1.union_with(set_example_2)))
print(type(set_example_1.difference_with(set_example_2)))

# %% [markdown]
# # Задание 4 (5 баллов)

# %% [markdown]
# Напишите декоратор `switch_privacy`:
# 1. Делает все публичные **методы** класса приватными
# 2. Делает все приватные методы класса публичными
# 3. Dunder методы и защищённые методы остаются без изменений
# 4. Должен работать тестовый код ниже, в теле класса писать код нельзя
# 
# **Модули использовать нельзя**

# %%
def switch_privacy(cls):
    methods = dir(cls)
    for method in methods:
        if method.startswith("__"): # skip dunders
            pass

        elif method.startswith(f"_{cls.__name__}"):
            method_content = getattr(cls, method)
            new_method = method.split("__")[1]
            delattr(cls, method)
            setattr(cls, new_method, method_content)

        elif method.startswith("_"): # skip protected
            pass

        else:
            method_content = getattr(cls, method)
            new_method = f"_{cls.__name__}__{method}"
            delattr(cls, method)
            setattr(cls, new_method, method_content)
    return cls

# %%
@switch_privacy
class ExampleClass:
    # Но не здесь
    def public_method(self):
        return 1
    
    def _protected_method(self):
        return 2
    
    def __private_method(self):
        return 3
    
    def __dunder_method__(self):
        pass

# %%
test_object = ExampleClass()

test_object._ExampleClass__public_method()   # Публичный метод стал приватным

# %%
test_object.private_method()   # Приватный метод стал публичным

# %%
test_object._protected_method()   # Защищённый метод остался защищённым

# %%
test_object.__dunder_method__()   # Дандер метод не изменился

# %%
hasattr(test_object, "public_method"), hasattr(test_object, "private")   # Изначальные варианты изменённых методов не сохраняются

# %% [markdown]
# # Задание 5 (7 баллов)

# %% [markdown]
# Напишите [контекстный менеджер](https://docs.python.org/3/library/stdtypes.html#context-manager-types) `OpenFasta`
# 
# Контекстные менеджеры это специальные объекты, которые могут работать с конструкцией `with ... as ...:`. В них нет ничего сложного, для их реализации как обычно нужно только определить только пару dunder методов. Изучите этот вопрос самостоятельно
# 
# 1. Объект должен работать как обычные файлы в питоне (наследоваться не надо, здесь лучше будет использовать **композицию**), но:
#     + При итерации по объекту мы должны будем получать не строку из файла, а специальный объект `FastaRecord`. Он будет хранить в себе информацию о последовательности. Важно, **не строки, а именно последовательности**, в fasta файлах последовательность часто разбивают на много строк
#     + Нужно написать методы `read_record` и `read_records`, которые по смыслу соответствуют `readline()` и `readlines()` в обычных файлах, но они должны выдавать не строки, а объект(ы) `FastaRecord`
# 2. Конструктор должен принимать один аргумент - **путь к файлу**
# 3. Класс должен эффективно распоряжаться памятью, с расчётом на работу с очень большими файлами
#     
# Объект `FastaRecord`. Это должен быть **датакласс** (см. про примеры декораторов в соответствующей лекции) с тремя полями:
# + `seq` - последовательность
# + `id_` - ID последовательности (это то, что в фаста файле в строке, которая начинается с `>` до первого пробела. Например, >**GTD326487.1** Species anonymous 24 chromosome) 
# + `description` - то, что осталось после ID (Например, >GTD326487.1 **Species anonymous 24 chromosome**)
# 
# 
# Напишите демонстрацию работы кода с использованием всех написанных методов, обязательно добавьте файл с тестовыми данными в репозиторий (не обязательно большой)
# 
# **Можно использовать модули из стандартной библиотеки**

# %%
from dataclasses import dataclass
import os


@dataclass
class FastaRecord:
    seq: str
    id_: str
    description: str

    def __str__(self):
        return (
            f'{self.id_} ({self.description})'
            '\n'
            f'{self.seq}'
            '\n'
        )
    
    def __repr__(self):
        return f'<FastaRecord object>'


class OpenFasta:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_object = None
        self.sequence_header = None
    
    def __enter__(self):
        self.file_object = open(self.file_path, "r")
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if self.file_object:
            self.file_object.close()
    
    def read_record(self):
        seq = ""
        id_ = ""
        description = ""

        if not self.sequence_header: # extract id and descr for the first sequence
            for line in self.file_object:
                line = line.strip()
                if line.startswith(">"): # just in case .fasta file starts with commented lines
                    id_ = line[1:].split(" ")[0]
                    description = " ".join(line[1:].split(" ")[1:])
                    break
        else: # extract id and descr for all sequences but the first one
            if self.sequence_header.startswith(">"):
                id_ = self.sequence_header[1:].split(" ")[0]
                description = " ".join(self.sequence_header[1:].split(" ")[1:])
        
        for line in self.file_object:
            line = line.strip()
            if line.startswith(">"):
                self.sequence_header = line
                break
            elif line == "": # end of the file
                break
            seq = "".join([seq, line])
        
        return FastaRecord(seq=seq, id_=id_, description=description)
    
    def read_records(self):
        while True:
            record = self.read_record()
            if not record.seq:
                break
            yield record

# %%
with OpenFasta(os.path.join("data", "example.fasta")) as fasta:
    for record in fasta.read_records():
        print(record)

# %%
with OpenFasta(os.path.join("data", "example.fasta")) as fasta:
    print(fasta.read_record())
    print(fasta.read_record())

# %% [markdown]
# # Задание 6 (7 баллов)

# %% [markdown]
# 1. Напишите код, который позволит получать все возможные (неуникальные) генотипы при скрещивании двух организмов. Это может быть функция или класс, что вам кажется более удобным.
# 
# Например, все возможные исходы скрещивания "Aabb" и "Aabb" (неуникальные) это
# 
# ```
# AAbb
# AAbb
# AAbb
# AAbb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# Aabb
# aabb
# aabb
# aabb
# aabb
# ```
# 
# 2. Напишите функцию, которая вычисляет вероятность появления определённого генотипа (его ожидаемую долю в потомстве).
# Например,
# 
# ```python
# get_offspting_genotype_probability(parent1="Aabb", parent2="Aabb", target_genotype="Аabb")   # 0.5
# 
# ```
# 
# 3. Напишите код, который выводит все уникальные генотипы при скрещивании `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` и `'АаббВвГгДДЕеЖжЗзИиЙйКкЛлМмНН'`, которые содержат в себе следующую комбинацию аллелей `'АаБбВвГгДдЕеЖжЗзИиЙйКкЛл'`
# 4. Напишите код, который расчитывает вероятность появления генотипа `'АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн'` при скрещивании `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн` и `АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн`
# 
# Важные замечания:
# 1. Порядок следования аллелей в случае гетерозигот всегда должен быть следующим: сначала большая буква, затем маленькая (вариант `AaBb` допустим, но `aAbB` быть не должно)
# 2. Подзадачи 3 и 4 могут потребовать много вычислительного времени (до 15+ минут в зависимости от железа), поэтому убедитесь, что вы хорошо протестировали написанный вами код на малых данных перед выполнением этих задач. Если ваш код работает **дольше 20 мин**, то скорее всего ваше решение не оптимально, попытайтесь что-нибудь оптимизировать. Если оптимальное решение совсем не получается, то попробуйте из входных данных во всех заданиях убрать последний ген (это должно уменьшить время выполнения примерно в 4 раза), но **за такое решение будет снято 2 балла**
# 3. Несмотря на то, что подзадания 2, 3 и 4 возможно решить математически, не прибегая к непосредственному получению всех возможных генотипов, от вас требуется именно brute-force вариант алгоритма
# 
# **Можно использовать модули из стандартной библиотеки питона**, но **за выполнение задания без использования модулей придусмотрено +3 дополнительных балла**

# %%
# Ваш код здесь (1 подзадание)
# class to work with alleles of one gene for a diploid organism

class Alleles:
    def __init__(self, first, second, p=1.0):
        first_dominant = first.isupper()
        
        # dominant always first
        if first_dominant:
            self.first = first
            self.second = second
        else:
            self.first = second
            self.second = first

        self.p = p
        """uncomment the following line if you want to use
        another version of combinations method!!!!!"""
        #self.homozygous = self.first == self.second
    
    def __eq__(self, other):
        return (self.first == other.first) and (self.second == other.second)
    
    def __str__(self):
        return f'{self.first}{self.second}'

    def __repr__(self):
        return f'{self.first}{self.second}'
    
    def combinations(self, other_alleles): 
        """returns list of all children one-gene genotypes (type Alleles)
        second version, more brutforcing in terms of combinations
        I'd rather use defaultdict here, but there's a restriction
        on modules :-("""
        child_1 = Alleles(self.first, other_alleles.first, p=0.25)
        child_2 = Alleles(self.first, other_alleles.second, p=0.25)
        child_3 = Alleles(self.second, other_alleles.first, p=0.25)
        child_4 = Alleles(self.second, other_alleles.second, p=0.25)
        children_non_unique = [child_1, child_2, child_3, child_4]

        children_unique = dict() # dict to collapse identical children one-gene genotypes and summarize the probability
        for child in children_non_unique:
            if (child.first, child.second) not in children_unique.keys():
                children_unique[(child.first, child.second)] = child.p
            else:
                children_unique[(child.first, child.second)] += child.p

        children_alleles = [] # list for unique children one-gene genotypes
        for child_alleles, child_p in children_unique.items():
            child = Alleles(child_alleles[0], child_alleles[1], child_p)
            children_alleles.append(child)

        return children_alleles
    '''
    def combinations(self, other_alleles):
        """first version, not sure if it is cheating and formula usage
        needs an uncommented 18 line!!!!!!!!"""
        if self.homozygous and other_alleles.homozygous:
            child = Alleles(self.first, other_alleles.first, p=1.0)
            return [child]
        elif self.homozygous:
            child_1 = Alleles(self.first, other_alleles.first, p=0.5)
            child_2 = Alleles(self.first, other_alleles.second, p=0.5)
            return [child_1, child_2]
        elif other_alleles.homozygous:
            child_1 = Alleles(self.first, other_alleles.first, p=0.5)
            child_2 = Alleles(self.second, other_alleles.first, p=0.5)
            return [child_1, child_2]
        else:
            child_1 = Alleles(self.first, other_alleles.first, p=0.25)
            child_2 = Alleles(self.first, other_alleles.second, p=0.5)
            child_3 = Alleles(self.second, other_alleles.second, p=0.25)
            return [child_1, child_2, child_3]
            '''
            
# class to work with genotypes of any genes of diploid organism

class Genotype:
    def __init__(self, genotype):
        self.genes_alleles = self.get_alleles(genotype)
    
    def __len__(self):
        return len(self.genes_alleles) # number of genes
    
    def __repr__(self):
        repr = "".join(str(x) for x in self.genes_alleles)
        return repr
    
    def __str__(self):
        str_repr = "".join(str(x) for x in self.genes_alleles)
        return str_repr
    
    @classmethod # to avoid reinitializing via strings
    def from_list(cls, alleles_list):
        indiv = cls("")
        indiv.genes_alleles = alleles_list
        return indiv
    
    def get_alleles(self, genotype):
        """Extract unique alleles of all genes from a string"""
        n_alleles = len(genotype) // 2
        gtype = []
        for i in range(n_alleles):
            first = genotype[i * 2]
            second = genotype[i * 2 + 1]
            allele = Alleles(first, second)
            gtype.append(allele)
        return gtype
    
    def mate(self, other):
        """combine genotypes of two individuals"""
        if len(self.genes_alleles) != len(other.genes_alleles):
            raise IndexError("parents' genotypes must correspond")
        return [x[0].combinations(x[1]) for x in zip(self.genes_alleles, other.genes_alleles)]

    def startswith(self, prefix):
        """for 3 task"""
        if len(self.genes_alleles) < len(prefix.genes_alleles): # prefix can not be smaller than genotype
            return False
        for als_idx in range(len(prefix.genes_alleles)):
            if self.genes_alleles[als_idx] != prefix.genes_alleles[als_idx]: # prefix alleles can not be different from the same genotype alleles
                return False
        return True
    
    def gtype_prob(self):
        """probability of genotype"""
        probability = 1
        for gene in self.genes_alleles:
            probability *= gene.p
        return probability


def combinations(allele_pairs):
    """recursive function to make all combinations of possible 
    one-gene genotypes for any gene number"""
    if len(allele_pairs) == 1: # 1 gene left
        for one_gene_alleles in allele_pairs[0]:
            yield [one_gene_alleles]
    else:
        for gtype in allele_pairs[0]:
            for one_gene_alleles in combinations(allele_pairs[1:]):
                yield [gtype] + one_gene_alleles

def unique_gtypes(unique_gtypes):
    unique_genotypes = []
    for gtype in combinations(unique_gtypes):
        genotype = Genotype.from_list(gtype)
        unique_genotypes.append(genotype)
    return unique_genotypes

def non_unique_gtypes(unique_gtypes):
    genotype_len = len(unique_gtypes) * 2
    genotype_number = genotype_len ** 2
    non_unique_genotypes = []
    for gtype in combinations(unique_gtypes):
        genotype = Genotype.from_list(gtype)
        gtype_p = genotype.gtype_prob()
        gtype_duplicates = int(genotype_number * gtype_p)
        non_unique_genotypes.extend([genotype] * gtype_duplicates)
    return non_unique_genotypes      

def unique_offspring(p1, p2):
    p1_gt, p2_gt = Genotype(p1), Genotype(p2)
    alleles_per_gene = p1_gt.mate(p2_gt)
    return unique_gtypes(alleles_per_gene)

def non_unique_offspring(p1, p2):
    p1_gt, p2_gt = Genotype(p1), Genotype(p2)
    alleles_per_gene = p1_gt.mate(p2_gt)
    return non_unique_gtypes(alleles_per_gene)


# %%
parent1 = "Aabb"
parent2 = "Aabb"

for child_gtype in non_unique_offspring(parent1, parent2):
    print(child_gtype)

# %%
parent1 = "AaBb"
parent2 = "AaBB"

for child_gtype in non_unique_offspring(parent1, parent2):
    print(child_gtype)

# %%
# (2 subtask)

def get_offspring_genotype_probability(parent1, parent2, target_genotype):
    for child_gtype in unique_offspring(parent1, parent2):
        if str(child_gtype) == target_genotype:
            return child_gtype.gtype_prob()
    return 0.0

# %%
get_offspring_genotype_probability(parent1="Aabb", parent2="Aabb", target_genotype="Aabb")   # 0.5

# %%
# Ваш код здесь (3 подзадание)

prefix = Genotype("АаБбВвГгДдЕеЖжЗзИиЙйКкЛл")
parent1 = Genotype("АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн")
parent2 = Genotype("АаббВвГгДДЕеЖжЗзИиЙйКкЛлМмНН")
alleles_per_gene = parent1.mate(parent2)
for offspring in combinations(alleles_per_gene):
    offspring_gt = Genotype.from_list(offspring)
    if offspring_gt.startswith(prefix):
        print(offspring_gt)
    else:
        continue

# %%
# Ваш код здесь (4 подзадание)

offspring_wanted = "АаБбввГгДдЕеЖжЗзИиЙйккЛлМмНн"
parent_1 = "АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн"
parent_2 = "АаБбВвГгДдЕеЖжЗзИиЙйКкЛлМмНн"

print(get_offspring_genotype_probability(parent1=parent_1, parent2=parent_2, target_genotype=offspring_wanted))

# %%



