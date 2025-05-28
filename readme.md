# Healthcare AI Agent 🏥

A smart AI agent that processes Excel files and fills healthcare-related data for specific states in India.

## Features ✨

- **Excel File Processing**: Upload blank Excel files with column headers
- **Automatic Data Filling**: AI agent fills data based on column names and keywords
- **State-Specific Data**: Currently supports Bihar state with comprehensive healthcare data
- **Multiple Categories**: Hospitals, Services, Companies, Funding Sources, Government Schemes
- **Download Results**: Get processed Excel files with filled data

## Installation 🚀

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/healthcare-ai-agent.git
cd healthcare-ai-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

### Deployment Options

#### 1. Streamlit Cloud (Recommended)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Deploy with one click

#### 2. Heroku Deployment
1. Create `Procfile`:
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

2. Deploy to Heroku:
```bash
heroku create your-app-name
git push heroku main
```

#### 3. Railway Deployment
1. Connect GitHub repo to Railway
2. Auto-deploy on push

## Usage 📋

### Step 1: Prepare Excel File
Create an Excel file with column headers containing keywords:
- `Hospital_Name` or `Medical_Center`
- `Services_Available` or `Treatment_Types`
- `Healthcare_Company` or `Provider`
- `Funding_Source` or `Finance`
- `Government_Scheme` or `Program`

### Step 2: Upload and Process
1. Select state (Bihar currently available)
2. Upload your Excel file
3. Click "Process File"
4. Download the filled Excel file

### Step 3: Use the Data
Use the processed data for:
- Healthcare analysis
- Research projects
- Policy planning
- Market analysis

## Data Categories 📊

### Bihar Healthcare Data
- **Hospitals**: AIIMS Patna, Patna Medical College, etc.
- **Services**: Primary, Secondary, Tertiary healthcare
- **Companies**: Apollo, Fortis, Max Healthcare, etc.
- **Funding**: NHM, Ayushman Bharat, World Bank, etc.
- **Schemes**: Government healthcare initiatives

## File Structure 📁

```
healthcare-ai-agent/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore file
└── data/                # Healthcare data (optional)
```

## Contributing 🤝

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-state`)
3. Add data for new states
4. Commit changes (`git commit -am 'Add new state data'`)
5. Push to branch (`git push origin feature/new-state`)
6. Create Pull Request

## Adding New States 🗺️

To add data for new states, update the `healthcare_data` dictionary in `app.py`:

```python
"new_state": {
    "hospitals": ["Hospital 1", "Hospital 2"],
    "services": ["Service 1", "Service 2"],
    "companies": ["Company 1", "Company 2"],
    "funding_sources": ["Source 1", "Source 2"],
    "government_schemes": ["Scheme 1", "Scheme 2"]
}
```

## Future Enhancements 🚀

- [ ] Add more states (Maharashtra, Karnataka, etc.)
- [ ] Real-time data fetching from government APIs
- [ ] Advanced analytics and visualization
- [ ] PDF report generation
- [ ] Database integration
- [ ] Multi-language support

## Technologies Used 💻

- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **OpenPyXL**: Excel file processing
- **Python**: Core programming language

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 🆘

For support, email your-email@example.com or create an issue on GitHub.

## Demo 🎥

[Add link to live demo here]

---

Made with ❤️ for Healthcare in India
