# HotelTravel App

HotelTravel is a comprehensive travel companion app that allows users to explore hotel options, calculate distances, and
find local attractions all within a single platform. It also includes a Telegram bot that provides quick access to
simple statistical features.

## Key Features

- Interactive hotel search and price comparison.
- Distance calculations between multiple hotels.
- Attraction exploration within the city.
- Detailed insights into hotel pricing categories.
- Telegram bot integration for seamless access.

## Technologies Used

- Python (Streamlit, Pydeck, TeleBot, Pytest, BeautifulSoap4, Geopy)
- Docker for containerization
- C++ (Asio + nlohmann/json) for server-side calculations
- GitHub Actions for CI/CD
- Bash scripting

# Installation and Setup on Linux

Just follow the link (it's deployed app on Streamlit):`https://hoteltravel-7u2nbdhmyje3fwugrt7wn6.streamlit.app`

## Or

1. Clone the repository:
    ```bash
   git@github.com:Bonartze/HotelTravel.git 

2. Navigate to the project directory:
    ```bash
    cd HotelTravel
    ```

5. Run the Streamlit app (locally via docker image):
    ```bash
   sudo apt-get install docker 
   docker build -t run -f Dockerfile.app .
   docker run -p 8501:8501 run
    ```

## Usage

- Open the Streamlit app in your browser at `http://localhost:8501` (If you launched web locally, using docker).
- Use the interactive map to explore hotels and attractions.
- Access the Telegram bot using `/start` command and explore features like distance calculations, hotel ratings, and
  more.
- Get access to bot: `https://t.me/hotel_maps_bot`

## Contributing

Contributions are welcome! Please fork the repository and create a pull request.
