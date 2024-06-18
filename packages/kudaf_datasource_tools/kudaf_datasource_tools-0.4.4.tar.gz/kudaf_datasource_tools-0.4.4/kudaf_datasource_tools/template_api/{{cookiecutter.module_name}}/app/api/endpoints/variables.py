from typing import Optional
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from app.core.config import settings
from app.logic.data import (
    parquet_variable_data_iterator, 
    variable_data_iterator,
)
from app.core.security import (
    validate_analytics_user,
    get_kudaf_permissions,
)
from app.utils.utils import (
    show_error_response,
    prepend_datasource_name,
    extract_date_filters,
)


router = APIRouter()


@router.get("/{kudaf_variable_name}", response_class=StreamingResponse)
async def stream_download_kudaf_variable_data(
    kudaf_variable_name: str,
    start: Optional[str] = None, # datetime.today().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat(),
    stop: Optional[str] = None, # datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).isoformat(),
    feide_token_info: str = Depends(validate_analytics_user),
    ):
    """
    Stream download a CSV data file corresponding the following Kudaf Variable(s):  
    {% for var in cookiecutter.variable_mappings %}
    - {{ var }}
    {% endfor %}

    **For variables with Temporality Types EVENT, STATUS and ACCUMULATED** only, 
    it accepts the following **optional query parameters**: \n
    - **start**: Start date in timestamp ISO format: YYYY-MM-DD (e.g 2023-09-01)
    - **stop**: End date in timestamp ISO format: YYYY-MM-DD

    (Detailed info on timestamp ISO format available at: https://www.iso.org/iso-8601-date-and-time-format.html)\n
    The above query parameters will be **ignored for variables with FIXED** Temporality Type. \n
    
    ### Note: Feide authentication required
    - A valid **Bearer JWT Token** from Feide is required (in the Auth header of the request) to access this endpoint \n

    """
    # Check whether Feide User has been granted access to the requested variable
    feide_user_id: str = feide_token_info.get("sub", "")
    granted_permissions = get_kudaf_permissions(feide_user_id=feide_user_id)

    if kudaf_variable_name not in granted_permissions:
        show_error_response(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing permission for Kudaf Variable: {}".format(kudaf_variable_name),
        )

    # Check whether requested variable is one served by this API
    if kudaf_variable_name not in settings.VARIABLE_MAPPINGS:
        show_error_response(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Variable not found"
        )

    filename_csv = prepend_datasource_name(
        ds_name=settings.DATASOURCE_NAME,
        var_name=kudaf_variable_name,
    ) + '.csv'

    var_mappings = settings.VARIABLE_MAPPINGS.get(kudaf_variable_name)
    attr_columns = var_mappings.get('attribute_columns')

    # No temporality filtering case (FIXED)
    if var_mappings.get('temporality_type') == 'FIXED' or \
        attr_columns is None or \
        (start is None and stop is None):
        return StreamingResponse(
            content=parquet_variable_data_iterator(kudaf_variable_name, limit_rows=100), 
            media_type="text/csv",
            headers={'Content-Disposition': f'attachment; filename="{filename_csv}"'}
        )
    # Time filtering case (EVENT, STATUS, ACCUMULATED)
    elif attr_columns is not None or \
       (start is not None or stop is not None):
        date_filters = extract_date_filters(attr_columns, start, stop)

        return StreamingResponse(
            content=variable_data_iterator(
                variable_name=kudaf_variable_name, 
                filters=date_filters
            ), 
            media_type="text/csv",
            headers={'Content-Disposition': f'attachment; filename="{filename_csv}"'}
        )
    else:
        show_error_response(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid Start/Stop parameters"
        )
