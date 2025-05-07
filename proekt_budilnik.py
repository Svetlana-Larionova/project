import time
import winsound
from datetime import datetime
import threading


class AlarmClock:
    def __init__(self):
        self.alarms = []
        self.running = True

    def get_time_input(self, prompt):
        while True:
            time_str = input(prompt + " (формат ЧЧ:ММ): ")
            try:
                time_obj = datetime.strptime(time_str, "%H:%M").time()
                return time_str
            except ValueError:
                print("Неправильный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ.")

    def add_alarm(self):
        alarm_time = self.get_time_input("Введите время будильника")
        alarm_type = input("Выберите тип уведомления (1 - текст, 2 - звук): ")
        alarm_days = []

        if input("Добавить дни недели? (y/n): ").lower() == 'y':
            days = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"]
            print("Доступные дни: пн, вт, ср, чт, пт, сб, вс")
            selected = input("Введите дни через запятую (например, пн,ср,пт): ").split(',')
            alarm_days = [day.strip() for day in selected if day.strip() in days]

        alarm = {
            'time': alarm_time,
            'type': alarm_type,
            'days': alarm_days,
            'repeat': input("Повторять каждые 5 минут? (y/n): ").lower() == 'y'
        }
        self.alarms.append(alarm)
        print(f"Будильник добавлен на {alarm_time}")

    def check_alarms(self):
        while self.running:
            now = datetime.now()
            current_time = now.strftime("%H:%M")
            current_day = ["пн", "вт", "ср", "чт", "пт", "сб", "вс"][now.weekday()]

            for alarm in self.alarms[:]:
                if alarm['time'] == current_time:
                    if not alarm['days'] or current_day in alarm['days']:
                        self.trigger_alarm(alarm)
                        if alarm['repeat']:
                            # Обновляем время будильника на +5 минут для повтора
                            h, m = map(int, alarm['time'].split(':'))
                            m = (m + 5) % 60
                            h = (h + (m // 60)) % 24
                            alarm['time'] = f"{h:02d}:{m:02d}"
                        else:
                            self.alarms.remove(alarm)

            time.sleep(10)  # Проверяем каждые 10 секунд, чтобы не нагружать процессор

    def trigger_alarm(self, alarm):
        print("\n" + "=" * 20)
        print("Время вставать!!!")
        print("=" * 20 + "\n")

        if alarm['type'] == '2':
            try:
                # Проигрываем стандартный звук будильника
                winsound.Beep(1000, 2000)  # Частота 1000 Гц, длительность 2000 мс
            except:
                print("Невозможно воспроизвести звук")

        # Ждем подтверждения от пользователя
        input("Нажмите Enter, чтобы отключить будильник...")

    def run(self):
        print("=== Программа Будильник ===")
        print("Команды: add - добавить будильник, list - список будильников, exit - выход")

        # Запускаем поток для проверки будильников
        alarm_thread = threading.Thread(target=self.check_alarms, daemon=True)
        alarm_thread.start()

        while self.running:
            command = input("\nВведите команду: ").lower()

            if command == 'add':
                self.add_alarm()
            elif command == 'list':
                print("\nТекущие будильники:")
                for i, alarm in enumerate(self.alarms, 1):
                    days = ', '.join(alarm['days']) if alarm['days'] else 'каждый день'
                    repeat = " (повтор каждые 5 мин)" if alarm['repeat'] else ""
                    print(
                        f"{i}. Время: {alarm['time']}, Дни: {days}, Тип: {'звук' if alarm['type'] == '2' else 'текст'}{repeat}")
            elif command == 'exit':
                self.running = False
                print("Программа завершает работу...")
            else:
                print("Неизвестная команда")


if __name__ == "__main__":
    alarm_clock = AlarmClock()
    alarm_clock.run()