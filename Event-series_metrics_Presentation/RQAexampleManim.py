from manim import *
import numpy as np

config.background_color = XKCD.OFFWHITE # Set background color to white

Text.set_default(color=XKCD.DARK)  # Set default color for text
MathTex.set_default(color=XKCD.DARK)  # Set default color for text
NumberLine.set_default(color=XKCD.DARK)  # Set default color for number lines

def logistic_map(r, x):
    return r * x * (1 - x)

class LogisticMapRecurrence(Scene):
    def construct(self):
        # Parameters for the logistic map
        r = 3.8  # Control parameter
        iterations = 500  # Number of iterations
        x0 = 0.1  # Initial value

        # Generate the logistic map data
        x_values = [x0]
        for _ in range(iterations - 1):
            x_values.append(logistic_map(r, x_values[-1]))

        # Normalize values to fit within the unit square [0, 1]
        x_values = np.array(x_values)
        x_values_normalized = (x_values - np.min(x_values)) / (np.max(x_values) - np.min(x_values))

        # Create the axes and square
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 1, 0.2],
            axis_config={"include_tip": False},
        ).set_width(5).set_height(5)
        square = Square(side_length=5, color=WHITE).move_to(axes)

        # Plot the logistic map (initial line)
        points = [axes.c2p(x, y) for x, y in zip(x_values_normalized[:-1], x_values_normalized[1:])]
        logistic_curve = VMobject(color=BLUE).set_points_as_corners(points)

        # Translate logistic map to the top of the square
        translated_curve = logistic_curve.copy().shift(UP * 2.5)

        # Mirror logistic map across the diagonal of the square
        mirrored_curve = logistic_curve.copy().rotate(PI / 2, about_point=axes.c2p(0, 0))

        # Create the recurrence plot within the square
        recurrence_plot = VGroup()
        for i, x1 in enumerate(x_values_normalized):
            for j, x2 in enumerate(x_values_normalized):
                if abs(x1 - x2) < 0.05:  # Threshold for recurrence
                    recurrence_plot.add(Dot(point=axes.c2p(x1, x2), radius=0.01, color=RED))

# Add and animate elements to the scene
        self.play(Create(axes), Create(square))
        self.play(Create(logistic_curve))
        self.play(logistic_curve.animate.shift(UP * 2.5))
        self.play(Transform(logistic_curve, mirrored_curve))
        self.play(FadeIn(recurrence_plot))

        # Wait to observe the final result
        self.wait(3)


class FunctionPlotWithDots(Scene):
    def construct(self):
        # Define the function to plot
        def func(x):
            return np.sin(2 * np.pi * x)
        
        # Define epsilon threshold
        epsilon = 0.3

        # Create the axes
        axes = Axes(
            x_range=[0, 1, 0.1],
            y_range=[-1, 1, 0.5],
            axis_config={"include_tip": False}
        ).set_width(6).set_height(4)
        
        # Generate function plot
        graph = axes.plot(func, color=XKCD.MIDNIGHTBLUE)
        
        # Add plot to scene
        self.add(axes, graph)
        
        # Define intervals
        num_points = 10
        x_values = np.linspace(0, 1, num_points)
        
        # Create animation objects
        dots = VGroup()
        #lines = VGroup()
        thresholdone = MathTex('1', stroke_color=XKCD.DARK).to_edge(DOWN)
        thresholdzero = MathTex('0', stroke_color=XKCD.DARK).to_edge(DOWN)
        
        for i, x1 in enumerate(x_values):
            y1 = func(x1)
            dot1 = Dot(axes.c2p(x1, y1), color=XKCD.CARMINE) #plots interpolation/data point
            dots.add(dot1)
            threshold_line = DoubleArrow(axes.c2p(x1, y1-epsilon), axes.c2p(x1, y1+epsilon), color=YELLOW, tip_shape_start=ArrowCircleTip, tip_shape_end=ArrowCircleTip)
            self.play(FadeIn(dot1), Create(threshold_line), run_time=0.1)
            
            for j in range(i+1, num_points):
                x2 = x_values[j]
                y2 = func(x2)
                dot2 = Dot(axes.c2p(x2, y2), color=XKCD.MIDNIGHTBLUE) #plots comparison point
                level_line = DashedLine(axes.c2p(x2,y2), axes.c2p(x1,y2), color=XKCD.CARMINE) #plots line at level of comparison point
                difference_line = Line(start=axes.c2p(x1, y1), end=axes.c2p(x1, y2), color=None)
                difference_brace = Brace(difference_line, direction=LEFT, color=XKCD.CARMINE)
                difference_label = difference_brace.get_tex(f'\\lVert y_{i} - y_{j} \\rVert')
                
                # Animate appearance
                self.play(FadeIn(dot2), Create(level_line), run_time=0.5)
                self.wait(1)
                self.play(Create(difference_brace), run_time=0.5)
                self.wait(1)
                self.play(Create(difference_label), run_time=0.5)
                self.wait(1)
                
                if abs(y1 - y2) < epsilon:
                    self.play(Transform(difference_label, thresholdone), run_time=1)
                else:
                    self.play(Transform(difference_label, thresholdzero), run_time=1)
                self.wait(0.75)

                self.play(FadeOut(dot2), FadeOut(level_line), FadeOut(difference_brace), FadeOut(difference_label), run_time=1)
            self.play(FadeOut(threshold_line), run_time=1)
            
        # Add dots to scene
        self.add(dots)
        self.wait(2)

class RecurrencePlot(Scene):
    def construct(self):
        # Define the function to plot
        def func(x):
            return np.sin(2 * np.pi * x)
        
        # Define epsilon threshold
        epsilon = 0.3

        n = 10
        cell_size = 0.5

        grid = VGroup()

        # Set up empty grid in lower 2/3 of screen
        for i in range(n):
            for j in range(n):
                empty_cell = Square(side_length=cell_size)
                empty_cell.set_fill(WHITE, opacity=0.0)
                empty_cell.set_stroke(GRAY, width=0.5)
                empty_cell.move_to(np.array([j * cell_size, i * cell_size, 0]))
                grid.add(empty_cell)

        grid.move_to(DOWN)

        # Create a mini axes plot in upper third
        axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[-1, 1, 0.5],
            axis_config={"include_tip": False},
        )

        grid_width = n * cell_size
        axes_spacing = axes.height/2
        axes.set_width(grid_width)
        axes.next_to(grid, UP, buff=axes_spacing, aligned_edge=DOWN)

        #…and rotated duplicate on the left
        axes2 = axes.copy().rotate(PI/2).next_to(grid, LEFT, buff=axes_spacing, aligned_edge=RIGHT)
        axes2.set_height(grid_width)
        
        graph = axes.plot(func, color=XKCD.MIDNIGHTBLUE)
        graph2 = axes2.plot(func, color=XKCD.MIDNIGHTBLUE)
        self.play(Create(axes), Create(graph))
        self.play(Transform(axes.copy(), axes2), Transform(graph.copy(), graph2))
        self.play(Create(grid))
        # Define intervals
        num_points = 10
        x_values = np.linspace(0, 1, num_points)
        
        for i, x1 in enumerate(x_values):
            y1 = func(x1)
            dot1 = Dot(axes2.c2p(x1, y1), color=XKCD.CARMINE) #plots interpolation/data point
            self.play(FadeIn(dot1), run_time=0.1)
            
            for j in range(num_points):
                snappypace = 0.01 if i * n + j >= 5 else 0.2
                x2 = x_values[j]
                y2 = func(x2)
                dot2 = Dot(axes.c2p(x2, y2), color=XKCD.CARMINE) #plots comparison point
                square = grid[i * n + j]
                comparison_line = DashedLine(axes.c2p(x2,y2), square, color=XKCD.CARMINE) #plots line at level of comparison point
                reference_line = DashedLine(axes2.c2p(x1, y1), square, color=XKCD.CARMINE)
                
                # Animate appearance
                self.play(FadeIn(dot2), Create(reference_line), run_time=snappypace)
                self.wait(snappypace)
                self.play(Create(comparison_line), run_time=snappypace)
                self.wait(snappypace)
                
                if abs(y1 - y2) < epsilon:
                    square_color = BLACK
                else:
                    square_color = WHITE
                square.set_fill(square_color, opacity=1.0)
                square.set_stroke(GRAY, width=0.5)
                self.play(FadeIn(square), run_time=snappypace)
                self.wait(snappypace)
                self.play(FadeOut(dot2), FadeOut(reference_line), FadeOut(comparison_line), run_time=snappypace)
            self.play(FadeOut(dot1), run_time=snappypace)
        self.wait(2)



if __name__ == "__main__":
    from manim import config
    config.media_width = "75%"  # Adjust preview size
    """
    config.pixel_height = 1920
    config.pixel_width = 1920
    config.frame_height = 6.0"""
    scene = FunctionPlotWithDots() #LogisticMapRecurrence()
    scene.render()
    