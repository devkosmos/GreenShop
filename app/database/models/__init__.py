# Импортируйте все модели из отдельных файлов
from database.models.user import Users
from database.models.catalog import Category, Products, Category  # или другие модели из catalog.py

# Можно также сделать автоматический импорт
# __all__ = ['User', 'Catalog', 'Product', 'Category']