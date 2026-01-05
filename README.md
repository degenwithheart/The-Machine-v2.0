# The Machine v2.0 - AI-Powered Surveillance System

## Features

✅ **Real-time Face Recognition** - Detect and identify faces from camera feed
✅ **ECC Encryption** - Bitcoin-style SECP256k1 elliptic curve cryptography
✅ **AI Integration** - OpenAI GPT and DeepFace support
✅ **Admin Panel** - Secure management interface
✅ **Event Logging** - Comprehensive surveillance logs
✅ **Unknown Face Capture** - Automatically save unidentified faces

## Quick Start

### 1. Install

```bash
./INSTALL.sh
```

### 2. Activate Environment

```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### 3. Add Known Faces

Place clear face images in `src/facebase/known_faces/`:

- Format: `person_name.jpg`
- Example: `john_doe.jpg`, `jane_smith.jpg`

### 4. Run

```bash
python src/main.py
```

## Usage

### Camera Mode

- Press **'q'** to quit
- Press **'s'** to save current frame
- Press **'l'** to save event log
- Press **'r'** to reload known faces database

### Admin Panel

Default password: `admin123` ⚠️ **Change immediately!**

**Features:**

- View system statistics
- Manage face database
- Configure AI providers
- Analyze faces with DeepFace
- Change password (re-encrypts data with ECC)

### AI Configuration

**Mock AI** (Default)

- No setup required
- For testing

**OpenAI GPT**

```bash
export OPENAI_API_KEY="your-key-here"
```

- Event analysis
- Threat assessment
- Summary generation

**DeepFace**

- Age estimation
- Gender detection
- Emotion recognition
- Race classification

## Project Structure

```
The-Machine/
├── ai/
│   └── impl.py                 # AI implementation
├── src/
│   ├── main.py                 # Main entry point
│   ├── face_recognition.py     # Face recognition engine
│   ├── face_tracking.py        # Tracking system
│   ├── secure_storage.py       # ECC encryption
│   ├── admin.py                # Admin utilities
│   ├── admin_clean.py          # Admin interface
│   ├── ai_core.py              # AI contracts
│   ├── ai_adapters.py          # AI providers
│   ├── ai_hooks.py             # Event hooks
│   ├── ai_loader.py            # Dynamic loading
│   └── facebase/
│       ├── known_faces/        # Database
│       ├── unknown_faces/      # Captured unknowns
│       └── watchlist/          # Alert faces
└── requirements.txt
```

## Security Features

- **SECP256k1** - Bitcoin's elliptic curve
- **Double SHA256** - Password hashing
- **ECDSA** - Signature verification
- **PBKDF2** - Key derivation (100k iterations)
- **Data Integrity** - Cryptographic signatures

## Testing

```bash
python test_system.py
```

## Troubleshooting

**Camera not detected:**
- Check camera permissions
- Try different camera index in code
- Ensure no other app is using camera

**Import errors:**
```bash
pip install -r requirements.txt
```

**Face not recognized:**
- Add multiple photos of the person
- Ensure good lighting
- Use clear, front-facing images

**AI errors:**
- Mock AI always works
- OpenAI requires API key
- DeepFace downloads models on first run

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."
```

## Next Steps

1. ✅ System is working with mock AI
2. Add your face images to database
3. Test camera mode
4. Configure AI providers
5. Set up watchlist
6. Deploy on dedicated hardware

## Legal Notice

⚠️ **Important:** 
- Check local laws before deployment
- Obtain consent where required
- Use responsibly and ethically
- This is for authorized surveillance only

## License

MIT License - See LICENSE file

## Credits

Inspired by Person of Interest's "The Machine"
Original concept by [@Jo-Dan](https://github.com/Jo-Dan)
