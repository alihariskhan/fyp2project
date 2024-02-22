from datetime import datetime


class Invoice:
    def invoice(self):
        start_time_str = '5:30:00'  # Example time
        end_time_str = '15:45:30'  # Example time

        start_time = datetime.strptime(start_time_str, '%H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%H:%M:%S')

        result = (end_time - start_time).total_seconds()/3600

        result_rounded = round(result, 2)

        print(f"{result_rounded}")

        return '123'