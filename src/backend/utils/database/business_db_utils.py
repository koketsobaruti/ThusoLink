from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Union
from ...schemas.business.business_schema import BusinessCreate, BusinessEmailResponse, BusinessLocationResponse, BusinessPhoneResponse, BusinessResponse, BusinessSocialResponse, BusinessUpdate
from ...models.business.business_model import BusinessEmail, BusinessLocation, BusinessPhone, BusinessSocial, Business
from ...utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Business DB Utils")
class BusinessDBUtils:
    def __init__(self, db: Session):
        self.db = db

    def get_business_by_name(self, name: str):
        """
        Retrieve a BusinessEmail, BusinessPhone, BusinessSocial, Business by its name.
        """
        try:
            business = self.db.query(Business).filter(Business.name.ilike(name)).first()
            if not business:
                logger.warning(f"Business not found: {name}")
                raise HTTPException(
                    status_code= status.HTTP_404_NOT_FOUND,
                    detail="Business not found."
                )
            # get the id of the business
            business_id = self.get_business_id(name)
            business_obj = self.db.query(Business).filter(Business.id == business_id).first()
            # get BusinessEmail, BusinessPhone, BusinessSocial where business_id matches
            emails = self.db.query(BusinessEmail).filter(BusinessEmail.business_id == business_id).all()
            phones = self.db.query(BusinessPhone).filter(BusinessPhone.business_id == business_id).all()
            socials = self.db.query(BusinessSocial).filter(BusinessSocial.business_id == business_id).all()
            locations = self.db.query(BusinessLocation).filter(BusinessLocation.business_id == business_id).all()
            email_dict = [BusinessEmailResponse.model_validate(p) for p in emails]
            phones_dict = [BusinessPhoneResponse.model_validate(p) for p in phones]
            socials_dict = [BusinessSocialResponse.model_validate(p) for p in socials]
            locations_dict = [BusinessLocationResponse.model_validate(p) for p in locations]
            # logger.info(f'Emails retrieved for business {name}: {email_dict}')
            business_response = {
                "id": business_obj.id,
                "owner_id": business_obj.owner_id,
                "name": business_obj.name,
                "description": business_obj.description,
                "phones": phones_dict,
                "emails": email_dict,
                "locations": locations_dict,
                "socials": socials_dict,
                "created_at": business_obj.created_at,
                "updated_at": business_obj.updated_at
            }

            return business_response
        except HTTPException as e:
            logger.error(f"Error retrieving business by name: {name} - {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Unexpected error retrieving business by name: {name} - {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while retrieving the business."
            )
                                                        
    def get_business(self, business_name: str):
        business = self.db.query(Business).filter(Business.name == business_name).first()
        return business
    
    def get_business_id(self, business_name: str):
        business = self.get_business(business_name)
        if business:
            return business.id
        return None
    
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
    