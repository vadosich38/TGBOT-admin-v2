from database.connection_fabric import get_db_conn


ADMIN = 423997885
HELP_TEXT = "СПИСОК КОМАНД"
ADMIN_TEXT = "КАК СТАТЬ АДМИНОМ"
START_TEXT = "Добро пожаловать в бота! Бот пока не выполняет никакого функционала, но вы можете стать его" \
             " администратором. \nДля этого пришлите создателю бота @digitalve свой telegram id"
db_connection = get_db_conn()
