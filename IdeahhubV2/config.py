class Config:
    SECRET_KEY = "ideahub-secret-key"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/ideahub_pos"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = False  