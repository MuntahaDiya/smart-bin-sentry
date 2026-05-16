#  Smart Bin Sentry
**An AI-powered digital bouncer for recycling bins, built to prevent hazardous waste contamination.**

# The Problem
Current recycling bins rely entirely on the "honor system." A recent incident at BTU Cottbus where an e-scooter caused a fire in a trash container proved that lacking physical preventative measures is a major safety hazard.

# The Solution
Smart Bin Sentry uses a camera and the Google Cloud Vision API to analyze waste at the point of disposal. It acts as an automated gatekeeper:
* 🟢 **Paper/Cardboard:** System verifies the material, flashes a Green UI, and (in hardware) unlocks the bin.
* 🔴 **Contaminants (Plastics/E-waste):** System detects a mismatch, flashes a Red UI, and keeps the bin locked.

# Tech Stack
**Python 3**
**Google Cloud Vision API** (Multimodal AI classification)
**OpenCV** (Real-time video capture and UI overlay)

*(Note: The hardware deployment utilizes a Raspberry Pi and servo-motor locking mechanism).*

