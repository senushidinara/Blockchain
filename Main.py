import os
import random
import time
from typing import Optional, Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from serial import Serial, SerialException
from datetime import datetime

# --- Configuration ---
# NOTE: Set this to your actual serial port (e.g., 'COM3', '/dev/ttyUSB0', 'ttyACM0')
SERIAL_PORT = os.environ.get("SERIAL_PORT", "COM99") # Fallback dummy port
BAUDRATE = 9600

# Global flag for hardware status
IS_SERIAL_ACTIVE = False
serial_connection: Optional[Serial] = None

# --- Pydantic Models for Data Validation and Schema ---

class BioSignalData(BaseModel):
    """Schema for the raw biosignal data input."""
    signal_type: Literal["EEG", "ECG", "GSR"] = "EEG"
    reading_value: float
    timestamp: datetime = datetime.now()
    user_id: str = "NG-User-1234"

class AnalysisResult(BaseModel):
    """Schema for the AI analysis output."""
    action_suggestion: str
    risk_level: Literal["Low", "Moderate", "High"]
    consent_ledger_update: str

class LedgerStatus(BaseModel):
    """Schema for the mock ledger status."""
    contract_name: str
    status: Literal["Operational", "Offline"]
    last_block_number: int
    total_consents_recorded: int

# --- Hardware Initialization and Fallback ---

def initialize_serial():
    """Attempts to connect to the serial port and sets the global flag."""
    global IS_SERIAL_ACTIVE, serial_connection

    print(f"Attempting to connect to serial port: {SERIAL_PORT}...")
    try:
        # Open the serial port with a timeout
        serial_connection = Serial(SERIAL_PORT, BAUDRATE, timeout=1)
        IS_SERIAL_ACTIVE = True
        print(f"✅ Successfully connected to serial port {SERIAL_PORT}")
        # Give Arduino/device time to reset
        time.sleep(2) 
    except SerialException as e:
        IS_SERIAL_ACTIVE = False
        print(f"⚠️ Serial connection failed on {SERIAL_PORT}. Running in mock data mode.")
        print(f"   Error details: {e}")
        serial_connection = None

# --- FastAPI App Initialization ---

app = FastAPI(
    title="NeuroGuard Bio-API",
    description="FastAPI service for reading biosignals and mocking AI/Blockchain interactions.",
    version="1.0.0"
)

# Initialize serial connection when the app starts up
@app.on_event("startup")
async def startup_event():
    """Runs the serial initialization logic on startup."""
    initialize_serial()

# --- Utility Functions (Simulations) ---

def read_serial_data() -> Optional[str]:
    """Reads a line from the serial port if active."""
    if serial_connection and IS_SERIAL_ACTIVE:
        try:
            # Read until newline, decode, and strip whitespace
            line = serial_connection.readline().decode('utf-8').strip()
            if line:
                return line
        except SerialException as e:
            print(f"Runtime Serial Error: {e}")
            global IS_SERIAL_ACTIVE
            IS_SERIAL_ACTIVE = False # Disable active status on failure
    return None

def generate_mock_data() -> BioSignalData:
    """Generates synthetic, fluctuating biosignal data."""
    signal_type = random.choice(["EEG", "ECG", "GSR"])
    if signal_type == "EEG":
        value = random.uniform(50, 150)
    elif signal_type == "ECG":
        value = random.uniform(60, 100)
    else: # GSR
        value = random.uniform(0.1, 5.0)

    return BioSignalData(
        signal_type=signal_type,
        reading_value=round(value, 2),
        timestamp=datetime.now(),
        user_id="NG-Simulated-User-789"
    )

def mock_ai_analysis(data: BioSignalData) -> AnalysisResult:
    """Simulates AI analysis based on the reading value."""
    value = data.reading_value

    if data.signal_type == "EEG" and value > 120:
        risk = "High"
        action = "Emergency Alert & System Shutdown"
    elif data.signal_type == "ECG" and (value < 65 or value > 95):
        risk = "Moderate"
        action = "Increase monitoring frequency and log event."
    else:
        risk = "Low"
        action = "Continue passive monitoring."

    # Simulate blockchain update message
    ledger_msg = f"Consent ledger update mocked: New reading for {data.user_id} logged with Risk: {risk}."

    return AnalysisResult(
        action_suggestion=action,
        risk_level=risk,
        consent_ledger_update=ledger_msg
    )

# --- API Endpoints ---

@app.get("/", tags=["Status"])
async def root():
    """Basic health check and serial status."""
    status_msg = "Operational (Mock Data Mode)"
    if IS_SERIAL_ACTIVE:
        status_msg = f"Operational (Serial Active on {SERIAL_PORT})"
    
    return {
        "message": "NeuroGuard API is running.",
        "serial_status": status_msg
    }

@app.get("/biosignals/live", response_model=BioSignalData, tags=["Data Acquisition"])
async def get_live_biosignals():
    """
    Reads the latest biosignal data. Uses the serial port if active,
    otherwise returns synthesized mock data.
    """
    raw_data = read_serial_data()
    
    if raw_data:
        try:
            # Assume serial data is a simple comma-separated string: "signal_type,value,user_id"
            parts = raw_data.split(',')
            if len(parts) >= 2:
                signal_type = parts[0].strip()
                reading_value = float(parts[1].strip())
                user_id = parts[2].strip() if len(parts) > 2 else "NG-Serial-Device"
                
                return BioSignalData(
                    signal_type=signal_type,
                    reading_value=reading_value,
                    user_id=user_id
                )
        except ValueError:
            print(f"Error parsing serial data: {raw_data}. Returning mock data.")
            pass # Fall through to mock data
        except Exception as e:
            print(f"Unexpected error in serial read/parse: {e}. Returning mock data.")
            pass

    # Fallback to mock data if serial is inactive or reading failed
    return generate_mock_data()


@app.post("/process_data", response_model=AnalysisResult, tags=["AI & Ledger"])
async def analyze_and_update(data: BioSignalData):
    """
    Receives biosignal data, triggers mock AI analysis, 
    and simulates a blockchain consent ledger update.
    """
    analysis = mock_ai_analysis(data)
    
    # Simulate a time delay for heavy AI/Blockchain processing
    await time.sleep(0.05) 

    return analysis

@app.get("/ledger/status", response_model=LedgerStatus, tags=["AI & Ledger"])
async def get_ledger_status():
    """
    Mocks the current operational status of the NeuroGuardConsentLedger contract.
    """
    return LedgerStatus(
        contract_name="NeuroGuardConsentLedger",
        status="Operational",
        last_block_number=random.randint(1000000, 1500000),
        total_consents_recorded=random.randint(5000, 10000)
    )

# Set logging level for serial debugging (optional, useful if issues arise)
# import logging
# logging.basicConfig(level=logging.DEBUG)
# serial.setLogLevel('Debug')

