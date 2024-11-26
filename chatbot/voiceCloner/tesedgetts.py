{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import asyncio\n",
    "import edge_tts"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [],
   "source": [
    "async def text_to_speech(text, voice, output_file):\n",
    "    \"\"\"Convert text to speech and save as an MP3.\"\"\"\n",
    "    tts = edge_tts.Communicate(text, voice)\n",
    "    with open(output_file, \"wb\") as file:\n",
    "        async for chunk in tts.stream():\n",
    "            if chunk[\"type\"] == \"audio\":\n",
    "                file.write(chunk[\"data\"])\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "d:\\backup project\\DreamConnect\\venv\\lib\\site-packages\\executing\\executing.py:845: RuntimeWarning: coroutine 'text_to_speech' was never awaited\n",
      "  for i, inst in islice(enumerate(instructions), start, None):\n",
      "RuntimeWarning: Enable tracemalloc to get the object allocation traceback\n",
      "d:\\backup project\\DreamConnect\\venv\\lib\\site-packages\\executing\\executing.py:845: RuntimeWarning: coroutine 'main' was never awaited\n",
      "  for i, inst in islice(enumerate(instructions), start, None):\n",
      "RuntimeWarning: Enable tracemalloc to get the object allocation traceback\n"
     ]
    },
    {
     "ename": "RuntimeError",
     "evalue": "asyncio.run() cannot be called from a running event loop",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mRuntimeError\u001b[0m                              Traceback (most recent call last)",
      "Cell \u001b[1;32mIn[11], line 8\u001b[0m\n\u001b[0;32m      5\u001b[0m     \u001b[38;5;28;01mawait\u001b[39;00m text_to_speech(text, voice, output_file)\n\u001b[0;32m      7\u001b[0m \u001b[38;5;66;03m# Run the main function in an async context\u001b[39;00m\n\u001b[1;32m----> 8\u001b[0m \u001b[43masyncio\u001b[49m\u001b[38;5;241;43m.\u001b[39;49m\u001b[43mrun\u001b[49m\u001b[43m(\u001b[49m\u001b[43mmain\u001b[49m\u001b[43m(\u001b[49m\u001b[43m)\u001b[49m\u001b[43m)\u001b[49m\n",
      "File \u001b[1;32mC:\\Program Files\\Python310\\lib\\asyncio\\runners.py:33\u001b[0m, in \u001b[0;36mrun\u001b[1;34m(main, debug)\u001b[0m\n\u001b[0;32m      9\u001b[0m \u001b[38;5;250m\u001b[39m\u001b[38;5;124;03m\"\"\"Execute the coroutine and return the result.\u001b[39;00m\n\u001b[0;32m     10\u001b[0m \n\u001b[0;32m     11\u001b[0m \u001b[38;5;124;03mThis function runs the passed coroutine, taking care of\u001b[39;00m\n\u001b[1;32m   (...)\u001b[0m\n\u001b[0;32m     30\u001b[0m \u001b[38;5;124;03m    asyncio.run(main())\u001b[39;00m\n\u001b[0;32m     31\u001b[0m \u001b[38;5;124;03m\"\"\"\u001b[39;00m\n\u001b[0;32m     32\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m events\u001b[38;5;241m.\u001b[39m_get_running_loop() \u001b[38;5;129;01mis\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[38;5;28;01mNone\u001b[39;00m:\n\u001b[1;32m---> 33\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mRuntimeError\u001b[39;00m(\n\u001b[0;32m     34\u001b[0m         \u001b[38;5;124m\"\u001b[39m\u001b[38;5;124masyncio.run() cannot be called from a running event loop\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[0;32m     36\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m coroutines\u001b[38;5;241m.\u001b[39miscoroutine(main):\n\u001b[0;32m     37\u001b[0m     \u001b[38;5;28;01mraise\u001b[39;00m \u001b[38;5;167;01mValueError\u001b[39;00m(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124ma coroutine was expected, got \u001b[39m\u001b[38;5;132;01m{!r}\u001b[39;00m\u001b[38;5;124m\"\u001b[39m\u001b[38;5;241m.\u001b[39mformat(main))\n",
      "\u001b[1;31mRuntimeError\u001b[0m: asyncio.run() cannot be called from a running event loop"
     ]
    }
   ],
   "source": [
    "async def main():\n",
    "    text = \"Hello, how are you today?\"\n",
    "    voice = \"en-US-AriaNeural\"  # Example voice\n",
    "    output_file = \"output.mp3\"\n",
    "    await text_to_speech(text, voice, output_file)\n",
    "\n",
    "# Run the main function in an async context\n",
    "asyncio.run(main())"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "venv",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.10.11"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
