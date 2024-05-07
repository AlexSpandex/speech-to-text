import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const socket = io('http://localhost:3000'); // Adjust URL/port as needed

function SpeechDisplay() {
    const [messages, setMessages] = useState([]);

    useEffect(() => {
        socket.on('speech', data => {
            setMessages(messages => [...messages, {text: data.text, color: data.color}]);
        });

        socket.on('error', error => {
            console.error('Error:', error.message);
        });

        return () => {
            socket.off('speech');
            socket.off('error');
        };
    }, []);

    return (
        <div>
            {messages.map((msg, index) => (
                <p key={index} style={{ color: msg.color }}>
                    {msg.text}
                </p>
            ))}
        </div>
    );
}

export default SpeechDisplay;