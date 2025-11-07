# The Machine v2.0 - AI-Powered Surveillance System

“**What if an AI could observe information and decide what matters?**” Imagine an AI that watches information flow by and decides what’s important. This PoC shows how an AI can observe real-time data, extract meaningful signals, and generate a high-level narrative without intervening or taking action. This project was inspired by [@Jo-Dan](https://github.com/Jo-Dan) and their work on [The-Machine](https://github.com/Jo-Dan/The-Machine) and hit TV show Person of Interest's 'Machine'.

## 🚀 Key Features

- **AI Integration**: Drop-in architecture supporting multiple AI providers (OpenAI, DeepFace, TensorFlow, etc.)
- **Facial Recognition**: Real-time face detection and recognition using advanced algorithms
- **Secure Storage**: Encrypted data storage with Fernet encryption and file hashing
- **Tri-Authentication**: Password, face, and voice authentication for admin access
- **Multi-Camera Support**: Simultaneous monitoring from multiple camera sources
- **Privacy Features**: Face masking and privacy protection options
- **Comprehensive Logging**: Detailed event logging and system health monitoring
- **Watchlist Management**: Alert system for faces of interest
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Modular Design**: Easy to extend and customize

## 📁 Project Structure

```
The-Machine/
├── AI_INTERFACE.md           # Comprehensive API documentation
├── LICENSE                   # Project license
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── ai/
│   └── impl.py              # AI implementation with fallbacks
└── src/
    ├── main.py              # CLI entry point and menu system
    ├── admin_clean.py       # Clean admin interface with tri-auth
    ├── admin.py             # Admin utilities and management
    ├── ai_adapters.py       # Safe AI API wrappers
    ├── ai_core.py           # AI interface stubs and contracts
    ├── ai_hooks.py          # Event-driven AI integration hooks
    ├── ai_loader.py         # Dynamic AI module loading system
    ├── face_recognition.py  # Face recognition engine
    ├── face_tracking.py     # Real-time face tracking
    ├── secure_storage.py    # Encryption and secure data storage
    ├── facebase/
    │   ├── known_faces/     # Database of known faces
    │   ├── unknown_faces/   # Captured unknown faces
    │   └── watchlist/       # Faces requiring alerts
    └── utils/
        └── __init__.py      # Image processing utilities
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- Webcam(s) for video capture
- Optional: GPU for accelerated AI processing

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/degenwithheart/The-Machine.git
   cd The-Machine
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize secure storage:**
   ```bash
   python src/secure_storage.py
   ```
   This creates encryption keys and sets up the admin account.

5. **Add known faces:**
   Place clear, well-lit face images in `src/facebase/known_faces/`

6. **Run the system:**
   ```bash
   python src/main.py
   ```

## 🎯 Usage

### Main Menu Options
- **Camera Mode**: Start real-time surveillance
- **Admin Panel**: Access administrative functions
- **AI Integration**: Configure and test AI providers
- **System Status**: View health and performance metrics

### Admin Features
- Tri-authentication (password/face/voice)
- Face database management
- Watchlist configuration
- System monitoring and logs
- Privacy settings and masking
- Backup and restore functionality

### AI Integration
The system supports multiple AI providers through a drop-in architecture:
- OpenAI GPT integration
- DeepFace for facial analysis
- Custom AI modules via adapters
- Event-driven hooks for AI processing

## 🔧 Configuration

### Environment Variables
```bash
export AI_PROVIDER=openai  # or deepface, tensorflow, etc.
export ENCRYPTION_KEY_PATH=src/secret.key
export FACEBASE_PATH=src/facebase/
```

### AI Providers
Configure AI providers in `ai/impl.py` or add custom adapters in `src/ai_adapters.py`.

## 📚 Documentation

- **AI_INTERFACE.md**: Complete API reference and integration guide
- **Comprehensive Code Comments**: Every file includes detailed docstrings and inline comments for easy maintenance
- **Modular Architecture**: Easy to extend and customize components

## 🔒 Security Features

- **Encryption**: Fernet-based symmetric encryption for sensitive data
- **File Hashing**: SHA256 verification for data integrity
- **Secure Wipe**: Safe deletion of sensitive files
- **Access Control**: Multi-factor authentication for admin functions
- **Audit Logging**: Complete activity tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add comprehensive comments to new code
4. Test thoroughly
5. Submit a pull request

## 📝 Recent Updates (v2.0)

- ✅ **Complete Code Documentation**: Added comprehensive comments to all 12+ files
- ✅ **Enhanced AI Integration**: Improved drop-in architecture with better error handling
- ✅ **Security Improvements**: Strengthened encryption and authentication
- ✅ **Cross-Platform Compatibility**: Better support for Windows, macOS, Linux
- ✅ **Performance Optimizations**: Improved face detection and tracking algorithms
- ✅ **Modular Refactoring**: Cleaner separation of concerns and easier maintenance

## ⚠️ Notes

- Some features require optional dependencies (OpenCV, TensorFlow, etc.)
- GPU acceleration recommended for optimal AI performance
- Ensure proper lighting and camera positioning for best recognition accuracy
- System includes privacy protection features - review local laws before deployment

## 📄 License

See LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check AI_INTERFACE.md for technical details
- Review code comments for implementation guidance
- Create an issue on GitHub for bugs or feature requests
