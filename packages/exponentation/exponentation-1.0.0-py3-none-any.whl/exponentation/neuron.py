from typing import Union, Any

import pandas as pd
import torch
import torch.nn as nn
import numpy as np
from pandas import DataFrame

from .methods import *
from .utils import get_key, is_prime

from .settings import train_data_file_path, model_path

train_data = pd.read_csv(train_data_file_path)


class Exponentation(nn.Module):
    def __init__(self):
        super(Exponentation, self).__init__()
        self.fc1 = nn.Linear(4, 32)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(32, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc_time = nn.Linear(64, 7)
        self.fc_memory = nn.Linear(64, 7)

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.relu(x)
        x = self.fc3(x)
        x = self.relu(x)

        time_prediction = self.fc_time(x)
        memory_prediction = self.fc_memory(x)

        return time_prediction, memory_prediction


model = Exponentation()
model.load_state_dict(torch.load(model_path))
# Перевод модели в режим оценки
model.eval()


def is_prime_list(numbers: list[int]) -> list[bool]:
    return [is_prime(num) for num in numbers]


methods_mapping = {
    "power_with_naive": 0,
    "accum": 1,
    "tree": 2,
    "binary": 3,
    "stairs": 4,
    "power_fact": 5,
    "right_left": 6,
}


def _get_normalized_array(
    list_: np.ndarray[Any, np.dtype],
    max_value: Union[int, float],
    min_value: Union[int, float],
) -> np.array:
    numpy_array = np.array(list_)
    return (numpy_array - min_value) / (max_value - min_value)


def _get_prediction(
    base: list[int, float], exponent: list[int], t_factor: list[int]
) -> tuple[list, list]:
    base = np.array(base)
    exponent = np.array(exponent)
    t_factor = np.array(t_factor)
    # Нормализация входных данных
    max_base = train_data.max().iloc[0]
    min_base = train_data.min().iloc[0]
    max_exp = train_data.max().iloc[1]
    min_exp = train_data.min().iloc[1]
    normalized_base = _get_normalized_array(
        list_=base, max_value=max_base, min_value=min_base
    )
    normalized_exp = _get_normalized_array(
        list_=exponent, max_value=max_exp, min_value=min_exp
    )
    input_data = (
        normalized_base,
        normalized_exp,
        t_factor,
        is_prime_list(normalized_exp),
    )
    # Создание тестового массива с правильной размерностью
    tester = np.vstack(input_data).T
    tester_torch = torch.tensor(tester, dtype=torch.float32)
    # Передача данных модели для предсказания
    with torch.no_grad():
        time_outputs, memory_outputs = model(tester_torch)
    # Определение индексов с максимальными значениями для времени и памяти
    predicted_time = torch.argmax(time_outputs, dim=1)
    predicted_memory = torch.argmax(memory_outputs, dim=1)
    # Получение предсказанных методов
    predicted_time_method = [
        get_key(methods_mapping, idx.item()) for idx in predicted_time
    ]
    predicted_memory_method = [
        get_key(methods_mapping, idx.item()) for idx in predicted_memory
    ]
    return predicted_time_method, predicted_memory_method


def get_best_methods(
    base: list[int, float],
    exponent: list[int],
    t_factor: list[int],
    by_time=True,
    by_memory=True,
) -> DataFrame:
    """
    ...
    """
    if not by_time and not by_memory:
        raise Exception("...")  # написать текст ошибки.
    predicted_time_method, predicted_memory_method = _get_prediction(
        base=base, exponent=exponent, t_factor=t_factor
    )
    df = pd.DataFrame(
        {
            "Base": base,
            "Exponent": exponent,
            "Consider Temperature": t_factor,
        }
    )
    if by_time:
        df["Best method time"] = predicted_time_method
    if by_memory:
        df["Best method memory"] = predicted_memory_method
    return df


def _calculate_result_by_best_method(
    df: DataFrame, by_time_method=True, by_memory_method=False
) -> tuple[list, list]:
    methods = {
        "power_with_naive": power_with_naive,
        "tree": tree,
        "accum": accum,
        "right_left": right_left,
        "stairs": stairs,
        "power_fact": power_fact,
        "binary": binary,
    }
    if not by_time_method and not by_memory_method:
        raise Exception("...")
    method_name = "Best method time" if by_time_method else "Best method memory"
    results = []
    method_names = []
    for _, row in df.iterrows():
        method = methods[row[method_name]]
        base = row["Base"]
        exponent = row["Exponent"]
        result = Decimal(str(method(base, exponent)))
        results.append(result)
        method_names.append(row[method_name])
    return results, method_names


def get_result_by_best_method(
    df: DataFrame, by_time_method=True, by_memory_method=False
) -> DataFrame:
    results, method_names = _calculate_result_by_best_method(
        df=df, by_time_method=by_time_method, by_memory_method=by_memory_method
    )
    df["Method"] = method_names
    df["Result"] = results
    df.drop(columns=["Best method memory"], inplace=True)
    df.drop(columns=["Best method time"], inplace=True)
    return df
