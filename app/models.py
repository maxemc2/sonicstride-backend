from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, JSON, TIMESTAMP, Enum, func
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from database import Base

class SceneEnum(str, PyEnum):
    Running = 'Running'
    Walking = 'Walking'
    NULL = 'NULL'

class GenreEnum(str, PyEnum):
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
    Other = 'Other'

class Config(Base):
    __tablename__ = 'configs'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    author = Column(String, default='Sonicstride')
    interaction_type = Column(String)
    bpm = Column(Integer)
    create_time = Column(TIMESTAMP, server_default=func.now())
    labels = Column(String)

    audios = relationship("ConfigAudio", back_populates="config")
    tracks = relationship("Track", back_populates="config")

class AudioFile(Base):
    __tablename__ = 'audio_files'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    author = Column(String)
    type = Column(String, nullable=False)
    genre = Column(Enum(GenreEnum))
    key = Column(String)
    bpm = Column(Integer)
    file_path = Column(String, nullable=False)

    configs = relationship("ConfigAudio", back_populates="audio_file")

class ConfigAudio(Base):
    __tablename__ = 'config_audios'
    config_id = Column(Integer, ForeignKey('configs.id'), primary_key=True)
    audio_id = Column(Integer, ForeignKey('audio_files.id'), primary_key=True)

    config = relationship("Config", back_populates="audios")
    audio_file = relationship("AudioFile", back_populates="configs")

class Track(Base):
    __tablename__ = 'tracks'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    config_id = Column(Integer, ForeignKey('configs.id'))
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    loop = Column(Boolean)
    decay = Column(Boolean)
    initial_gain = Column(Float)
    track_initial_gain = Column(Float)
    track_gain_node = Column(JSON)
    effect_nodes = Column(JSON)

    config = relationship("Config", back_populates="tracks")
    events = relationship("Event", back_populates="track")

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    track_id = Column(Integer, ForeignKey('tracks.id'))
    type = Column(String, nullable=False)

    track = relationship("Track", back_populates="events")
    actions = relationship("Action", back_populates="event")

class Action(Base):
    __tablename__ = 'actions'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    event_id = Column(Integer, ForeignKey('events.id'))
    target = Column(String)
    property = Column(String)
    method = Column(String)
    value = Column(Float)
    end_time = Column(Float)

    event = relationship("Event", back_populates="actions")
