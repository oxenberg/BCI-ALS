from arduino.dataCollector import DataCollectorOnline


def main():
    collector = DataCollectorOnline()
    collector.start_experiment()


if __name__ == "__main__":
    main()
