#cosine product integration






# Example usage



if __name__ == '__main__':
    import numpy as np
    from scipy.integrate import quad
    def cosine_product_integration(a1, f1, a2, f2, interval):
        def integrand(x):
            return a1 * np.cos(2 * np.pi * f1 * x) * a2 * np.cos(2 * np.pi * f2 * x)
        integration_result, _ = quad(integrand, interval[0], interval[1])
        return integration_result
    a1 = 1.0  # Amplitude of the first cosine function
    f1 = 2.0  # Frequency of the first cosine function
    a2 = 0.5  # Amplitude of the second cosine function
    f2 = 3.0  # Frequency of the second cosine function
    interval = (0, 1)  # Integration interval
    integration_result = cosine_product_integration(a1, f1, a2, f2, interval)
    print("The integration result is:", integration_result)
