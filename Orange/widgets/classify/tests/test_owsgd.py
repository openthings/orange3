# Test methods with long descriptive names can omit docstrings
# pylint: disable=missing-docstring
from Orange.data import Table
from Orange.widgets.classify.owsgd import OWSGD
from Orange.widgets.tests.base import (
    WidgetTest, WidgetLearnerTestMixin, ParameterMapping
)


class TestOWSGD(WidgetTest, WidgetLearnerTestMixin):
    def setUp(self):
        self.widget = self.create_widget(
            OWSGD, stored_settings={"auto_apply": False})
        self.init()
        self.valid_datasets = (self.iris,)
        self.parameters = [
            ParameterMapping('loss', self.widget.cls_loss_function_combo,
                             list(zip(*self.widget.cls_losses))[1]),
            ParameterMapping('epsilon', self.widget.cls_epsilon_spin),
            ParameterMapping('penalty', self.widget.penalty_combo,
                             list(zip(*self.widget.penalties))[1]),
            ParameterMapping.from_attribute(self.widget, 'alpha'),
            ParameterMapping.from_attribute(self.widget, 'l1_ratio'),
            ParameterMapping('learning_rate', self.widget.learning_rate_combo,
                             list(zip(*self.widget.learning_rates))[1]),
            ParameterMapping.from_attribute(self.widget, 'eta0'),
            ParameterMapping.from_attribute(self.widget, 'power_t'),
        ]

    def test_output_coefficients(self):
        """Check if coefficients are on output after apply"""
        self.assertIsNone(self.get_output("Coefficients"))
        self.send_signal("Data", self.data)
        self.widget.apply_button.button.click()
        coeffs = self.get_output("Coefficients")
        self.assertIsInstance(coeffs, Table)
        domain = self.data.domain
        self.assertEqual(coeffs.X.shape, (len(domain.attributes) + 1,
                                          len(domain.class_var.values)))
        self.send_signal("Data", None)
        self.assertIsNone(self.get_output("Coefficients"))
