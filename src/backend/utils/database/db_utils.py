# src/backend/utils/db_utils.py
from backend.models.business.service_model import BusinessService
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from fastapi import Depends
from ...depends.dependencies import get_current_user
from ...models.business.business_model import BusinessEmail, BusinessLocation, BusinessPhone, BusinessSocial, Business
from ...schemas.business.business_schema import BusinessCreate, BusinessResponse, BusinessUpdate
from ...models.user.user_model import User
from ...schemas.user.user_schema import UserCreate
from typing import Union
from ...utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("DB Utils")
class DBUtils:
    def __init__(self, db: Session):
        self.db = db

    def email_exists(self, email: str) -> None:
        """
        Raises HTTPException if a user with the given email already exists.
        """
        existing_user = self.db.query(User).filter(User.email == email).first()
        if existing_user:
            logger.warning(f"Attempt to register with existing email: {email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered."
            )

    def business_exists(self, business_data: Union[BusinessCreate, BusinessUpdate]) -> bool:
        """
        Check whether a business with the same name, contacts, or socials exists.
        Locations are not checked for duplicates, because multiple businesses
        can share the same physical location.

        Returns True if a potential duplicate is found, False otherwise.
        """

        try:
            # 🏢 Check business name
            if business_data.name:
                if self.db.query(Business).filter(Business.name.ilike(business_data.name)).first():
                    logger.info(f"Duplicate business name found: {business_data.name}")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,        
                        detail="Business name already registered."
                    )

            # ☎️ Check phone numbers
            if business_data.phones:
                for phone in business_data.phones:
                    existing_phone = self.db.query(BusinessPhone).filter(
                        BusinessPhone.number == phone.number
                    ).first()
                    if existing_phone:
                        logger.info(f"Duplicate business phone number found: {phone.number}")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Business phone number '{phone.number}' is already registered."
                        )

            # 📧 Check emails
            if business_data.emails:
                for email in business_data.emails:
                    existing_email = self.db.query(BusinessEmail).filter(
                        BusinessEmail.email == email.email
                    ).first()
                    if existing_email:
                        logger.info(f"Duplicate business email found: {email.email}")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Business email '{email.email}' is already registered."
                        )


            # 🌐 Check socials
            if business_data.socials:
                for social in business_data.socials:
                    if self.db.query(BusinessSocial).filter(
                    BusinessSocial.platform == social.platform,
                    BusinessSocial.handle == social.handle
                    ).first():
                        logger.info("Duplicate business social found.")
                        raise HTTPException(
                            status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Business social handle already registered."
                        )
                    
            logger.info("No duplicate business found.")
            # return False
        except Exception as e:
            logger.error(f"Error checking business existence: {str(e)}")    
            raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking business existence: {str(e)}"
            )
    
    def get_current_user_id(self, email) -> int:
        logger.info(f"Fetching user ID for email: {email}")
        user_obj = self.db.query(User).filter(User.email == email).first()
        if not user_obj:
            logger.error(f"User not found in DB for email: {email}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        return user_obj.id
    
    def get_business_id(self, business_name: str) -> str:
        logger.info(f"Fetching business ID for business name: {business_name}")
        business_obj = self.db.query(Business).filter(Business.name == business_name).first()
        if not business_obj:
            logger.error(f"Business not found in DB for name: {business_name}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found."
            )
        return business_obj.id
    
    
    def user_business_exists(self, business_id: str, user_id: int) -> Business:
        logger.info(f"Fetching business ID: {business_id} for user ID: {user_id}")
        business_obj = self.db.query(Business).filter(
            Business.id == business_id,
            Business.owner_id == user_id
        ).first()
        if not business_obj:
            logger.error(f"Business not found or does not belong to user ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found or does not belong to the user."
            )
        
    def existing_service(self, service_name: str, business_id: str):
        logger.info(f"Checking for existing service '{service_name}' in business ID: {business_id}")
        existing_service = self.db.query(BusinessService).filter(
            BusinessService.business_id == business_id,
            BusinessService.name.ilike(service_name)
        ).first()
        if existing_service:
            logger.warning(f"Service '{service_name}' already exists in business ID: {business_id}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service '{service_name}' already exists for this business."
            )