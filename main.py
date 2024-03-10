"""

Playground APIs utilize JWT (JSON Web Tokens) for secure token-based authentication, managing sports equipment inventory. 

Users can perform operations like retrieving all equipment, creating, updating, and deleting items, ensuring a professional and secure Playground environment.

"""


from fastapi import Request, HTTPException
from app.models import EquipmentSchema, UserSchema, UserLoginSchema, EquipmentSchemaDB, UserSchemaDB, get_db
from app.auth.jwt_handler import signJWT, decodeJWT
from fastapi import FastAPI, Depends, Body 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.auth.jwt_bearer import jwtBearer
from sqlalchemy.orm import Session
from app.database import Base
from sqlalchemy.future import select
import json
import warnings
from sqlalchemy import inspect
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext



app = FastAPI()


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


warnings.filterwarnings("ignore", category=DeprecationWarning, module="httpx._client")

# landing zone
@app.get("/")
async def root():
    return {"message": "Proceed to /docs url for api documentation"}



# get all equipments
@app.get("/equipments", dependencies=[Depends(jwtBearer())], tags=['equipment'])
async def get_equipments(current_user: str = Depends(jwtBearer()), db: Session = Depends(get_db)):
    """
    Get All Equipments

    Retrieve a list of all sports equipments owned by the current user.

    - **current_user**: Current user's access token.

    - **db**: Database session.

    - **return**: A dictionary containing a list of equipments with their details.
      If no equipments are found, a message stating "No equipments found" is returned.
    """
    try:
        token_dict = json.loads(current_user)
        decoded_token = decodeJWT(token_dict['access_token'])
        current_user_email = decoded_token['userID']
        result = await db.execute(select(EquipmentSchemaDB).where(EquipmentSchemaDB.owner_email == current_user_email))
        equipments = result.fetchall()
        if len(equipments) == 0:
            return {"message": "No equipments found"}
        equipments_list = [{"id": equipment[0].id, "item": equipment[0].item, "quantity": equipment[0].quantity} for equipment in equipments]      
        return {"equipments": equipments_list}
    except:
        raise HTTPException(status_code=403, detail="Invalid or expired token, login again")



# create a new equipment
@app.post("/equipments", dependencies=[Depends(jwtBearer())], tags=['equipment'])
async def create_equipment(equipment: EquipmentSchema, current_user: str = Depends(jwtBearer()), db: Session = Depends(get_db)):
    """
    Create a New Equipment

    Add a new sports equipment to the current user's inventory.

    - **equipment**: Equipment details to be added.
    
    - **current_user**: Current user's access token.
    
    - **db**: Database session.
    
    - **return**: A message confirming the addition of the equipment.
      If the token is invalid or expired, a 403 Forbidden error is returned.
    """
    try:
        token_dict = json.loads(current_user)
        decoded_token = decodeJWT(token_dict['access_token'])
        current_user_email = decoded_token['userID']
        
        equipment_db = EquipmentSchemaDB(item=equipment.item, quantity=equipment.quantity, owner_email=current_user_email)
        db.add(equipment_db)
        await db.commit()
        await db.refresh(equipment_db)
        return {"message": "Equipment has been added"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=403, detail="Invalid or expired token, login again")    



# get single equipment
@app.get("/equipments/{equipment_name}", tags=['equipment'])
async def get_equipment(equipment_name: str, current_user: str = Depends(jwtBearer()), db: Session = Depends(get_db)):
    """
    Get Single Equipment

    Retrieve details of a specific sports equipment owned by the current user.

    - **equipment_name**: Name of the sports equipment to retrieve.

    - **current_user**: Current user's access token.

    - **db**: Database session.

    - **return**: Details of the requested equipment.
      If the token is invalid or expired, a 403 Forbidden error is returned.
    """
    try:
        token_dict = json.loads(current_user)
        decoded_token = decodeJWT(token_dict['access_token'])
        current_user_email = decoded_token['userID']
        result = await db.execute(select(EquipmentSchemaDB).where((EquipmentSchemaDB.owner_email == current_user_email) & (EquipmentSchemaDB.item == equipment_name)))
        equipments = result.fetchall()
        if len(equipments) == 0:
            return {"message": "No equipments found"}
        equipments_list = [{"id": equipment[0].id, "item": equipment[0].item, "quantity": equipment[0].quantity} for equipment in equipments]      
        return {"equipments": equipments_list}
    except:
        raise HTTPException(status_code=403, detail="Invalid or expired token, login again")



# delete an equipment
@app.delete("/equipments/{equipment_name}", dependencies=[Depends(jwtBearer())], tags=['equipment'])
async def delete_equipment(equipment_name: str, current_user: str = Depends(jwtBearer()), db: Session = Depends(get_db)):
    """
    Delete Equipment

    Remove a sports equipment owned by the current user.

    - **equipment_name**: Name of the sports equipment to delete.

    - **current_user**: Current user's access token.

    - **db**: Database session.

    - **return**: Confirmation message after successful deletion.
      If the token is invalid or expired, a 403 Forbidden error is returned.
      If no matching equipment is found, a message indicating no equipment is found is returned.
    """
    try:
        token_dict = json.loads(current_user)
        decoded_token = decodeJWT(token_dict['access_token'])
        current_user_email = decoded_token['userID']
        equipment = await db.execute(select(EquipmentSchemaDB).where((EquipmentSchemaDB.owner_email == current_user_email) & (EquipmentSchemaDB.item == equipment_name)))
        equipment = equipment.scalar()
        if equipment is None:
            return {"message": "No equipments found"}
        await db.delete(equipment)
        await db.commit()
        return {"message": "Equipment has been deleted"}
    except:
        raise HTTPException(status_code=403, detail="Invalid or expired token, login again")



# update an equipment
@app.put("/equipments", dependencies=[Depends(jwtBearer())], tags=['equipment'])  
async def update_equipment(equipment_obj: EquipmentSchema, current_user: str = Depends(jwtBearer()), db: Session = Depends(get_db)):
    """
    Update Equipment

    Modify the quantity of a sports equipment owned by the current user.

    - **equipment_obj**: The updated information for the sports equipment.

    - **current_user**: Current user's access token.

    - **db**: Database session.

    - **return**: Confirmation message after successful update.
      If the token is invalid or expired, a 403 Forbidden error is returned.
      If no matching equipment is found, a message indicating no equipment is found is returned.
    """
    try:
        token_dict = json.loads(current_user)
        decoded_token = decodeJWT(token_dict['access_token'])
        current_user_email = decoded_token['userID']
        
        equipment = await db.execute(select(EquipmentSchemaDB).where((EquipmentSchemaDB.owner_email == current_user_email) & (EquipmentSchemaDB.item == equipment_obj.item)))
        equipment = equipment.scalar()
        if equipment is None:
            return {"message": "No equipment found"}
        equipment.quantity = equipment_obj.quantity
        await db.commit()
        return {"message": "Quantity of equipment has been updated"}
    except:
        raise HTTPException(status_code=403, detail="Invalid or expired token, login again")



# get items with no quantity left
@app.get("/equipments/outofstock/", dependencies=[Depends(jwtBearer())], tags=['equipment'])
async def get_outofstock_items(current_user: str = Depends(jwtBearer()), db: Session = Depends(get_db)):
    """
    Get Items with No Quantity Left

    Retrieve a list of sports equipments with zero quantity left owned by the current user.

    - **current_user**: Current user's access token.

    - **db**: Database session.

    - **return**: List of sports equipments with zero quantity.
    
      If the token is invalid or expired, a 403 Forbidden error is returned.
      If no matching equipment is found, a message indicating no equipment is found is returned.
    """
    try:
        token_dict = json.loads(current_user)
        decoded_token = decodeJWT(token_dict['access_token'])
        current_user_email = decoded_token['userID']
        result = await db.execute(select(EquipmentSchemaDB).where((EquipmentSchemaDB.owner_email == current_user_email) & (EquipmentSchemaDB.quantity == 0)))
        equipments = result.fetchall()
        if len(equipments) == 0:
            return {"message": "No equipments found"}
        equipments_list = [{"id": equipment[0].id, "item": equipment[0].item, "quantity": equipment[0].quantity} for equipment in equipments]      
        return {"equipments": equipments_list}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=403, detail="Invalid or expired token, login again")



# check if user exists in database
async def check_user(db: Session, data: UserLoginSchema):
    try:
        result = await db.execute(select(UserSchemaDB).where(UserSchemaDB.email == data.email))
        db_user = result.scalar()
        if db_user and password_context.verify(data.password, db_user.password):
            return True
        return False
    except:
        return False
        
    
    
# create signup
@app.post("/user/signup", tags=['user'])
async def user_signup(user: UserSchema = Body(default=None), db: Session = Depends(get_db)):
    """
    Create Signup

    Register a new user and generate an access token for authentication.

    - **user**: User details including name, email, and password.

    - **db**: Database session.

    - **return**: Access token for the registered user.
    
      If the email is already registered, an error indicating email duplication is returned.
    """
    try:
        hashed_password = password_context.hash(user.password)
        db_user = UserSchemaDB(name=user.name, email=user.email, password=hashed_password)
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return signJWT(user.email)
    except IntegrityError as e:
        # Handle the unique constraint violation (email already exists)
        return {"error": "Email is already registered"} 
    
    

# login user
@app.post("/user/login", tags=['user'])
async def user_login(data: UserLoginSchema = Body(default=None), db: Session = Depends(get_db)):
    """
    Login User

    Authenticate a user with provided login credentials and generate an access token.

    - **data**: User login details including email and password.

    - **db**: Database session.

    - **return**: Access token for the authenticated user.
      If login details are invalid, an error indicating the login failure is returned.
    """
    if await check_user(db, data):
        return signJWT(data.email)
    return {
        "error": "Invalid login details"
        }   
