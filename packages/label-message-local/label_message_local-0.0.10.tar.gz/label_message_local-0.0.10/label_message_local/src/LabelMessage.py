from database_mysql_local.generic_crud import GenericCRUD
from logger_local.MetaLogger import MetaLogger

from .LabelConstants import LABEL_MESSAGE_CODE_LOGGER_OBJECT


class LabelsMessageLocal(GenericCRUD, metaclass=MetaLogger, object=LABEL_MESSAGE_CODE_LOGGER_OBJECT):

    def __init__(self, is_test_data: bool = False):
        super().__init__(default_schema_name="label_message",
                         default_table_name="label_message_table",
                         default_view_table_name='label_message_view',
                         is_test_data=is_test_data)

    def add_label_message(self, *, label_id: int, message_id: int) -> int:
        label_data = {
            "label_id": label_id,
            "message_id": message_id
        }
        label_message_id = self.insert(data_dict=label_data)
        return label_message_id
