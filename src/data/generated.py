import spline
import logging as log
import constants as c

def get_oscilation_test_data(startvalue,slope=0,oscilations=10,initial_oscilation_amplitude=1,
                             final_oscilation_amplitude=20,number_of_values=40,interpolated=True):
    """Get values that go from minimum to maximum, with a given number of oscilations,
    that increase or decrease linearly in amplitude with every oscilation"""

    values = []
    current_oscilation = initial_oscilation_amplitude
    oscilation_growth_factor = (final_oscilation_amplitude-initial_oscilation_amplitude) / oscilations
    value = startvalue

    for osc in range(0,oscilations):
        log.debug("osc %s, value %s, oscilation %s, osc growth %s, value slope %s" % (osc, value, current_oscilation,
                                                                                      oscilation_growth_factor, slope))
        values.append(value)
        values.append(value+current_oscilation/2.0)
        values.append(value-current_oscilation/2.0)
        value += slope
        current_oscilation += oscilation_growth_factor

    log.debug("Generated oscilation values are %s " % values)

    # Generate the splite off the "oscilations" * 3 values
    f = spline.generate_spline(values) 

    # Now generate exactly "number_of_values" out of the spline function
    x = 0
    result = []
    for i in range(0,number_of_values):
        interpolated_value = f(x)
        #print "Value %s has index %s and value %s" % (i, x, interpolated_value)
        result.append(interpolated_value)
        x += oscilations*3.0 / number_of_values

    if interpolated:
        return result
    else:
        return values


def get_assorted_test_data(plotit=False):
    test_data = [
            # Tropical temp
            get_oscilation_test_data(30, initial_oscilation_amplitude=3, final_oscilation_amplitude=4),
            # Desert temp high variation, getting hotter
            get_oscilation_test_data(20,slope=1,initial_oscilation_amplitude=20, final_oscilation_amplitude=30), 
            # Polar, cold, getting colder
            get_oscilation_test_data(-10,slope=-2,initial_oscilation_amplitude=20,final_oscilation_amplitude=40)
    ]

    if plotit:
        import plot
        plot.plot_test_multi(test_data)

    return test_data

if __name__ == "__main__":
    get_assorted_test_data(plotit=True)
