from .admin_cmd import admin_cmd_router, admin_cmd
from .delete_admin import delete_admin_router, delete_admin, id_to_delete_admin, cancel_deleting_cmd
from .help import help_cmd_router, help_cmd
from .new_admin import new_admin_router, new_admin_cmd, cancel_cmd, new_admin_id
from .send import send_cmd_router, send_cmd, cancel_send_cmd, new_text_send, confirm_cmd
from .start import start_router, start_cmd
from .status import status_cmd_router, status_cmd


print("INIT handlers")
