import json
import math
import sympy as sp
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# ------------------------------------------------------------------------------
#                                                                              #
#                        1. SMART CALCULATOR MODULE                            #
#                                                                              #
# ------------------------------------------------------------------------------

def home_page(request):
    return render(request, 'content/home.html')

def calculator_page(request):
    return render(request, 'content/calculator.html')

@csrf_exempt
def process_calculation(request):
    """Processes basic mathematical expressions securely."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            expression = data.get('expression', '')
            
            # Security: Allow only basic math characters
            allowed_chars = set("0123456789+-*/(). ")
            if not set(expression).issubset(allowed_chars):
                return JsonResponse({'error': 'Invalid characters in expression'}, status=400)
            
            result = eval(expression)
            
            # Format integer outputs cleanly
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            elif isinstance(result, float):
                result = round(result, 5)
                
            return JsonResponse({'result': result})
            
        except ZeroDivisionError:
            return JsonResponse({'error': 'Cannot divide by zero'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Invalid mathematical format'}, status=400)
            
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# ------------------------------------------------------------------------------
#                                                                              #
#                          2. UNIT CONVERTER MODULES                           #
#                                                                              #
# ------------------------------------------------------------------------------

# ------------------------- A. HEIGHT CONVERTER -------------------------
def height_page(request):
    return render(request, 'content/height.html')

@csrf_exempt
def calculate_height(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            val = float(data.get('value', 0))
            from_unit = data.get('from_unit', 'cm')
            to_unit = data.get('to_unit', 'm')

            rates = { 'mm': 1000.0, 'cm': 100.0, 'm': 1.0, 'in': 39.3701, 'ft': 3.28084, 'yd': 1.09361 }
            if from_unit not in rates or to_unit not in rates:
                return JsonResponse({'error': 'Invalid Units Provided'}, status=400)

            in_meters = val / rates[from_unit]
            final_result = in_meters * rates[to_unit]

            formatted_result = int(final_result) if final_result.is_integer() else round(final_result, 5)
            return JsonResponse({'result': formatted_result})
        except ValueError:
            return JsonResponse({'error': 'Invalid Numerical Input'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

# ------------------------- B. DISTANCE CONVERTER -------------------------
def distance_page(request):
    return render(request, 'content/distance.html')

@csrf_exempt
def calculate_distance(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            val = float(data.get('value', 0))
            from_unit = data.get('from_unit', 'm')
            to_unit = data.get('to_unit', 'km')

            dist_rates = { 'm': 1.0, 'km': 0.001, 'mi': 0.000621371, 'yd': 1.09361, 'ft': 3.28084, 'nmi': 0.000539957 }
            if from_unit not in dist_rates or to_unit not in dist_rates:
                return JsonResponse({'error': 'Invalid Units Provided'}, status=400)

            in_meters = val / dist_rates[from_unit]
            final_ans = in_meters * dist_rates[to_unit]
            
            formatted_result = int(final_ans) if final_ans.is_integer() else round(final_ans, 5)
            return JsonResponse({'result': formatted_result})
        except ValueError:
            return JsonResponse({'error': 'Invalid Numerical Input'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

# ------------------------- C. AREA CONVERTER -------------------------
def area_page(request):
    return render(request, 'content/area.html')

@csrf_exempt
def calculate_area(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            val = float(data.get('value', 0))
            from_unit = data.get('from_unit', 'sq_m')
            to_unit = data.get('to_unit', 'sq_ft')

            area_rates = { 'sq_m': 1.0, 'sq_km': 0.000001, 'sq_ft': 10.7639, 'sq_yd': 1.19599, 'acre': 0.000247105, 'hectare': 0.0001, 'bigha': 0.000395368, 'biswa': 0.00790737 }
            if from_unit not in area_rates or to_unit not in area_rates:
                return JsonResponse({'error': 'Invalid Units Provided'}, status=400)

            in_base_unit = val / area_rates[from_unit]
            final_ans = in_base_unit * area_rates[to_unit]
            
            formatted_result = int(final_ans) if final_ans.is_integer() else round(final_ans, 5)
            return JsonResponse({'result': formatted_result})
        except ValueError:
            return JsonResponse({'error': 'Invalid Numerical Input'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)

# ------------------------- D. WEIGHT CONVERTER -------------------------
def weight_page(request):
    return render(request, 'content/weight.html')

@csrf_exempt
def calculate_weight(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            val = float(data.get('value', 0))
            from_unit = data.get('from_unit', 'kg')
            to_unit = data.get('to_unit', 'g')

            weight_rates = { 'g': 1.0, 'mcg': 1000000.0, 'mg': 1000.0, 'ct': 5.0, 'kg': 0.001, 'q': 0.00001, 'ton': 0.000001, 'lb': 0.00220462, 'oz': 0.035274, 'st': 0.000157473 }
            if from_unit not in weight_rates or to_unit not in weight_rates:
                return JsonResponse({'error': 'Invalid Units Provided'}, status=400)

            in_base_grams = val / weight_rates[from_unit]
            final_ans = in_base_grams * weight_rates[to_unit]
            
            formatted_result = int(final_ans) if final_ans.is_integer() else round(final_ans, 5)
            return JsonResponse({'result': formatted_result})
        except ValueError:
            return JsonResponse({'error': 'Invalid Numerical Input'}, status=400)
        except Exception:
            return JsonResponse({'error': 'Internal Server Error'}, status=500)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


# ------------------------------------------------------------------------------
#                                                                              #
#                        3. FINANCE & GST CALCULATOR                           #
#                                                                              #
# ------------------------------------------------------------------------------

def gst_page(request):
    return render(request, 'content/finance.html')

@csrf_exempt
def calculate_gst(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            amount = float(data.get('amount', 0))
            rate = float(data.get('rate', 18))
            action = data.get('action', 'add')
            supply_type = data.get('supply_type', 'intra')

            if amount < 0 or rate < 0:
                return JsonResponse({'status': 'error', 'error': 'Negative arithmetic values are disallowed'}, status=400)

            if action == 'add':
                total_gst = amount * (rate / 100)
                grand_total = amount + total_gst
                base_amount = amount
            else:
                grand_total = amount
                base_amount = amount / (1 + (rate / 100))
                total_gst = grand_total - base_amount

            cgst = sgst = igst = 0.0
            if supply_type == 'intra':
                cgst = total_gst / 2
                sgst = total_gst / 2
            else:
                igst = total_gst

            response_payload = {
                'status': 'success', 'base_amount': f"{base_amount:.2f}", 'total_gst': f"{total_gst:.2f}",
                'cgst': f"{cgst:.2f}", 'sgst': f"{sgst:.2f}", 'igst': f"{igst:.2f}", 'grand_total': f"{grand_total:.2f}"
            }
            return JsonResponse(response_payload)
        except (ValueError, TypeError):
            return JsonResponse({'status': 'error', 'error': 'Malformed dataset parameters'}, status=400)
        except Exception:
            return JsonResponse({'status': 'error', 'error': 'Server arithmetic processing failure'}, status=500)
    return JsonResponse({'status': 'error', 'error': 'Only POST method is allowed'}, status=405)


# ------------------------------------------------------------------------------
#                                                                              #
#                   4. ULTIMATE PHYSICS & STUDENT ENGINE                       #
#                                                                              #
# ------------------------------------------------------------------------------

def student_page(request):
    return render(request, 'content/student.html')

@require_POST
@csrf_exempt
def calculate_physics(request):
    """Core computational engine for Engineering and Physics formulas."""
    
    if request.content_type != 'application/json':
        return JsonResponse({'status': 'error', 'message': 'Invalid Data Format!'}, status=415)

    try:
        data = json.loads(request.body)
        formula = data.get('formula')

        # Helper function: Extracts input safely, keeps strings for symbolic math (Laplace)
        def get_val(key, default=0.0):
            val = data.get(key)
            if val in [None, '']:
                return default
            try:
                return float(val)
            except ValueError:
                return val

        val1 = get_val('val1')
        val2 = get_val('val2')
        val3 = get_val('val3')
        val4 = get_val('val4')
        
        # Security: Prevent server overflow from massive numerical inputs
        max_limit = 10000000
        if isinstance(val1, (int, float)) and isinstance(val2, (int, float)) and isinstance(val3, (int, float)):
            if abs(val1) > max_limit or abs(val2) > max_limit or abs(val3) > max_limit:
                return JsonResponse({'status': 'error', 'message': 'Values exceed safe server limits!'}, status=400)

        result_str = "--"

        # ======================================================================
        #                     SECTION A: IOT HARDWARE & CIRCUITS
        # ======================================================================
        
        # --- IoT Hardware ---
        if formula == 'ledResistor':
            result = (val1 - val2) / val3 if val3 != 0 else 0
            result_str = f"{result:.4g}"
            
        elif formula == 'vdiv':
            result = val1 * (val3 / (val2 + val3)) if (val2 + val3) != 0 else 0
            result_str = f"{result:.4g}"
            
        elif formula == 'adcConvert':
            result = (val1 * val2) / (val3 - 1) if (val3 - 1) != 0 else 0
            result_str = f"{result:.4g}"
            
        elif formula == 'battery':
            result = val1 / val2 if val2 != 0 else 0
            result_str = f"{result:.4g}"
            
        elif formula == 'energy':
            result = val1 * val2
            result_str = f"{result:.4g}"
            
        # --- Basic Circuitry ---
        elif formula == 'voltage':
            result = val1 * val2
            result_str = f"{result:.4g}"
            
        elif formula == 'current':
            result = val1 / val2 if val2 != 0 else 0
            result_str = f"{result:.4g}"
            
        elif formula == 'resistance':
            result = val1 / val2 if val2 != 0 else 0
            result_str = f"{result:.4g}"
            
        elif formula == 'power':
            result = val1 * val2
            result_str = f"{result:.4g}"

        # --- Electromagnetism & Optics ---
        elif formula == 'rctime':
            result = val1 * val2
            result_str = f"{result:.4g}"
            
        elif formula == 'charge':
            result = val1 * val2
            result_str = f"{result:.4g}"
            
        elif formula == 'transformer':
            result = val1 * (val3 / val2) if val2 != 0 else 0
            result_str = f"{result:.4g}"
            
        elif formula == 'magneticForce':
            result = val1 * val2 * val3 * math.sin(math.radians(val4))
            result_str = f"{result:.4g}"

        elif formula == 'heat':
            result = (val1 ** 2) * val2 * val3
            result_str = f"{result:.4g}"
            
        elif formula == 'tempCF':
            result = (val1 * 9/5) + 32
            result_str = f"{result:.4g}"
            
        elif formula == 'tempKC':
            result = val1 + 273.15
            result_str = f"{result:.4g}"

        elif formula == 'wavelength':
            result = 299792458 / val1 if val1 != 0 else 0
            result_str = f"{result:.4g}"
            
        elif formula == 'frequency':
            result = 299792458 / val1 if val1 != 0 else 0
            result_str = f"{result:.4g}"
            
        elif formula == 'illuminance':
            result = val1 / (val2 ** 2) if val2 != 0 else 0
            result_str = f"{result:.4g}"


        # ======================================================================
        #                 SECTION B: NEWTON'S CLASSICAL MECHANICS
        # ======================================================================
        
        # --- 1. Kinematics (Equations of Motion) ---
        elif formula == 'motionFirst':
            result = val1 + (val2 * val3)
            result_str = f"{result:.4g}"

        elif formula == 'motionSecond':
            result = (val1 * val2) + (0.5 * val3 * (val2 ** 2))
            result_str = f"{result:.4g}"
        
        elif formula == 'motionThird':
            val = (val1 ** 2) + (2 * val2 * val3)
            if val < 0:
                return JsonResponse({'status': 'error', 'message': 'Negative value inside square root.'})
            result = math.sqrt(val)
            result_str = f"{result:.4g}"
        
        # --- 2. Force & Gravity ---
        elif formula == 'newtonForce':
            result = val1 * val2
            result_str = f"{result:.4g}"

        elif formula == 'momentumRate':
            if val2 == 0:
                return JsonResponse({'status': 'error', 'message': 'Time derivative (dt) cannot be zero.'})
            result = val1 / val2
            result_str = f"{result:.4g}"

        elif formula == 'newtonGravity':
            if val3 == 0:
                return JsonResponse({'status': 'error', 'message': 'Distance (r) cannot be zero.'})
            G = 6.67430e-11
            result = G * (val1 * val2) / (val3 ** 2)
            result_str = f"{result:.4e}"
            
        elif formula == 'newtonWeight':
            g = 9.81
            result = val1 * g
            result_str = f"{result:.4g}"

        elif formula == 'newtonWork':
            radians = math.radians(val3)
            result = val1 * val2 * math.cos(radians)
            result_str = f"{result:.4g}"

        # --- 3. Thermodynamics, Fluid Mechanics & Optics ---
        elif formula == 'newtonCooling':
            result = -val1 * (val2 - val3)
            result_str = f"{result:.4g}"

        elif formula == 'newtonViscosity':
            if val3 == 0:
                return JsonResponse({'status': 'error', 'message': 'Layer Distance cannot be zero.'})
            result = val1 * (val2 / val3)
            result_str = f"{result:.4g}"
        
        elif formula == 'newtonLens':
            if val1 * val2 < 0:
                return JsonResponse({'status': 'error', 'message': 'Product of Distance cannot be negative.'})
            result = math.sqrt(val1 * val2)
            result_str = f"{result:.4g}"

        elif formula == 'newtonRestitution':
            if (val3 - val4) == 0:
                return JsonResponse({'status': 'error', 'message': 'Initial relative velocity cannot be zero.'})
            result = (val2 - val1) / (val3 - val4)
            result_str = f"{result:.4g}"

        elif formula == 'newtonSound':
            if val2 <= 0:
                return JsonResponse({'status': 'error', 'message': 'Density must be strictly positive.'})
            result = math.sqrt(val1 / val2)
            result_str = f"{result:.4g}"


        # ======================================================================
        #               SECTION C: ADVANCED MATHEMATICS (LAPLACE)
        # ======================================================================
        
        # --- 1. Base Transforms ---
        elif formula == 'laplaceTransform':
            if not val1:
                return JsonResponse({'status': 'error', 'message': 'Expression cannot be empty.'})
            t, s = sp.symbols('t s')
            f_t = sp.sympify(str(val1))
            laplace_result = sp.laplace_transform(f_t, t, s, noconds=True)
            result_str = str(laplace_result)

        elif formula == 'inverseLaplace':
            if not val1:
                return JsonResponse({'status': 'error', 'message': 'Expression cannot be empty.'})
            t, s = sp.symbols('t s')
            F_s = sp.sympify(str(val1))
            result = sp.inverse_laplace_transform(F_s, s, t)
            result_str = str(result)

        # --- 2. Advanced Theorems ---
        elif formula == 'laplaceShifting':
            if not val1:
                return JsonResponse({'status': 'error', 'message': 'Expression cannot be empty.'})
            t, s = sp.symbols('t s')
            f_t = sp.sympify(str(val1))
            shifted_f_t = f_t * sp.exp(val2 * t)
            result = sp.laplace_transform(shifted_f_t, t, s, noconds=True)
            result_str = str(result)

        elif formula == 'laplaceDerivative':
            if not val1:
                return JsonResponse({'status': 'error', 'message': 'Expression cannot be empty.'})
            t, s = sp.symbols('t s')
            f_t = sp.sympify(str(val1))
            F_s = sp.laplace_transform(f_t, t, s, noconds=True)
            raw_result = (s * F_s) - val2
            result = sp.simplify(raw_result)
            result_str = str(result)

        elif formula == 'laplaceSecondDerivative':
            if not val1:
                return JsonResponse({'status': 'error', 'message': 'Expression cannot be empty.'})
            t, s = sp.symbols('t s')
            f_t = sp.sympify(str(val1))
            F_s = sp.laplace_transform(f_t, t, s, noconds=True)
            raw_result = (s**2 * F_s) - (s * val2) - val3
            result = sp.simplify(raw_result)
            result_str = str(result)

        elif formula == 'laplaceMultiplyByT':
            n_val = int(val2) if val2 else 1
            if not val1:
                return JsonResponse({'status': 'error', 'message': 'Expression cannot be empty.'})
            t, s = sp.symbols('t s')
            f_t = sp.sympify(str(val1))
            F_s = sp.laplace_transform(f_t, t, s, noconds=True)
            derivative_Fs = sp.diff(F_s, s, n_val)
            raw_result = ((-1)**n_val) * derivative_Fs
            result = sp.simplify(raw_result)
            result_str = str(result)

        elif formula == 'laplaceIntegral':
            if not val1:
                return JsonResponse({'status': 'error', 'message': 'Expression cannot be empty.'})
            t, s = sp.symbols('t s')
            f_t = sp.sympify(str(val1))
            F_s = sp.laplace_transform(f_t, t, s, noconds=True)
            raw_result = F_s / s
            result = sp.simplify(raw_result)
            result_str = str(result)

        # --- Error Fallback ---
        else:
            return JsonResponse({'status': 'error', 'message': 'Formula not found in the Engine.'})

        return JsonResponse({'status': 'success', 'result': result_str})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Corrupted JSON Payload!'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)