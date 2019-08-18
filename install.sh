# Install requirements
pip install -r requirements.txt

# Run pyinstaller
pyinstaller --onefile MangaDownloader.py

# Remove artifacts of pyintaller
rm -rf "__pycache__"
rm -rf "build"
rm -rf "MangaDownloader.spec"