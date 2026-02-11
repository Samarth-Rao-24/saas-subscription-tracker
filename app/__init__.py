def create_app():
    load_dotenv()

    app = Flask(__name__)

    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object("app.config.ProductionConfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")

    @app.route("/")
    def home():
        return "SaaS Subscription Tracker is running 🚀"

    return app
