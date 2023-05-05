from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        """Метод возвращает строку сообщения"""

        return (self.message.format(**asdict(self)))


@dataclass
class Training:
    """Базовый класс тренировки."""

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    MIN_IN_H: ClassVar[float] = 60

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""

        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

        raise NotImplementedError("Требуется определить get_spent_calories()")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""

        return InfoMessage(
            self.__class__.__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: ClassVar[float] = 18
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.79

    def get_spent_calories(self) -> float:
        return (
            (
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT
            )
            * self.weight
            / self.M_IN_KM
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    K_WLK_1: ClassVar[float] = 0.035
    K_WLK_2: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[float] = 100
    SQUARE: ClassVar[float] = 2

    action: int
    duration: float
    weight: float
    height: int

    def get_spent_calories(self) -> float:
        return (
            (
                self.K_WLK_1
                * self.weight
                + (
                    (self.get_mean_speed()
                     * self.KMH_IN_MSEC
                     ) ** self.SQUARE
                    / (self.height
                       / self.CM_IN_M
                       )
                ) * self.K_WLK_2
                  * self.weight
            )
            * self.duration
            * self.MIN_IN_H
        )


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    K_SW_1: ClassVar[float] = 1.1
    K_SW_2: ClassVar[float] = 2
    LEN_STEP: ClassVar[float] = 1.38

    action: int
    duration: float
    weight: float
    length_pool: int
    count_pool: int
    length_pool = float
    count_pool = float

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.K_SW_1) * self.K_SW_2
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    type_dict: dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in type_dict:
        raise ValueError(f"Такой тренировки - {workout_type}, не найдено")
    return type_dict[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
