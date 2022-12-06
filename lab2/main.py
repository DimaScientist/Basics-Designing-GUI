from __future__ import annotations

import sys
import math
from enum import Enum
from typing import TYPE_CHECKING

from PyQt5 import QtWidgets, QtCore

from main_ui import Ui_MainWindow

if TYPE_CHECKING:
    from typing import Optional


class BMICategory(Enum):
    UNDERWEIGHT_SEVERE_THINNESS = "Недостаточный вес (сильная худоба)"
    UNDERWEIGHT_MODERATE_THINNESS = "Недостаточный вес (умеренная худоба)"
    UNDERWEIGHT_MILD_THINNESS = "Недостаточный вес (лёгкая худоба)"
    NORMAL_RANGE = "Норма"
    OVERWEIGHT_PRE_OBESE = "Избыточный вес (предожирение)"
    OBESE_CLASS_I = "Ожирение I степени"
    OBESE_CLASS_II = "Ожирение II степени"
    OBESE_CLASS_III = "Ожирение III степени"

    @classmethod
    def get_by_bmi_value(cls, bmi_value: Optional[float]) -> BMICategory:
        category = None
        if bmi_value:
            if bmi_value < 16.0:
                category = BMICategory.UNDERWEIGHT_SEVERE_THINNESS
            elif 16.0 <= bmi_value <= 16.9:
                category = BMICategory.UNDERWEIGHT_MODERATE_THINNESS
            elif 17.0 <= bmi_value <= 18.4:
                category = BMICategory.UNDERWEIGHT_MILD_THINNESS
            elif 18.5 <= bmi_value <= 24.9:
                category = BMICategory.NORMAL_RANGE
            elif 25.0 <= bmi_value <= 29.9:
                category = BMICategory.OVERWEIGHT_PRE_OBESE
            elif 30.0 <= bmi_value <= 34.9:
                category = BMICategory.OBESE_CLASS_I
            elif 35.0 <= bmi_value <= 39.9:
                category = BMICategory.OBESE_CLASS_II
            elif 40.0 <= bmi_value:
                category = BMICategory.OBESE_CLASS_III
        return category


class BMI(QtCore.QObject):
    update_signal = QtCore.pyqtSignal(float, float)

    def __init__(self):
        super().__init__()
        self.value = None
        self.category = None

    def update_bmi_by_height_and_weight(self, weight: float, height: float):
        self.value = weight / height ** 2
        self.category = BMICategory.get_by_bmi_value(self.value)

    def update_bmi(self, bmi_value: float):
        self.value = bmi_value
        self.category = BMICategory.get_by_bmi_value(self.value)


class BodyParams(QtCore.QObject):
    update_signal_params = QtCore.pyqtSignal(float, float)
    update_signal_by_bmi = QtCore.pyqtSignal(float, float, float)

    def __init__(self):
        super().__init__()
        self.weight = None
        self.height = None

    def update_body_params(self, weight: float, height: float):
        self.weight = weight
        self.height = height

    def update_body_params_by_bmi(self, bmi: float, height: Optional[float] = None, weight: Optional[float] = None):
        if height:
            self.weight = bmi * height ** 2
        if weight:
            self.height = math.sqrt(bmi * weight)


class Application(QtWidgets.QMainWindow):

    def __init__(self):
        super(Application, self).__init__()
        self.bmi = BMI()
        self.body_params = BodyParams()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.bmi.update_signal.connect(self.bmi.update_bmi_by_height_and_weight)
        self.body_params.update_signal_by_bmi.connect(self.body_params.update_body_params_by_bmi)
        self.body_params.update_signal_params.connect(self.body_params.update_body_params)

        self.bmi_text_edit = self.ui.bmiTextEdit
        self.category_text_edit = self.ui.categoryTextEdit
        self.height_text_edit = self.ui.heightTextEdit
        self.weight_text_edit = self.ui.weightTextEdit

        self.ui.pushButton.clicked.connect(self.btn_clicked)

    def btn_clicked(self) -> None:
        height = float(self.height_text_edit.toPlainText()) if self.height_text_edit.toPlainText() else None
        weight = float(self.weight_text_edit.toPlainText()) if self.weight_text_edit.toPlainText() else None
        bmi = float(self.bmi_text_edit.toPlainText()) if self.bmi_text_edit.toPlainText() else None

        if height is not None and weight is not None:
            self.bmi.update_signal.emit(weight, height)
            self.body_params.update_signal_params.emit(weight, height)
        if bmi is not None:
            if height is not None:
                self.body_params.update_signal_by_bmi.emit(bmi, height, 0)
            if weight is not None:
                self.body_params.update_signal_by_bmi.emit(bmi, 0, weight)
            self.bmi.update_signal.emit(self.body_params.weight, self.body_params.height)

        self.weight_text_edit.setText(str(round(self.body_params.weight, 2)))
        self.height_text_edit.setText(str(round(self.body_params.height, 2)))
        self.bmi_text_edit.setText(str(round(self.bmi.value, 2)))
        self.category_text_edit.setText(self.bmi.category.value)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    application = Application()
    application.show()

    sys.exit(app.exec())
