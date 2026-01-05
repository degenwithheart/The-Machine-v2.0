# Quick Start Guide

## Installation (2 minutes)

```bash
./INSTALL.sh
source .venv/bin/activate
```

## Add Your Face (1 minute)

```bash
# Take a selfie or use existing photo
cp /path/to/your/photo.jpg src/facebase/known_faces/your_name.jpg
```

## Run (instant)

```bash
python src/main.py
```

## First Use

1. Select option **1** (Camera Mode)
2. Camera will start
3. Your face will be recognized
4. Press **'q'** to quit

## Change Admin Password

1. Select option **2** (Admin Panel)
2. Login with: `admin123`
3. Select option **5** (Change Password)
4. Enter new password

## Enable AI

### OpenAI
```bash
export OPENAI_API_KEY="sk-your-key"
python src/main.py
# Select option 3 (AI Configuration)
# Select option 2 (OpenAI)
```

### DeepFace
```bash
python src/main.py
# Select option 3 (AI Configuration)
# Select option 3 (DeepFace)
# First run downloads models (~500MB)
```

## Tips

- **Good lighting** = better recognition
- **Multiple photos** = higher accuracy
- **Front-facing images** work best
- Name files: `first_last.jpg`

## Keyboard Controls (Camera Mode)

| Key | Action |
|-----|--------|
| q   | Quit |
| s   | Save frame |
| l   | Save event log |
| r   | Reload faces |

## Common Issues

**"Camera not found"**

→ Check if camera is plugged in or in use

**"Module not found"**

→ Run: `pip install -r requirements.txt`

**"Low recognition accuracy"**

→ Add more photos with different angles

**"DeepFace slow"**

→ First run downloads models, subsequent runs are faster
