CS-350

Emerging System Architectures & Technologies

Project Overview

This repository contains projects developed for the SNHU CS-350 class, focusing on embedded system design and state machine implementation. The projects chosen utilized microcontrollers and peripherals to solve real-life problems.

LightStateMachine.py

This project was designed to transmit and display Morse code on an LCD screen. The system uses a state machine to control the timing and transitions between dots, dashes, and spaces, ensuring accurate representation of Morse code sequences.

Thermostat.py

This project implements a state machine that allows the user to switch between three states: idle, heating, and cooling. The user can adjust the temperature up or down using installed peripherals. The LED display provides visual feedback on the current system state, ensuring intuitive user interaction.

Key Accomplishments

Both projects were successfully implemented. The integration of the LCD display and LED indicators allowed for real-time user feedback. I am particularly proud of the LightStateMachine project. During development, I encountered a hardware malfunction where only half of the LCD screen was viewable. This made the assignment significantly more challenging, as it was like working with limited visibility. I reassembled the solderless board multiple times, thinking I had made a mistake. Despite my efforts, I was unable to fix the issue and realized it was likely a hardware defect. I continued developing the project under these conditions, and in the end, the system worked as intended, which was a great accomplishment.

Areas for Improvement

The timing mechanisms in Morse code transmission can be optimized for improved accuracy. Enhancements in error handling for invalid user inputs in the thermostat system can improve reliability. Future iterations could explore power efficiency optimizations for embedded systems to reduce energy consumption.

Tools & Resources Added to Support Network

Microcontroller documentation, including references for Raspberry Pi and Microchip, was crucial in developing these projects. State machine frameworks for Python helped streamline development. Embedded systems development guides provided additional insights. I have also been part of a Python community on Discord since I was first introduced to Python coding in IT-140. Additionally, I have several friends in IT with extensive experience, whom I can troubleshoot with when needed.

Transferable Skills

State machine design is a fundamental skill that applies to embedded systems, game development, and automation. Embedded system programming experience gained in this project is beneficial for IoT, robotics, and real-time applications. Working with peripherals such as LCDs, buttons, and LEDs enhances hardware interfacing skills, which are valuable in various projects. The emphasis on code modularity and maintainability ensures that future modifications and extensions can be implemented seamlessly.

Project Maintainability & Readability

The codebase follows a well-structured format with clear function definitions and comments. Consistent naming conventions for variables and functions enhance readability. The modular design allows for easy updates and scalability. While there was a base code provided, it contained numerous #FIX ME comments and unrelated information. I removed the majority of these to improve readability. A comprehensive README ensures that future developers can quickly understand and build upon the project.

This repository serves as a strong foundation for learning embedded system development and state machine implementation, making it a valuable resource for future projects and coursework.
