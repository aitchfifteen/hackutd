import os
import csv
from statistics import mean

os.environ['NO_MAC_EXTENSIONS'] = '1'

class DataPoint:
    def __init__(self, time, instantaneousVolume, setpointVolume, valvePercentOpen):
        self.time = time
        self.instantaneousVolume = instantaneousVolume
        self.setpointVolume = setpointVolume
        self.valvePercentOpen = valvePercentOpen

def readData(fileName):
    dataPoints = []
    lastSetpoint = -1
    lastValvePercent = -1

    try:
        with open(fileName, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Skip header
            for parts in reader:
                if len(parts) < 2 or parts[1].strip() == '':
                    continue  # Skip malformed rows or rows missing instantaneous volume

                time = parts[0]
                try:
                    instantaneousVolume = float(parts[1])
                except ValueError:
                    print(f"Error parsing instantaneous volume at time {time}")
                    continue

                setpointVolume = lastSetpoint
                if len(parts) > 2 and parts[2].strip() != '':
                    try:
                        setpointVolume = float(parts[2])
                    except ValueError:
                        print(f"Error parsing setpoint volume at time {time}")

                valvePercentOpen = lastValvePercent
                if len(parts) > 3 and parts[3].strip() != '':
                    try:
                        valvePercentOpen = float(parts[3])
                    except ValueError:
                        print(f"Error parsing valve percent open at time {time}")

                lastSetpoint = setpointVolume
                lastValvePercent = valvePercentOpen
                dataPoints.append(DataPoint(time, instantaneousVolume, setpointVolume, valvePercentOpen))
    except FileNotFoundError as e:
        print(f"Error reading the file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

    return dataPoints

def detectHydrateFormation(dataPoints):
    TARGET_TOLERANCE = 0.1  # Initial tolerance
    WINDOW_SIZE = 1  # Number of points to analyze trends

    hydrateFormationDetected = False
    hydrate_times = []
    normal_times = []

    for i in range(WINDOW_SIZE, len(dataPoints)):
        window = dataPoints[i - WINDOW_SIZE:i]
        current = dataPoints[i]

        if current.setpointVolume <= 0 or current.valvePercentOpen <= 0:
            continue

        # Check if instantaneous volume consistently fails to meet target
        withinTarget = [
            abs(dp.instantaneousVolume - dp.setpointVolume) <= dp.setpointVolume * TARGET_TOLERANCE
            for dp in window
        ]

        valveChanges = [abs(dp.valvePercentOpen - window[j - 1].valvePercentOpen) for j, dp in enumerate(window) if j > 0]
        volumeChanges = [
            abs(dp.instantaneousVolume - window[j - 1].instantaneousVolume) for j, dp in enumerate(window) if j > 0
        ]

        # Detect hydrate formation
        if not all(withinTarget):
            if mean([abs(dp.instantaneousVolume - current.instantaneousVolume) for dp in window]) < current.setpointVolume * 0.05:
                if all(valveChanges) and sum(volumeChanges) < current.setpointVolume * 0.1:
                    if not hydrateFormationDetected:
                        print(f"Hydrate formation suspected at {current.time}.")
                        hydrateFormationDetected = True
                        hydrate_times.append(current.time)
        else:
            if hydrateFormationDetected:
                print(f"System back to normal at {current.time}.")
                hydrateFormationDetected = False
                normal_times.append(current.time)

    if not hydrateFormationDetected and not normal_times:
        print("System has been normal throughout.")

    return hydrate_times, normal_times

def main():
    fileName = "Courageous_729H-09_25-09_28.csv"
    dataPoints = readData(fileName)
    hydrate_times, normal_times = detectHydrateFormation(dataPoints)
    # Optionally, you can save hydrate_times and normal_times to a file or process further.

if __name__ == '__main__':
    main()