# Stop & Talk

This project is a React application that captures audio input from a microphone, converts speech to text in real-time, analyzes the sentiment of the spoken words, and displays the text and sentiment analysis results dynamically on a webpage.

## Features

- **Real-Time Speech Recognition**: Converts spoken language into text using the microphone.
- **Sentiment Analysis**: Analyzes the sentiment of the recognized speech and colors the text accordingly (green for positive, yellow for neutral, red for negative).
- **Dynamic Updates**: Utilizes WebSocket communication to update the webpage in real-time without needing to refresh the page.
- **Microphone Status Detection**: Displays the current status of the microphone to inform the user if the microphone is active or not detected.

## Technology Stack

- **React**: Frontend framework for building the user interface.
- **Socket.IO Client**: Enables real-time, bi-directional communication between web clients and the server.
- **CSS3**: For styling the application.

## Setup and Installation

### Prerequisites

- Node.js and npm (Node Package Manager)
- A modern web browser that supports ES6 and WebSockets

### Installing Dependencies

To install the necessary packages, run the following command in the project directory:

```bash
npm install
```
### Running the Application
To start the application on your local machine, run:

```bash
npm start
```

This command will start the React application and open it in your default web browser. The application will be available at http://localhost:3000.

To start the server on your local machine, add another terminal tab and go to the server folder, run:

```bash
python app.py
```