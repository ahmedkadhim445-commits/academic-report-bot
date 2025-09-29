# Academic Report Bot

A Telegram bot that generates professional academic reports in DOCX and PDF formats with structured content, proper formatting, and citation support.

## Features

- 🎓 Generates structured academic reports (5-40 pages)
- 🌐 Supports Arabic and English languages with proper RTL/LTR formatting
- 📝 Multiple citation styles: APA, IEEE, MLA, Harvard, Chicago
- 📄 Exports to DOCX (always) and PDF (when pandoc available)
- 🎯 Smart word count control (~360 words/page ±5%)
- 📋 Professional formatting: Times New Roman 14pt, 1.5 line spacing
- 🏗️ Complete document structure: cover page, TOC, introduction, body, conclusion, references

## Report Structure

Each generated report includes:

1. **Cover Page** - Title, student info, university details
2. **Table of Contents** - Clean heading list (no page numbers)
3. **Introduction** - Contextual overview of the topic
4. **Main Body** - Multiple sections with H1/H2 headings and bullet points:
   - Literature Review
   - Methodology  
   - Results and Analysis
   - Discussion
5. **Conclusion** - Summary and future directions
6. **References** - Properly formatted citations in chosen style

## Quick Start

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ahmedkadhim445-commits/academic-report-bot.git
   cd academic-report-bot
   ```

2. **Set up Python environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your BOT_TOKEN
   ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

### Docker Deployment

1. **Build and run with Docker:**
   ```bash
   docker build -t academic-report-bot .
   docker run -d --name report-bot -p 8080:8080 -e BOT_TOKEN=your_token_here academic-report-bot
   ```

2. **Or use Docker Compose:**
   ```yaml
   version: '3.8'
   services:
     academic-report-bot:
       build: .
       ports:
         - "8080:8080"
       environment:
         - BOT_TOKEN=your_telegram_bot_token
         - OPENAI_API_KEY=optional_openai_key
         - PANDOC_PATH=optional_pandoc_path
       restart: unless-stopped
   ```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BOT_TOKEN` | Yes | Telegram Bot Token from [@BotFather](https://t.me/botfather) |
| `OPENAI_API_KEY` | No | OpenAI API key (for future AI features) |
| `PANDOC_PATH` | No | Custom pandoc installation path |

## Bot Usage

1. **Start a conversation:** Send `/start` to the bot
2. **Follow the prompts:** The bot will ask for:
   - Report title
   - Language (Arabic/English)
   - Student name(s)
   - Professor name
   - University details
   - College and department
   - Academic year
   - Target pages (5-40)
   - Reference style (APA/IEEE/MLA/Harvard/Chicago)
3. **Receive your report:** The bot generates and sends your report in DOCX format (and PDF if available)

## Bot Commands

- `/start` - Begin creating a new report
- `/status` - Check current report generation progress  
- `/cancel` - Cancel current report generation

## Technical Details

### Word Count Control

The bot targets approximately 360 words per page (±5% tolerance) and automatically adjusts content through:
- **Expansion:** Adds elaborative sentences and details when content is too short
- **Trimming:** Removes redundant phrases when content is too long
- **Multi-pass adjustment:** Up to 3 adjustment passes for optimal length

### Language Support

- **English:** Left-to-right formatting with standard academic structure
- **Arabic:** Right-to-left formatting with proper Unicode support and RTL paragraph alignment

### File Export

- **DOCX:** Always generated with full formatting
- **PDF:** Generated via pypandoc when pandoc is available, gracefully skipped otherwise

### Health Check

The bot includes a Flask server for health monitoring:
- `GET /health` - Health check endpoint
- `GET /` - Service information

## Development

### Project Structure

```
academic-report-bot/
├── main.py              # Telegram bot with conversation handlers
├── report_builder.py    # DOCX generation with formatting
├── references.py        # Citation formatting (APA/IEEE/MLA/Harvard/Chicago)  
├── page_control.py      # Word count management (~360 words/page)
├── test_page_control.py # Unit tests for page control
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

### Running Tests

```bash
# Run page control tests
python test_page_control.py

# Run with coverage (install coverage first)
pip install coverage
coverage run test_page_control.py
coverage report
```

### Adding New Features

The modular design allows easy extension:
- **New citation styles:** Add formatters in `references.py`
- **Additional languages:** Extend language detection and formatting in `report_builder.py`
- **Enhanced content generation:** Modify section builders in `report_builder.py`
- **New export formats:** Add converters alongside PDF export logic

## Troubleshooting

### Common Issues

1. **"pypandoc not found" warnings:** PDF generation requires pandoc. Install with:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install pandoc
   
   # macOS
   brew install pandoc
   
   # Windows
   # Download from https://pandoc.org/installing.html
   ```

2. **Bot not responding:** Check that BOT_TOKEN is correctly set and bot is active

3. **Memory issues with large reports:** The bot limits reports to 40 pages to prevent resource exhaustion

4. **Unicode issues:** Ensure your system supports UTF-8 encoding for proper Arabic text handling

### Logs

The bot uses Python logging. Check console output for detailed operation logs and error messages.

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
