# Voice AI Assistant

A real-time voice AI assistant built with LiveKit that provides conversational AI capabilities with comprehensive performance metrics tracking.

## 🚀 Features

- **Real-time Voice Conversation**: Natural voice interactions with low-latency responses
- **Multi-modal AI Stack**:
  - Speech-to-Text: Deepgram Nova-3 model with multilingual support
  - Language Model: Google Gemini 2.0 Flash
  - Text-to-Speech: Cartesia Sonic-2 with custom voice
- **Advanced Audio Processing**:
  - Voice Activity Detection (VAD) using Silero
  - Noise cancellation with BVC (Background Voice Cancellation)
  - Multilingual turn detection
- **Performance Monitoring**: Comprehensive metrics collection and Excel export
- **State Management**: Real-time tracking of user and agent states
- **Interrupt Handling**: Seamless user interruption support for natural conversations

## 🎤 Interrupt Handling

The voice agent supports natural conversation flow with intelligent interrupt handling:

- **Real-time Detection**: Uses Silero VAD to detect when user starts speaking
- **Graceful Interruption**: Automatically stops agent speech when user interrupts
- **Context Preservation**: Maintains conversation context across interruptions
- **Low-latency Response**: Quick detection and response to user voice activity
- **Natural Flow**: Enables back-and-forth conversation without waiting for agent to finish

This ensures conversations feel natural and responsive, similar to human-to-human interactions.

## 📊 Metrics Tracked

The application automatically tracks and logs key performance indicators:

- **EOU Delay**: End-of-utterance delay (time from user stops speaking to processing begins)
- **TTFT**: Time to First Token (LLM response latency)
- **TTFB**: Time to First Byte (TTS processing latency)
- **Total Latency**: Combined end-to-end response time

All metrics are automatically saved to Excel files with timestamps for analysis.

## 🛠️ Tech Stack

- **Framework**: LiveKit Agents
- **Speech Recognition**: Deepgram API
- **Language Model**: Google Gemini 2.0 Flash
- **Text-to-Speech**: Cartesia API
- **Audio Processing**: Silero VAD, BVC Noise Cancellation
- **Data Processing**: Pandas, OpenPyXL
- **Environment Management**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- API keys for:
  - LiveKit Cloud
  - Deepgram
  - Google AI (Gemini)
  - Cartesia

## 🚀 Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd voice-agent
   ```

2. **Create and activate virtual environment**:

   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # or
   source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following variables:
   ```env
   LIVEKIT_URL=your_livekit_url
   LIVEKIT_API_KEY=your_livekit_api_key
   LIVEKIT_API_SECRET=your_livekit_api_secret
   DEEPGRAM_API_KEY=your_deepgram_api_key
   GOOGLE_API_KEY=your_google_api_key
   CARTESIA_API_KEY=your_cartesia_api_key
   ```

## 🎯 Usage

### Download model files 

```bash
python agent.py download-files
```
### Running the Voice Agent on console

```bash
python agent.py console
```
### Connect to LiveKit playground
Start your agent in dev mode to connect it to LiveKit and make it available from anywhere on the internet

```bash
python agent.py dev
```

The agent will:

1. Initialize all AI services
2. Connect to the LiveKit room
3. Greet the user and start listening
4. Process voice interactions in real-time
5. Log performance metrics automatically

### Metrics Collection

Metrics are automatically collected during conversations and saved to Excel files in the `metrics/` folder. Files are named with timestamps (e.g., `session_metrics20250609_031434.xlsx`).

## 📁 Project Structure

```
voice-agent/
├── agent.py              # Main application entry point
├── metrics.py             # Metrics collection and Excel export
├── requirements.txt       # Python dependencies
├── .env                  # Environment variables (create this)
├── README.md             # This file
├── metrics/              # Generated metrics Excel files

```

## 🔧 Configuration

### Agent Behavior

The AI assistant is configured with:

- **Instructions**: Helpful, concise responses (max 2 lines)
- **Temperature**: 0.8 (balanced creativity and consistency)
- **Language**: Multilingual support
- **Voice**: Custom Cartesia voice profile

### Audio Settings

- **STT Model**: Deepgram Nova-3 (multilingual)
- **TTS Model**: Cartesia Sonic-2
- **VAD**: Silero Voice Activity Detection
- **Noise Cancellation**: BVC (Background Voice Cancellation)

## 📊 Performance Metrics

The application tracks several key performance indicators:

| Metric        | Description                                 | Typical Range |
| ------------- | ------------------------------------------- | ------------- |
| EOU Delay     | Time from user stops speaking to processing | 100-500ms     |
| TTFT          | LLM first token generation time             | 200-800ms     |
| TTFB          | TTS first audio byte generation             | 100-400ms     |
| Total Latency | End-to-end response time                    | 500-1500ms    |

## 🔍 Monitoring

The application provides real-time console output showing:

- User and agent state changes
- Performance metrics as they're collected
- Connection status and errors

## 🛡️ Security Notes

- Keep your `.env` file secure and never commit it to version control
- Use environment-specific API keys
- Consider rate limiting for production deployments
- Monitor API usage and costs

## 🚀 Deployment

For production deployment:

1. Set up a production LiveKit server
2. Configure proper logging and monitoring
3. Implement rate limiting and user authentication
4. Set up automated metrics analysis
5. Consider containerization with Docker

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Audio not working**: Check microphone permissions and audio device settings
2. **High latency**: Verify internet connection and API key quotas
3. **Connection errors**: Ensure LiveKit URL and credentials are correct
4. **Missing metrics**: Check that Excel files are being generated in the metrics folder

### Support

For support and questions:

- Check the LiveKit documentation
- Review API provider documentation (Deepgram, Google, Cartesia)
- Open an issue in this repository

## 🔄 Recent Updates

- Integrated comprehensive metrics tracking
- Added Excel export functionality
- Improved error handling and state management
- Enhanced multilingual support
- Added noise cancellation features

---

**Note**: This is a development version. For production use, additional security, monitoring, and scaling considerations should be implemented.
