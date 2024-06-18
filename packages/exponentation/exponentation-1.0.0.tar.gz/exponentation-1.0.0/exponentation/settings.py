import os

# Получить абсолютный путь к текущему файлу
current_directory = os.path.dirname(os.path.abspath(__file__))

# Создать путь к файлу данных
train_data_file_path = os.path.join(current_directory, "data", "Data_learning.csv")
model_path = os.path.join(current_directory, "data", "my_model.pth")
