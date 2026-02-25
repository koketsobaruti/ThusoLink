# ThusoLink
ThusoLink is a modern service-booking platform that connects customers with local businesses.
It enables businesses to manage availability and bookings, while customers can easily request appointments through a streamlined system that uses WhatsApp for Business integration.

## Overview 
ThusoLink is designed to:
- Allow businesses to set and manage availability
- Enable customers to request bookings
- Automatically handle booking confirmations (initial version)
- Sync booking and availability status
- Support future WhatsApp webhook integration
- Provide a scalable backend architecture
The goal is to create a lightweight but powerful scheduling infrastructure that works both with and without a dedicated mobile app

## Architecture
### Backend
- FastAPI – API framework
- PostgreSQL – Database
- SQLAlchemy – ORM
- Alembic – Migrations
- Pydantic – Schema validation
### Additional Integrations
- WhatsApp Webhook Integration

## Features
### Business Features
- Set availability (open / unavailable days)
- Update availability in bulk
- View bookings
- Automatic booking confirmation (v1)
- Booking status tracking
### Booking System
- Create booking request
- Auto-confirm bookings
- Sync availability when booking is confirmed
- Prevent double-booking using constraints
### Status Handling
Shared enum for:
- AVAILABLE
- UNAVAILABLE
- REQUESTED
- CONFIRMED
- DECLINED
- COMPLETED

## Installation

#### Using bash run:
```python
git clone https://github.com/yourusername/thuso-link.git
cd thuso-link
```
#### Create virtual enviroment: 
```python
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```
#### Install Dependencies:
```python
pip install -r requirements.txt
```

#### Configure Environment Variables:
```python
DATABASE_URL=postgresql://user:password@localhost/thusolink
SECRET_KEY=your_jwt_secret_key
WHATSAPP_PHONE_NUMBER_ID = your_whatsapp_phone_number_id
APP_ID
APP_SECRET = your_meta_app_secret
RECIPIENT_WAID = whatsapp_recepient_phone_number
WHATSAPP_TOKEN = your_token_from_whatsapp_app
VERIFY_TOKEN = verify_token
```
#### Run database migrations
```python
alembic revision --autogenerate -m "description of change"
alembic upgrade head
```
#### Start server 
```python
uvicorn app.main:app --reload OR fastapi dev (run this from src/ directory)
```
API will be available at: http://127.0.0.1:8000 and docs are at http://127.0.0.1:8000/docs
## Data Integrity
- Unique constraints prevent duplicate bookings.
- Availability updates are transactional.
- Booking status and availability status use a shared scheduling enum.
- Timestamps (created_at, updated_at) track state changes.

## Testing
```python
pytest
```
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.
### Issue Naming Convention

To maintain consistency and make it easier to track issues, we follow the following naming format for all issues and tests:

```
<FEATURE_TYPE>-v1.<MINOR>.<PATCH>-<BRIEF_DESCRIPTION>
```

Where:

- **FEATURE_TYPE** – Short code representing the feature or module:
  - `BK` → Booking  
  - `AV` → Availability  
  - `DB` → Database / backend logic  
  - `API` → API endpoints  
  - `UI` → UI / frontend  

- **v1.<MINOR>.<PATCH>** – Version of this feature/test:
  - **MINOR** → major iteration of this feature  
  - **PATCH** → small changes or bug fixes  

- **BRIEF_DESCRIPTION** – Short summary of the issue or test, using underscores instead of spaces.

**Example:**

For adding a test to the booking feature in version 1 of the app:

```
BK-v1.0.0-get_bookings_test
```

This clearly indicates the feature, version, and purpose of the test.
Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
