# Academic Report Bot

A Telegram bot that generates professional academic reports in both Word (.docx) and PDF formats. The bot guides users through a step-by-step process to collect all necessary information and generates properly formatted academic documents.

## Features

- 🎓 **Interactive Flow**: Step-by-step data collection via Telegram chat
- 📝 **Multiple Formats**: Generates both .docx and .pdf files
- 🌍 **Language Support**: English and Arabic language options
- 📊 **Flexible Length**: Supports reports from 5 to 40 pages
- 📚 **Reference Styles**: APA, IEEE, MLA, Harvard, and Chicago citation formats
- ✨ **Professional Formatting**: Times New Roman 14pt, 1.5 line spacing
- 📋 **Complete Structure**: Cover page, table of contents, introduction, body, conclusion, and references

## Requirements

- Python 3.11+
- LibreOffice (for PDF conversion)
- Telegram Bot Token

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ahmedkadhim445-commits/academic-report-bot.git
cd academic-report-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your BOT_TOKEN
```

4. Run the bot:
```bash
python bot.py
```

## Docker Usage

```bash
docker build -t academic-report-bot .
docker run -e BOT_TOKEN=your_token_here academic-report-bot
```

## Bot Flow

1. **Title**: Enter the report title
2. **Language**: Choose English or Arabic
3. **Student**: Enter student's full name
4. **Professor**: Enter professor's name
5. **University**: Enter university name
6. **College**: Enter college/faculty name
7. **Department**: Enter department name
8. **Year**: Enter academic year
9. **Pages**: Choose number of pages (5-40)
10. **Reference Style**: Select citation format (APA/IEEE/MLA/Harvard/Chicago)

The bot then generates and sends both .docx and .pdf versions of the academic report.

## Document Structure

- **Cover Page**: University, college, department, title, student/professor info
- **Table of Contents**: Section listing (without page numbers)
- **Introduction**: Research overview and objectives
- **Body Sections**: Literature review, methodology, results, analysis
- **Conclusion**: Summary and findings
- **References**: Properly formatted citations in chosen style

## License

MIT License - see [LICENSE](LICENSE) file for details.
