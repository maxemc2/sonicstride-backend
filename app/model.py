from enum import Enum
from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
# Local Application Imports
from database import Base

# Enum for default scene
class SceneEnum(str, Enum):
    Running = 'Running'
    Walking = 'Walking'
    NULL = 'NULL'

# Enum for music genres
class GenreEnum(str, Enum):
    Ambient = 'Ambient'
    Nature_Sounds = 'Nature Sounds'
    Instrumental = 'Instrumental'
    Lofi = 'Lofi'
    Classical = 'Classical'
    Jazz = 'Jazz'
    Electronic = 'Electronic'
    Meditative = 'Meditative'
    Binaural_Beats = 'Binaural Beats'
    ASMR = 'ASMR'
    Chillhop = 'Chillhop'
    Soundscapes = 'Soundscapes'
    World_Music = 'World Music'
    Folk = 'Folk'
    Rain_Sounds = 'Rain Sounds'
    Ocean_Waves = 'Ocean Waves'
    White_Noise = 'White Noise'
    Other = 'other'

# SQLAlchemy model for the Musics table
class MusicsModel(Base):
    __tablename__ = 'musics'

    # Unique identifier
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4, unique=True, nullable=False)
    # Title of the experiment
    experiment_title = Column(String, nullable=False)
    # Default scene enum
    default_scene = Column(SQLAlchemyEnum(SceneEnum), nullable=False)
    # Genre enum
    genre = Column(SQLAlchemyEnum(GenreEnum), nullable=False)
    # Beats per minute, can be null
    bpm = Column(Integer, nullable=True)
    # Musical key, can be null
    key = Column(String, nullable=True)
    # Name of the song
    song_name = Column(String, nullable=False)
    # Track ID in the format '01A-001-V1'
    track_id = Column(String, nullable=False)
    # Music file path
    music_file = Column(String, nullable=False, default='path/to/music/file.mp3')
    # Upload date, auto set to current date and time
    upload_date = Column(DateTime, default=datetime.utcnow, nullable=False)