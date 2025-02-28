# CS-350
Emerging Sys Arch &amp; Tech

Project Overview:
  This repository contains projects developed for the SNHU CS-350 class, focusing on embedded system design and state machine implementation. The projects chosen utilized microcontrollers and peripherals to solve real-life problems.

Summarize the project and what problem it was solving.
  LightStateMachine.py: This project was designed to transmit and display Morse code on an LCD screen. The system uses a state machine to control the timing and transitions between dots, dashes, and spaces, ensuring accurate representation of Morse code sequences.

  Thermostat.py: This project implements a state machine that allows the user to switch between three states: idle, heating, and cooling. The user can adjust the temperature up or down using installed peripherals. The LED display provides visual feedback on the current system state, ensuring intuitive user interaction.

What did you do particularly well?
  Both projects were successfully implemented. The integration of the LCD display and LED indicators allowed for real-time user feedback. I am partiuarly pround of the LightStateMachine; During the project, I had hardware malfunction where only half of the LCD screen was viewable. It was a difficult assignment, essentially given that I had 1 hand tied behind my back, so to speak. I had reassembled the solderless board many times over, thinking I had done something incorrectly. Despite my efforts, I was unable to fix the issue, resulting to the fact that it may have not been myself but rather a hardware issue. So I continued on half-blind. It turned out, it worked as intended!

Where could you improve?
  The timing mechanisms in Morse code transmission can be optimized for improved accuracy. Enhancements in error handling for invalid user inputs in the thermostat system can improve reliability. Future iterations could explore power efficiency optimizations for embedded systems to reduce energy consumption.

What tools and/or resources are you adding to your support network?
  Microcontroller documentation, including references for Raspberry Pi and Microchip, was crucial in developing these projects. State machine frameworks for Python helped streamline development. Embedded systems development guides provided additional insights. I also have been apart of a python community on Discord since I was first introducted into Python Coding, since IT-140. I have several friend that are also in IT, with many years of experience that I can troubleshoot with.

What skills from this project will be particularly transferable to other projects and/or course work?
  State machine design is a fundamental skill that applies to embedded systems, game development, and automation. Embedded system programming experience gained in this project is beneficial for IoT, robotics, and real-time applications. Working with peripherals such as LCDs, buttons, and LEDs enhances hardware interfacing skills, which are valuable in various projects. The emphasis on code modularity and maintainability ensures that future modifications and extensions can be implemented seamlessly.
  
How did you make this project maintainable, readable, and adaptable?
  The codebase follows a well-structured format with clear function definitions and comments. Consistent naming conventions for variables and functions enhance readability. The modular design allows for easy updates and scalability. While there was a base code given, it was littered with #FIX ME and other unrelated information. I removed a majorit of these for easier readability as well. A comprehensive README ensures that future developers can quickly understand and build upon the project.
