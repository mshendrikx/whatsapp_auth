import dotenv
import project

dotenv.load_dotenv()

app = project.create_app()

app.run()