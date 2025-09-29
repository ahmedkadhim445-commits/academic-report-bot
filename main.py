"""Main Telegram bot module for academic report generation."""

import os
import logging
import asyncio
from typing import Dict, Any, Optional
import tempfile
import shutil
from pathlib import Path

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    ConversationHandler, ContextTypes, filters
)
from telegram.constants import ParseMode
from flask import Flask, jsonify
import threading
from dotenv import load_dotenv

from report_builder import ReportBuilder
from page_control import get_page_estimate

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(TITLE, LANGUAGE, STUDENT_NAMES, PROFESSOR, UNIVERSITY, 
 COLLEGE, DEPARTMENT, YEAR, PAGES, REFERENCE_STYLE) = range(10)

# Bot data storage (in production, use database)
user_reports: Dict[int, Dict[str, Any]] = {}

class AcademicReportBot:
    """Academic Report Telegram Bot."""
    
    def __init__(self, token: str):
        self.token = token
        self.app = None
        self.flask_app = Flask(__name__)
        self._setup_flask()
    
    def _setup_flask(self):
        """Setup Flask app for health checks."""
        @self.flask_app.route('/health')
        def health_check():
            return jsonify({"status": "ok", "service": "academic-report-bot"})
        
        @self.flask_app.route('/')
        def root():
            return jsonify({
                "service": "academic-report-bot",
                "status": "running",
                "description": "Academic Report Generator Bot"
            })
    
    def run_flask(self):
        """Run Flask app in separate thread."""
        self.flask_app.run(host='0.0.0.0', port=8080, debug=False)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start command handler."""
        user = update.effective_user
        logger.info(f"User {user.id} started the bot")
        
        welcome_message = """
🎓 Welcome to Academic Report Bot!

I'll help you generate professional academic reports in DOCX format (and PDF if available).

I'll ask you a series of questions to customize your report:
• Report title
• Language (Arabic/English)  
• Student name(s)
• Professor name
• University details
• Number of pages (5-40)
• Reference style

Let's start! What's your report title?
        """
        
        await update.message.reply_text(welcome_message.strip())
        return TITLE
    
    async def get_title(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get report title."""
        user_id = update.effective_user.id
        title = update.message.text.strip()
        
        if not title or len(title) < 5:
            await update.message.reply_text(
                "Please provide a meaningful report title (at least 5 characters):"
            )
            return TITLE
            
        # Initialize user report data
        user_reports[user_id] = {'title': title}
        
        # Language selection
        keyboard = [['English', 'العربية']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"Great! Your report title is: *{title}*\n\n"
            "Now, please select the language for your report:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return LANGUAGE
    
    async def get_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get report language."""
        user_id = update.effective_user.id
        language_text = update.message.text.strip()
        
        if language_text == 'English':
            language = 'EN'
        elif language_text == 'العربية':
            language = 'AR'
        else:
            keyboard = [['English', 'العربية']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(
                "Please select a valid language option:",
                reply_markup=reply_markup
            )
            return LANGUAGE
            
        user_reports[user_id]['language'] = language
        
        await update.message.reply_text(
            f"Language set to: *{language_text}*\n\n"
            "Please enter the student name(s) (separate multiple names with commas):",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN
        )
        return STUDENT_NAMES
    
    async def get_student_names(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get student names."""
        user_id = update.effective_user.id
        names = update.message.text.strip()
        
        if not names:
            await update.message.reply_text("Please enter at least one student name:")
            return STUDENT_NAMES
            
        user_reports[user_id]['student_names'] = names
        
        await update.message.reply_text(
            f"Student name(s): *{names}*\n\n"
            "Please enter the professor's name:",
            parse_mode=ParseMode.MARKDOWN
        )
        return PROFESSOR
    
    async def get_professor(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get professor name."""
        user_id = update.effective_user.id
        professor = update.message.text.strip()
        
        if not professor:
            await update.message.reply_text("Please enter the professor's name:")
            return PROFESSOR
            
        user_reports[user_id]['professor'] = professor
        
        await update.message.reply_text(
            f"Professor: *{professor}*\n\n"
            "Please enter the university name:",
            parse_mode=ParseMode.MARKDOWN
        )
        return UNIVERSITY
    
    async def get_university(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get university name."""
        user_id = update.effective_user.id
        university = update.message.text.strip()
        
        if not university:
            await update.message.reply_text("Please enter the university name:")
            return UNIVERSITY
            
        user_reports[user_id]['university'] = university
        
        await update.message.reply_text(
            f"University: *{university}*\n\n"
            "Please enter the college name:",
            parse_mode=ParseMode.MARKDOWN
        )
        return COLLEGE
    
    async def get_college(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get college name."""
        user_id = update.effective_user.id
        college = update.message.text.strip()
        
        if not college:
            await update.message.reply_text("Please enter the college name:")
            return COLLEGE
            
        user_reports[user_id]['college'] = college
        
        await update.message.reply_text(
            f"College: *{college}*\n\n"
            "Please enter the department name:",
            parse_mode=ParseMode.MARKDOWN
        )
        return DEPARTMENT
    
    async def get_department(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get department name."""
        user_id = update.effective_user.id
        department = update.message.text.strip()
        
        if not department:
            await update.message.reply_text("Please enter the department name:")
            return DEPARTMENT
            
        user_reports[user_id]['department'] = department
        
        await update.message.reply_text(
            f"Department: *{department}*\n\n"
            "Please enter the academic year (e.g., 2024):",
            parse_mode=ParseMode.MARKDOWN
        )
        return YEAR
    
    async def get_year(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get academic year."""
        user_id = update.effective_user.id
        year_text = update.message.text.strip()
        
        try:
            year = int(year_text)
            if year < 2000 or year > 2030:
                raise ValueError("Year out of range")
        except ValueError:
            await update.message.reply_text(
                "Please enter a valid year (e.g., 2024):"
            )
            return YEAR
            
        user_reports[user_id]['year'] = year
        
        await update.message.reply_text(
            f"Academic year: *{year}*\n\n"
            "How many pages should the report have? (Enter a number between 5 and 40):",
            parse_mode=ParseMode.MARKDOWN
        )
        return PAGES
    
    async def get_pages(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get target page count."""
        user_id = update.effective_user.id
        pages_text = update.message.text.strip()
        
        try:
            pages = int(pages_text)
            if pages < 5 or pages > 40:
                raise ValueError("Pages out of range")
        except ValueError:
            await update.message.reply_text(
                "Please enter a valid number of pages (5-40):"
            )
            return PAGES
            
        user_reports[user_id]['pages'] = pages
        
        # Reference style selection
        keyboard = [
            ['APA', 'IEEE'],
            ['MLA', 'Harvard'],
            ['Chicago']
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        
        await update.message.reply_text(
            f"Target pages: *{pages}*\n\n"
            "Finally, please select your preferred reference style:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        return REFERENCE_STYLE
    
    async def get_reference_style(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Get reference style and generate report."""
        user_id = update.effective_user.id
        style = update.message.text.strip().upper()
        
        valid_styles = ['APA', 'IEEE', 'MLA', 'HARVARD', 'CHICAGO']
        if style not in valid_styles:
            keyboard = [
                ['APA', 'IEEE'],
                ['MLA', 'Harvard'],
                ['Chicago']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(
                "Please select a valid reference style:",
                reply_markup=reply_markup
            )
            return REFERENCE_STYLE
            
        user_reports[user_id]['reference_style'] = style
        
        # Show summary and start generating
        report_data = user_reports[user_id]
        summary = f"""
📋 *Report Summary:*

📖 Title: {report_data['title']}
🌐 Language: {report_data['language']}
👤 Student(s): {report_data['student_names']}
👨‍🏫 Professor: {report_data['professor']}
🏛️ University: {report_data['university']}
🏢 College: {report_data['college']}
📚 Department: {report_data['department']}
📅 Year: {report_data['year']}
📄 Pages: {report_data['pages']}
📝 Reference Style: {style}

🔄 Generating your report... This may take a few moments.
        """
        
        await update.message.reply_text(
            summary.strip(),
            reply_markup=ReplyKeyboardRemove(),
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Generate the report
        try:
            file_path = await self._generate_report(report_data)
            await self._send_report(update, file_path, report_data['title'])
            
            # Clean up
            if os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception as e:
            logger.error(f"Error generating report for user {user_id}: {e}")
            await update.message.reply_text(
                "❌ Sorry, there was an error generating your report. Please try again with /start."
            )
        
        # Clear user data
        if user_id in user_reports:
            del user_reports[user_id]
            
        return ConversationHandler.END
    
    async def _generate_report(self, report_data: Dict[str, Any]) -> str:
        """Generate the academic report."""
        logger.info(f"Generating report: {report_data['title']}")
        
        # Create report builder
        builder = ReportBuilder()
        
        # Build the report
        content = builder.build_report(report_data)
        
        # Save the document
        safe_title = "".join(c for c in report_data['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        filename = f"{safe_title}_report.docx"
        file_path = builder.save(filename)
        
        logger.info(f"Report generated: {file_path}")
        return file_path
    
    async def _send_report(self, update: Update, file_path: str, title: str):
        """Send the generated report to user."""
        try:
            # Try to convert to PDF if pypandoc is available
            pdf_path = None
            try:
                import pypandoc
                pdf_path = file_path.replace('.docx', '.pdf')
                pypandoc.convert_file(file_path, 'pdf', outputfile=pdf_path)
                logger.info(f"PDF generated: {pdf_path}")
            except ImportError:
                logger.info("pypandoc not available, skipping PDF generation")
            except Exception as e:
                logger.warning(f"PDF generation failed: {e}")
                pdf_path = None
            
            # Send DOCX file
            with open(file_path, 'rb') as docx_file:
                await update.message.reply_document(
                    document=docx_file,
                    filename=os.path.basename(file_path),
                    caption=f"📄 Your academic report: *{title}*\n\nGenerated in DOCX format.",
                    parse_mode=ParseMode.MARKDOWN
                )
            
            # Send PDF if available
            if pdf_path and os.path.exists(pdf_path):
                with open(pdf_path, 'rb') as pdf_file:
                    await update.message.reply_document(
                        document=pdf_file,
                        filename=os.path.basename(pdf_path),
                        caption=f"📄 Your academic report: *{title}*\n\nGenerated in PDF format.",
                        parse_mode=ParseMode.MARKDOWN
                    )
                os.remove(pdf_path)
            
            await update.message.reply_text(
                "✅ Report generated successfully!\n\n"
                "Use /start to generate another report."
            )
            
        except Exception as e:
            logger.error(f"Error sending report: {e}")
            await update.message.reply_text(
                "❌ Error sending the report. Please try again."
            )
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Status command handler."""
        user_id = update.effective_user.id
        
        if user_id in user_reports:
            report_data = user_reports[user_id]
            fields_completed = len([k for k, v in report_data.items() if v is not None])
            total_fields = 10
            
            status_text = f"📊 *Report Generation Status*\n\n"
            status_text += f"Progress: {fields_completed}/{total_fields} fields completed\n\n"
            
            for field, value in report_data.items():
                status_text += f"• {field.replace('_', ' ').title()}: {value if value else '❌ Not set'}\n"
                
            await update.message.reply_text(status_text, parse_mode=ParseMode.MARKDOWN)
        else:
            await update.message.reply_text(
                "📊 No active report generation session.\n\n"
                "Use /start to begin creating a new report."
            )
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel command handler."""
        user_id = update.effective_user.id
        
        if user_id in user_reports:
            del user_reports[user_id]
            
        await update.message.reply_text(
            "❌ Report generation cancelled.\n\n"
            "Use /start to begin a new report.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    async def unknown_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle unknown commands."""
        await update.message.reply_text(
            "❓ Unknown command. Available commands:\n\n"
            "/start - Start generating a new report\n"
            "/status - Check current progress\n"
            "/cancel - Cancel current report generation"
        )
    
    def run_bot(self):
        """Run the Telegram bot."""
        # Build application
        self.app = Application.builder().token(self.token).build()
        
        # Setup conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                TITLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_title)],
                LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_language)],
                STUDENT_NAMES: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_student_names)],
                PROFESSOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_professor)],
                UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_university)],
                COLLEGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_college)],
                DEPARTMENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_department)],
                YEAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_year)],
                PAGES: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_pages)],
                REFERENCE_STYLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_reference_style)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        
        # Add handlers
        self.app.add_handler(conv_handler)
        self.app.add_handler(CommandHandler('status', self.status))
        self.app.add_handler(MessageHandler(filters.COMMAND, self.unknown_command))
        
        logger.info("Starting Telegram bot...")
        
        # Start Flask in background thread
        flask_thread = threading.Thread(target=self.run_flask, daemon=True)
        flask_thread.start()
        logger.info("Flask health check server started on port 8080")
        
        # Run bot
        self.app.run_polling(drop_pending_updates=True)

def main():
    """Main function."""
    # Get bot token from environment
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logger.error("BOT_TOKEN environment variable is required")
        return
    
    # Create and run bot
    bot = AcademicReportBot(bot_token)
    
    try:
        bot.run_bot()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot error: {e}")

if __name__ == '__main__':
    main()