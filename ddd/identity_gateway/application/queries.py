import uuid
from abc import ABC
from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime

class Query(BaseModel, frozen=True):
    pass
