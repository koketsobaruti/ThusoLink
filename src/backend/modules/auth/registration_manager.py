from ...models.business.service_model import BusinessService
from ...schemas.business.service_schema import BusinessServiceCreate
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ...utils.auth.hash_utils import hash_password
from ...models.business.business_model import Business
from ...utils.database.db_utils import DBUtils
from ...schemas.user.user_schema import UserCreate, UserResponse
from ...schemas.general_response import GeneralResponse
from ...models.user.user_model import User
from ...schemas.business.business_schema import BusinessCreate
from datetime import datetime, timezone
from ...models.business.business_model import BusinessEmail,BusinessPhone, BusinessLocation, BusinessSocial
# import logger_utils
from ...utils.logger_utils import LoggerUtils
logger = LoggerUtils.get_logger("Registration Manager")

class RegistrationManager:
    def __init__(self, db: Session):
        self.db = db
        self.db_utils = DBUtils(self.db)

    def register_user(self, user: UserCreate) -> GeneralResponse:
        try:
            # db_utils = DBUtils(self.db)
            # Check for duplicates
            self.db_utils.email_exists(user.email)
            # Hash the password
            hashed_pw = hash_password(user.password)
            # get current timestamp
            created_at = updated_at =  datetime.now(timezone.utc)
            # Create DB model instance
            new_user = User(
                full_name=user.full_name,
                email=user.email,
                password_hash=hashed_pw,
                created_at=created_at,
                updated_at=updated_at
            )
            logger.info(f"Registering new user: {new_user}")
            # Save to DB
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)

            return GeneralResponse(status=status.HTTP_201_CREATED,
                                   message="User registered successfully"
                                   )

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error during user registration: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
        
    def register_business(self, business:BusinessCreate, user_id) -> GeneralResponse:
        try:
            self.db_utils.business_exists(business)
            now = datetime.now(timezone.utc)
            
            # If no duplicates, proceed to create business
            # 2️⃣ Create the Business object and set relationships
            now = datetime.now(timezone.utc)
            new_business = Business(
                owner_id=user_id,
                name=business.name,
                description=business.description,
                created_at=now,
                updated_at=now
            )

            # # 3️⃣ Add contacts via relationship
            # if business.contacts:
            #     new_business.contacts = [
            #         BusinessContact(**b_contact.model_dump()) for b_contact in business.contacts
            #     ]

            if business.emails:
                new_business.emails = [
                    BusinessEmail(
                        **b_email.model_dump(exclude={"created_at"}),
                        created_at=now
                    )
                    for b_email in business.emails
                ]

            if business.phones:
                new_business.phones = [
                    BusinessPhone(**b_phone.model_dump(exclude={"created_at"}),
                        created_at=now) 
                        for b_phone in business.phones
                ]

            if business.locations:
                new_business.locations = [
                    BusinessLocation(**b_location.model_dump(exclude={"created_at"}),
                        created_at=now) 
                        for b_location in business.locations
                ]
            if business.socials:
                new_business.socials = [
                    BusinessSocial(**b_social.model_dump(exclude={"created_at"}),
                        created_at=now) 
                        for b_social in business.socials
                ]

            # 6️⃣ Add and commit
            self.db.add(new_business)
            self.db.commit()

            return GeneralResponse(
                status=status.HTTP_201_CREATED,
                message="Business registered successfully",
                data={"name": new_business.name}
            )
        
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error during business registration: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )
        
    def register_service(self, service:BusinessServiceCreate, user_id, business_id) -> GeneralResponse:
        try:
            # Ensure the business belongs to the user
            self.db_utils.user_business_exists(business_id, user_id)
            # Check for duplicate service name within the same business
            self.db_utils.existing_service(service.name, business_id)
            
            # Create the service
            new_service = BusinessService(
                business_id=business_id,
                name=service.name,
                description=service.description,
                price=service.price,
                currency=service.currency.value,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            self.db.add(new_service)
            self.db.commit()

            return GeneralResponse(
                status=status.HTTP_201_CREATED,
                message="Service registered successfully",
                data={"name": new_service.name}
            )

        except Exception as e:
            self.db.rollback()
            logger.error(f"Error during service registration: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred: {str(e)}"
            )