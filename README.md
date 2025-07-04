# Wedding App – QR-Based Photo & Video Sharing

A mobile-first web platform crafted especially for Bangladeshi and South Asian weddings in the UK. Built with quick usability in mind, this tool allows guests to scan QR codes at events, instantly upload photos and videos, and enjoy a shared online gallery. 

Used by a niche videography company as part of their in-house suite of products.

---

## Features

- **QR Code Uploads**  
  Seamlessly scan and share moments—no app or login required.

- **Central Event Gallery**  
  View all guest uploads from each ceremony: Mehndi, Nikkah, Walima, and Reception.

- **Multi-Day Support**  
  Organise uploads per wedding day or sub-event.

- **Download as ZIP**  
  Couples can access all uploads after the event in one simple download.

- **Azure-Powered Storage**  
  Files are securely saved in the cloud for scalable, long-term access.

- **Admin Controls**  
  Host dashboard for managing uploads and retrieving files.

---

## Ideal For

- Wedding Videographers and Photographers  
- Event Planners and Coordinators  
- South Asian Families Hosting Multi-Day Functions

---

## How It Works

1. Host creates a new event via the web interface.
2. Unique QR codes are generated for each sub-event.
3. Guests scan the code and upload their photos/videos.
4. A shared online gallery displays all uploaded content.
5. The host downloads a ZIP archive of the full collection.

---

## Technology Stack

- **Python Flask** – Web backend
- **Azure Blob Storage** – File storage
- **HTML/CSS** – Mobile-friendly frontend
- **qrcode (Python)** – QR code generation
- **Deployed via Azure App Service**

---

## Setup Instructions

```bash
git clone https://github.com/ruvel-ai-dev/wedding_app.git
cd wedding_app
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Create a `.env` file with your Azure settings:

```ini
AZURE_CONNECTION_STRING=your-connection-string
CONTAINER_NAME=weddingphotos
```

---

## License

MIT License – use freely and adapt for weddings, events, and beyond.

---

Crafted with care for modern South Asian celebrations in the UK. Contact: ruvel.ai.dev@gmail.com
