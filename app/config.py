from pydantic import BaseSettings
import os


class Setting(BaseSettings):
	"""Config file for setting up database connection URL"""

	database_host: str
	database_port: int
	database_password: str
	database_username: str
	database_name: str
	
	class Config:
		"""Declaring the env_file and pointing to required database credentials location"""

		env_file = ".env_cloud"
	
	
settings = Setting()
print(settings)
