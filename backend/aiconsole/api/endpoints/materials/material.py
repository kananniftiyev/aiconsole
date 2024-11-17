# The AIConsole Project
#
# Copyright 2023 10Clouds
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .crud import create_material, get_material, update_material, delete_material
from .database import SessionLocal
from .schemas import MaterialCreate, MaterialUpdate, MaterialOut

router = APIRouter()

# TODO: Material Status Change endpoint.
# TODO: Material Exists endpoint.
# ! Project Structure fix.

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def sanitize_asset_id(value: str) -> str:
    return value.strip().strip("'").strip('"')

@router.post("/{asset_id}", response_model=MaterialOut)
async def create_material_endpoint(asset_id: str, material: MaterialCreate, db: Session = Depends(get_db)):
    """
    Create a new material for the given asset ID.
    
    - **asset_id**: The ID of the asset.
    - **material**: Material creation data.
    - **Response model**: `MaterialOut`
    """
    sanitized_asset_id = sanitize_asset_id(asset_id)
    material_data = material.dict()
    material_data['id'] = sanitized_asset_id
    return create_material(db, material_data)

@router.get("/{asset_id}", response_model=MaterialOut)
async def get_material_endpoint(asset_id: str, db: Session = Depends(get_db)):
    """
    Retrieve the material for the given asset ID.
    
    - **asset_id**: The ID of the asset.
    - **Response model**: `MaterialOut`
    - **404 error**: Material not found.
    """
    print(asset_id)
    sanitized_asset_id = sanitize_asset_id(asset_id)
    material = get_material(db, sanitized_asset_id)
    if not material:
        raise HTTPException(status_code=404, detail="Material not found")
    return material

@router.patch("/{asset_id}", response_model=MaterialOut)
async def update_material_endpoint(asset_id: str, material: MaterialUpdate, db: Session = Depends(get_db)):
    """
    Update the material for the given asset ID.
    
    - **asset_id**: The ID of the asset.
    - **material**: Material update data.
    - **Response model**: `MaterialOut`
    - **404 error**: Material not found.
    """
    sanitized_asset_id = sanitize_asset_id(asset_id)
    material_data = material.dict()
    updated_material = update_material(db, sanitized_asset_id, material_data)
    if not updated_material:
        raise HTTPException(status_code=404, detail="Material not found")
    return updated_material

@router.delete("/{asset_id}", response_model=dict)
async def delete_material_endpoint(asset_id: str, db: Session = Depends(get_db)):
    """
    Delete the material for the given asset ID.
    
    - **asset_id**: The ID of the asset.
    - **Response model**: `{ "status": "ok" }`
    - **404 error**: Material not found.
    """
    sanitized_asset_id = sanitize_asset_id(asset_id)
    deleted_material = delete_material(db, sanitized_asset_id)
    if not deleted_material:
        raise HTTPException(status_code=404, detail="Material not found")
    return {"status": "ok"}


@router.post("/migrate", response_model=dict)
async def run_migration():
    pass
