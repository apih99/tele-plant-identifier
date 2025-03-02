import os
import logging
import requests
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp-01-21')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! I'm a Plant Identifier Bot. Send me a photo of a plant, and I'll tell you what it is!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "Send me a clear photo of a plant, and I'll identify it for you. "
        "I'll provide information like the plant's name, scientific name, colors, "
        "a brief history, and treatment plan."
    )

async def process_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process the image sent by the user and identify the plant."""
    # Check if the message contains a photo
    if not update.message.photo:
        await update.message.reply_text("Please send me a photo of a plant.")
        return
    
    # Let the user know we're processing the image
    await update.message.reply_text("Analyzing your plant image... Please wait.")
    
    # Get the photo with the highest resolution
    photo = update.message.photo[-1]
    
    # Get the file from Telegram servers
    file = await context.bot.get_file(photo.file_id)
    file_url = file.file_path
    
    try:
        # Download the image
        response = requests.get(file_url)
        image_data = response.content
        
        # Prepare the prompt for Gemini
        prompt = """
        Identify this plant from the image. If this is not a plant or the image is unclear, 
        respond with ONLY: "I couldn't identify a plant in this image. Please send a clearer image of a plant."
        
        If it is a plant, provide the following information in this exact format:
        
        Name: [common name of the plant]
        Scientific Name: [scientific name]
        Colors: [main colors of the plant]
        Brief History: [a short paragraph about the plant's history or origin]
        Treatment Plan: [basic care instructions including water, light, soil requirements]
        """
        
        # Process with Gemini
        response = model.generate_content([prompt, {"mime_type": "image/jpeg", "data": image_data}])
        result = response.text
        
        # Check if Gemini couldn't identify a plant
        if "I couldn't identify a plant in this image" in result:
            await update.message.reply_text("❌ I couldn't identify a plant in this image. Please send a clearer image of a plant.")
        else:
            # Format the response to make it more visually appealing
            formatted_result = result.strip()
            
            # Replace section headers with emoji and formatting
            formatted_result = formatted_result.replace("Name:", "🌿 *Name:*")
            formatted_result = formatted_result.replace("Scientific Name:", "🌱 *Scientific Name:*")
            
            # Format the scientific name in italics (assuming it follows the Scientific Name: label)
            import re
            # Updated pattern to better match scientific names with various formats
            scientific_name_pattern = r"(🌱 \*Scientific Name:\* )([A-Z][a-z]+(?: [a-z]+)+)"
            formatted_result = re.sub(scientific_name_pattern, r"\1_\2_", formatted_result)
            formatted_result = formatted_result.replace("Colors:", "🎨 *Colors:*")
            formatted_result = formatted_result.replace("Brief History:", "📚 *Brief History:*")
            formatted_result = formatted_result.replace("Treatment Plan:", "💧 *Treatment Plan:*")
            
            # Add spacing between sections for better readability
            formatted_result = formatted_result.replace("🌿 *Name:*", "🌿 *Name:*")
            formatted_result = formatted_result.replace("🌱 *Scientific Name:*", "\n\n🌱 *Scientific Name:*")
            formatted_result = formatted_result.replace("🎨 *Colors:*", "\n\n🎨 *Colors:*")
            formatted_result = formatted_result.replace("📚 *Brief History:*", "\n\n📚 *Brief History:*")
            formatted_result = formatted_result.replace("💧 *Treatment Plan:*", "\n\n💧 *Treatment Plan:*")
            
            # Add timestamp at the end
            from datetime import datetime
            current_time = datetime.now().strftime("%I:%M %p")
            formatted_result += f"\n\n_{current_time}_"
            
            # Send the formatted response with Markdown parsing
            await update.message.reply_text(formatted_result, parse_mode='Markdown')
            
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        await update.message.reply_text(
            "Sorry, I encountered an error while processing your image. Please try again later."
        )

def main() -> None:
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.PHOTO, process_image))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()