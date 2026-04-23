"""
Scientific Calculator with Error Analysis
Flask Backend - Numerical Methods Project
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ============= ERROR ANALYSIS FUNCTIONS =============

class ErrorAnalysis:
    """Class for error analysis calculations"""
    
    @staticmethod
    def absolute_error(true_value, approximate_value):
        """Calculate absolute error"""
        if true_value == 0:
            return None
        return abs(true_value - approximate_value)
    
    @staticmethod
    def relative_error(true_value, approximate_value):
        """Calculate relative error"""
        if true_value == 0:
            return None
        return abs((true_value - approximate_value) / true_value)
    
    @staticmethod
    def percentage_error(true_value, approximate_value):
        """Calculate percentage error"""
        rel_error = ErrorAnalysis.relative_error(true_value, approximate_value)
        if rel_error is None:
            return None
        return rel_error * 100
    
    @staticmethod
    def round_off_error(value, decimal_places):
        """Simulate round-off error"""
        rounded = round(value, decimal_places)
        return abs(value - rounded)
    
    @staticmethod
    def truncation_error_taylor(function_value, taylor_approx):
        """Calculate truncation error in Taylor series"""
        return abs(function_value - taylor_approx)
    
    @staticmethod
    def propagation_error(partial_derivatives, uncertainties):
        """
        Calculate error propagation
        partial_derivatives: list of partial derivatives
        uncertainties: list of measurement uncertainties
        """
        error_sum = sum((pd * u)**2 for pd, u in zip(partial_derivatives, uncertainties))
        return math.sqrt(error_sum)

# ============= NUMERICAL METHODS FUNCTIONS =============

class NumericalMethods:
    """Class for numerical methods calculations"""
    
    @staticmethod
    def bisection_method(func_str, a, b, tolerance=1e-5, max_iterations=100):
        """Bisection method for root finding"""
        try:
            results = []
            iteration = 0
            
            # Create a safe function evaluator
            def safe_eval(x):
                try:
                    safe_dict = {'x': x, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                                'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
                                'abs': abs, 'pi': math.pi, 'e': math.e}
                    return eval(func_str, {"__builtins__": {}}, safe_dict)
                except:
                    return None
            
            fa = safe_eval(a)
            fb = safe_eval(b)
            
            if fa is None or fb is None or fa * fb > 0:
                return {"error": "Invalid interval or function", "results": []}
            
            while iteration < max_iterations:
                c = (a + b) / 2
                fc = safe_eval(c)
                
                if fc is None:
                    return {"error": "Error evaluating function", "results": results}
                
                results.append({
                    "iteration": iteration + 1,
                    "a": round(a, 8),
                    "b": round(b, 8),
                    "c": round(c, 8),
                    "f(c)": round(fc, 8),
                    "error": round(abs(b - a) / 2, 8)
                })
                
                if abs(fc) < tolerance or abs(b - a) / 2 < tolerance:
                    results.append({
                        "root": round(c, 8),
                        "function_value": round(fc, 8),
                        "iterations": iteration + 1,
                        "final_error": round(abs(b - a) / 2, 8)
                    })
                    break
                
                if fa * fc < 0:
                    b = c
                    fb = fc
                else:
                    a = c
                    fa = fc
                
                iteration += 1
            
            return {"success": True, "results": results}
        except Exception as e:
            return {"error": str(e), "results": []}
    
    @staticmethod
    def newton_raphson(func_str, derivative_str, x0, tolerance=1e-5, max_iterations=100):
        """Newton-Raphson method for root finding"""
        try:
            results = []
            x = x0
            
            def safe_eval(expr, x_val):
                try:
                    safe_dict = {'x': x_val, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                                'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
                                'abs': abs, 'pi': math.pi, 'e': math.e}
                    return eval(expr, {"__builtins__": {}}, safe_dict)
                except:
                    return None
            
            for iteration in range(max_iterations):
                fx = safe_eval(func_str, x)
                fpx = safe_eval(derivative_str, x)
                
                if fx is None or fpx is None:
                    return {"error": "Error evaluating function or derivative", "results": results}
                
                if abs(fpx) < 1e-10:
                    return {"error": "Derivative too close to zero", "results": results}
                
                x_new = x - fx / fpx
                error = abs(x_new - x)
                
                results.append({
                    "iteration": iteration + 1,
                    "x": round(x, 8),
                    "f(x)": round(fx, 8),
                    "f'(x)": round(fpx, 8),
                    "x_new": round(x_new, 8),
                    "error": round(error, 8)
                })
                
                if error < tolerance:
                    results.append({
                        "root": round(x_new, 8),
                        "iterations": iteration + 1,
                        "final_error": round(error, 8)
                    })
                    break
                
                x = x_new
            
            return {"success": True, "results": results}
        except Exception as e:
            return {"error": str(e), "results": []}
    
    @staticmethod
    def false_position(func_str, a, b, tolerance=1e-5, max_iterations=100):
        """False Position (Regula Falsi) method"""
        try:
            results = []
            
            def safe_eval(x):
                try:
                    safe_dict = {'x': x, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                                'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt,
                                'abs': abs, 'pi': math.pi, 'e': math.e}
                    return eval(func_str, {"__builtins__": {}}, safe_dict)
                except:
                    return None
            
            fa = safe_eval(a)
            fb = safe_eval(b)
            
            if fa is None or fb is None or fa * fb > 0:
                return {"error": "Invalid interval or function", "results": []}
            
            for iteration in range(max_iterations):
                fc = (a * fb - b * fa) / (fb - fa)
                f_fc = safe_eval(fc)
                
                if f_fc is None:
                    return {"error": "Error evaluating function", "results": results}
                
                error = abs(b - a)
                results.append({
                    "iteration": iteration + 1,
                    "a": round(a, 8),
                    "b": round(b, 8),
                    "c": round(fc, 8),
                    "f(c)": round(f_fc, 8),
                    "error": round(error, 8)
                })
                
                if abs(f_fc) < tolerance or error < tolerance:
                    results.append({
                        "root": round(fc, 8),
                        "function_value": round(f_fc, 8),
                        "iterations": iteration + 1
                    })
                    break
                
                if fa * f_fc < 0:
                    b = fc
                    fb = f_fc
                else:
                    a = fc
                    fa = f_fc
            
            return {"success": True, "results": results}
        except Exception as e:
            return {"error": str(e), "results": []}

# ============= BASIC CALCULATOR FUNCTIONS =============

class BasicCalculator:
    """Basic scientific calculations"""
    
    @staticmethod
    def calculate(expression):
        """Safely evaluate mathematical expression"""
        try:
            safe_dict = {
                'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
                'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
                'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
                'exp': math.exp, 'log': math.log, 'log10': math.log10,
                'sqrt': math.sqrt, 'abs': abs, 'pi': math.pi, 'e': math.e,
                'factorial': math.factorial, 'degrees': math.degrees,
                'radians': math.radians
            }
            result = eval(expression, {"__builtins__": {}}, safe_dict)
            return {"result": result, "success": True}
        except Exception as e:
            return {"error": str(e), "success": False}

# ============= FLASK ROUTES =============

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """Basic calculator endpoint"""
    data = request.json
    expression = data.get('expression', '')
    result = BasicCalculator.calculate(expression)
    return jsonify(result)

@app.route('/api/error-analysis', methods=['POST'])
def error_analysis():
    """Error analysis endpoint"""
    data = request.json
    analysis_type = data.get('type')
    
    try:
        if analysis_type == 'absolute_error':
            error = ErrorAnalysis.absolute_error(data['true_value'], data['approximate_value'])
            return jsonify({
                "success": True,
                "error": error,
                "formula": "|True Value - Approximate Value|"
            })
        
        elif analysis_type == 'relative_error':
            error = ErrorAnalysis.relative_error(data['true_value'], data['approximate_value'])
            return jsonify({
                "success": True,
                "error": error,
                "formula": "|True Value - Approximate Value| / |True Value|"
            })
        
        elif analysis_type == 'percentage_error':
            error = ErrorAnalysis.percentage_error(data['true_value'], data['approximate_value'])
            return jsonify({
                "success": True,
                "error": error,
                "formula": "Relative Error × 100%"
            })
        
        elif analysis_type == 'round_off_error':
            error = ErrorAnalysis.round_off_error(data['value'], data['decimal_places'])
            return jsonify({
                "success": True,
                "error": error,
                "formula": "|Original Value - Rounded Value|"
            })
        
        elif analysis_type == 'propagation_error':
            error = ErrorAnalysis.propagation_error(
                data['partial_derivatives'],
                data['uncertainties']
            )
            return jsonify({
                "success": True,
                "error": error,
                "formula": "√(Σ(∂f/∂x_i × δx_i)²)"
            })
        
        else:
            return jsonify({"success": False, "error": "Unknown analysis type"})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/api/bisection', methods=['POST'])
def bisection():
    """Bisection method endpoint"""
    data = request.json
    result = NumericalMethods.bisection_method(
        data.get('function'),
        float(data.get('a')),
        float(data.get('b')),
        float(data.get('tolerance', 1e-5)),
        int(data.get('max_iterations', 100))
    )
    return jsonify(result)

@app.route('/api/newton-raphson', methods=['POST'])
def newton_raphson():
    """Newton-Raphson method endpoint"""
    data = request.json
    result = NumericalMethods.newton_raphson(
        data.get('function'),
        data.get('derivative'),
        float(data.get('x0')),
        float(data.get('tolerance', 1e-5)),
        int(data.get('max_iterations', 100))
    )
    return jsonify(result)

@app.route('/api/false-position', methods=['POST'])
def false_position():
    """False Position method endpoint"""
    data = request.json
    result = NumericalMethods.false_position(
        data.get('function'),
        float(data.get('a')),
        float(data.get('b')),
        float(data.get('tolerance', 1e-5)),
        int(data.get('max_iterations', 100))
    )
    return jsonify(result)

@app.route('/api/help', methods=['GET'])
def help_section():
    """Help and documentation endpoint"""
    return jsonify({
        "title": "Scientific Calculator - Help",
        "sections": {
            "Basic Calculation": "Use standard mathematical expressions with sin, cos, tan, exp, log, sqrt, etc.",
            "Functions": "sin, cos, tan, asin, acos, atan, sinh, cosh, tanh, exp, log, log10, sqrt, factorial",
            "Constants": "pi (π), e",
            "Operators": "+ - * / ** (power) % (modulo)",
            "Bisection": "f(a) and f(b) must have opposite signs",
            "Newton-Raphson": "Requires function and its derivative",
            "False Position": "Another bracketing method, f(a) and f(b) must have opposite signs"
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)