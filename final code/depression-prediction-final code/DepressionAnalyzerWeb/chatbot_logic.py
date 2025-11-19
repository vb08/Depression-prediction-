import random

def get_chatbot_response(user_msg, user_name="Friend"):
    msg = user_msg.lower().strip()
    
    # Basic Greetings
    if any(g in msg for g in ["hi","hello","hey"]):
        return f"Hello {user_name}! 💛 How are you feeling today?"

    # Mood-based responses
    if any(w in msg for w in ["sad","depressed","down","hopeless"]):
        return "I’m sorry you're feeling sad 💛 I'm here to listen."

    if "stress" in msg:
        return "Stress is difficult. Try deep breathing for 2 minutes."

    if "depression" in msg:
        return "Depression is serious. Talking to someone helps a lot 💛"

    # Self-care tips
    if "self-care" in msg or "tips" in msg:
        tips = [
            "Sleep 7–8 hours daily.",
            "Eat healthy and stay hydrated.",
            "Go for a short walk outdoors.",
            "Practice mindfulness or meditation.",
            "Talk to someone you trust about your feelings."
        ]
        return "Here are some self-care tips:\n" + "\n".join(tips)

    # Motivational messages
    if "motivation" in msg or "quote" in msg:
        quotes = [
            "You are stronger than you think — keep going.",
            "Even the darkest night will end, and the sun will rise.",
            "Every day may not be good, but there’s something good in every day.",
            "Small steps every day lead to big changes.",
            "You’ve made it through 100% of your bad days so far — that’s strength!"
        ]
        return random.choice(quotes)

    # Helpline info
    if "helpline" in msg or "help" in msg:
        return ("Here are some mental health helplines:\n"
                "India: NIMHANS 080-4611 0007, AASRA +91-9820466726\n"
                "US: 988 Suicide and Crisis Lifeline\n"
                "UK: Samaritans 116 123")

    # Learn about depression
    if "learn" in msg or "depression" in msg:
        return ("Depression is a common mental health condition. "
                "Symptoms include sadness, fatigue, and loss of interest. "
                "Treatment includes therapy, medication, and emotional support.")

    # Default fallback
    return "I’m here for you. Tell me more 💛"
