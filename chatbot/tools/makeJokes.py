from jokeapi import Jokes
import asyncio

def get_joke():
    """Fetch a random joke synchronously."""
    async def fetch_joke():
        # Initialize the joke API asynchronously
        jokes_api = await Jokes()
        # Get a random joke
        joke = await jokes_api.get_joke()
        # Format the joke
        if joke["type"] == "single":
            return joke["joke"]
        else:
            return f"{joke['setup']} - {joke['delivery']}"

    # Run the async function synchronously using asyncio.run()
    return asyncio.run(fetch_joke())
