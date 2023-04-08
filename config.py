# import os
#
#
# class Config:
#     DEBUG = False
#     TESTING = False
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'my_secret_key'
#     # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///mydatabase.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#
#
# class DevelopmentConfig(Config):
#     DEBUG = True
#
#
# class TestingConfig(Config):
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///mytestdatabase.db'
#
#
# class ProductionConfig(Config):
#     pass
