from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_password: str 
    database_hostname : str
    database_username: str
    database_port : str
    secret_key : str
    database_name : str
    algorithm : str 
    access_token_expiration_time : int
    
    class Config:
        env_file = ".env"
    
    
settings = Settings()