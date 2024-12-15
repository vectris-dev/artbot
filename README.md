# ArtBot - DALL-E Image Generator

ArtBot is a Python script that automates the generation of images using OpenAI's DALL-E 3 model. It processes prompts from a CSV file and generates corresponding images, saving both the images and their revised prompts.

## Features

- Generates images using DALL-E 3 model
- Processes multiple prompts from a CSV file
- Supports generating multiple images per prompt
- Automatically saves images and revised prompts
- Includes error handling and retry mechanism
- Configurable delay between image generations to avoid rate limits

## Prerequisites

- Python 3.x
- OpenAI API key

## Installation

1. Clone this repository
2. Install required dependencies:
    ```bash
    pip install openai pillow python-dotenv requests
    ```
3. Copy `example.env` to `.env` and add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_api_key_here
    ```

## Usage

1. An `example.csv` file is included in the repository to help you get started. You can modify it or create your own CSV file with the following format:
    ```csv
    prompt,count
    "your prompt here",1
    "another prompt",2
    ```
    - The first column contains the image prompts
    - The second column (optional) specifies how many images to generate for each prompt

2. Run the script:
    ```bash
    python artbot.py
    ```

The script will:
- Create an `output` directory if it doesn't exist
- Process each prompt in the CSV file
- Generate the specified number of images for each prompt
- Save images as PNG files with timestamps
- Save prompts in corresponding TXT files

## Configuration

You can modify these variables in the script:
- `use_guidance`: Toggle whether to prepend guidance text to prompts to prevent openAI from modifying the prompt (default: True)
- `delay`: Time to wait between image generations (default: 2 seconds)
- `retry_delay`: Time to wait before retrying after an error (default: 10 seconds)
- `run_count`: Number of times to process the entire CSV file (default: 1)

## Output

Files are saved in the `output` directory with the following naming convention:
- Images: `YYYYMMDD_HHMMSS_microseconds.png`
- Revised prompts: `YYYYMMDD_HHMMSS_microseconds.txt`

## Error Handling

The script includes automatic retry functionality for failed requests and will continue processing remaining prompts even if errors occur.

## License

MIT License