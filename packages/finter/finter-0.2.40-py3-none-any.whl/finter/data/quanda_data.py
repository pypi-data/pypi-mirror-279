import json

import pandas as pd
from finter.api.quanda_data_api import QuandaDataApi
from finter.settings import logger


class QuandaData:

    @staticmethod
    def object_list(prefix=''):
        try:
            data = QuandaDataApi().quanda_data_obj_list_retrieve(prefix=prefix)
            return data['object_list']
        except Exception as e:
            logger.error(f"API call failed: {e}")
            return []

    @staticmethod
    def get(object_name, is_file_type=False):
        if is_file_type:
            data = QuandaDataApi().quanda_data_get_retrieve(
                object_name=object_name,
                deserialize=False, _preload_content=False
            )
            data = data.data
            help_str = \
"""
\n
# example:
import pandas as pd
from io import BytesIO
data = QuandaData.get('object_name', is_file_type=True)
df = pd.read_excel(BytesIO(data)) # in case of excel file
---------------------------------------------
"""
        else:
            data = QuandaDataApi().quanda_data_get_retrieve(object_name=object_name)
            data = data['data']
            help_str = \
"""
\n
# example:
import pandas as pd
data = QuandaData.get('object_name')
df = pd.read_json(data) #in case of json file
---------------------------------------------
"""
        logger.info(help_str)
        return data
