import os
from dotenv import load_dotenv
load_dotenv() # Load .env file when module is imported

import datetime # Added for current year
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, Column, Integer, Text, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "a_default_fallback_secret_key_for_dev")

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Initialize database tables and create admin user if needed
def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        print("Database tables checked/created.")
        
        # Check if there's at least one user in the database
        db_session = next(get_db_session())
        user_count = db_session.query(User).count()
        if user_count == 0:
            admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
            admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
            print(f"Creating default admin user (email: {admin_email})")
            admin_user = User(email=admin_email)
            admin_user.set_password(admin_password)
            db_session.add(admin_user)
            db_session.commit()
        db_session.close()
    except Exception as e:
        print(f"Error initializing database: {e}")

# --- Database Setup ---
RAW_DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = ""

if not RAW_DATABASE_URL:
    print("WARNING: DATABASE_URL environment variable not found for Flask app. Using initial local placeholder.")
    DATABASE_URL = "postgresql://user:password@host:port/dbname_placeholder_initial"
elif RAW_DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = RAW_DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://", 1)
    print(f"Flask App: Adjusted DATABASE_URL from asyncpg to sync: {DATABASE_URL}")
elif RAW_DATABASE_URL.startswith("postgres://"): # Heroku-style
    DATABASE_URL = RAW_DATABASE_URL.replace("postgres://", "postgresql://", 1)
    print(f"Flask App: Adjusted DATABASE_URL from Heroku-style to sync: {DATABASE_URL}")
else:
    DATABASE_URL = RAW_DATABASE_URL

print(f"Flask App: Final DATABASE_URL for engine creation: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base, UserMixin):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

class Joke(Base):
    __tablename__ = "jokes"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    joke_text = Column(Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    db_session = next(get_db_session())
    try:
        return db_session.query(User).get(int(user_id))
    finally:
        db_session.close()

# Context processor to make current year available to all templates
@app.context_processor
def inject_current_year():
    return {'current_year': datetime.datetime.utcnow().year}

# Initialize the database when the app is created
with app.app_context():
    init_db()

def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash('Please enter both email and password', 'warning')
            return render_template('login.html')
        
        db_session = next(get_db_session())
        try:
            user = db_session.query(User).filter_by(email=email).first()
            
            if user and user.check_password(password):
                login_user(user)
                next_page = request.args.get('next')
                flash('Logged in successfully', 'success')
                return redirect(next_page or url_for('index'))
            else:
                flash('Invalid email or password', 'danger')
        except SQLAlchemyError as e:
            flash(f"Database error: {str(e)}", "danger")
        finally:
            db_session.close()
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not email or not password:
            flash('Please enter both email and password', 'warning')
            return render_template('register.html')
            
        if password != confirm_password:
            flash('Passwords do not match', 'warning')
            return render_template('register.html')
        
        db_session = next(get_db_session())
        try:
            existing_user = db_session.query(User).filter_by(email=email).first()
            if existing_user:
                flash('Email already registered', 'warning')
                return render_template('register.html')
            
            new_user = User(email=email)
            new_user.set_password(password)
            db_session.add(new_user)
            db_session.commit()
            
            flash('Account created successfully. Please log in.', 'success')
            return redirect(url_for('login'))
        except SQLAlchemyError as e:
            db_session.rollback()
            flash(f"Error creating account: {str(e)}", "danger")
        finally:
            db_session.close()
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route("/")
@login_required
def index():
    db_session = next(get_db_session())
    jokes_list = []
    try:
        jokes_list = db_session.query(Joke).order_by(Joke.id).all()
    except SQLAlchemyError as e:
        flash(f"Error fetching jokes: {str(e)}", "danger")
    finally:
        db_session.close()
    return render_template("index.html", jokes=jokes_list)

@app.route("/add", methods=["GET", "POST"])
@login_required
def add_joke():
    if request.method == "POST":
        joke_text = request.form.get("joke_text")
        if not joke_text or joke_text.strip() == "":
            flash("Joke text cannot be empty!", "warning")
            return redirect(url_for("add_joke"))
        
        db_session = next(get_db_session())
        try:
            new_joke = Joke(joke_text=joke_text.strip())
            db_session.add(new_joke)
            db_session.commit()
            flash("Joke added successfully!", "success")
            return redirect(url_for("index"))
        except SQLAlchemyError as e:
            db_session.rollback()
            flash(f"Error adding joke: {str(e)}", "danger")
        finally:
            db_session.close()
    return render_template("add_joke.html")

@app.route("/edit/<int:joke_id>", methods=["GET", "POST"])
@login_required
def edit_joke(joke_id):
    db_session = next(get_db_session())
    joke_to_edit = None
    try:
        joke_to_edit = db_session.query(Joke).get(joke_id)
        if not joke_to_edit:
            flash("Joke not found!", "danger")
            return redirect(url_for("index"))

        if request.method == "POST":
            new_text = request.form.get("joke_text")
            if not new_text or new_text.strip() == "":
                flash("Joke text cannot be empty!", "warning")
                return render_template("edit_joke.html", joke=joke_to_edit)
            
            joke_to_edit.joke_text = new_text.strip()
            db_session.commit()
            flash("Joke updated successfully!", "success")
            return redirect(url_for("index"))
        
        return render_template("edit_joke.html", joke=joke_to_edit)
    except SQLAlchemyError as e:
        if db_session.is_active:
            db_session.rollback()
        flash(f"Error editing joke: {str(e)}", "danger")
        return redirect(url_for("index"))
    finally:
        db_session.close()

@app.route("/delete/<int:joke_id>", methods=["POST"])
@login_required
def delete_joke(joke_id):
    db_session = next(get_db_session())
    try:
        joke_to_delete = db_session.query(Joke).get(joke_id)
        if joke_to_delete:
            db_session.delete(joke_to_delete)
            db_session.commit()
            flash("Joke deleted successfully!", "success")
        else:
            flash("Joke not found!", "danger")
    except SQLAlchemyError as e:
        if db_session.is_active:
            db_session.rollback()
        flash(f"Error deleting joke: {str(e)}", "danger")
    finally:
        db_session.close()
    return redirect(url_for("index"))

@app.route("/mcp-config")
@login_required
def mcp_config():
    api_key = os.getenv("JOKE_MCP_SERVER_API_KEY", "123")
    return render_template("mcp_config.html", api_key=api_key)

if __name__ == "__main__":
    # This block is for direct execution (python app.py)
    # .env is already loaded at the top of the file.
    print("Flask app __main__ block: Running for local development.")
    print(f"Flask app __main__ block: Using DATABASE_URL: {DATABASE_URL}")
    
    # Initialize database tables and admin user
    init_db()
    
    print(f"Flask app starting locally on http://0.0.0.0:5001")
    app.run(debug=True, host="0.0.0.0", port=5001)
