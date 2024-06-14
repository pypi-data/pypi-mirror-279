import asyncpg
from typing import Dict, Optional, List, Union
import logging


class DatabaseManager:
    """
    Класс для управления базой данных PostgreSQL с использованием библиотеки asyncpg.
    """

    def __init__(self, deletion_password: str,
                 dsn: Optional[str] = None,
                 host: Optional[str] = None,
                 port: Optional[int] = None,
                 user: Optional[str] = None,
                 password: Optional[str] = None,
                 database: Optional[str] = None):
        """
        Инициализация менеджера базы данных.

        :param dsn: Строка DSN для подключения к базе данных.
        :param deletion_password: Пароль для удаления данных или таблиц.
        :param host: Хост базы данных.
        :param port: Порт базы данных.
        :param user: Имя пользователя базы данных.
        :param password: Пароль базы данных.
        :param database: Имя базы данных.
        """
        self.dsn = dsn
        self.deletion_password = deletion_password
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

        self.dsn_flag = bool(dsn)

        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    async def __aenter__(self):
        """
        Устанавливает соединение с базой данных при входе в асинхронный контекстный менеджер.
        """
        try:
            if self.dsn_flag:
                self.connection = await asyncpg.connect(dsn=self.dsn)
            else:
                self.connection = await asyncpg.connect(
                    host=self.host,
                    port=self.port,
                    user=self.user,
                    password=self.password,
                    database=self.database
                )
            self.logger.info("Соединение с базой данных установлено.")
        except asyncpg.PostgresError as e:
            self.logger.error(f"Ошибка при подключении к базе данных: {e}")
            raise
        return self

    async def __aexit__(self, exc_type, exc, tb):
        """
        Закрывает соединение с базой данных при выходе из асинхронного контекстного менеджера.
        """
        if self.connection:
            try:
                await self.connection.close()
                self.logger.info("Соединение с базой данных закрыто.")
            except asyncpg.PostgresError as e:
                self.logger.error(f"Ошибка при закрытии соединения с базой данных: {e}")

    async def create_table(self, table_name: str, columns: List[str], debug: bool = False):
        """
        Создает таблицу в базе данных.

        :param table_name: Имя таблицы.
        :param debug: Выводит дебагом sql запрос.
        :param columns: Список строк, определяющих столбцы таблицы.
        """
        try:
            async with self.connection.transaction():
                columns_clause = ', '.join(columns)
                query = f'CREATE TABLE IF NOT EXISTS {table_name} ({columns_clause});'
                if debug:
                    self.logger.debug(f'SQL запрос: {query}')
                await self.connection.execute(query)
                self.logger.info(f"Таблица {table_name} успешно создана.")
        except asyncpg.PostgresError as e:
            self.logger.error(f"Возникла ошибка при создании таблицы {table_name}. Детали: {e}")

    async def select_data(self, table_name: str, where_dict: Optional[Union[Dict, List[Dict]]] = None,
                          columns: Optional[List[str]] = None, one_dict: bool = False,
                          debug: bool = False) -> Union[List[Dict], Dict]:
        """
        Извлекает данные из таблицы базы данных.

        :param table_name: Имя таблицы.
        :param where_dict: Условия для фильтрации данных.
        :param columns: Список столбцов для извлечения.
        :param one_dict: Возвращать ли только одну запись в виде словаря.
        :param debug: Выводит дебагом SQL запрос и параметры.
        :return: Список словарей с данными или один словарь, если one_dict=True.
        """
        try:
            async with self.connection.transaction():
                column_names = ', '.join(columns) if columns else '*'
                where_clause = ''
                all_values = []
                if where_dict:
                    if isinstance(where_dict, dict):
                        conditions = ' AND '.join(f"{key} = ${i + 1}" for i, key in enumerate(where_dict.keys()))
                        where_clause = f' WHERE {conditions}'
                        all_values = list(where_dict.values())
                    elif isinstance(where_dict, list):
                        where_clauses = []
                        index = 1
                        for condition in where_dict:
                            where_clauses.append(
                                ' AND '.join(f"{key} = ${index + i}" for i, key in enumerate(condition.keys())))
                            index += len(condition)
                            all_values.extend(condition.values())
                        where_clause = ' WHERE (' + ') OR ('.join(where_clauses) + ')'
                query = f'SELECT {column_names} FROM {table_name}{where_clause};'

                if debug:
                    self.logger.debug(f'SQL запрос: {query}')
                    self.logger.debug(f'Параметры запроса: {all_values}')

                rows = await self.connection.fetch(query, *all_values)
                all_data = [dict(row) for row in rows]

                if one_dict and all_data:
                    self.logger.info(f"Успешно получили одну запись из таблицы {table_name}.")
                    return all_data[0]
                if all_data:
                    self.logger.info(f"Успешно получили {len(all_data)} запись(ей) из таблицы {table_name}.")
                else:
                    self.logger.info(f"В таблице {table_name} по вашему запросу данных не найдено.")
                return all_data
        except asyncpg.PostgresError as e:
            self.logger.error(f"Ошибка при выполнении запроса к таблице {table_name}: {e}")
            return []

    async def insert_data(self, table_name: str, records_data: Union[dict, List[dict]], debug: bool = False):
        """
        Вставляет данные в таблицу базы данных.

        :param table_name: Имя таблицы.
        :param records_data: Словарь или список словарей с данными для вставки.
        :param debug: Выводит дебагом SQL запрос и параметры.
        """
        try:
            async with self.connection.transaction():
                if isinstance(records_data, dict):
                    records_data = [records_data]

                if not records_data:
                    self.logger.info("Список записей пуст.")
                    return

                count_dict = len(records_data)

                first_record = records_data[0]
                columns = ', '.join(first_record.keys())
                total_records = len(records_data)
                total_columns = len(first_record)

                all_placeholders = ', '.join(
                    f"({', '.join(f'${j * total_columns + i + 1}' for i in range(total_columns))})"
                    for j in range(total_records)
                )

                query = f'INSERT INTO {table_name} ({columns}) VALUES {all_placeholders};'
                values = [value for record in records_data for value in record.values()]

                if debug:
                    self.logger.debug(f'SQL запрос: {query}')
                    self.logger.debug(f'Параметры запроса: {values}')

                await self.connection.execute(query, *values)
                self.logger.info(f"Успешно добавлены(а) {count_dict} запись(ей) в таблицу {table_name}.")
        except asyncpg.PostgresError as e:
            self.logger.error(f"Ошибка при добавлении записи(ей) в таблицу {table_name}: {e}")

    async def insert_data_with_update(self, table_name: str, records_data: Union[dict, List[dict]],
                                      conflict_column: str, debug: bool = False):
        """
        Вставляет данные в таблицу базы данных. При конфликте по уникальному ключу обновляет запись.

        :param table_name: Имя таблицы.
        :param records_data: Словарь или список словарей с данными для вставки.
        :param conflict_column: Имя столбца для проверки конфликта уникальности.
        :param debug: Выводит дебагом SQL запрос и параметры.
        """
        try:
            async with self.connection.transaction():
                if isinstance(records_data, dict):
                    records_data = [records_data]

                if not records_data:
                    self.logger.info("Список записей пуст.")
                    return

                first_record = records_data[0]
                columns = ', '.join(first_record.keys())
                total_records = len(records_data)
                total_columns = len(first_record)

                all_placeholders = ', '.join(
                    f"({', '.join(f'${j * total_columns + i + 1}' for i in range(total_columns))})"
                    for j in range(total_records)
                )

                update_columns = ', '.join(
                    f"{col} = EXCLUDED.{col}" for col in first_record.keys() if col != conflict_column)

                query = f'''
                    INSERT INTO {table_name} ({columns}) 
                    VALUES {all_placeholders}
                    ON CONFLICT ({conflict_column}) DO UPDATE 
                    SET {update_columns}
                    RETURNING (xmax = 0) AS inserted;
                '''
                values = [value for record in records_data for value in record.values()]

                if debug:
                    self.logger.debug(f'SQL запрос: {query}')
                    self.logger.debug(f'Параметры запроса: {values}')

                result = await self.connection.fetch(query, *values)

                inserted_count = sum(1 for record in result if record['inserted'])
                updated_count = total_records - inserted_count

                if inserted_count > 0:
                    self.logger.info(f"Успешно добавлено {inserted_count} запись(ей) в таблицу {table_name}.")
                if updated_count > 0:
                    self.logger.info(f"Успешно обновлено {updated_count} запись(ей) в таблице {table_name}.")
        except asyncpg.PostgresError as e:
            self.logger.error(f"Ошибка при добавлении записей в таблицу {table_name}: {e}")

    async def update_data(self, table_name: str,
                          where_dict: Union[Dict[str, Union[str, int]], List[Dict[str, Union[str, int]]]],
                          update_dict: Dict[str, Union[str, int]], debug: bool = False):
        """
        Обновляет данные в таблице базы данных.

        :param table_name: Имя таблицы.
        :param where_dict: Условия для выбора записей для обновления.
        :param update_dict: Словарь с данными для обновления.
        :param debug: Выводит дебагом SQL запрос и параметры.
        """
        try:
            async with self.connection.transaction():
                set_clause = ', '.join(f"{key} = ${i + 1}" for i, key in enumerate(update_dict.keys()))
                all_values = list(update_dict.values())

                if isinstance(where_dict, dict):
                    where_clause = ' AND '.join(
                        f"{key} = ${len(update_dict) + i + 1}" for i, key in enumerate(where_dict.keys()))
                    all_values.extend(where_dict.values())
                elif isinstance(where_dict, list):
                    where_clauses = []
                    index = len(update_dict) + 1
                    for condition in where_dict:
                        where_clause_parts = []
                        for i, key in enumerate(condition.keys()):
                            where_clause_parts.append(f"{key} = ${index}")
                            index += 1
                        where_clauses.append(' AND '.join(where_clause_parts))
                        all_values.extend(condition.values())
                    where_clause = ' OR '.join(f'({clause})' for clause in where_clauses)

                query = f'UPDATE {table_name} SET {set_clause} WHERE {where_clause};'

                if debug:
                    self.logger.debug(f'SQL запрос: {query}')
                    self.logger.debug(f'Параметры запроса: {all_values}')

                await self.connection.execute(query, *all_values)
                self.logger.info(f"Запись(и) в таблице {table_name} успешно обновлена(ы).")
        except asyncpg.PostgresError as e:
            self.logger.error(f"Ошибка при обновлении записей в таблице {table_name}: {e}")

    async def delete_data(self, table_name: str,
                          where_dict: Union[Dict[str, Union[str, int]], List[Dict[str, Union[str, int]]]],
                          debug: bool = False):
        """
        Удаляет данные из таблицы базы данных.

        :param table_name: Имя таблицы.
        :param where_dict: Условия для выбора записей для удаления.
        :param debug: Выводит дебагом SQL запрос и параметры.
        """
        try:
            async with self.connection.transaction():
                where_clause = ''
                all_values = []
                if isinstance(where_dict, dict):
                    where_clause = ' AND '.join(f"{key} = ${i + 1}" for i, key in enumerate(where_dict.keys()))
                    all_values.extend(where_dict.values())
                elif isinstance(where_dict, list):
                    where_clauses = []
                    index = 1
                    for condition in where_dict:
                        where_clauses.append(
                            ' AND '.join(f"{key} = ${index + i}" for i, key in enumerate(condition.keys())))
                        index += len(condition)
                        all_values.extend(condition.values())
                    where_clause = ' OR '.join(f'({clause})' for clause in where_clauses)

                query = f'DELETE FROM {table_name} WHERE {where_clause};'
                if debug:
                    self.logger.debug(f'SQL запрос: {query}')
                    self.logger.debug(f'Параметры запроса: {all_values}')
                await self.connection.execute(query, *all_values)
                self.logger.info("Записи успешно удалены.")
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при удалении записей: {e}')

    async def delete_all_data(self, table_name: str, password: str, debug: bool = False):
        """
        Удаляет все данные из таблицы базы данных.

        :param table_name: Имя таблицы.
        :param password: Пароль для подтверждения операции удаления всех данных.
        :param debug: Выводит дебагом SQL запрос и параметры.
        """
        if password != self.deletion_password:
            self.logger.warning("Неверный пароль. Удаление всех записей невозможно.")
            return
        try:
            async with self.connection.transaction():
                query = f'DELETE FROM {table_name};'
                await self.connection.execute(query)
                if debug:
                    self.logger.debug(f'SQL запрос: {query}')
                self.logger.info("Все записи успешно удалены.")
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при удалении всех записей: {e}')

    async def drop_table(self, table_name: str, password: str, debug: bool = False):
        """
        Удаляет таблицу из базы данных.

        :param table_name: Имя таблицы.
        :param password: Пароль для подтверждения операции удаления таблицы.
        :param debug: Выводит дебагом SQL запрос и параметры.
        """
        if password != self.deletion_password:
            self.logger.warning("Неверный пароль. Удаление таблицы невозможно.")
            return
        try:
            async with self.connection.transaction():
                query = f'DROP TABLE IF EXISTS {table_name};'
                if debug:
                    self.logger.debug(f'SQL запрос: {query}')
                await self.connection.execute(query)
                self.logger.info(f"Таблица {table_name} успешно удалена.")
        except asyncpg.PostgresError as e:
            self.logger.error(f'Ошибка при удалении таблицы: {e}')
