# Seal/Stamp Data Extraction API

A FastAPI-based application that extracts seal and stamp information from document images using OpenAI's vision model. This API specifically identifies and extracts three key signature fields: Owner Signature, Structural Engineer, and Registered Engineer.

## Features

- **Image Processing**: Supports multiple image formats (JPG, JPEG, PNG, GIF, BMP, WEBP, TIFF)
- **AI-Powered Extraction**: Uses OpenAI's vision model to analyze and extract text from images
- **Structured Output**: Returns data in a standardized JSON format
- **Error Handling**: Comprehensive error handling with appropriate status codes
- **Input Validation**: Validates image files and paths before processing

## Project Structure

```
project/
├── main.py              # FastAPI application entry point
├── connectAPI.py        # Core image analysis logic
├── model.py            # Pydantic models for request validation
├── helper.py           # Utility functions for image processing
├── requirements.txt    # Python dependencies
└── .env               # Environment variables (not included)
```

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thirumurugan2001/extract_seal_stamp_data__from_image.git
   cd extract_seal_stamp_data__from_image
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   GPT_URL=your_openai_base_url
   AZURE_OPENAI_KEY=your_openai_api_key
   MODEL=your_model_name
   ```

## Usage

### Starting the Server

Run the application:
```bash
python main.py
```

The server will start on `http://0.0.0.0:8080` with auto-reload enabled.

### API Endpoint

**POST** `/api/extract_seal_stamp_data__from_image`

#### Request Body

```json
{
    "file_path": "path/to/your/image.png"
}
```

#### Successful Response (200)

```json
{
    "status": true,
    "statusCode": 200,
    "message": "Successfully analyzed the image",
    "OWNER SIGNATURE": "For HEADWAY PREMIER INDUSPARK PRIVATE LIMITED",
    "STRUCTURAL ENGINEER": "A.N. RAVICHANDRAN",
    "REGISTERED ENGINEER": "A.N. RAVICHANDRAN"
}
```

#### Error Responses

**Empty File Path (400)**
```json
{
    "message": "File path cannot be empty",
    "stratusCode": 400,
    "status": false,
    "data": [{}]
}
```

**Invalid Image File (400)**
```json
{
    "status": false,
    "statusCode": 400,
    "message": "I don't see a valid image. Please upload a supported image file (JPG, PNG, GIF, BMP, WEBP, or TIFF).",
    "data": [{}]
}
```

**Base64 Conversion Error (400)**
```json
{
    "status": false,
    "statusCode": 400,
    "message": "Failed to convert the image into base64 format",
    "data": [{}]
}
```

**General Error (400)**
```json
{
    "status": false,
    "statusCode": 400,
    "message": "Error details here",
    "data": [{}]
}
```

## Extraction Fields

The API extracts three specific signature fields:

1. **OWNER SIGNATURE**
   - Matches labels: "OWNER SIGNATURE", "SIGNATURE OF OWNER", "OWNER's SIGNATURE"

2. **STRUCTURAL ENGINEER**
   - Matches labels: "STRUCTURAL ENGINEER", "SIGNATURE OF STRUCTURAL ENGINEER", "STRUCTURAL ENGINEER'S SIGNATURE"

3. **REGISTERED ENGINEER**
   - Matches labels: "REGISTERED ENGINEER", "ARCHITECT SIGNATURE", "SIGNATURE OF ARCHITECT", "LICENSED SURVEYOR", "ARCHITECT/LICENSED SURVEYOR SIGNATURE"

## Testing the API

### Using curl

```bash
curl -X POST "http://localhost:8080/api/extract_seal_stamp_data__from_image" \
     -H "Content-Type: application/json" \
     -d '{
       "file_path": "C:/path/to/your/image.png"
     }'
```

### Using Python requests

```python
import requests

url = "http://localhost:8080/api/extract_seal_stamp_data__from_image"
payload = {
    "file_path": "C:/path/to/your/image.png"
}

response = requests.post(url, json=payload)
print(response.json())
```

## Dependencies

- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for FastAPI
- **OpenAI**: AI model integration
- **Pillow**: Image processing library
- **Pydantic**: Data validation using Python type annotations
- **python-dotenv**: Environment variable management

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GPT_URL` | OpenAI API base URL | Yes |
| `AZURE_OPENAI_KEY` | OpenAI API key | Yes |
| `MODEL` | OpenAI model name | Yes |

### Supported Image Formats

- JPEG/JPG
- PNG
- GIF
- BMP
- WEBP
- TIFF

## Error Handling

The application includes comprehensive error handling for:

- Invalid file paths
- Unsupported image formats
- Image processing failures
- API communication errors
- JSON parsing errors

## Development

### Running in Development Mode

The application runs with auto-reload enabled by default:

```bash
python main.py
```

### API Documentation

FastAPI automatically generates interactive API documentation:
- Swagger UI: `http://localhost:8080/docs`
- ReDoc: `http://localhost:8080/redoc`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions, please [create an issue](link-to-issues) in the repository.

## Changelog

### Version 1.0.0
- Initial release
- Basic seal/stamp data extraction functionality
- Support for multiple image formats
- Comprehensive error handling