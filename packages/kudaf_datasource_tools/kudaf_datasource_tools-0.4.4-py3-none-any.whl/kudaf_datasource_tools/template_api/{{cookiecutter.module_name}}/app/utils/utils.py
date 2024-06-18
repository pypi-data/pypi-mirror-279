import os 
import json
from datetime import datetime, timezone
from typing import Optional, List
from pyarrow import scalar
from fastapi import Response, HTTPException, status
from fastapi.logger import logger


def extract_date_filters(
    attr_columns: Optional[List[str]], 
    start: Optional[str], 
    stop: Optional[str],
):
    # Temporary filtering may be needed
    # Ensure correct ISO format for temporal query parameters
    try:
        startdate = datetime.fromisoformat(start) if start else datetime(1970, 1, 1)
        stopdate = datetime.fromisoformat(stop) if stop else datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc)
    except ValueError as e:
        show_error_response(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e) + " -> See: https://www.iso.org/iso-8601-date-and-time-format.html"
        )

    if stop > datetime.now().isoformat():
        # Replace by last midnight
        stop = datetime.now().replace(
            hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc).isoformat()

    if start > datetime.now().isoformat() or start >= stop:
        # Sanity check on the date
        show_error_response(status_code=status.HTTP_400_BAD_REQUEST, detail="Malformed input")

    # Map temporal attrs names to start/stop
    start_attr = "".join(_attr for _attr in attr_columns if 'start' in _attr.lower() or 'begin' in _attr.lower())
    stop_attr = "".join(_attr for _attr in attr_columns if 'stop' in _attr.lower() or 'end' in _attr.lower())

    startdate = startdate.replace(tzinfo=timezone.utc)
    stopdate = stopdate.replace(tzinfo=timezone.utc)

    date_filters = [
        (start_attr, '>=', scalar(startdate)), 
        (stop_attr, '<=', scalar(stopdate))
    ]

    return date_filters


def prepend_datasource_name(ds_name: str, var_name: str) -> str:
    """
    Ensures the name of the Datasource is somehow included in
    the variable name, otherwise pre-pends it
    """
    if ds_name.lower() not in var_name.lower():
        return ds_name.upper() + "_" + var_name
    else:
        return var_name


def safe_file_open_w(path:str):
    ''' 
    Open "path" for writing, creating any parent directories as needed.
    '''
    os.makedirs(os.path.dirname(path), exist_ok=True)

    return open(path, 'w', newline='')


def show_error_response(
    response: Optional[Response] = None, 
    status_code: Optional[int] = status.HTTP_400_BAD_REQUEST,
    headers: Optional[dict] = None, 
    detail: Optional[str] = None
    ) -> HTTPException:
    """
    Raise an HTTP exception
    """
    if response is None:
        raise HTTPException(
            status_code=status_code,
            detail=detail,
            headers=headers,
        )
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json(),
            headers=headers,
        )


def load_json(filepath: str) -> dict:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to open file at {str(filepath)}")
        return []
    