#!/usr/bin/env python3
"""
Academic Report Bot - A Telegram bot for generating professional academic reports
"""

import os
import logging
from typing import Dict, Any
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
from report_generator import ReportGenerator

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(TITLE, LANGUAGE, STUDENT, PROFESSOR, UNIVERSITY, 
 COLLEGE, DEPARTMENT, YEAR, PAGES, REF_STYLE) = range(10)

class AcademicReportBot:
    def __init__(self):
        self.report_generator = ReportGenerator()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start the conversation and ask for report title."""
        await update.message.reply_text(
            "🎓 Welcome to Academic Report Generator Bot!\n\n"
            "I'll help you create a professional academic report in both Word (.docx) and PDF formats.\n\n"
            "Let's start by entering the title of your report:"
        )
        return TITLE

    async def get_title(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store title and ask for language."""
        context.user_data['title'] = update.message.text
        
        keyboard = [['English', 'Arabic']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"Great! Your report title: '{update.message.text}'\n\n"
            "Now, please select the language for your report:",
            reply_markup=reply_markup
        )
        return LANGUAGE

    async def get_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store language and ask for student name."""
        lang_map = {'English': 'EN', 'Arabic': 'AR'}
        language = update.message.text
        
        if language not in lang_map:
            await update.message.reply_text(
                "Please select either 'English' or 'Arabic' using the keyboard."
            )
            return LANGUAGE
            
        context.user_data['language'] = lang_map[language]
        
        await update.message.reply_text(
            f"Language set to: {language}\n\n"
            "Please enter the student's full name:",
            reply_markup=ReplyKeyboardRemove()
        )
        return STUDENT

    async def get_student(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store student name and ask for professor name."""
        context.user_data['student'] = update.message.text
        
        await update.message.reply_text(
            f"Student: {update.message.text}\n\n"
            "Please enter the professor's name:"
        )
        return PROFESSOR

    async def get_professor(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store professor name and ask for university."""
        context.user_data['professor'] = update.message.text
        
        await update.message.reply_text(
            f"Professor: {update.message.text}\n\n"
            "Please enter the university name:"
        )
        return UNIVERSITY

    async def get_university(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store university and ask for college."""
        context.user_data['university'] = update.message.text
        
        await update.message.reply_text(
            f"University: {update.message.text}\n\n"
            "Please enter the college/faculty name:"
        )
        return COLLEGE

    async def get_college(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store college and ask for department."""
        context.user_data['college'] = update.message.text
        
        await update.message.reply_text(
            f"College: {update.message.text}\n\n"
            "Please enter the department name:"
        )
        return DEPARTMENT

    async def get_department(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store department and ask for year."""
        context.user_data['department'] = update.message.text
        
        await update.message.reply_text(
            f"Department: {update.message.text}\n\n"
            "Please enter the academic year (e.g., 2024):"
        )
        return YEAR

    async def get_year(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store year and ask for number of pages."""
        try:
            year = int(update.message.text)
            if year < 1900 or year > 2100:
                raise ValueError("Invalid year range")
        except ValueError:
            await update.message.reply_text(
                "Please enter a valid year (e.g., 2024):"
            )
            return YEAR
            
        context.user_data['year'] = year
        
        await update.message.reply_text(
            f"Year: {year}\n\n"
            "Please enter the number of pages for your report (5-40):"
        )
        return PAGES

    async def get_pages(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store pages and ask for reference style."""
        try:
            pages = int(update.message.text)
            if pages < 5 or pages > 40:
                raise ValueError("Pages out of range")
        except ValueError:
            await update.message.reply_text(
                "Please enter a valid number of pages between 5 and 40:"
            )
            return PAGES
            
        context.user_data['pages'] = pages
        
        keyboard = [['APA', 'IEEE'], ['MLA', 'Harvard'], ['Chicago']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"Pages: {pages}\n\n"
            "Finally, please select the reference style:",
            reply_markup=reply_markup
        )
        return REF_STYLE

    async def get_ref_style(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store reference style and generate report."""
        ref_styles = ['APA', 'IEEE', 'MLA', 'Harvard', 'Chicago']
        ref_style = update.message.text
        
        if ref_style not in ref_styles:
            await update.message.reply_text(
                "Please select a valid reference style using the keyboard."
            )
            return REF_STYLE
            
        context.user_data['ref_style'] = ref_style
        
        await update.message.reply_text(
            f"Reference style: {ref_style}\n\n"
            "🔄 Generating your academic report... This may take a few moments.",
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Generate the report
        try:
            report_data = context.user_data
            docx_path, pdf_path = await self.report_generator.generate_report(report_data)
            
            # Send both files
            with open(docx_path, 'rb') as docx_file:
                await update.message.reply_document(
                    document=docx_file,
                    filename=f"{report_data['title']}.docx",
                    caption="📄 Your academic report in Word format"
                )
            
            with open(pdf_path, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"{report_data['title']}.pdf",
                    caption="📄 Your academic report in PDF format"
                )
            
            await update.message.reply_text(
                "✅ Report generated successfully!\n\n"
                "Use /start to create another report."
            )
            
            # Clean up files
            os.remove(docx_path)
            os.remove(pdf_path)
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            await update.message.reply_text(
                "❌ Sorry, there was an error generating your report. Please try again with /start."
            )
        
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel the conversation."""
        await update.message.reply_text(
            "Report generation cancelled. Use /start to begin again.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

def main():
    """Start the bot."""
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logger.error("BOT_TOKEN not found in environment variables")
        return
    
    # Create bot instance
    bot = AcademicReportBot()
    
    # Create application
    application = Application.builder().token(bot_token).build()
    
    # Add conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', bot.start)],
        states={
            TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_title)],
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_language)],
            STUDENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_student)],
            PROFESSOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_professor)],
            UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_university)],
            COLLEGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_college)],
            DEPARTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_department)],
            YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_year)],
            PAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_pages)],
            REF_STYLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, bot.get_ref_style)],
        },
        fallbacks=[CommandHandler('cancel', bot.cancel)],
    )
    
    application.add_handler(conv_handler)
    
    # Start the bot
    logger.info("Starting Academic Report Bot...")
    application.run_polling()

if __name__ == '__main__':
    main()