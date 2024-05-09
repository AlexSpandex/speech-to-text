import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import './SpeechDisplay.css';

const socket = io('http://localhost:3000');  

function SpeechDisplay() {
    const [messages, setMessages] = useState([]);
    const [micStatus, setMicStatus] = useState('Checking microphone...');

    useEffect(() => {
        socket.on('speech', data => {
            addMessageWithTypingEffect(data.text, data.color);
        });

        socket.on('mic_status', data => {
            setMicStatus(data.status);
        });

        socket.on('error', error => {
            console.error('Error:', error.message);
        });

        return () => {
            socket.off('speech');
            socket.off('mic_status');
            socket.off('error');
        };
    }, []);

    const addMessageWithTypingEffect = (text, color) => {
        const sentimentClass = color === 'green' ? 'positive'
            : color === 'yellow' ? 'neutral'
            : 'negative';
        
        let typedText = '';
        let index = 0;
        const typingSpeed = 50; // milliseconds

        const intervalId = setInterval(() => {
            if (index < text.length) {
                typedText += text.charAt(index);
                setMessages(messages => [...messages.slice(0, -1), { text: typedText, class: `${sentimentClass} typing` }]);
                index++;
            } else {
                clearInterval(intervalId);
                // Remove typing class once complete
                setMessages(messages => [...messages.slice(0, -1), { text: typedText, class: sentimentClass }]);
            }
        }, typingSpeed);

        // Add initial empty message with typing class
        setMessages(messages => [...messages, { text: '', class: `${sentimentClass} typing` }]);
    };

    return (
        <div className="messages-container">
            {messages.map((msg, index) => (
                <p key={index} className={msg.class}>
                    {msg.text}
                </p>
            ))}
            <p className="mic-status">{micStatus}</p>
        </div>
    );
}

export default SpeechDisplay;
