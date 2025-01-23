from typing import Optional

from pydantic import BaseModel, Field, ValidationError


class InputData(BaseModel):
    id: int = Field(..., description="ID único do item")
    name: str = Field(..., min_length=3, max_length=50, description="Nome do item")
    price: float = Field(..., gt=0, description="Preço do item (deve ser maior que 0)")
    category: Optional[str] = Field(None, description="Categoria opcional do item")
