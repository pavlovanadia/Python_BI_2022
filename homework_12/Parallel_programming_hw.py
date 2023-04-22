# %% [markdown]
# В формулировке заданий будет использоваться понятие **worker**. Это слово обозначает какую-то единицу параллельного выполнения, в случае питона это может быть **поток** или **процесс**, выбирайте то, что лучше будет подходить к конкретной задаче

# %% [markdown]
# # Задание 1 (7 баллов)

# %% [markdown]
# В одном из заданий по ML от вас требовалось написать кастомную реализацию Random Forest. Её проблема состоит в том, что она работает медленно, так как использует всего один поток для работы. Добавление параллельного программирования в код позволит получить существенный прирост в скорости обучения и предсказаний.
# 
# В данном задании от вас требуется добавить возможность обучать случайный лес параллельно и использовать параллелизм для предсказаний. Для этого вам понадобится:
# 1. Добавить аргумент `n_jobs` в метод `fit`. `n_jobs` показывает количество worker'ов, используемых для распараллеливания
# 2. Добавить аргумент `n_jobs` в методы `predict` и `predict_proba`
# 3. Реализовать функционал по распараллеливанию в данных методах
# 
# В результате код `random_forest.fit(X, y, n_jobs=2)` и `random_forest.predict(X, y, n_jobs=2)` должен работать в ~1.5-2 раза быстрее, чем `random_forest.fit(X, y, n_jobs=1)` и `random_forest.predict(X, y, n_jobs=1)` соответственно
# 
# Если у вас по каким-то причинам нет кода случайного леса из ДЗ по ML, то вы можете написать его заново или попросить у однокурсника. *Детали* реализации ML части оцениваться не будут, НО, если вы поломаете логику работы алгоритма во время реализации параллелизма, то за это будут сниматься баллы
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона, а также функции и классы из **sklearn** при помощи которых вы изначально писали лес

# %%
from typing import Tuple, Any, Callable, Optional, Union, List

# %%
import numpy as np
import threading
from concurrent.futures import ThreadPoolExecutor
from sklearn.base import BaseEstimator
from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier

class RandomForestClassifierCustom(BaseEstimator):
    """
    A Random Forest Classifier.

    ...

    Attributes
    ----------
    n_estimators : int
        Number of trees in a forest, 10 by default.
    max_depth : int
        Maximum depth of trees, None by default.
    max_features : int
        Maximum feature number to split a node, None by default.
    random_state : int
        Random state, 111 by default.
    trees : list(DecisionTreeClassifier)
        List to save all classifiers of the forest.
    feat_ids_by_tree: list(np.ndarray)
        List to save feature ids of each tree.
    
    Methods
    -------
    __init__(self, n_estimators, max_depth, max_features, random_state)
        Constructs all the necessary attributes for the class object.

        Parameters
        ----------
        n_estimators : int
            Number of estimators, 10 by default.
        max_depth : int
            Maximum depth of a single tree, None by default.
        max_features : int
            Maximum feature number for a single tree, None by default.
        random_state : int
            Random state, 111 by default.

    fit(self, X, y, n_jobs)
        Trains model on the data given. 

        Parameters
        ----------
        X : np.ndarray
            Array of training features.
        y : np.ndarray
            Array of train targets.
        n_jobs : int
            Number of parallel processes, 1 by default.

        Returns
        -------
        RandomForestClassifierCustom object
            Fitted random forest.

    predict_proba(self, X, n_jobs)
        Predicts probabilities of given X to belong to each class.

        Parameters
        ----------
        X : np.ndarray
            Array of test features.
        n_jobs : int
            Number of parallel processes, 1 by default.

        Returns
        -------
        np.ndarray object
            Predicted probabilities of belonging to each class.

    predict(self, X, n_jobs)
        Predicts the class of each X observation.

        Parameters
        ----------
        X : np.ndarray
            Array of test features.
        n_jobs : int
            Number of parallel processes, 1 by default.

        Returns
        -------
        np.ndarray object
            Predicted class labels.
    """
    def __init__(self, 
                 n_estimators: int = 10, 
                 max_depth: int = None, 
                 max_features: int = None, 
                 random_state: int = 111):
        """
        Constructs all the necessary attributes for the class object.

        Parameters
        ----------
        n_estimators : int
            Number of estimators, 10 by default.
        max_depth : int
            Maximum depth of a single tree, None by default.
        max_features : int
            Maximum feature number for a single tree, None by default.
        random_state : int
            Random state, 111 by default.
        """
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.max_features = max_features
        self.random_state = random_state

        self.trees: List[DecisionTreeClassifier] = [] # точно ли тут нужен тупинг?
        self.feat_ids_by_tree: List[np.ndarray] = [] # и тут тоже?

    def fit(self, 
            X: np.ndarray, 
            y: np.ndarray, 
            n_jobs: int = 1) -> 'RandomForestClassifierCustom':
        """
        Trains model on the data given.

        Parameters
        ----------
        X : np.ndarray
            Array of training samples.
        y : np.ndarray
            Array of train targets.
        n_jobs : int
            Number of parallel processes, 1 by default.

        Returns
        -------
        RandomForestClassifierCustom object
            Fitted random forest.
        """
        self.classes_ = sorted(np.unique(y))

        def fit_tree(tree_num: int) -> Tuple[DecisionTreeClassifier, np.ndarray]:
            """
            Fits a single tree of a forest.

            Parameters
            ----------
            tree_num : int
                Number of the tree.
            
            Returns
            -------
            tuple(DecisionTreeClassifier, np.ndarray)
                Tuple of tree and features if was fit on.
            """
            rng = np.random.default_rng(seed=self.random_state + tree_num)
            mx_ftrs = rng.choice(X.shape[1], self.max_features, replace=False)
            psample = rng.choice(X.shape[0], X.shape[0] // 2, replace=True)
            psample_X = X[np.ix_(psample, mx_ftrs)]
            psample_y = y[psample]

            mdl = DecisionTreeClassifier(max_depth=self.max_depth,
                                         max_features=self.max_features,
                                         random_state=self.random_state)
            mdl.fit(psample_X, psample_y)
            return mdl, mx_ftrs 

        with ThreadPoolExecutor(max_workers=n_jobs) as executor: # ????? do i need typing here????
            tree_data = list(executor.map(fit_tree, range(self.n_estimators)))

        self.trees, self.feat_ids_by_tree = zip(*tree_data)

        return self

    def predict_proba(self, 
                      X: np.ndarray, 
                      n_jobs: int = 1) -> np.ndarray:
        """
        Predicts probabilities of given X to belong to each class.

        Parameters
        ----------
        X : np.ndarray
            Array of test features.
        n_jobs : int
            Number of parallel processes, 1 by default.

        Returns
        -------
        np.ndarray object
            Predicted probabilities of belonging to each class.
        """
        def tree_proba(tree_num: int) -> np.ndarray:
            """
            Calculates probabilities of observations to belong to each class
            with all trees in forest.

            Parameters
            ----------
            tree_num : int
                Number of the tree.

            Returns
            -------
            np.ndarray object
                Probabilities of oobservations to belong to each class.
            """
            return self.trees[tree_num].predict_proba(X[:, self.feat_ids_by_tree[tree_num]])

        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            y_proba = list(executor.map(tree_proba, range(self.n_estimators)))

        return np.array(y_proba).mean(axis=0)

    def predict(self, 
                X: np.ndarray, 
                n_jobs: int = 1) -> np.ndarray:
        """
        Predicts the class of each X observation.

        Parameters
        ----------
        X : np.ndarray
            Array of test features.
        n_jobs : int
            Number of parallel processes, 1 by default.

        Returns
        -------
        np.ndarray object
            Predicted class labels.
        """
        probas = self.predict_proba(X, n_jobs=n_jobs)
        predictions = np.argmax(probas, axis=1)

        return predictions
    

X, y = make_classification(n_samples=100000)

# %%
random_forest = RandomForestClassifierCustom(max_depth=30, n_estimators=10, max_features=2, random_state=42)

# %%
%%time

_ = random_forest.fit(X, y, n_jobs=1)

# %%
%%time

preds_1 = random_forest.predict(X, n_jobs=1)

# %%
random_forest = RandomForestClassifierCustom(max_depth=30, n_estimators=10, max_features=2, random_state=42)

# %%
%%time

_ = random_forest.fit(X, y, n_jobs=2)

# %%
%%time

preds_2 = random_forest.predict(X, n_jobs=2)

# %%
(preds_1 == preds_2).all()   # Количество worker'ов не должно влиять на предсказания

# %% [markdown]
# #### Какие есть недостатки у вашей реализации параллельного Random Forest (если они есть)? Как это можно исправить? Опишите словами, можно без кода (+1 дополнительный балл)

# %% [markdown]
# Ответ пишите тут

# %% [markdown]
# # Задание 2 (9 баллов)

# %% [markdown]
# Напишите декоратор `memory_limit`, который позволит ограничивать использование памяти декорируемой функцией.
# 
# Декоратор должен принимать следующие аргументы:
# 1. `soft_limit` - "мягкий" лимит использования памяти. При превышении функцией этого лимита должен будет отображён **warning**
# 2. `hard_limit` - "жёсткий" лимит использования памяти. При превышении функцией этого лимита должно будет брошено исключение, а функция должна немедленно завершить свою работу
# 3. `poll_interval` - интервал времени (в секундах) между проверками использования памяти
# 
# Требования:
# 1. Потребление функцией памяти должно отслеживаться **во время выполнения функции**, а не после её завершения
# 2. **warning** при превышении `soft_limit` должен отображаться один раз, даже если функция переходила через этот лимит несколько раз
# 3. Если задать `soft_limit` или `hard_limit` как `None`, то соответствующий лимит должен быть отключён
# 4. Лимиты должны передаваться и отображаться в формате `<number>X`, где `X` - символ, обозначающий порядок единицы измерения памяти ("B", "K", "M", "G", "T", ...)
# 5. В тексте warning'ов и исключений должен быть указан текщий объём используемой памяти и величина превышенного лимита
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона, можно писать вспомогательные функции и/или классы
# 
# В коде ниже для вас предопределены некоторые полезные функции, вы можете ими пользоваться, а можете не пользоваться

# %%
import os
import psutil
import time
import warnings
import concurrent.futures
from functools import wraps
import signal
import threading
from queue import Queue

def get_memory_usage() -> int:
    """
    Gets the actual memory usage of a process.
    
    Returns
    -------
    int
        The actual memory usage (bytes).
    """
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss


def bytes_to_human_readable(n_bytes: int) -> str: 
    """
    Converts bytes to a human readable format.
    
    Parameters
    ----------
    n_bytes : int
        The bytes number.
    
    Returns
    -------
    str
        A human readable representation of bytes.
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for idx, s in enumerate(symbols):
        prefix[s] = 1 << (idx + 1) * 10
    for s in reversed(symbols):
        if n_bytes >= prefix[s]:
            value = float(n_bytes) / prefix[s]
            return f"{value:.2f}{s}"
    return f"{n_bytes}B"


def human_readable_to_bytes(human_readable: str) -> int:
    """
    Converts human readable to bytes.
    
    Parameters
    ----------
    human_readable : str
        Number of bytes.
    
    Returns
    -------
    int
        The number of bytes.
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    number = float(human_readable[:-1])
    symbol = human_readable[-1]
    if symbol in symbols:
        return int(number * (1 << (symbols.index(symbol) + 1) * 10))
    return int(number)

def memory_check_function(
        soft_limit: Optional[int], 
        hard_limit: Optional[int], 
        poll_interval: float, 
        control_queue: Queue) -> Optional[str]:
    """
    Checks if the memory usage exceeds the limits.
    
    Parameters
    ----------
    soft_limit : Optional[int]
        Soft memory limit.
    hard_limit : Optional[int]
        Hard memory limit.
    poll_interval : float
        The time interval between checks.
    control_queue : Queue
        A queue to control when to stop the checks.
    
    Returns
    -------
    Optional[str]
        Was the hard limit exceeded or not.
    """
    soft_limit_warning_shown = False
    while True:
        if not control_queue.empty():
            break
        mem_usage = get_memory_usage()
        if soft_limit and (mem_usage > soft_limit) and not soft_limit_warning_shown:
            soft_limit_warning_shown = True
            warnings.warn(f"Warning! Memory usage exceeded soft limit ({bytes_to_human_readable(mem_usage)} > {bytes_to_human_readable(soft_limit)})")
        if hard_limit and (mem_usage > hard_limit):
            return 'hard_limit_exceeded'
        time.sleep(poll_interval)
    return None

class MemoryLimitExceeded(Exception):
    """
    exception class to handle for situation when usage exceeds the hard limit.
    """
    pass

def memory_limit(soft_limit: Optional[str] = None, hard_limit: Optional[str] = None, poll_interval: int = 1) -> Callable:
    """
    Decorator to check memory limits for a function.
    
    Parameters
    ----------
    soft_limit : Optional[str]
        Soft memory limit, human-readable, None by default..
    hard_limit : Optional[str]
        Hard memory limit, human-readable, None by default..
    poll_interval : int
        Time interval between memory usage checks, 1 by default..
    
    Returns
    -------
    Callable
        Wrapped function that checks memory limits.
    """
    def decorator(function: Callable) -> Callable:
        """
        Decorator function that wraps to check memory usage.

        Parameters
        ----------
        function : Callable
            The function for wrappimg.

        Returns
        -------
        Callable
            Wrapped function with memory usage ckeck.
        """
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper function that executes the input function and checks its memory usage.
            If memory usage exceeds the limits, warnings or exceptions will be raised.

            Parameters
            ----------
            *args : Any
                Positional arguments for the input function.
            **kwargs : Any
                Keyword arguments for the input function.

            Returns
            -------
            Any
                Value of input function.
            """
            nonlocal soft_limit, hard_limit 

            def memory_check() -> None: 
                """
                Monitors memory usage of process and checks if it exceeds the soft or hard limits.
                """
                nonlocal soft_limit_warning_shown 
                while not function_executed:
                    mem_usage = get_memory_usage() # how much memory is used
                    if soft_limit and (mem_usage > soft_limit) and not soft_limit_warning_shown:
                        soft_limit_warning_shown = True
                        warnings.warn(f"Memory usage exceeded soft limit ({bytes_to_human_readable(mem_usage)} > {bytes_to_human_readable(soft_limit)})")
                    if hard_limit and (mem_usage > hard_limit):
                        os.kill(os.getpid(), signal.SIGUSR1) # kills the the process
                    time.sleep(poll_interval)

            def handle_memory_limit_exceeded(signum: int, frame: Any) -> None:
                """
                Handles the signal that occurs when memory usage exceeds hard limit,
                raises an exception with a message if so.

                Parameters
                ----------
                signum : int
                    Signal number.
                frame : Any
                    Stack frame when the signal occured.
                """
                raise MemoryLimitExceeded(f"Memory usage exceeded hard limit ({bytes_to_human_readable(get_memory_usage())} > {bytes_to_human_readable(hard_limit)})")

            soft_limit_warning_shown = False
            if soft_limit:
                soft_limit = human_readable_to_bytes(soft_limit)
            if hard_limit:
                hard_limit = human_readable_to_bytes(hard_limit)

            signal.signal(signal.SIGUSR1, handle_memory_limit_exceeded) # takes the signal and calls the handle fnction
            function_executed = False
            monitor_thread = threading.Thread(target=memory_check)
            monitor_thread.daemon = True
            monitor_thread.start()

            try:
                result = function(*args, **kwargs)
            except MemoryLimitExceeded as e:
                print(e)
                result = None
            finally:
                function_executed = True

            return result
        return wrapper
    return decorator


# %%
@memory_limit(soft_limit="100M", hard_limit="1000M", poll_interval=0.1)
def memory_increment() -> List[int]:
    """
    Функция для тестирования
    
    В течение нескольких секунд достигает использования памяти 1.89G
    Потребление памяти и скорость накопления можно варьировать, изменяя код

    Returns
    -------
    list
    """
    lst = []
    for i in range(50000000):
        if i % 500000 == 0:
            time.sleep(0.1)
        lst.append(i)
    return lst

_ = memory_increment()


# %% [markdown]
# # Задание 3 (11 баллов)

# %% [markdown]
# Напишите функцию `parallel_map`. Это должна быть **универсальная** функция для распараллеливания, которая эффективно работает в любых условиях.
# 
# Функция должна принимать следующие аргументы:
# 1. `target_func` - целевая функция (обязательный аргумент)
# 2. `args_container` - контейнер с позиционными аргументами для `target_func` (по-умолчанию `None` - позиционные аргументы не передаются)
# 3. `kwargs_container` - контейнер с именованными аргументами для `target_func` (по-умолчанию `None` - именованные аргументы не передаются)
# 4. `n_jobs` - количество workers, которые будут использованы для выполнения (по-умолчанию `None` - количество логических ядер CPU в системе)
# 
# Функция должна работать аналогично `***PoolExecutor.map`, применяя функцию к переданному набору аргументов, но с некоторыми дополнениями и улучшениями
#     
# Поскольку мы пишем **универсальную** функцию, то нам нужно будет выполнить ряд требований, чтобы она могла логично и эффективно работать в большинстве ситуаций
# 
# 1. `target_func` может принимать аргументы любого вида в любом количестве
# 2. Любые типы данных в `args_container`, кроме `tuple`, передаются в `target_func` как единственный позиционный аргумент. `tuple` распаковываются в несколько аргументов
# 3. Количество элементов в `args_container` должно совпадать с количеством элементов в `kwargs_container` и наоборот, также значение одного из них или обоих может быть равно `None`, в иных случаях должна кидаться ошибка (оба аргумента переданы, но размеры не совпадают)
# 
# 4. Функция должна выполнять определённое количество параллельных вызовов `target_func`, это количество зависит от числа переданных аргументов и значения `n_jobs`. Сценарии могут быть следующие
#     + `args_container=None`, `kwargs_container=None`, `n_jobs=None`. В таком случае функция `target_func` выполнится параллельно столько раз, сколько на вашем устройстве логических ядер CPU
#     + `args_container=None`, `kwargs_container=None`, `n_jobs=5`. В таком случае функция `target_func` выполнится параллельно **5** раз
#     + `args_container=[1, 2, 3]`, `kwargs_container=None`, `n_jobs=5`. В таком случае функция `target_func` выполнится параллельно **3** раза, несмотря на то, что `n_jobs=5` (так как есть всего 3 набора аргументов для которых нам нужно получить результат, а лишние worker'ы создавать не имеет смысла)
#     + `args_container=None`, `kwargs_container=[{"s": 1}, {"s": 2}, {"s": 3}]`, `n_jobs=5`. Данный случай аналогичен предыдущему, но здесь мы используем именованные аргументы
#     + `args_container=[1, 2, 3]`, `kwargs_container=[{"s": 1}, {"s": 2}, {"s": 3}]`, `n_jobs=5`. Данный случай аналогичен предыдущему, но здесь мы используем и позиционные, и именованные аргументы
#     + `args_container=[1, 2, 3, 4]`, `kwargs_container=None`, `n_jobs=2`. В таком случае в каждый момент времени параллельно будет выполняться **не более 2** функций `target_func`, так как нам нужно выполнить её 4 раза, но у нас есть только 2 worker'а.
#     + В подобных случаях (из примера выше) должно оптимизироваться время выполнения. Если эти 4 вызова выполняются за 5, 1, 2 и 1 секунды, то параллельное выполнение с `n_jobs=2` должно занять **5 секунд** (не 7 и тем более не 10)
# 
# 5. `parallel_map` возвращает результаты выполнения `target_func` **в том же порядке**, в котором были переданы соответствующие аргументы
# 6. Работает с функциями, созданными внутри других функций
# 
# Для базового решения от вас не ожидается **сверххорошая** оптимизация по времени и памяти для всех возможных случаев. Однако за хорошо оптимизированную логику работы можно получить до **+3 дополнительных баллов**
# 
# Вы можете сделать класс вместо функции, если вам удобнее
# 
# В задании можно использовать только модули из **стандартной библиотеки** питона
# 
# Ниже приведены тестовые примеры по каждому из требований

# %%
import itertools

# %%
from typing import Callable, List, Tuple, Dict, Any, Optional, Union

def parallel_map(target_func: Callable[..., Any],
                 args_container: Optional[Union[List[Tuple], Tuple]] = None,
                 kwargs_container: Optional[List[Dict[str, Any]]] = None,
                 n_jobs: Optional[int] = None) -> List[Any]:
    """
    Puts args and kwargs in function.

    Parameters
    ----------
    target_func : Callable[..., Any]
        The function to be executed.
    args_container : Optional[Union[List[Tuple], Tuple]]
        List of tuples with args, None by default.
    kwargs_container : Optional[List[Dict[str, Any]]]
        List of dictionaries with kwargs, None by default.
    n_jobs : Optional[int]
        The number of threads, None by default.

    Returns
    -------
    List[Any]
        List of results of function with arguments and keyword arguments.
    """
    
    if n_jobs is None:
        n_jobs = os.cpu_count()

    if args_container is None and kwargs_container is None:
        args_container = [tuple() for _ in range(n_jobs)]

    if args_container is None:
        args_container = list(itertools.repeat(tuple(), len(kwargs_container)))

    if kwargs_container is None:
        kwargs_container = list(itertools.repeat(dict(), len(args_container)))

    if len(args_container) != len(kwargs_container):
        raise ValueError("Lengths of args_container and kwargs_container must match.")

    tasks = zip((tuple([arg]) if not isinstance(arg, tuple) else arg for arg in args_container), kwargs_container)

    def apply_args_and_kwargs(args: Tuple, kwargs: Dict[str, Any]) -> Any:
        """
        Applies the target function to on set of args and kwargs.

        Parameters
        ----------
        args : Tuple
            Positional arguments to be passed to function.
        kwargs : Dict[str, Any]
            Keyword arguments to be passed to function.

        Returns
        -------
        Any
            Result of function executing with args and kwargs.
        """
        return target_func(*args, **kwargs)

    with concurrent.futures.ThreadPoolExecutor(max_workers=n_jobs) as executor: 
        futures = [executor.submit(apply_args_and_kwargs, args, kwargs) for args, kwargs in tasks] 
        results = [future.result() for future in futures] 

    return results

# %%
import time


# Это только один пример тестовой функции, ваша parallel_map должна уметь эффективно работать с ЛЮБЫМИ функциями
# Поэтому обязательно протестируйте код на чём-нибудбь ещё
def test_func(x: Optional[int] = 1,
              s: Optional[int] = 2,
              a: Optional[int] = 1,
              b: Optional[int] = 1,
              c: Optional[int] = 1) -> int:
    """
    Quadric equasion.

    Parameters
    ----------
    x : Optional[int]
        x, 1 by default.
    s : Optional[int]
        s, 2 by default.
    a : Optional[int]
        a, 1 by default.
    b : Optional[int]
        b, 1 by default.
    c : Optional[int]
        c, 1 by default.

    Returns
    -------
    int
        Some number for function test.
    """
    time.sleep(s)
    return a*x**2 + b*x + c

# %%
%%time

# Пример 2.1
# Отдельные значения в args_container передаются в качестве позиционных аргументов
parallel_map(test_func, args_container=[1, 2.0, 3j-1, 4])   # Здесь происходят параллельные вызовы: test_func(1) test_func(2.0) test_func(3j-1) test_func(4)

# %%
%%time

# Пример 2.2
# Элементы типа tuple в args_container распаковываются в качестве позиционных аргументов
parallel_map(test_func, [(1, 1), (2.0, 2), (3j-1, 3), 4])    # Здесь происходят параллельные вызовы: test_func(1, 1) test_func(2.0, 2) test_func(3j-1, 3) test_func(4)

# %%
%%time

# Пример 3.1
# Возможна одновременная передача args_container и kwargs_container, но количества элементов в них должны быть равны
parallel_map(test_func,
             args_container=[1, 2, 3, 4],
             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}, {"s": 3}])

# Здесь происходят параллельные вызовы: test_func(1, s=3) test_func(2, s=3) test_func(3, s=3) test_func(4, s=3)

# %%
%%time

# Пример 3.2
# args_container может быть None, а kwargs_container задан явно
parallel_map(test_func,
             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}, {"s": 3}])

# %%
%%time

# Пример 3.3
# kwargs_container может быть None, а args_container задан явно
parallel_map(test_func,
             args_container=[1, 2, 3, 4])

# %%
%%time

# Пример 3.4
# И kwargs_container, и args_container могут быть не заданы
parallel_map(test_func)

# %%
%%time

# Пример 3.5
# При несовпадении количеств позиционных и именованных аргументов кидается ошибка
parallel_map(test_func,
             args_container=[1, 2, 3, 4],
             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}])

# %%
%%time

# Пример 4.1
# Если функция не имеет обязательных аргументов и аргумент n_jobs не был передан, то она выполняется параллельно столько раз, сколько ваш CPU имеет логических ядер
# В моём случае это 24, у вас может быть больше или меньше
parallel_map(test_func)

# %%
%%time

# Пример 4.2
# Если функция не имеет обязательных аргументов и передан только аргумент n_jobs, то она выполняется параллельно n_jobs раз
parallel_map(test_func, n_jobs=2)

# %%
%%time

# Пример 4.3
# Если аргументов для target_func указано МЕНЬШЕ, чем n_jobs, то используется такое же количество worker'ов, сколько было передано аргументов
parallel_map(test_func,
             args_container=[1, 2, 3],
             n_jobs=5)   # Здесь используется 3 worker'a

# %%
%%time

# Пример 4.4
# Аналогичный предыдущему случай, но с именованными аргументами
parallel_map(test_func,
             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}],
             n_jobs=5)   # Здесь используется 3 worker'a

# %%
%%time

# Пример 4.5
# Комбинация примеров 4.3 и 4.4 (переданы и позиционные и именованные аргументы)
parallel_map(test_func,
             args_container=[1, 2, 3],
             kwargs_container=[{"s": 3}, {"s": 3}, {"s": 3}],
             n_jobs=5)   # Здесь используется 3 worker'a

# %%
%%time

# Пример 4.6
# Если аргументов для target_func указано БОЛЬШЕ, чем n_jobs, то используется n_jobs worker'ов
parallel_map(test_func,
             args_container=[1, 2, 3, 4],
             kwargs_container=None,
             n_jobs=2)   # Здесь используется 2 worker'a

# %%
%%time

# Пример 4.7
# Время выполнения оптимизируется, данный код должен отрабатывать за 5 секунд
parallel_map(test_func,
             kwargs_container=[{"s": 5}, {"s": 1}, {"s": 2}, {"s": 1}],
             n_jobs=2)

# %%
def test_func2(string, sleep_time=1):
    time.sleep(sleep_time)
    return string

# Пример 5
# Результаты возвращаются в том же порядке, в котором были переданы соответствующие аргументы вне зависимости от того, когда завершился worker
arguments = ["first", "second", "third", "fourth", "fifth"]
parallel_map(test_func2,
             args_container=arguments,
             kwargs_container=[{"sleep_time": 5}, {"sleep_time": 4}, {"sleep_time": 3}, {"sleep_time": 2}, {"sleep_time": 1}])

# %%
%%time


def test_func3():
    def inner_test_func(sleep_time):
        time.sleep(sleep_time)
    return parallel_map(inner_test_func, args_container=[1, 2, 3])

# Пример 6
# Работает с функциями, созданными внутри других функций
test_func3()


