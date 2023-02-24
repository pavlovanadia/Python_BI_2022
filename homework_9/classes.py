# %% [markdown]
# # Задание 1 (5 баллов)

# %% [markdown]
# Напишите классы **Chat**, **Message** и **User**. Они должны соответствовать следующим требованиям:
# 
# **Chat**:
# + Должен иметь атрибут `chat_history`, где будут храниться все сообщения (`Message`) в обратном хронологическом порядке (сначала новые, затем старые)
# + Должен иметь метод `show_last_message`, выводящий на экран информацию о последнем сообщении
# + Должен иметь метод `get_history_from_time_period`, который принимает два опциональных аргумента (даты с которой и по какую мы ищем сообщения и выдаём их). Метод также должен возвращать объект типа `Chat`
# + Должен иметь метод `show_chat`, выводящий на экран все сообщения (каждое сообщение в таком же виде как и `show_last_message`, но с разделителем между ними)
# + Должен иметь метод `recieve`, который будет принимать сообщение и добавлять его в чат
# 
# **Message**:
# + Должен иметь три обязательных атрибута
#     + `text` - текст сообщения
#     + `datetime` - дата и время сообщения (встроенный модуль datetime вам в помощь). Важно! Это должна быть не дата создания сообщения, а дата его попадания в чат! 
#     + `user` - информация о пользователе, который оставил сообщение (какой тип данных использовать здесь, разберётесь сами)
# + Должен иметь метод `show`, который печатает или возвращает информацию о сообщении с необходимой информацией (дата, время, юзер, текст)
# + Должен иметь метод `send`, который будет отправлять сообщение в чат
# 
# **User**:
# + Класс с информацией о юзере, наполнение для этого класса придумайте сами
# 
# Напишите несколько примеров использования кода, которое показывает взаимодействие между объектами.
# 
# В тексте задания намерено не указано, какие аргументы должны принимать методы, пускай вам в этом поможет здравый смысл)
# 
# В этом задании не стоит флексить всякими продвинутыми штуками, для этого есть последующие
# 
# В этом задании можно использовать только модуль `datetime`

# %%
from datetime import datetime as dt

# %%
class Chat:
    def __init__(self):
        self.chat_history = []

    def show_last_message(self):
        if len(self.chat_history) > 0:
            return self.chat_history[0]
        print('<No messages in the chat>')
        return None
    
    def get_history_from_time_period(self, start_time=None, end_time=None):
        if start_time is None:
            start_time = self.chat_history[-1].datetime
        if end_time is None:
            end_time = self.chat_history[0].datetime
        chat_period = [msg for msg in self.chat_history if start_time <= msg.datetime <= end_time]
        chat_2 = Chat()
        chat_2.chat_history = chat_period
        return chat_2

    def show_chat(self):
        if len(self.chat_history) == 0:
            print('<The chat is empty>')
        for msg in self.chat_history[::-1]:
            msg.show()
            print()
    
    def receive(self, msg):
        msg.datetime = dt.now()
        self.chat_history.insert(0, msg)
    


class Message:
    def __init__(self, user, message, datetime=None):
        self.user = user.username
        self.message = message
        self.datetime = datetime
    
    def __str__(self):
        return (f'{self.datetime}'
                '\n'
                f'{self.user}:'
                '\n'
                f'{self.message}')

    def __repr__(self):
        return (f'{self.datetime}'
                '\n'
                f'{self.user}:'
                '\n'
                f'{self.message}')
    
    def show(self):
        print(f'user: {self.user}' 
                '\n'
                f'sent on: {self.datetime}'
                '\n'
                f'message: {self.message}')

    def send(self, chat_obj):
        chat_obj.receive(self)



class User:
    def __init__(self, username, name, lastname, birthdate, status):
        self.username = username
        self.name = name
        self.lastname = lastname
        self.birthdate = birthdate
        self.status = status
    
    def __str__(self):
        return f'{self.name} {self.lastname} ({self.username}) *{self.status}*'

    def __repr__(self):
        return f'<username: {self.username}; name: {self.name} {self.lastname}; birth: {self.birthdate}; status: {self.status}>'

# %%
didi = User("didi", "Vladimir", "Beckett", 1952, "promised salvation")
gogo = User("gogo", "Estragon", "Beckett", 1952, "never arrives")

# %%
msg_1 = Message(didi, "Gogo.")
msg_2 = Message(gogo, "What?")
msg_3 = Message(didi, "Suppose we repented.")
msg_4 = Message(gogo, "Repented what?")
msg_5 = Message(didi, "Oh....")
msg_6 = Message(didi, "We wouldn't have to go into the details.")

# %%
my_fav_quote_ever = Chat()

# %%
didi

# %%
gogo

# %%
print(msg_1)

# %%
msg_1.send(my_fav_quote_ever)

# %%
my_fav_quote_ever.show_last_message()

# %%
my_fav_quote_ever.show_chat()

# %%
msg_2.send(my_fav_quote_ever)

# %%
my_fav_quote_ever.show_last_message()

# %%
my_fav_quote_ever.show_chat()

# %%
msg_3.send(my_fav_quote_ever)
msg_4.send(my_fav_quote_ever)
msg_5.send(my_fav_quote_ever)
msg_6.send(my_fav_quote_ever)

# %%
my_fav_quote_ever.show_chat()

# %%
msg_1.show()

# %%
msg_3.show()

# %% [markdown]
# to check how get_history_from_time_period works, just set the datetime parameters below according to the two messaged information above

# %%
my_fav_quote_ever.get_history_from_time_period(
    start_time=dt(2023, 2, 23, 22, 20, 39), 
    end_time=dt(2023, 2, 24, 1, 39, 32)).show_chat()

# %% [markdown]
# # Задание 2 (3 балла)

# %% [markdown]
# В питоне как-то слишком типично и неинтересно происходят вызовы функций. Напишите класс `Args`, который будет хранить в себе аргументы, а функции можно будет вызывать при помощи следующего синтаксиса.
# 
# Использовать любые модули **нельзя**, да и вряд-ли это как-то поможет)

# %%
class Args:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __rlshift__(self, func):
        return func(*self.args, **self.kwargs)

# %%
sum << Args([1, 2])

# %%
(lambda a, b, c: a**2 + b + c) << Args(1, 2, c=50)

# %% [markdown]
# # Задание 3 (5 баллов)

# %% [markdown]
# Сделайте класс наследник `float`. Он должен вести себя как `float`, но также должен обладать некоторыми особенностями:
# + При получении атрибутов формата `<действие>_<число>` мы получаем результат такого действия над нашим числом
# + Создавать данные атрибуты в явном виде, очевидно, не стоит
# 
# Подсказка: если в процессе гуглёжки, вы выйдете на такую тему как **"Дескрипторы", то это НЕ то, что вам сейчас нужно**
# 
# Примеры использования ниже

# %%
class StrangeFloat(float):
    def __init__(self, val):
        super().__init__()
        self.val = val

    def __getattribute__(self, name):
        try:
            action, num = name.split("_")
            num = float(num)
        except ValueError:
            return super().__getattribute__(name)
    
        if action == "add":
            return StrangeFloat(self.val + num)
        elif action == "subtract":
            return StrangeFloat(self.val - num)
        elif action == "multiply":
            return StrangeFloat(self.val * num)
        elif action == "divide":
            return StrangeFloat(self.val / num)
        else:
            raise NotImplementedError(f'Cannot find action {action} for strangefloat')

# %%
number = StrangeFloat(3.5)

# %%
number.add_1

# %%
number.subtract_20

# %%
number.multiply_5

# %%
number.divide_25

# %%
number.add_1.add_2.multiply_6.divide_8.subtract_9

# %%
getattr(number, "add_-2.5")   # Используем getattr, так как не можем написать number.add_-2.5 - это SyntaxError

# %%
number + 8   # Стандартные для float операции работают также

# %%
number.as_integer_ratio()   # Стандартные для float операции работают также  (это встроенный метод float, писать его НЕ НАДО)

# %%
number.imag

# %% [markdown]
# # Задание 4 (3 балла)

# %% [markdown]
# В данном задании мы немного отдохнём и повеселимся. От вас требуется заменить в данном коде максимально возможное количество синтаксических конструкций на вызовы dunder методов, dunder атрибутов и dunder переменных.
# 
# Маленькая заметка: полностью всё заменить невозможно. Например, `function()` можно записать как `function.__call__()`, но при этом мы всё ещё не избавляемся от скобочек, так что можно делать так до бесконечности `function.__call__.__call__.__call__.__call__.....__call__()` и при всём при этом мы ещё не избавляемся от `.` для доступа к атрибутам. В общем, замените всё, что получится, не закапываясь в повторы, как в приведённом примере. Чем больше разных методов вы найдёте и используете, тем лучше и тем выше будет балл
# 
# Код по итогу дожен работать и печатать число **4420.0**, как в примере. Структуру кода менять нельзя, просто изменяем конструкции на синонимичные
# 
# И ещё маленькая подсказка. Заменить здесь можно всё кроме:
# + Конструкции `for ... in ...`:
# + Синтаксиса создания лямбда функции
# + Оператора присваивания `=`
# + Конструкции `if-else`

# %%
import numpy as np


matrix = []
for idx in range(0, 100, 10):
    matrix += [list(range(idx, idx + 10))]
    
selected_columns_indices = list(filter(lambda x: x in range(1, 5, 2), range(len(matrix))))
selected_columns = map(lambda x: [x[col] for col in selected_columns_indices], matrix)

arr = np.array(list(selected_columns))

mask = arr[:, 1] % 3 == 0
new_arr = arr[mask]

product = new_arr @ new_arr.T

if (product[0] < 1000).all() and (product[2] > 1000).any():
    print(product.mean())

# %%
# Ваш код здесь
np = __import__("numpy")

matrix = list.__call__()
for idx in range.__call__(0, 100, 10):
    matrix.__iadd__([list.__call__(range.__call__(idx, idx.__add__(10)))])
    
selected_columns_indices = list.__call__(filter.__call__(lambda x: x in range(1, 5, 2), range.__call__(matrix.__len__())))
selected_columns = map.__call__(lambda x: list.__call__(x.__getitem__(col) for col in selected_columns_indices), matrix)

arr = np.array(list.__call__(selected_columns))

mask = arr.__getitem__((slice.__call__(None), 1)).__mod__(3).__eq__(0)
new_arr = arr.__getitem__(mask)

product = new_arr.__matmul__(new_arr.T)

if all.__call__((product.__getitem__(0).__lt__(1000))).__and__(any.__call__((product.__getitem__(2).__gt__(1000)))):
    print.__call__(product.mean())

# %% [markdown]
# # Задание 5 (10 баллов)

# %% [markdown]
# Напишите абстрактный класс `BiologicalSequence`, который задаёт следующий интерфейс:
# + Работа с функцией `len`
# + Возможность получать элементы по индексу и делать срезы последовательности (аналогично строкам)
# + Вывод на печать в удобном виде и возможность конвертации в строку
# + Возможность проверить алфавит последовательности на корректность
# 
# Напишите класс `NucleicAcidSequence`:
# + Данный класс реализует интерфейс `BiologicalSequence`
# + Данный класс имеет новый метод `complement`, возвращающий комплементарную последовательность
# + Данный класс имеет новый метод `gc_content`, возвращающий GC-состав (без разницы, в процентах или в долях)
# 
# Напишите классы наследники `NucleicAcidSequence`: `DNASequence` и `RNASequence`
# + `DNASequence` должен иметь метод `transcribe`, возвращающий транскрибированную РНК-последовательность
# + Данные классы не должны иметь <ins>публичных методов</ins> `complement` и метода для проверки алфавита, так как они уже должны быть реализованы в `NucleicAcidSequence`.
# 
# Напишите класс `AminoAcidSequence`:
# + Данный класс реализует интерфейс `BiologicalSequence`
# + Добавьте этому классу один любой метод, подходящий по смыслу к аминокислотной последовательности. Например, метод для нахождения изоэлектрической точки, молекулярного веса и т.д.
# 
# Комментарий по поводу метода `NucleicAcidSequence.complement`, так как я хочу, чтобы вы сделали его опредедённым образом:
# 
# При вызове `dna.complement()` или условного `dna.check_alphabet()` должны будут вызываться соответствующие методы из `NucleicAcidSequence`. При этом, данный метод должен обладать свойством полиморфизма, иначе говоря, внутри `complement` не надо делать условия а-ля `if seuqence_type == "DNA": return self.complement_dna()`, это крайне не гибко. Данный метод должен опираться на какой-то общий интерфейс между ДНК и РНК. Создание экземпляров `NucleicAcidSequence` не подразумевается, поэтому код `NucleicAcidSequence("ATGC").complement()` не обязан работать, а в идеале должен кидать исключение `NotImplementedError` при вызове от экземпляра `NucleicAcidSequence`
# 
# Вся сложность задания в том, чтобы правильно организовать код. Если у вас есть повторяющийся код в сестринских классах или родительском и дочернем, значит вы что-то делаете не так.
# 
# 
# Маленькое замечание: По-хорошему, между классом `BiologicalSequence` и классами `NucleicAcidSequence` и `AminoAcidSequence`, ещё должен быть класс-прослойка, частично реализующий интерфейс `BiologicalSequence`, но его писать не обязательно, так как задание и так довольно большое (правда из-за этого у вас неминуемо возникнет повторяющийся код в классах `NucleicAcidSequence` и `AminoAcidSequence`)

# %%
from abc import ABC, abstractmethod

class BiologicalSequence(ABC):
    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def is_valid_alphabet(self):
        pass

class BioSeqInterface(BiologicalSequence):
    def __init__(self, sequence):
        self.sequence = sequence.upper()
    
    def __len__(self):
        return len(self.sequence)
    
    def __getitem__(self, index):
        return self.sequence.__getitem__(index)
    
    def __str__(self):
        return str(self.sequence)
    
class NucleicAcidSequence(BioSeqInterface):
    def __init__(self, sequence):
        super().__init__(sequence)
        self.compl_rule = None

    def is_valid_alphabet(self):
        if self.compl_rule is None:
            raise NotImplementedError
        ncltds = set(self.sequence)
        right_nucltds = set(self.compl_rule.keys())
        if len(ncltds.difference(right_nucltds)) != 0:
            return False
        return True
    
    def complement(self):
        if self.compl_rule == None:
            raise NotImplementedError
        compl_seq = [self.compl_rule[nucl] for nucl in self.sequence]
        return "".join(compl_seq)
    
    def gc_content(self):
        gc_count = self.sequence.count("G") + self.sequence.count("C")
        gc_cont = 100 * gc_count / len(self.sequence)
        return gc_cont
    
class DNASequence(NucleicAcidSequence):
    def __init__(self, sequence):
        super().__init__(sequence)
        self.compl_rule = {
            "A": "T",
            "T": "A",
            "G": "C",
            "C": "G",
            "N": "N"
        }

    def transcribe(self):
        transcribe_rule = {
            "A": "U",
            "T": "A",
            "G": "C",
            "C": "G",
            "N": "N"
        }
        transcribe_result = [transcribe_rule[nucl] for nucl in self.sequence]
        return "".join(transcribe_result)

class RNASequence(NucleicAcidSequence):
    def __init__(self, sequence):
        super().__init__(sequence)
        self.compl_rule = {
            "A": "U",
            "U": "A",
            "G": "C",
            "C": "G",
            "N": "N"
        }

    def reverse_transcribe(self):
        rev_transcribe_rule = {
            "U": "A",
            "A": "T",
            "G": "C",
            "C": "G",
            "N": "N"
        }
        rev_transcribe_result = [rev_transcribe_rule[nucl] for nucl in self.sequence]
        return "".join(rev_transcribe_result)
    
class AminoAcidSequence(BioSeqInterface):
    def __init__(self, sequence):
        super().__init__(sequence)

    def is_valid_alphabet(self):
        self_aminoacids = set(self.sequence)
        aminoacids = set("ACDEFGHIKLMNPQRSTVWY")
        not_aminoacids = self_aminoacids.difference(aminoacids)
        return len(not_aminoacids) == 0
    
    def molecular_weight(self):
        aminoacid_weight = {
            "A": 89.09, "C": 121.16, "D": 133.10, "E": 147.13,
            "F": 165.19, "G": 75.07, "H": 155.16, "I": 131.17,
            "K": 146.19, "L": 131.17, "M": 149.21, "N": 132.12,
            "P": 115.13, "Q": 146.15, "R": 174.20, "S": 105.09,
            "T": 119.12, "V": 117.15, "W": 204.23, "Y": 181.19
        }
        prot_weight = sum([aminoacid_weight[aminoacid] for aminoacid in self.sequence])
        return prot_weight

# %%
NucleicAcidSequence("ATCGCGATCG")[2:5]

# %%
len(NucleicAcidSequence("ATCGCGATCG"))

# %%
DNASequence("ATGCGCT").complement()

# %%
RNASequence("UUAGCUG").complement()

# %%
len(RNASequence("UUAGCUG"))

# %%
NucleicAcidSequence("ATCGCGATCG").complement()

# %%
NucleicAcidSequence("ATCGCGATCG").is_valid_alphabet()

# %%



