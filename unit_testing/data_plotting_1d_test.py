import unittest
from random import random

from matplotlib.pyplot import subplots
from numpy import linspace, ndarray, pi, sin

from graphinglib.data_plotting_1d import Curve, Histogram, Scatter
from graphinglib.fits import FitFromPolynomial
from graphinglib.graph_elements import Point


class TestCurve(unittest.TestCase):
    def setUp(self):
        x = linspace(0, 3 * pi, 200)
        self.testCurve = Curve(x, sin(x), "Test Curve", color="k")

    def test_xdata_is_list_or_ndarray(self):
        self.assertIsInstance(self.testCurve.x_data, list | ndarray)

    def test_ydata_is_list_or_ndarray(self):
        self.assertIsInstance(self.testCurve.y_data, list | ndarray)

    def test_default_value(self):
        self.assertEqual(self.testCurve.line_width, "default")

    def test_color_is_str(self):
        self.assertIsInstance(self.testCurve.color, str)

    def test_label_is_str(self):
        self.assertIsInstance(self.testCurve.label, str)

    def test_from_function(self):
        self.assertIsInstance(
            Curve.from_function(
                lambda x: x**2,
                0,
                1,
                "Test",
                color="k",
                line_width=1,
                line_style="-",
                number_of_points=400,
            ),
            Curve,
        )

    def test_add_errorbars(self):
        self.testCurve.add_errorbars(0.1, 0.1)
        self.testCurve.add_errorbars(0.1, [0.2, 0.3] * 100)
        self.testCurve.add_errorbars([0.2, 0.3] * 100, 0.1)
        self.testCurve.add_errorbars(0.3, None)
        self.testCurve.add_errorbars(None, 0.3)

    def test_get_point_at_x(self):
        point = self.testCurve.get_point_at_x(0.5)
        self.assertEqual(point.x, 0.5)
        self.assertAlmostEqual(point.y, sin(0.5), places=3)

    def test_get_points_at_y(self):
        points = self.testCurve.get_points_at_y(0)
        for i, point in enumerate(points):
            self.assertEqual(point.y, 0)
            self.assertAlmostEqual(point.x, i * pi, places=3)

    def test_curve_is_plotted(self):
        x = linspace(0, 3 * pi, 200)
        self.testCurve = Curve(
            x, sin(x), "Test Curve", color="k", line_width=3, line_style="--"
        )
        _, self.testAxes = subplots()
        self.testCurve._plot_element(self.testAxes, 0)
        self.assertEqual(len(self.testAxes.get_lines()), 1)

    def test_get_derivative_curve(self):
        self.assertIsInstance(self.testCurve.get_derivative_curve(), Curve)

    def test_get_integral_curve(self):
        self.assertIsInstance(self.testCurve.get_integral_curve(), Curve)

    def test_get_tangent_curve(self):
        self.assertIsInstance(self.testCurve.get_tangent_curve(0), Curve)

    def test_get_normal_curve(self):
        self.assertIsInstance(self.testCurve.get_normal_curve(0), Curve)

    def test_area_between(self):
        self.assertAlmostEqual(self.testCurve.area_between(0, pi), 2, places=3)

    def test_slope_at(self):
        self.assertAlmostEqual(self.testCurve.slope_at(pi / 2), 0, places=5)

    def test_arc_length_between(self):
        self.assertAlmostEqual(
            self.testCurve.arc_length_between(0, pi), 3.820, places=3
        )

    def test_intersection(self):
        x = linspace(0, 3 * pi, 200)
        other_curve = Curve(x, 0.005 * x**2 + 0.1, "Other Curve", color="k")
        points = self.testCurve.intersection(other_curve)
        points_x = [0.1, 2.9962, 6.6072, 8.9052]
        points_y = [0.1, 0.14489, 0.3183, 0.4965]
        self.assertEqual(len(points), 4)
        for i, point in enumerate(points):
            self.assertIsInstance(point, Point)
            self.assertAlmostEqual(point.x, points_x[i], places=3)
            self.assertAlmostEqual(point.y, points_y[i], places=3)

    def test_add_curves(self):
        x = linspace(0, 3 * pi, 200)
        other_curve = Curve(x, 0.005 * x**2 + 0.1, "Other Curve", color="k")
        curve_sum = self.testCurve + other_curve
        self.assertIsInstance(curve_sum, Curve)
        self.assertAlmostEqual(curve_sum.get_point_at_x(0).y, 0.1, places=3)
        self.assertAlmostEqual(curve_sum.get_point_at_x(2).y, 1.029, places=3)

    def test_subtract_curves(self):
        x = linspace(0, 3 * pi, 200)
        other_curve = Curve(x, 0.005 * x**2 + 0.1, "Other Curve", color="k")
        curve_sub = self.testCurve - other_curve
        self.assertIsInstance(curve_sub, Curve)
        self.assertAlmostEqual(curve_sub.get_point_at_x(0).y, -0.1, places=3)
        self.assertAlmostEqual(curve_sub.get_point_at_x(2).y, 0.789, places=3)

    def test_multiply_curves(self):
        x = linspace(0, 3 * pi, 200)
        other_curve = Curve(x, 0.005 * x**2 + 0.1, "Other Curve", color="k")
        curve_mult = self.testCurve * other_curve
        self.assertIsInstance(curve_mult, Curve)
        self.assertAlmostEqual(curve_mult.get_point_at_x(0).y, 0, places=3)
        self.assertAlmostEqual(curve_mult.get_point_at_x(2).y, 0.109, places=3)

    def test_divide_curves(self):
        x = linspace(0, 3 * pi, 200)
        other_curve = Curve(x, 0.005 * x**2 + 0.1, "Other Curve", color="k")
        curve_div = self.testCurve / other_curve
        self.assertIsInstance(curve_div, Curve)
        self.assertAlmostEqual(curve_div.get_point_at_x(0).y, 0, places=3)
        self.assertAlmostEqual(curve_div.get_point_at_x(2).y, 7.57748, places=2)

    def test_max_curves(self):
        curve_max = max(self.testCurve)
        self.assertAlmostEqual(curve_max, 1, places=3)

    def test_min_curves(self):
        curve_min = min(self.testCurve)
        self.assertAlmostEqual(curve_min, -1, places=3)

    def test_add_different_sizes(self):
        x = linspace(0, 3 * pi, 100)
        other_curve = Curve(x, 0.005 * x**2 + 0.1, "Other Curve", color="k")
        curve_sum = self.testCurve + other_curve
        self.assertIsInstance(curve_sum, Curve)
        self.assertAlmostEqual(curve_sum.get_point_at_x(0).y, 0.1, places=3)


class TestScatter(unittest.TestCase):
    def setUp(self):
        x = linspace(0, 3 * pi, 200)
        self.testScatter = Scatter(x, sin(x), "Test Curve")

    def test_scatter_is_scatter(self):
        self.assertIsInstance(self.testScatter, Scatter)

    def test_xdata_is_list_or_ndarray(self):
        self.assertIsInstance(self.testScatter.x_data, list | ndarray)

    def test_color_is_str(self):
        self.assertIsInstance(self.testScatter.face_color, str)
        self.assertIsInstance(self.testScatter.edge_color, str)

    def test_label_is_str(self):
        self.assertIsInstance(self.testScatter.label, str)

    def test_from_function(self):
        self.assertIsInstance(
            Scatter.from_function(
                lambda x: x**2,
                0,
                1,
                "Test",
                face_color="k",
                edge_color="k",
                marker_size=1,
                marker_style="o",
                number_of_points=400,
            ),
            Scatter,
        )

    def test_add_errorbars(self):
        self.testScatter.add_errorbars(0.1, 0.1)
        self.testScatter.add_errorbars(0.1, [0.2, 0.3] * 100)
        self.testScatter.add_errorbars([0.2, 0.3] * 100, 0.1)
        self.testScatter.add_errorbars(0.3, None)
        self.testScatter.add_errorbars(None, 0.3)

    def test_get_point_at_x(self):
        point = self.testScatter.get_point_at_x(0.5)
        self.assertEqual(point.x, 0.5)
        self.assertAlmostEqual(point.y, sin(0.5), places=3)

    def test_get_points_at_y(self):
        points = self.testScatter.get_points_at_y(0)
        for i, point in enumerate(points):
            self.assertEqual(point.y, 0)
            self.assertAlmostEqual(point.x, i * pi, places=3)

    def test_curve_is_plotted(self):
        x = linspace(0, 3 * pi, 200)
        self.testScatter = Scatter(
            x,
            sin(x),
            "test scatter",
            face_color="k",
            edge_color="k",
            marker_size=30,
            marker_style="o",
        )
        _, self.testAxes = subplots()
        self.testScatter._plot_element(self.testAxes, 0)
        self.assertEqual(len(self.testAxes.collections), 1)

    def test_add_scatter(self):
        x = linspace(0, 3 * pi, 200)
        other_scatter = Scatter(x, 0.005 * x**2 + 0.1, "Other Scatter")
        scatter_sum = self.testScatter + other_scatter
        self.assertIsInstance(scatter_sum, Scatter)
        self.assertAlmostEqual(scatter_sum.get_point_at_x(0).y, 0.1, places=3)
        self.assertAlmostEqual(scatter_sum.get_point_at_x(2).y, 1.029, places=3)

    def test_subtract_scatter(self):
        x = linspace(0, 3 * pi, 200)
        other_scatter = Scatter(x, 0.005 * x**2 + 0.1, "Other Scatter")
        scatter_sub = self.testScatter - other_scatter
        self.assertIsInstance(scatter_sub, Scatter)
        self.assertAlmostEqual(scatter_sub.get_point_at_x(0).y, -0.1, places=3)
        self.assertAlmostEqual(scatter_sub.get_point_at_x(2).y, 0.789, places=3)

    def test_multiply_scatter(self):
        x = linspace(0, 3 * pi, 200)
        other_scatter = Scatter(x, 0.005 * x**2 + 0.1, "Other Scatter")
        scatter_mult = self.testScatter * other_scatter
        self.assertIsInstance(scatter_mult, Scatter)
        self.assertAlmostEqual(scatter_mult.get_point_at_x(0).y, 0, places=3)
        self.assertAlmostEqual(scatter_mult.get_point_at_x(2).y, 0.109, places=3)

    def test_divide_scatter(self):
        x = linspace(0, 3 * pi, 200)
        other_scatter = Scatter(x, 0.005 * x**2 + 0.1, "Other Scatter")
        scatter_div = self.testScatter / other_scatter
        self.assertIsInstance(scatter_div, Scatter)
        self.assertAlmostEqual(scatter_div.get_point_at_x(0).y, 0, places=3)
        self.assertAlmostEqual(scatter_div.get_point_at_x(2).y, 7.57748, places=2)

    def test_max_scatter(self):
        scatter_max = max(self.testScatter)
        self.assertAlmostEqual(scatter_max, 1, places=3)

    def test_min_scatter(self):
        scatter_min = min(self.testScatter)
        self.assertAlmostEqual(scatter_min, -1, places=3)

    def test_add_different_sizes(self):
        x = linspace(0, 3 * pi, 100)
        other_scatter = Scatter(x, 0.005 * x**2 + 0.1, "Other Scatter")
        with self.assertRaises(ValueError):
            new_scatter = self.testScatter + other_scatter


class TestHistogram(unittest.TestCase):
    def setUp(self):
        self.testHist = Histogram(
            [random() for _ in range(100)],
            20,
            label="Random Distribution",
            face_color="silver",
            edge_color="k",
        )

    def test_label_is_str(self):
        self.assertEqual(self.testHist.label[:19], "Random Distribution")

    def test_xdata_is_list_or_ndarray(self):
        self.assertIsInstance(self.testHist.data, list | ndarray)

    def test_face_color_is_str(self):
        self.assertEqual(self.testHist.face_color, "silver")

    def test_edge_color_is_str(self):
        self.assertEqual(self.testHist.edge_color, "k")

    def test_bins_is_int(self):
        self.assertEqual(self.testHist.number_of_bins, 20)

    def test_alpha_is_default(self):
        self.assertEqual(self.testHist.alpha, "default")

    def test_hist_type_is_str(self):
        self.assertEqual(self.testHist.hist_type, "default")

    def test_plot_residuals_from_fit(self):
        curve = Curve.from_function(lambda x: x**2, 0, 1)
        fit = FitFromPolynomial(curve, degree=2)
        histo = self.testHist.plot_residuals_from_fit(fit, 30)
        self.assertIsInstance(histo, Histogram)
