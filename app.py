from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# টেলিগ্রাম বট টোকেন (আপনার টোকেন এখানে রাখুন)
TOKEN = "7263895780:AAE_bE8vRI3Ill9cqX1eH-HS9UWqZjqlXHE"

# পরীক্ষার প্রশ্ন সেট
questions = {
    "Q1": {
        "sentence": "The environment (a) _ various things. All the things of the environment are related to (b) _ another.",
        "answers": {
            "a": ["includes", "contains", "consists of"],
            "b": ["each", "one", "every"]
        }
    },
    "Q2": {
        "sentence": "A large number of people learn English (a) _ the world. Some people use it (b) _ a fast language.",
        "answers": {
            "a": ["across", "around", "throughout"],
            "b": ["as", "like"]
        }
    }
}

user_data = {}

# /start কমান্ড
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data[update.message.chat_id] = {"score": 0, "current_question": 0}
    keyboard = [[InlineKeyboardButton("Start Exam", callback_data="start_exam")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Examiner Bot! Click below to start.", reply_markup=reply_markup)

# পরীক্ষা শুরু করার ফাংশন
async def start_exam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_data[chat_id]["score"] = 0
    user_data[chat_id]["current_question"] = 0
    await send_question(chat_id, context)

# প্রশ্ন পাঠানোর ফাংশন
async def send_question(chat_id, context):
    user_info = user_data[chat_id]
    question_keys = list(questions.keys())

    if user_info["current_question"] < len(question_keys):
        q_key = question_keys[user_info["current_question"]]
        q_data = questions[q_key]
        
        await context.bot.send_message(chat_id, f"**{q_key}:** {q_data['sentence']}\n\nPlease type your answers as:\na) answer\nb) answer")
    
    else:
        await context.bot.send_message(chat_id, f"Exam finished! Your total score: {user_info['score']} / {len(questions) * 2}")

# উত্তর চেক করার ফাংশন
async def check_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    user_info = user_data.get(chat_id, None)

    if not user_info:
        await update.message.reply_text("Please start the exam by typing /start.")
        return

    question_keys = list(questions.keys())
    current_question_index = user_info["current_question"]

    if current_question_index >= len(question_keys):
        await update.message.reply_text("You have completed the exam! Type /start to take it again.")
        return

    q_key = question_keys[current_question_index]
    q_data = questions[q_key]
    
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
    user_info["current_question"] += 1

    # ফলাফল দেখানো
    response = f"✔️ Correct Answers: {correct_count}\n" + "\n".join(incorrect_responses) if incorrect_responses else "✅ All Correct!"
    await update.message.reply_text(response)

    # পরবর্তী প্রশ্ন পাঠানো
    await send_question(chat_id, context)

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
