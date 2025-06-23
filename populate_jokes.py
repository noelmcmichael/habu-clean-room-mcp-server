import asyncio
from dotenv import load_dotenv
load_dotenv()

from sqlalchemy.ext.asyncio import AsyncSession
from database import engine
from models import Base, Joke

sample_jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my wife she was drawing her eyebrows too high. She looked surprised.",
    "Why don't programmers like nature? It has too many bugs.",
    "I used to hate facial hair, but then it grew on me.",
    "What do you call a fake noodle? An impasta!",
    "Why did the scarecrow win an award? He was outstanding in his field!",
    "I'm reading a book about anti-gravity. It's impossible to put down!",
    "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
    "Why don't skeletons fight each other? They don't have the guts.",
    "I would tell you a UDP joke, but you might not get it."
]

async def populate_database():
    """Populate the database with sample jokes."""
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Adding sample jokes...")
    async with AsyncSession(engine, expire_on_commit=False) as db_session:
        # Check if jokes already exist
        from sqlalchemy.future import select
        result = await db_session.execute(select(Joke))
        existing_jokes = result.scalars().all()
        
        if existing_jokes:
            print(f"Database already has {len(existing_jokes)} jokes. Skipping population.")
            return
        
        # Add sample jokes
        for joke_text in sample_jokes:
            joke = Joke(joke_text=joke_text)
            db_session.add(joke)
        
        await db_session.commit()
        print(f"Added {len(sample_jokes)} jokes to the database.")

if __name__ == "__main__":
    asyncio.run(populate_database())