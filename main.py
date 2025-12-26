# main.py
from fastapi import FastAPI, HTTPException, Query, Depends
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./speed_cameras.db")

# Fix for Render PostgreSQL URL format
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database Model
class CameraDB(Base):
    """Database model for speed cameras"""
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    cross_street_1 = Column(String, nullable=False)
    cross_street_2 = Column(String, nullable=False)
    zipcode = Column(String(5), nullable=False, index=True)
    speed_limit = Column(Integer, nullable=False)
    direction = Column(String(2), nullable=False)


# Create tables
Base.metadata.create_all(bind=engine)


# Pydantic Models
class CameraCreate(BaseModel):
    """Schema for creating a new camera"""
    cross_street_1: str = Field(..., min_length=1, max_length=100, examples=["5th Ave"])
    cross_street_2: str = Field(..., min_length=1, max_length=100, examples=["W 42nd St"])
    zipcode: str = Field(..., pattern=r"^\d{5}$", examples=["10001"])
    speed_limit: int = Field(..., ge=5, le=85, examples=[25])
    direction: str = Field(..., examples=["N"])

    @field_validator('direction')
    @classmethod
    def validate_direction(cls, v: str) -> str:
        valid_directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
        if v not in valid_directions:
            raise ValueError(f'Direction must be one of {valid_directions}')
        return v


class CameraUpdate(BaseModel):
    """Schema for updating an existing camera"""
    cross_street_1: Optional[str] = Field(None, min_length=1, max_length=100, examples=["5th Ave"])
    cross_street_2: Optional[str] = Field(None, min_length=1, max_length=100, examples=["W 42nd St"])
    zipcode: Optional[str] = Field(None, pattern=r"^\d{5}$", examples=["10001"])
    speed_limit: Optional[int] = Field(None, ge=5, le=85, examples=[25])
    direction: Optional[str] = Field(None, examples=["N"])

    @field_validator('direction')
    @classmethod
    def validate_direction(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            valid_directions = ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
            if v not in valid_directions:
                raise ValueError(f'Direction must be one of {valid_directions}')
        return v


class Camera(BaseModel):
    """Schema for camera response"""
    id: int
    cross_street_1: str
    cross_street_2: str
    zipcode: str
    speed_limit: int
    direction: str

    model_config = {"from_attributes": True}


# FastAPI app
app = FastAPI(
    title="Speed Camera API",
    description="RESTful API for managing speed camera data across the country",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get DB session
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Initialize with sample data
@app.on_event("startup")
def startup_event():
    """Initialize database with sample data on startup"""
    db = SessionLocal()
    try:
        # Check if data already exists
        count = db.query(CameraDB).count()
        if count == 0:
            # Add sample data with accurate real-world locations
            sample_cameras = [
                CameraDB(
                    cross_street_1="5th Ave",
                    cross_street_2="W 42nd St",
                    zipcode="10036",
                    speed_limit=25,
                    direction="N"
                ),
                CameraDB(
                    cross_street_1="Broadway",
                    cross_street_2="W 34th St",
                    zipcode="10001",
                    speed_limit=25,
                    direction="S"
                ),
                CameraDB(
                    cross_street_1="Park Ave",
                    cross_street_2="E 59th St",
                    zipcode="10022",
                    speed_limit=30,
                    direction="E"
                ),
                CameraDB(
                    cross_street_1="Madison Ave",
                    cross_street_2="E 72nd St",
                    zipcode="10021",
                    speed_limit=25,
                    direction="W"
                ),
                CameraDB(
                    cross_street_1="Wilshire Blvd",
                    cross_street_2="S Beverly Dr",
                    zipcode="90212",
                    speed_limit=35,
                    direction="W"
                ),
                CameraDB(
                    cross_street_1="Sunset Blvd",
                    cross_street_2="N Highland Ave",
                    zipcode="90028",
                    speed_limit=35,
                    direction="E"
                ),
                CameraDB(
                    cross_street_1="Michigan Ave",
                    cross_street_2="E Randolph St",
                    zipcode="60601",
                    speed_limit=30,
                    direction="N"
                ),
                CameraDB(
                    cross_street_1="State St",
                    cross_street_2="W Madison St",
                    zipcode="60602",
                    speed_limit=25,
                    direction="S"
                ),
                CameraDB(
                    cross_street_1="Market St",
                    cross_street_2="5th St",
                    zipcode="94103",
                    speed_limit=25,
                    direction="NE"
                ),
                CameraDB(
                    cross_street_1="Lombard St",
                    cross_street_2="Hyde St",
                    zipcode="94133",
                    speed_limit=15,
                    direction="E"
                ),
            ]
            db.add_all(sample_cameras)
            db.commit()
    finally:
        db.close()


# Routes
@app.get("/", tags=["root"])
def read_root():
    """Root endpoint with API information"""
    return {
        "message": "Speed Camera API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/cameras/zipcode/{zipcode}", response_model=List[Camera], tags=["cameras"])
def get_cameras_by_zipcode(zipcode: str, db: Session = Depends(get_db)):
    """
    Get all cameras in a specific zipcode.

    Returns an empty list if no cameras are found.
    """
    if not zipcode.isdigit() or len(zipcode) != 5:
        raise HTTPException(
            status_code=400,
            detail="Invalid zipcode format. Must be 5 digits."
        )

    cameras = db.query(CameraDB).filter(CameraDB.zipcode == zipcode).all()
    return cameras


@app.get("/cameras/search", response_model=List[Camera], tags=["cameras"])
def search_cameras_by_street(
        street: str = Query(..., description="Street name to search for", min_length=1),
        zipcode: str = Query(..., pattern=r"^\d{5}$", description="5-digit zipcode"),
        db: Session = Depends(get_db)
):
    """
    Search cameras by street name and zipcode.

    The street name is matched against both cross streets (case-insensitive).
    Returns an empty list if no cameras are found.
    """
    if not zipcode.isdigit() or len(zipcode) != 5:
        raise HTTPException(
            status_code=400,
            detail="Invalid zipcode format. Must be 5 digits."
        )

    cameras = db.query(CameraDB).filter(
        CameraDB.zipcode == zipcode
    ).filter(
        (CameraDB.cross_street_1.ilike(f"%{street}%")) |
        (CameraDB.cross_street_2.ilike(f"%{street}%"))
    ).all()

    return cameras


@app.post("/cameras", response_model=Camera, status_code=201, tags=["cameras"])
def create_camera(camera: CameraCreate, db: Session = Depends(get_db)):
    """
    Create a new speed camera.

    Prevents duplicate cameras at the same intersection (same cross streets and zipcode).
    """
    # Check for duplicate
    existing = db.query(CameraDB).filter(
        CameraDB.cross_street_1 == camera.cross_street_1,
        CameraDB.cross_street_2 == camera.cross_street_2,
        CameraDB.zipcode == camera.zipcode
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Camera already exists at {camera.cross_street_1} "
                f"and {camera.cross_street_2} in zipcode {camera.zipcode}"
            )
        )

    db_camera = CameraDB(**camera.model_dump())
    db.add(db_camera)
    db.commit()
    db.refresh(db_camera)
    return db_camera


@app.put("/cameras/{camera_id}", response_model=Camera, tags=["cameras"])
def update_camera(
        camera_id: int,
        camera: CameraUpdate,
        db: Session = Depends(get_db)
):
    """
    Update an existing camera.

    All fields except ID can be updated. Only provide fields you want to change.
    """
    db_camera = db.query(CameraDB).filter(CameraDB.id == camera_id).first()

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    # Update only provided fields
    update_data = camera.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_camera, key, value)

    db.commit()
    db.refresh(db_camera)
    return db_camera


@app.delete("/cameras/{camera_id}", tags=["cameras"])
def delete_camera(camera_id: int, db: Session = Depends(get_db)):
    """
    Delete a camera by ID.

    This is a hard delete and cannot be undone.
    """
    db_camera = db.query(CameraDB).filter(CameraDB.id == camera_id).first()

    if not db_camera:
        raise HTTPException(status_code=404, detail="Camera not found")

    db.delete(db_camera)
    db.commit()
    return {"message": "Camera deleted successfully"}


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint for monitoring"""
    return {"status": "healthy"}