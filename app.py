import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# টেলিগ্রাম বট টোকেন (আপনার টোকেন এখানে রাখুন)
TOKEN = "7263895780:AAE_bE8vRI3Ill9cqX1eH-HS9UWqZjqlXHE"

# পরীক্ষার প্রশ্ন সেট
questions = {
    "Q1": {
        "sentence": "The environment (a) _ various things. All the things of the environment are related to (b) _ another. Any chance in the ecosystem can (c) _ All the other parts. To prevent the environment of destruction is the (d) _ of human beings. The environment should be (e) _ neat and clean to enjoy a healthy and comfortable (f) _ . But people are not (g) _ of the dangerous effect of the ecological change. They do unwise things and bring about dangers for their own (h) _ . Imbalance in the ecology brings about chemistic (i) _ and the results of change of various natural (j) _.",
        "answers": {
            "a": ["includes", "contains", "consists of"],
            "b": ["each", "one", "every"],
            "c": ["affect", "impact", "influence"],
            "d": ["duty", "responsibility", "task"],
            "e": ["kept", "maintained", "preserved"],
            "f": ["life", "existence", "living"],
            "g": ["aware", "conscious", "mindful"],
            "h": ["selves", "existence", "future"],
            "i": ["imbalance", "disorder", "disruption"],
            "j": ["disasters", "calamities", "catastrophes"]
        }
    },
    "Q2": {
        "sentence": "A large number of people learn English (a) _ the world. Some people use it (b) _ a fast language and some people take it as a (c) _ language. Many international (d) _ now depend on English for (e) _ with offices in different countries. They offer employment to people (f) _ adequate knowledge of English. The advertisements (g) _ in many dailies (h) _ in English. So it would not be (i) _ to neglect this (j) _ language.",
        "answers": {
            "a": ["across", "around", "throughout"],
            "b": ["as", "like"],
            "c": ["second", "foreign", "official"],
            "d": ["organizations", "companies", "institutions"],
            "e": ["communication", "interaction"],
            "f": ["with", "having"],
            "g": ["are published", "appear", "are printed"],
            "h": ["are", "appear", "are written"],
            "i": ["wise", "smart", "good"],
            "j": ["global", "important", "universal"]
        }
    }
}

user_data = {}

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.message.chat_id] = {"score": 0, "current_question": None}
    keyboard = [[InlineKeyboardButton("Start Exam", callback_data="start_exam")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Examiner Bot! Click below to start the exam.", reply_markup=reply_markup)

# পরীক্ষা শুরু করার ফাংশন
async def start_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data[chat_id]["score"] = 0
    user_data[chat_id]["current_question"] = random.choice(list(questions.keys()))  # র্যান্ডম প্রশ্ন নির্বাচন
    await send_question(chat_id, context)

# প্রশ্ন পাঠানোর ফাংশন (র্যান্ডম প্রশ্ন)
async def send_question(chat_id, context):
    user_info = user_data[chat_id]
    question_key = user_info["current_question"]
    
    q_data = questions[question_key]
    
    # প্রশ্ন পাঠান
    await context.bot.send_message(chat_id, f"**{question_key}:** {q_data['sentence']}\n\nPlease type your answers as:\na) answer\nb) answer")

# উত্তর চেক করার ফাংশন
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_info = user_data.get(chat_id, None)

    if not user_info:
        await update.message.reply_text("Please start the exam by typing /start.")
        return

    question_key = user_info["current_question"]
    q_data = questions[question_key]
    
    user_answers = update.message.text.lower().split("\n")
    correct_count = 0
    incorrect_responses = []

    for ans in user_answers:
        parts = ans.split(") ")
        if len(parts) != 2:
            continue
        key, user_input = parts
        key = key.strip("(). ").lower()
        user_input = user_input.strip()

        if key in q_data["answers"] and user_input in q_data["answers"][key]:
            correct_count += 1
        else:
            incorrect_responses.append(f"❌ ({key}) Incorrect: {user_input} | Correct: {', '.join(q_data['answers'][key])}")

    user_info["score"] += correct_count

    # ফলাফল দেখানো
    response = f"✔️ Correct Answers: {correct_count}\n" + "\n".join(incorrect_responses) if incorrect_responses else "✅ All Correct!"
    await update.message.reply_text(response)

    # পরবর্তী প্রশ্নের জন্য আবার /start করতে হবে
    await update.message.reply_text("To take a new question, type /start.")

# বটের মেইন ফাংশন
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(start_exam, pattern="start_exam"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_answer))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
