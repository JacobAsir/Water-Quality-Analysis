# 💧 Water Quality Analysis System

A comprehensive machine learning-powered application for analyzing water quality parameters and providing expert recommendations for agricultural irrigation. The system features an intelligent chatbot that offers personalized advice based on water quality analysis results.

## 🌟 Features

- **Real-time Water Quality Analysis**: Analyze 9 key water quality parameters using machine learning
- **AI-Powered Expert Consultation**: Get personalized recommendations from an intelligent chatbot
- **Multi-language Support**: Available in English and Japanese
- **Interactive Dashboard**: Modern, responsive web interface with dark theme
- **Irrigation Suitability Assessment**: Determine if water is suitable for agricultural use
- **Treatment Recommendations**: Get specific advice on water treatment methods
- **Optimal Range Guidelines**: Built-in reference for optimal water quality parameters

## 🔬 Water Quality Parameters

The system analyzes the following parameters:

| Parameter | Unit | Optimal Range |
|-----------|------|---------------|
| pH | - | 6.5 - 8.5 |
| Hardness | mg/L | < 300 |
| Total Dissolved Solids (TDS) | ppm | < 1000 |
| Chloramines | mg/L | Variable |
| Sulfate | mg/L | < 400 |
| Conductivity | μS/cm | < 750 |
| Organic Carbon | mg/L | Variable |
| Trihalomethanes | μg/L | < 80 |
| Turbidity | NTU | < 5 |

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- GroQ API key for chatbot functionality

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/water-quality-analysis.git
   cd water-quality-analysis
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create .env file and add your GroQ API key
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## 📊 Machine Learning Model

The application uses a Support Vector Machine (SVM) classifier trained on water quality data to predict water potability. The model considers all 9 water quality parameters to make accurate predictions.

### Model Performance
- High accuracy in predicting water suitability for irrigation
- Robust handling of various water quality scenarios
- Standardized input processing for consistent results

## 🤖 AI Chatbot Features

The integrated chatbot provides:

- **Personalized Recommendations**: Based on your specific water quality results
- **Treatment Suggestions**: Specific methods to improve water quality
- **Crop-Specific Advice**: Recommendations tailored to different crop types
- **Multi-language Support**: Responses in English or Japanese
- **Context-Aware Conversations**: Maintains conversation history for better assistance

## 🛠️ Technology Stack

- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python
- **Machine Learning**: scikit-learn (SVM)
- **AI Chatbot**: LangChain + GroQ (Llama 3.1)
- **Data Processing**: pandas, numpy
- **Visualization**: plotly, matplotlib, seaborn

## 📁 Project Structure

```
water-quality-analysis/
├── app.py                      # Main Streamlit application
├── main.py                     # Core prediction and chatbot functions
├── chat.py                     # Chatbot implementation
├── model.pkl                   # Trained ML model
├── Water_quality_notebook.ipynb # Model training notebook
├── water_quality_data.csv      # Training dataset
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables
└── README.md                   # Project documentation
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Model Configuration

The application automatically loads the pre-trained model from `model.pkl`. If you want to retrain the model:

1. Open `Water_quality_notebook.ipynb`
2. Run all cells to train a new model
3. The new model will be saved as `model.pkl`

## 📈 Usage Examples

### Basic Water Quality Analysis

1. Enter water quality parameters in the left panel
2. Click "Analyze Water Quality"
3. View results and recommendations
4. Use the chatbot for detailed consultation

### Expert Consultation

1. After analyzing water quality, use the chat interface
2. Ask specific questions about:
   - Water treatment methods
   - Crop recommendations
   - Irrigation best practices
   - Parameter optimization

## 🌍 Multi-language Support

The application supports:
- **English**: Full interface and chatbot responses
- **Japanese**: Complete localization including chatbot

Switch languages using the dropdown in the top-right corner.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Water quality dataset contributors
- GroQ for providing AI model access
- Streamlit community for the excellent framework
- scikit-learn for machine learning capabilities


**Made with ❤️ for sustainable agriculture and water management**
